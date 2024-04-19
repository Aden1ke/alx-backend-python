#!/usr/bin/env python3
"""duck typing"""

from typing import Sequence, List, Tuple, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """returns a list of tuple"""
    return [(i, len(i)) for i in lst]
