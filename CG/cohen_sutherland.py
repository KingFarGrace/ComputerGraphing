#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
Cohen-Sutherland裁剪算法
'''
import matplotlib.pyplot as plt

UPPERMOST = 999999


class Point:

    def __init__(self, a, b):
        self.x = a
        self.y = b
        self.pos_code = 0

    def draw(self):
        plt.plot([self.x], [self.y], 'o')

    def set_pos_code(self, sec):
        # sec为区间列表，下标为0-3的项分别为裁剪框xmin， xmax， ymin， ymax
        # bin_pos_code为pos_code的二进制形式，按位倒序存储在列表中
        bin_pos_code = []
        bin_pos_code.append(1) if self.x < sec[0] else bin_pos_code.append(0)
        bin_pos_code.append(1) if self.x > sec[1] else bin_pos_code.append(0)
        bin_pos_code.append(1) if self.y < sec[2] else bin_pos_code.append(0)
        bin_pos_code.append(1) if self.y > sec[3] else bin_pos_code.append(0)
        print(bin_pos_code)
        # 转化为十进制
        for i in range(4):
            self.pos_code += bin_pos_code[i] * (2 ** i)

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
            else UPPERMOST
        self.b = self.start.y - self.start.x * self.k \
            if self.k != UPPERMOST \
            else UPPERMOST
        # ymin：直线最小纵坐标 ymax：直线最大纵坐标 xmin：直线最小横坐标 xmax：直线最大横坐标
        self.ymin = self.start.y if self.start.y < self.end.y else self.end.y
        self.ymax = self.start.y if self.start.y > self.end.y else self.end.y
        self.xmin = self.start.x if self.start.x < self.end.x else self.end.x
        self.xmax = self.start.x if self.start.x > self.end.x else self.end.x

    def draw(self):
        plt.plot([self.start.x, self.end.x], [self.start.y, self.end.y], '--')

    def get_edge_node(self, other_line):
        pass

    def __str__(self):
        if self.k == UPPERMOST:
            line_info = '直线方程为：x={}，起点({},{})，终点({},{})'\
                        .format(self.start.x,
                                self.start.x, self.start.y,
                                self.end.x, self.end.y)
        else:
            line_info = '直线方程为：y={}x+{}，起点({},{})，终点({},{})'\
                        .format(self.k, self.b,
                                self.start.x, self.start.y,
                                self.end.x, self.end.y)
        return line_info


class CuttingBox:
    point_list = []
    line_list = []

    def __init__(self):
        x1, y1 = map(int, input('请输入裁剪框左上角顶点横、纵坐标（用空格隔开）：').split())
        x2, y2 = map(int, input('请输入裁剪框右下角顶点横、纵坐标（用空格隔开）：').split())
        self.section = [x1, x2, y2, y1]
        # 顶点顺序：左上，右上，右下，左下
        point1 = Point(x1, y1)
        point2 = Point(x2, y1)
        point3 = Point(x2, y2)
        point4 = Point(x1, y2)
        # 边顺序：上右下左
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
    cline.start.set_pos_code(cbox.section)
    cline.end.set_pos_code(cbox.section)
    node_list = []
    if cline.start.pos_code == cline.end.pos_code == 0:
        plt.plot([xs, xe], [ys, ye], '-', c='r')
    else:
        for i in range(4):
            temp_l = cbox.line_list[i].get_edge_node(cline)
            if temp_l is not None:
                node_list.append(temp_l)
    for n in node_list:
        print(n)
    plt.grid(color='grey')
    plt.show()
