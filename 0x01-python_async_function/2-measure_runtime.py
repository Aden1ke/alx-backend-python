#!/usr/bin/env python3
""" this measures the runtime of the wsit_n"""

import time
import asyncio
wn = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ this returns the time it takes to execute the wait_n"""
    start = time.time()
    asyncio.run(wn(n, max_delay))
    end = time.time()
    return (end - start) / n
