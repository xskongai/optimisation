#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 12/4/25
Description: parento_front_classic_demos
"""
from typing import List, Tuple


class ParetoOptimizer:
    def __init__(self, minimize: List[bool]):
        self.minimize = minimize

    def dominates(self, x: Tuple[float], y: Tuple[float]) -> bool:
        # 判断 X是否支配Y
        better_or_equal = True
        strictly_better = False

        for i,min_obj in enumerate(self.minimize):
            if min_obj:
                if x[i] >y[i]:
                    better_or_equal = False
                if x[i] <y[i]:
                    strictly_better = True
            else:
                if x[i]<y[i]:
                    better_or_equal = False
                if x[i]>y[i]:
                    strictly_better = True
            return  better_or_equal and strictly_better


def main():
    pass


if __name__ == "__main__":
    main()
