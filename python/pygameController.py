import pygame
import math
import serial

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Arm IK")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

arm_length_1 = 75
arm_length_2 = 75
joint_1_angle = 0
joint_2_angle = 0

ser = serial.Serial('COM10', 9600)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def get_angles(x, y, l1, l2):
    r = math.sqrt(x**2 + y**2)
    if r > l1 + l2:
        theta_1 = math.atan2(y, x)
        theta_2 = 0
    else:
        cos_theta_2 = clamp((r**2 - l1**2 - l2**2) / (2 * l1 * l2), -1, 1)
        theta_2 = math.acos(cos_theta_2)
        cos_theta_1 = clamp((l1**2 + r**2 - l2**2) / (2 * l1 * r), -1, 1)
        alpha = math.atan2(y, x)
        beta = math.acos(cos_theta_1)
        theta_1 = alpha - beta
    return math.degrees(theta_1), math.degrees(theta_2)

def draw_arm(angle1, angle2, l1, l2):
    x1 = l1 * math.cos(math.radians(angle1))
    y1 = l1 * math.sin(math.radians(angle1))
    x2 = x1 + l2 * math.cos(math.radians(angle1 + angle2))
    y2 = y1 + l2 * math.sin(math.radians(angle1 + angle2))
    pygame.draw.line(screen, WHITE, (width // 2, height // 2), (width // 2 + x1, height // 2 - y1), 5)
    pygame.draw.line(screen, WHITE, (width // 2 + x1, height // 2 - y1), (width // 2 + x2, height // 2 - y2), 5)
    return (width // 2 + x2, height // 2 - y2)

running = True
final_angle1, final_angle2 = 0, 0

while running:
    screen.fill(BLACK)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    target_x = mouse_x - width // 2
    target_y = height // 2 - mouse_y
    angles = get_angles(target_x, target_y, arm_length_1, arm_length_2)
    
    if angles:
        joint_1_angle, joint_2_angle = angles
    end_pos = draw_arm(joint_1_angle, joint_2_angle, arm_length_1, arm_length_2)
    pygame.draw.circle(screen, RED, (mouse_x, mouse_y), 5)
    font = pygame.font.SysFont(None, 24)
    angle_text = font.render(f"Angle1: {joint_1_angle:.2f}°, Angle2: {joint_2_angle:.2f}°", True, RED)
    screen.blit(angle_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                message = f'a;{joint_1_angle:.2f}, b;{joint_2_angle:.2f}\n'
                ser.write(message.encode())
                print(f"Sent: {message.strip()}")

    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()

final_angle1 = joint_1_angle
final_angle2 = joint_2_angle
ser.close()
print(f"Final Angles - Joint 1: {final_angle1}°, Joint 2: {final_angle2}°")
