#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
直线段扫描转换算法
在测试中点画线法时发现一个问题：如果直线的斜率大于1，就不能正确显示图像，推测原因出在算法本身，
                            使用增量计算时x，y值变动不会超过1，因此显示的像素点永远在直线下方。
'''
import matplotlib.pyplot as plt


def midpoint(x0, y0, x1, y1):
    '''
    中点画线法绘制一条直线
    :param x0: 起点横坐标
    :param y0: 起点纵坐标
    :param x1: 中点横坐标
    :param y1: 终点纵坐标
    :return: 显示在屏幕上的像素点的横、纵坐标集
    a, b, d为给定参数，d1， d2为不同情况下的增量
    '''
    a = y0 - y1
    b = x1 - x0
    d = 2 * a + b
    d1, d2 = 2 * a, 2 * (a + b)
    x, y = x0, y0
    x_ax, y_ax = [x0], [y0]
    while x < x1:
        if d < 0:
            x += 1
            y += 1
            d += d2
        else:
            x += 1
            d += d1
        x_ax.append(x)
        y_ax.append(y)
    return x_ax, y_ax


xs, ys = map(int, input('请输入起点横、纵坐标（用空格隔开）：').split())
xe, ye = map(int, input('请输入终点横、纵坐标（用空格隔开）：').split())
x_axis, y_axis = midpoint(xs, ys, xe, ye)
print(x_axis)
print(y_axis)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.grid(color='grey')
plt.scatter(x_axis, y_axis)
plt.plot([xs, xe], [ys, ye], '-o')
plt.show()
