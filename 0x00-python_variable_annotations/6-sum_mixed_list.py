#!/usr/bin/env python3
"""
Contains a function that takes a mixed list of integers
"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """sum of all the numbers in the list as float"""
    return sum(mxd_lst)
