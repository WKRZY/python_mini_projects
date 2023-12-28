import random
import time

import pygame
import sys
import math
from shapely.geometry import Point

import math


def is_circle_inside_circle(center1, radius1, center2, radius2):
    distance = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    return abs(radius2 - radius1) >= distance >= 0 and radius1 < radius2


def are_two_circles_intersecting(center1, radius1, center2, radius2):
    distance = math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)
    return (radius1 + radius2) > distance > abs(radius1 - radius2)


# 初始化Pygame
pygame.init()

# 设置窗口大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

click_sound = pygame.mixer.Sound("../output.mp3")
# 设置圆的初始位置和大小
big_circle_radius = 50
small_circle_radius = 10
big_circle_x = screen_width // 2
big_circle_y = screen_height // 2
small_circle_x = big_circle_x
small_circle_y = big_circle_y
x_speed = 0.5
y_speed = 0.5


class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 1
        self.shape_obj = Point(self.x, self.y).buffer(self.radius)
        self.vx = 1
        self.vy = 1

    def move(self):

        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

    def change_direction(self, cross_point, big_ball_center):
        self_direction = [self.vx, self.vy]
        _direction = [cross_point[0] - big_ball_center[0], cross_point[1]- big_ball_center[1]]
        # 转为单位向量
        _direction = [_direction[0] / math.sqrt(_direction[0] ** 2 + _direction[1] ** 2),
                      _direction[1] / math.sqrt(_direction[0] ** 2 + _direction[1] ** 2)]
        sym_vec = self.symmetric_vector(self_direction, _direction)[:]
        self.vx, self.vy = -sym_vec[0], -sym_vec[1]

    @staticmethod
    def symmetric_vector(a, b):
        """
        计算向量a 关于向量b的对称向量
        :param a:
        :param b:
        :return:
        """
        # 参考链接https://www.yulucn.com/question/4251215506
        b_mod_squared = b[0] ** 2 + b[1] ** 2

        # 计算对称向量的x和y分量
        symmetric_x = (2 * a[1] * b[0] * b[1] + (a[0] * (b[0] ** 2 - b[1] ** 2))) / b_mod_squared
        symmetric_y = (2 * a[0] * b[0] * b[1] - (a[1] * (b[0] ** 2 - b[1] ** 2))) / b_mod_squared

        symmetric = [symmetric_x, symmetric_y]

        return symmetric

    def cross(self, other):
        return are_two_circles_intersecting([self.x, self.y], self.radius, [other.x, other.y], other.radius)

    def inside(self, other):
        return is_circle_inside_circle([self.x, self.y], self.radius, [other.x, other.y], other.radius)

    def get_intersections(self, other):
        # circle 1: (x0, y0), radius r0
        # circle 2: (x1, y1), radius r1
        x0, y0, r0 = self.x, self.y, self.radius
        x1, y1, r1 = other.x, other.y, other.radius
        d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

        # non intersecting
        if d > r0 + r1:
            return None
        # One circle within other
        if d < abs(r0 - r1):
            return None
        # coincident circles
        if d == 0 and r0 == r1:
            return None
        else:
            a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(r0 ** 2 - a ** 2)
            x2 = x0 + a * (x1 - x0) / d
            y2 = y0 + a * (y1 - y0) / d
            x3 = x2 + h * (y1 - y0) / d
            y3 = y2 - h * (x1 - x0) / d

            x4 = x2 - h * (y1 - y0) / d
            y4 = y2 + h * (x1 - x0) / d
            return (x3, y3), (x4, y4)


big_ball = Ball(big_circle_x, big_circle_y, 300)
small_ball = Ball(small_circle_x-100, small_circle_y+20, 1)
# 游戏主循环
while True:
    # 处理退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT or small_ball.radius >= big_ball.radius:
            pygame.quit()
            sys.exit()

    if small_ball.inside(big_ball):
        small_ball.move()
    else:
        small_ball.radius += 1  # 小圆的半径增大
        big_ball.radius -= 1  # 大圆的半径减小
        click_sound.play()
        print(small_ball.radius, big_ball.radius)
        cross_point = small_ball.get_intersections(big_ball)
        mean_x = 0.5 * (cross_point[0][0] + cross_point[1][0])
        mean_y = 0.5 * (cross_point[0][1] + cross_point[1][1])
        small_ball.change_direction([mean_x, mean_y], [big_ball.x, big_ball.y])
        print(f'pref pos {small_ball.x, small_ball.y}')
        print('pref v', small_ball.vx, small_ball.vy)
        if small_ball.radius >= big_ball.radius + 10:
            break
        while not small_ball.inside(big_ball):
            small_ball.move()
            # time.sleep(1)
            print(6)
            print('while pos', small_ball.x, small_ball.y)
            print('while v', small_ball.vx, small_ball.vy)
            if small_ball.radius >= big_ball.radius:
                break

    big_circle = pygame.draw.circle(screen, (255, 255, 255), (big_ball.x, big_ball.y),
                                    big_ball.radius)  # 大圆始终保持不变，所以不需要重新绘制大圆部分，只需要绘制小圆部分即可。
    small_circle = pygame.draw.circle(screen, (0, 0, 0), (small_ball.x, small_ball.y),
                                      small_ball.radius)  # 小圆始终保持不变，所以不需要重新绘制小圆部分，只需要绘制大圆部分即可。
    pygame.display.flip()  # 更新显示
    screen.fill((0, 0, 0))  # 清空屏幕
