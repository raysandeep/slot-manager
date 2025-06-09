from kubernetes import client, config
from .config import get_env


class K8sClient:
    def __init__(self):
        # load in-cluster config if available
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        self.apps = client.AppsV1Api()
        self.metrics = client.CustomObjectsApi()
        self.deployment = get_env("DEPLOYMENT_NAME", required=True)
        self.namespace = get_env("DEPLOYMENT_NAMESPACE", required=True)

    def get_deployment(self):
        return self.apps.read_namespaced_deployment(self.deployment, self.namespace)

    def current_replicas(self) -> int:
        dep = self.get_deployment()
        return dep.spec.replicas or 0

    def scale(self, replicas: int):
        body = {"spec": {"replicas": replicas}}
        self.apps.patch_namespaced_deployment_scale(
            name=self.deployment,
            namespace=self.namespace,
            body=body,
        )

    def cpu_mem_per_replica(self):
        dep = self.get_deployment()
        containers = dep.spec.template.spec.containers
        if not containers:
            return 0, 0
        resources = containers[0].resources
        limits = resources.limits or {}
        cpu = self._to_number(limits.get("cpu", "0"))
        mem = self._parse_mem(limits.get("memory", "0"))
        return cpu, mem

    def _to_number(self, cpu: str) -> float:
        if cpu.endswith("m"):
            return float(cpu[:-1]) / 1000.0
        return float(cpu)

    def _parse_mem(self, mem: str) -> int:
        if mem.lower().endswith("mi"):
            return int(mem[:-2])
        if mem.lower().endswith("gi"):
            return int(mem[:-2]) * 1024
        return int(mem)

