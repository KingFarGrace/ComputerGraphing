#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
Cohen-Sutherland裁剪算法
'''
import matplotlib.pyplot as plt


class Point:

    def __init__(self, a, b):
        self.x = a
        self.y = b

    def draw(self):
        plt.plot([self.x], [self.y], 'o')

    def __str__(self):
        point_info = '({}, {})'.format(self.x, self.y)
        return point_info


class Line:

    def __init__(self, point1, point2):
        self.start = point1
        self.end = point2
        # k = △y / △x，b代入起始点求解，若直线垂直x轴，则单独讨论
        self.k = (self.end.y - self.start.y) / (self.end.x - self.start.x) \
            if self.end.x - self.start.x != 0 \
            else None
        self.b = self.start.y - self.start.x * self.k \
            if self.k is not None \
            else None

    def draw(self):
        plt.plot([self.start.x, self.end.x], [self.start.y, self.end.y], '--')

    def __str__(self):
        if self.k is None:
            line_info = '直线方程为：x={}，起点({},{})，终点({},{})'\
                        .format(self.start.x, self.start.x, self.start.y, self.end.x, self.end.y)
        else:
            line_info = '直线方程为：y={}x+{}，起点({},{})，终点({},{})'\
                        .format(self.k, self.b, self.start.x, self.start.y, self.end.x, self.end.y)
        return line_info


class CuttingBox:
    point_list = []
    line_list = []

    def __init__(self):
        x1, y1 = map(int, input('请输入裁剪框其中一个顶点横、纵坐标（用空格隔开）：').split())
        x2, y2 = map(int, input('请输入与输入顶点在同一对角线上的顶点横、纵坐标（用空格隔开）：').split())

        point1 = Point(x1, y1)
        point2 = Point(x2, y1)
        point3 = Point(x2, y2)
        point4 = Point(x1, y2)

        line1 = Line(point1, point2)
        line2 = Line(point2, point3)
        line3 = Line(point3, point4)
        line4 = Line(point4, point1)

        self.point_list.append(point1)
        self.point_list.append(point2)
        self.point_list.append(point3)
        self.point_list.append(point4)

        self.line_list.append(line1)
        self.line_list.append(line2)
        self.line_list.append(line3)
        self.line_list.append(line4)

    def draw(self):
        for i in range(4):
            self.point_list[i].draw()
            self.line_list[i].draw()

    def __str__(self):
        box_info = "顶点集为：\n"
        for i in range(4):
            box_info += self.point_list[i] + ' '
        box_info += "\n\n四条边方程分别为：\n"
        for i in range(4):
            box_info += self.line_list[i] + '\n'
        return box_info


if __name__ == '__main__':
    xs, ys = map(int, input('请输入被裁剪直线起点横、纵坐标（用空格隔开）：').split())
    xe, ye = map(int, input('请输入被裁剪直线终点横、纵坐标（用空格隔开）：').split())
    cline = Line(Point(xs, ys), Point(xe, ye))
    cline.draw()
    cbox = CuttingBox()
    cbox.draw()
    plt.grid(color='grey')
    plt.show()
