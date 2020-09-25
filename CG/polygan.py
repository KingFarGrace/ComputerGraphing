#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
多边形扫描算法
'''
import math
import matplotlib.pyplot as plt


class Point:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    @staticmethod
    def findp(p_list, a, b):
        # 从一个点类列表中找到特定的点
        for p in p_list:
            if p.x == a and p.y == b:
                return p
        return None

    @classmethod
    def is_peek(cls, p, p_list):
        # 判断点是否为凸顶点
        idx = p_list.index(p)
        length = len(p_list)
        if p_list[(idx - 1 + length) % length].y < p.y \
                and p_list[(idx + 1) % length].y < p.y:
            return True
        else:
            return False

    @classmethod
    def is_btm(cls, p, p_list):
        # 判断点是否为凹顶点
        idx = p_list.index(p)
        length = len(p_list)
        if p_list[(idx - 1 + length) % length].y > p.y \
                and p_list[(idx + 1) % length].y > p.y:
            return True
        else:
            return False

    def __str__(self):
        info = '({}, {})'.format(self.x, self.y)
        return info


class Line:

    def __init__(self, point1, point2):
        self.start = point1
        self.end = point2
        # k = △y / △x，b代入起始点求解，若直线垂直x轴，则单独讨论
        self.k = (self.end.y - self.start.y) / (self.end.x - self.start.x) if self.end.x - self.start.x != 0 else None
        self.b = self.start.y - self.start.x * self.k if self.k is not None else None
        self.delta_x = None
        # ymin：直线最小纵坐标 ymax：直线最大纵坐标 xmin：直线最小纵坐标对应的横坐标
        self.ymin = self.start.y if self.start.y < self.end.y else self.end.y
        self.ymax = self.start.y if self.start.y > self.end.y else self.end.y
        self.xmin = self.start.x if self.start.y == self.ymin else self.end.x

    def get_delta_x(self):
        # 求步长△x
        if self.k is not None and self.b is not None:
            self.delta_x = (self.end.x - self.start.x) / (self.end.y - self.start.y)
        elif self.k is None:
            self.delta_x = 0
        else:
            self.delta_x = None

    def __str__(self):
        if self.k is None:
            line_info = '直线方程为：x={}，起点({},{})，终点({},{})'\
                        .format(self.start.x, self.start.x, self.start.y, self.end.x, self.end.y)
        else:
            line_info = '直线方程为：y={}x+{}，起点({},{})，终点({},{})'\
                        .format(self.k, self.b, self.start.x, self.start.y, self.end.x, self.end.y)
        return line_info


class NET:
    # NET新边表：表项结构为（扫描线编号，边列表）
    table = []
    # 访问数组：记录边类数组中对应下标的边是否被录入新边表中
    checked = []

    def __init__(self, lnum, low, high, l_list):
        for i in range(lnum):
            self.checked.append(False)

        for i in range(high - low + 1):
            self.table.append([low + i, []])
            for idx in range(lnum):
                # 找到一条与当前扫描线相交（最低点在当前扫描线之下且不平行于x轴）且未被录入的边
                if l_list[idx].ymin <= low + i and self.checked[idx] is False and l_list[idx].k != 0:
                    self.table[i][1].append(l_list[idx])
                    l_list[idx].get_delta_x()
                    # 状态记为录入
                    self.checked[idx] = True

    def __str__(self):
        net_info = '新边表如下（倒序，舍弃平行于x轴的边）：\n'
        for item in self.table:
            net_info += '{} | '.format(item[0])
            for l in item[1]:
                net_info += '--> | {:2} | {:2} | {:2} | '.format(l.xmin, l.delta_x, l.ymax)
            net_info += '\n'
        return net_info


if __name__ == '__main__':
    n = int(input('请输入您要创建的多边形边数：'))
    point_list = []
    line_list = []
    peek = 0
    for i in range(n):
        xn, yn = map(int, input('请按顺序（顺时针或逆时针）输入第{}个点横、纵坐标（用空格隔开）：'.format(i + 1)).split())
        if peek < yn:
            # 记录多边形最高点
            peek = yn
        point_list.append(Point(xn, yn))
    for i in range(n):
        line = Line(point_list[i], point_list[(i + 1) % n])
        line_list.append(line)
        plt.plot([line.start.x, line.end.x], [line.start.y, line.end.y], '-o')
    line_list.sort(key=lambda l: l.ymin)
    # 记录多边形最低点
    bottom = line_list[0].ymin

    net = NET(n, bottom, peek, line_list)
    print(net)
    # 创建并动态更新活性边表
    aet = [None, []]
    for item in net.table:
        # 读新边表，将部分信息写入活性边表，AET结构：（扫描线编号，[xmin，△x，ymax]）
        aet[0] = item[0]
        for l in item[1]:
            aet[1].append([l.xmin, l.delta_x, l.ymax])
        aet[1].sort(key=lambda k: k[0])
        # sec：填充区间数组
        sec = []
        for inf in aet[1]:
            # 读AET，将xmin加入区间，不添加重复值
            if inf[0] not in sec:
                sec.append(math.ceil(inf[0]))
        for i in sec:
            # 若区间值来自于凸顶点，则舍弃该区间
            p_temp = Point.findp(point_list, i, aet[0])
            if p_temp is not None:
                if Point.is_peek(p_temp, point_list):
                    sec.remove(i)
        sec_len = len(sec)
        # 经过处理后的区间数组可作如下分类讨论
        # 1.有奇数个区间值：直接全部做填充即可，除了首尾区间值其余都来自于凹顶点，不影响填充
        # 2.有偶数个区间值：从头开始每两个值构成一组区间，分块填充多个区间
        if sec_len % 2 != 0:
            for i in range(sec[0], sec[sec_len - 1]):
                plt.plot([i], [aet[0]], 'o')
        else:
            idx = 0
            while idx * 2 < sec_len:
                for i in range(sec[idx * 2], sec[idx * 2 + 1]):
                    plt.plot([i], [aet[0]], 'o')
                idx += 1
        # 删除“死边”，其余活性边的xmin加上△x
        # temp是为了解决坑爹的remove方法的bug
        temp = []
        for inf in aet[1]:
            if inf[2] == aet[0]:
                temp.append(inf)
            else:
                inf[0] += inf[1]
        for inf in temp:
            aet[1].remove(inf)

    plt.grid(color='grey')
    plt.show()
