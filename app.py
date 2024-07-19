import pygame
import sys
import random

# إعداد pygame
pygame.init()

# إعداد الشاشة
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("لعبة الطائر")

# إعداد الألوان
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# إعداد الطائر
bird_width = 50
bird_height = 50
bird_x = 100
bird_y = screen_height // 2
bird_velocity_y = 0
gravity = 0.5

# إعداد العقبات
obstacle_width = 70
obstacle_gap = 200
obstacle_velocity = 5

# إعداد الأشرار
enemy_width = 50
enemy_height = 50
enemy_velocity = 5
enemies = []

# إعداد الطلقات
bullet_width = 10
bullet_height = 5
bullets = []
bullet_velocity = 10

# إعداد النقاط
score = 0
level = 1
font = pygame.font.Font(None, 36)

def create_obstacle():
    gap_position = random.randint(100, screen_height - 100 - obstacle_gap)
    return {
        'x': screen_width,
        'top_height': gap_position,
        'bottom_height': screen_height - gap_position - obstacle_gap
    }

def create_enemy(obstacle):
    enemy_x = obstacle['x'] + obstacle_width
    possible_y_positions = []
    if obstacle['top_height'] > enemy_height:
        possible_y_positions.extend(range(0, obstacle['top_height'] - enemy_height + 1))
    if obstacle['bottom_height'] > enemy_height:
        possible_y_positions.extend(range(screen_height - obstacle['bottom_height'], screen_height - enemy_height + 1))
    
    if possible_y_positions:
        enemy_y = random.choice(possible_y_positions)
        return {
            'x': enemy_x,
            'y': enemy_y,
            'width': enemy_width,
            'height': enemy_height
        }
    return None

def create_boss(obstacle):
    boss_x = obstacle['x'] + obstacle_width
    return {
        'x': boss_x,
        'y': screen_height // 2 - 100,
        'width': 100,
        'height': 200
    }

def create_falling_column():
    return {
        'x': random.randint(0, screen_width - obstacle_width),
        'y': -obstacle_width,
        'width': obstacle_width,
        'height': obstacle_width
    }

def draw_obstacle(obstacle):
    pygame.draw.rect(screen, green, (obstacle['x'], 0, obstacle_width, obstacle['top_height']))
    pygame.draw.rect(screen, green, (obstacle['x'], screen_height - obstacle['bottom_height'], obstacle_width, obstacle['bottom_height']))

def draw_enemy(enemy):
    pygame.draw.rect(screen, red, (enemy['x'], enemy['y'], enemy['width'], enemy['height']))

def draw_bullet(bullet):
    pygame.draw.rect(screen, black, (bullet['x'], bullet['y'], bullet_width, bullet_height))

def draw_boss(boss):
    pygame.draw.rect(screen, red, (boss['x'], boss['y'], boss['width'], boss['height']))

def draw_falling_column(column):
    pygame.draw.rect(screen, black, (column['x'], column['y'], column['width'], column['height']))

def draw_score():
    score_text = font.render(f'Score: {score}', True, black)
    screen.blit(score_text, (10, 10))

def draw_level():
    level_text = font.render(f'Level: {level}', True, black)
    screen.blit(level_text, (screen_width - 120, 10))

def check_collision(bird_x, bird_y, obstacle):
    if (bird_x + bird_width > obstacle['x'] and bird_x < obstacle['x'] + obstacle_width):
        if (bird_y < obstacle['top_height'] or bird_y + bird_height > screen_height - obstacle['bottom_height']):
            return True
    return False

def check_enemy_collision(bird_x, bird_y, enemy):
    if (bird_x + bird_width > enemy['x'] and bird_x < enemy['x'] + enemy['width']):
        if (bird_y + bird_height > enemy['y'] and bird_y < enemy['y'] + enemy['height']):
            return True
    return False

def check_bullet_collision(bullet, enemy):
    if (bullet['x'] + bullet_width > enemy['x'] and bullet['x'] < enemy['x'] + enemy['width']):
        if (bullet['y'] + bullet_height > enemy['y'] and bullet['y'] < enemy['y'] + enemy['height']):
            return True
    return False

