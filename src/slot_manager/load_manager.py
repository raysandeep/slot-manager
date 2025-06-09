from .db import PostgresDB
from .redis_client import RedisClient
from .k8s_client import K8sClient
from .constants import CPU_PER_CALL, MEM_PER_CALL_MB, DEFAULT_REPLICA_CPU, DEFAULT_REPLICA_MEM_MB
from .config import get_env


class LoadManager:
    def __init__(self):
        self.region = get_env("HOME_REGION", required=True)
        self.db1 = PostgresDB("DB1_URL")
        self.db2 = PostgresDB("DB2_URL")
        self.redis = RedisClient()
        self.k8s = K8sClient()

    def compute_required_replicas(self) -> int:
        # upcoming interviews
        upcoming = self.db1.upcoming_interviews(self.region) + self.db2.upcoming_interviews(self.region)
        active = self.redis.active_egresses(self.region)
        total_needed = upcoming + active

        cpu_per_replica, mem_per_replica = self.k8s.cpu_mem_per_replica()
        if cpu_per_replica == 0:
            cpu_per_replica = DEFAULT_REPLICA_CPU
        if mem_per_replica == 0:
            mem_per_replica = DEFAULT_REPLICA_MEM_MB

        cpu_required = total_needed * CPU_PER_CALL
        mem_required = total_needed * MEM_PER_CALL_MB

        cpu_replicas = max(1, int((cpu_required + cpu_per_replica - 1) // cpu_per_replica))
        mem_replicas = max(1, int((mem_required + mem_per_replica - 1) // mem_per_replica))
        return max(cpu_replicas, mem_replicas)

    def reconcile(self):
        desired = self.compute_required_replicas()
        current = self.k8s.current_replicas()
        if desired != current:
            self.k8s.scale(desired)
        return {"desired": desired, "current": current}

    def available_slots(self) -> int:
        current = self.k8s.current_replicas()
        cpu_per_replica, mem_per_replica = self.k8s.cpu_mem_per_replica()
        if cpu_per_replica == 0:
            cpu_per_replica = DEFAULT_REPLICA_CPU
        if mem_per_replica == 0:
            mem_per_replica = DEFAULT_REPLICA_MEM_MB
        capacity = min(
            current * int(cpu_per_replica / CPU_PER_CALL),
            current * int(mem_per_replica / MEM_PER_CALL_MB),
        )
        active = self.redis.active_egresses(self.region)
        return max(0, capacity - active)
