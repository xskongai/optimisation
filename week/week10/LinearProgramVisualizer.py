#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Kong Xiaoshuang
Date: 11/14/25
Description: LinearProgramVisualizer
"""
import numpy as np
import matplotlib.pyplot as plt


def visualize_lp():
    x1 = np.linspace(0,25,200)
    # 约束边界
    raw_material = (2.2-0.1*x1)/0.1
    labour = (45-1.5*x1)/2.5

    demand1 = np.full_like(x1,18)
    demand2 = np.full_like(x1,30)

    # 绘制约束线
    plt.plot(x1,raw_material,label = "resource restrict (0.1x1+0.1x2 <=2.2)",color = "blue")
    plt.plot(x1,labour,label = "labour restriction(1.5x1+2.5x2 <=45",color = "green")
    plt.axvline(18,label="product 1 demand(x1<=18)",color = "purple")
    plt.axhline(30,label = "product 2 demand(x2<=30" ,color = "orange")

    # 可行域阴影
    x2 = np.minimum.reduce([raw_material,labour,demand2])
    plt.fill_between(x1,0,x2,where = (x1<=18),color = "lightgreen",alpha = 0.3)


    # 绘制目标函数等利润线（LOEP)
    for profit in [90,180,270]:
        plt.plot(x1,(profit-15*x1)/10,linestyle ="--",label= f"profit = {profit}")

    # 最优解点
    plt.scatter(18,4,color = 'red',zorder = 5)
    plt.text(18,4,"optimal(18,4), profit = 310",fontsize = 10,color = "red",ha = "left")

    plt.xlim(0,25)
    plt.ylim(0,35)
    plt.xlabel("x1 (product 1 num)")
    plt.ylabel("x2 (product 2 num")

    plt.title("")

    # 图表美化



def main():
    pass


if __name__ == "__main__":
    main()
