import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 设置小球的初始位置、速度、大小
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed = 1
ball_radius = 1

# 设置大圆的初始位置、大小
circle_x = screen_width // 2
circle_y = screen_height // 2
circle_radius = 60

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

            # 计算小球的位置
    ball_y += ball_speed

    # 碰撞检测
    if ball_y > screen_height or ball_y < 0:
        ball_speed = -ball_speed
        circle_radius -= 5
        ball_radius += 2
    if pygame.Rect(ball_x, ball_y, ball_radius * 2, ball_radius * 2).colliderect(
            pygame.Rect(circle_x, circle_y, circle_radius * 2, circle_radius * 2)):
        ball_speed = -ball_speed
        circle_radius -= 50
        ball_radius += 2

        # 绘制背景和小球
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    pygame.draw.circle(screen, BLUE, (int(circle_x), int(circle_y)), circle_radius)
    pygame.display.update()
