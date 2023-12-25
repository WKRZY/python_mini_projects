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
        self.speed = 0.1
        self.shape_obj = Point(self.x, self.y).buffer(self.radius)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def cross(self, other):
        return are_two_circles_intersecting([self.x, self.y], self.radius, [other.x, other.y], other.radius)

    def inside(self, other):
        return is_circle_inside_circle([self.x, self.y], self.radius, [other.x, other.y], other.radius)


big_ball = Ball(big_circle_x, big_circle_y, 300)
small_ball = Ball(small_circle_x, small_circle_y, 1)
# 游戏主循环
while True:
    # 处理退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if small_ball.inside(big_ball):
        small_ball.x += x_speed
        small_ball.y += y_speed
    else:
        small_ball.radius += 1  # 小圆的半径增大
        big_ball.radius -= 1  # 大圆的半径减小
        x_speed *= -1.0
        y_speed *= -1.0
        print(small_ball.radius, big_ball.radius)
        while not small_ball.inside(big_ball):
            small_ball.x += x_speed
            small_ball.y += y_speed

    big_circle = pygame.draw.circle(screen, (255, 255, 255), (big_ball.x, big_ball.y),
                                    big_ball.radius)  # 大圆始终保持不变，所以不需要重新绘制大圆部分，只需要绘制小圆部分即可。
    small_circle = pygame.draw.circle(screen, (0, 0, 0), (small_ball.x, small_ball.y),
                                      small_ball.radius)  # 小圆始终保持不变，所以不需要重新绘制小圆部分，只需要绘制大圆部分即可。
    pygame.display.flip()  # 更新显示
    screen.fill((0, 0, 0))  # 清空屏幕
