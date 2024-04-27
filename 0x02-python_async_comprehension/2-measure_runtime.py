#!/usr/bin/env python3
"""
A module imports and uses asynchronously runs an async definition
"""

import time
import asyncio
ac = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ this measures the runtime of the async functions """
    starts = time.time()
    await asyncio.gather(ac(), ac(), ac(), ac())
    end = time.time()
    return end - starts