def reset_game():
    global bird_x, bird_y, bird_velocity_y, current_obstacle, enemies, bullets, score, level, obstacle_velocity, enemy_velocity, falling_columns, boss
    bird_x = 100
    bird_y = screen_height // 2
    bird_velocity_y = 0
    current_obstacle = create_obstacle()
    enemies = []
    for _ in range(3):
        enemy = create_enemy(current_obstacle)
        if enemy:
            enemies.append(enemy)
    bullets = []
    score = 0
    level = 1
    obstacle_velocity = 5
    enemy_velocity = 5
    falling_columns = []
    boss = None

def game_over():
    screen.fill(white)
    game_over_text = font.render(f'Game Over! Score: {score}', True, black)
    restart_text = font.render('Press R to Restart or Q to Quit', True, black)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))
    pygame.display.flip()

def level_up():
    global level, obstacle_velocity, enemy_velocity
    level += 1
    obstacle_velocity += 1
    enemy_velocity += 1

def create_boss_level_obstacle():
    global current_obstacle
    current_obstacle = create_obstacle()

def create_boss_obstacle():
    global boss
    boss = create_boss(current_obstacle)

reset_game()

# إعداد المؤقت
clock = pygame.time.Clock()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity_y = -10
            elif event.key == pygame.K_RETURN:  # إطلاق الطلقات عند الضغط على Enter
                bullets.append({'x': bird_x + bird_width, 'y': bird_y + bird_height // 2})
            elif event.key == pygame.K_r:  # إعادة اللعبة عند الضغط على R
                reset_game()
                game_running = True
            elif event.key == pygame.K_q:  # إنهاء اللعبة عند الضغط على Q
                pygame.quit()
                sys.exit()

    if not game_running:
        continue

    # تحديث حركة الطائر
    bird_velocity_y += gravity
    bird_y += bird_velocity_y

    # تحديث حركة العقبة
    current_obstacle['x'] -= obstacle_velocity
    if current_obstacle['x'] < -obstacle_width:
        current_obstacle = create_obstacle()
        enemies = []
        for _ in range(3):
            enemy = create_enemy(current_obstacle)
            if enemy:
                enemies.append(enemy)
        score += 1  # زيادة النقاط عند المرور عبر العقبة

        # تغيير المستوى كلما تجاوز اللاعب عدد معين من النقاط
        if score % 5 == 0:
            level_up()
        
        if level % 5 == 0:  # مستوى يحتوي على الوحش
            create_boss_obstacle()

    # تحديث حركة الأشرار
    new_enemies = []
    for enemy in enemies:
        enemy['x'] -= enemy_velocity
        if enemy['x'] > -enemy_width:
            new_enemies.append(enemy)
    enemies = new_enemies
    if len(enemies) < 3 and level % 5 != 0:
        enemy = create_enemy(current_obstacle)
        if enemy:
            enemies.append(enemy)

    # تحديث حركة الطلقات
    new_bullets = []
    for bullet in bullets:
        bullet['x'] += bullet_velocity
        if bullet['x'] < screen_width:
            new_bullets.append(bullet)
            for enemy in enemies:
                if check_bullet_collision(bullet, enemy):
                    enemies.remove(enemy)
                    score += 10
                    break
    bullets = new_bullets

    # تحديث حركة الأشرار والمستوى
    if boss:
        boss['x'] -= enemy_velocity
        if boss['x'] < -boss['width']:
            boss = None

    # التحقق من الاصطدام
    if bird_y <= 0 or bird_y >= screen_height - bird_height or check_collision(bird_x, bird_y, current_obstacle):
        game_running = False
        game_over()

    # ملء الشاشة باللون الأبيض
    screen.fill(white)

    # رسم الطائر
    pygame.draw.rect(screen, blue, (bird_x, bird_y, bird_width, bird_height))

    # رسم العقبة
    draw_obstacle(current_obstacle)

    # رسم الأشرار
    for enemy in enemies:
        draw_enemy(enemy)
    
    # رسم الطلقات
    for bullet in bullets:
        draw_bullet(bullet)

    # رسم الوحش
    if boss:
        draw_boss(boss)

    # رسم مستوى اللعبة
    draw_level()

    # رسم النقاط
    draw_score()

    # تحديث الشاشة
    pygame.display.flip()

    # تحديد عدد الإطارات في الثانية
    clock.tick(30)
 
  