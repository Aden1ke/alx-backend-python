#!/usr/bin/env python3
""" this is the basic usage of async syntax """

import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    """ this generates a random wait"""
    delay: float = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
