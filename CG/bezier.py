#!/usr/bin/python3
# -*- encoding: utf-8 -*-

"""
使用 de Casteljau 递推算法生成 Bezier 曲线
本程序实现了画板功能，可以点击生成点，两点自动连线，大于两条线自动生成曲线，并且可以拖动已生成的点改变曲线形状
"""
import numpy as np
from matplotlib import pyplot as plt


class MyBezier:
    def __init__(self, line):
        self.line = line
        self.index_02 = None    # 保存拖动的这个点的索引
        self.press = None       # 状态标识，1为按下，None为没按下
        self.pick = None        # 状态标识，1为选中点并按下,None为没选中
        self.motion = None      # 状态标识，1为进入拖动,None为不拖动
        self.xs = list()        # 保存点的x坐标
        self.ys = list()        # 保存点的y坐标
        # 鼠标按下事件
        self.cidpress = line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        # 鼠标放开事件
        self.cidrelease = line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        # 鼠标拖动事件
        self.cidmotion = line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        # 鼠标选中事件
        self.cidpick = line.figure.canvas.mpl_connect('pick_event', self.on_picker)

    def on_press(self, event):
        # 鼠标按下调用
        if event.inaxes != self.line.axes:
            return
        self.press = 1

    def on_motion(self, event):
        # 鼠标拖动调用
        if event.inaxes != self.line.axes:
            return
        if self.press is None:
            return
        if self.pick is None:
            return
        if self.motion is None:
            # 整个if获取鼠标选中的点是哪个点
            self.motion = 1
            x = self.xs
            xdata = event.xdata
            ydata = event.ydata
            index_01 = 0
            for i in x:
                if abs(i - xdata) < 0.02:
                    # 0.02 为点半径
                    if abs(self.ys[index_01] - ydata) < 0.02:
                        break
                index_01 = index_01 + 1
            self.index_02 = index_01
        if self.index_02 is None:
            return
        self.xs[self.index_02] = event.xdata    # 鼠标的坐标覆盖选中的点的坐标
        self.ys[self.index_02] = event.ydata
        self.draw_01()

    def on_release(self, event):
        # 鼠标放开调用
        if event.inaxes != self.line.axes:
            return
        if self.pick is None:
            # 如果不是选中点，那就添加点
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
        if self.pick == 1 and self.motion != 1:
            # 如果是选中点，但不是拖动点，那就降阶
            x = self.xs
            xdata = event.xdata
            ydata = event.ydata
            index_01 = 0
            for i in x:
                if abs(i - xdata) < 0.02:
                    if abs(self.ys[index_01] - ydata) < 0.02: break
                index_01 = index_01 + 1
            self.xs.pop(index_01)
            self.ys.pop(index_01)
        self.draw_01()
        self.pick = None    # 所有状态恢复，鼠标按下到释放为一个周期
        self.motion = None
        self.press = None
        self.index_02 = None

    def on_picker(self, event):
        # 选中调用
        self.pick = 1

    def draw_01(self):
        # 绘图函数
        self.line.clear()               # 清除原有的图
        self.line.axis([0, 1, 0, 1])    # x和y范围0到1
        self.bezier(self.xs, self.ys)   # 生成Bezier曲线
        self.line.scatter(self.xs, self.ys, color='b', s=200, marker="o", picker=5)     # 画点
        self.line.plot(self.xs, self.ys, color='r')                                     # 画线
        self.line.figure.canvas.draw()  # 重构子图

    def bezier(self, *args):  # Bezier曲线公式转换，获取x和y
        n = len(args[0])  # 点的个数
        x_array, y_array = [], []
        x, y = [], []
        index = 0
        for t in np.linspace(0, 1):
            for k in range(1, n):
                for i in range(0, n - k):
                    if k == 1:
                        x_array.insert(i, args[0][i] * (1 - t) + args[0][i + 1] * t)
                        y_array.insert(i, args[1][i] * (1 - t) + args[1][i + 1] * t)
                        continue
                    # i != 1时,通过上一次迭代的结果计算
                    x_array[i] = x_array[i] * (1 - t) + x_array[i + 1] * t
                    y_array[i] = y_array[i] * (1 - t) + y_array[i + 1] * t
            if n == 1:
                x.insert(index, args[0][0])
                y.insert(index, args[1][0])
            else:
                x.insert(index, x_array[0])
                y.insert(index, y_array[0])
                x_array = []
                y_array = []
            index = index + 1
        self.line.plot(x, y)


if __name__ == '__main__':
    fig = plt.figure(2, figsize=(10, 10))   # 创建第二个绘图对象，1000*1000像素
    ax = fig.add_subplot()                  # 创建一个子图
    ax.set_title('Create Bezier')
    myBezier = MyBezier(ax)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()
