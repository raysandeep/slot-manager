# Constants for slot manager

CPU_PER_CALL = 0.5  # requested cpu for each egress call
MEM_PER_CALL_MB = 256  # memory in MB for each egress call

TIME_WINDOW_MINUTES = 15  # look ahead window for scheduled interviews
CRON_INTERVAL_MINUTES = 5  # scheduler interval

DEFAULT_REPLICA_CPU = 2  # cpu allocated for each replica (assumed)
DEFAULT_REPLICA_MEM_MB = 4096  # memory for each replica
