"""
Thread pools: the count comes from safe_inputs.cpu_threads (THREADS, else the cgroup CPU quota)
and is set in the environment before numpy is imported (OMP / OpenBLAS / MKL / numba read these
at import).
"""
from __future__ import annotations

import os
import sys

THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMBA_NUM_THREADS")


def set_env(n: int) -> None:
    for var in THREAD_VARS:
        # numba cannot change its thread count once loaded (a test harness that imported scanpy
        # before main() runs); in a container run nothing imports it before this point.
        if var == "NUMBA_NUM_THREADS" and "numba" in sys.modules:
            continue
        os.environ[var] = str(n)
