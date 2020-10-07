#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
Cohen-Sutherland裁剪算法
'''
import matplotlib.pyplot as plt

LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

border = {'left': 0, 'right': 0, 'bottom': 0, 'top': 0}
line = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}


def draw_cutting_box():
    lt = [border['left'], border['top']]
    rt = [border['right'], border['top']]
    lb = [border['left'], border['bottom']]
    rb = [border['right'], border['bottom']]
    plt.plot([lt[0], rt[0]], [lt[1], rt[1]], '--', c='k')
    plt.plot([rt[0], rb[0]], [rt[1], rb[1]], '--', c='k')
    plt.plot([rb[0], lb[0]], [rb[1], lb[1]], '--', c='k')
    plt.plot([lb[0], lt[0]], [lb[1], lt[1]], '--', c='k')


def draw_line(l, style, color):
    plt.plot([l['x1'], l['x2']],
             [l['y1'], l['y2']],
             style, c=color)


def get_pos_code(x, y):
    code = 0
    if x < border['left']:
        code += LEFT
    if x > border['right']:
        code += RIGHT
    if y < border['bottom']:
        code += BOTTOM
    if y > border['top']:
        code += TOP
    return code


def cutting(l):
    draw_line(l, '--', 'b')
    code1 = get_pos_code(l['x1'], l['y1'])
    code2 = get_pos_code(l['x2'], l['y2'])
    while code1 != 0 or code2 != 0:
        if code1 & code2 != 0:
            return
        code_temp = code1 if code1 != 0 else code2

        if LEFT & code_temp != 0:
            xt = border['left']
            yt = l['y1'] + (l['y2'] - l['y1']) * \
                 (border['left'] - l['x1']) / (l['x2'] - l['x1'])
        elif RIGHT & code_temp != 0:
            xt = border['right']
            yt = l['y1'] + (l['y2'] - l['y1']) * \
                 (border['right'] - l['x1']) / (l['x2'] - l['x1'])
        elif BOTTOM & code_temp != 0:
            yt = border['bottom']
            xt = l['x1'] + (l['x2'] - l['x1']) * \
                 (border['bottom'] - l['y1']) / (l['y2'] - l['y1'])
        elif TOP & code_temp != 0:
            yt = border['top']
            xt = l['x1'] + (l['x2'] - l['x1']) * \
                 (border['top'] - l['y1']) / (l['y2'] - l['y1'])

        if code_temp == code1:
            l['x1'] = xt
            l['y1'] = yt
            code1 = get_pos_code(xt, yt)
        else:
            l['x2'] = xt
            l['y2'] = yt
            code2 = get_pos_code(xt, yt)
    print(l)
    draw_line(l, '-', 'r')


if __name__ == '__main__':
    line['x1'], line['y1'] = map(int, input('请输入待裁剪直线起点横、纵坐标（用空格隔开）：').split())
    line['x2'], line['y2'] = map(int, input('请输入待裁剪直线终点横、纵坐标（用空格隔开）：').split())
    border['left'], border['right'], border['bottom'], border['top'] = \
        map(int, input('请输入裁剪框边界值，顺序为左右下上：').split())
    print(border)
    draw_cutting_box()
    cutting(line)
    plt.grid(color='grey')
    plt.show()
