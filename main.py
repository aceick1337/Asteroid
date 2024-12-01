import time
import random
from pygame import *

# pygame.init()

width, height = 1200, 722  # создание экрана
mw = display.set_mode((width, height))  # создание экрана

display.set_caption('Lobby')  # команда которая отвечает за название экрана
hero = image.load('image/kot (1).png')  # создание героя из фото
hero = transform.scale(hero, (50, 50))
hero_size = 50  # hero.get_rect().size#получение стандартного размера
speed = 10
hero_pos = [width // 2, height - 2 * hero_size]  # вычисление что бы персонаж всегда появлялся в центре

falling_objects = []  # список для падающих объектов
falling_speed = 10  # скорость падения объектов
object_spawn_time = 500  # время между появлениями новых объектов
last_spawn_time = 0  # последнее время появления объекта
game_duration = 20000
start_time = time.get_ticks()

mega_spawn_interval = 5000  # интервал появления мега-метеорита
last_mega_spawn = 0  # последнее время появления мега-метеорита
mega_active = False  # активен ли мега-метеорит
mega_meteor = None  # координаты мега-метеорита

background = image.load('image/космос.png')
background = transform.scale(background, (1200, 722))

falling_objects_img = image.load('image/asteroid.png')
falling_objects_img = transform.scale(falling_objects_img, (100, 100))

mega_meteor_img = image.load('image/meg (1).png')
mega_meteor_img = transform.scale(mega_meteor_img, (width // 2, height // 3))

clock = time.Clock()
run = True
victory = False  # flag pobedy
game_over = False

while run:
    for e in event.get():  # записывается все движения в е
        if e.type == QUIT:  # кнопка икса
            run = False

    keys = key.get_pressed()  # все что будет нажато на клавиатурке будет записано в кей
    if keys[K_LEFT] and hero_pos[0] > 0:
        hero_pos[0] -= speed
    if keys[K_RIGHT] and hero_pos[0] < width - hero_size:  # все это управление
        hero_pos[0] += speed
    if keys[K_UP] and hero_pos[1] > 0:
        hero_pos[1] -= speed
    if keys[K_DOWN] and hero_pos[1] < height - hero_size:
        hero_pos[1] += speed

    current_time = time.get_ticks()
    if current_time - last_spawn_time > object_spawn_time:
        # создаем новый падающий объект
        obj_x = random.randint(0, width - hero_size)
        obj_y = -hero_size
        falling_objects.append([obj_x, obj_y])
        last_spawn_time = current_time

    if current_time - last_mega_spawn > mega_spawn_interval and not mega_active:
        mega_active = True
        mega_meteor = [random.randint(0, width - width // 2), -height // 3]  # стартовая позиция
        last_mega_spawn = current_time
        falling_objects.clear()  # очищаем список обычных метеоритов

    if mega_active:
        mega_meteor[1] += falling_speed  # мега-метеорит падает
        if mega_meteor[1] > height:
            mega_active = False

    if not mega_active and current_time - last_spawn_time > object_spawn_time:
        obj_x = random.randint(0, width - hero_size)
        obj_y = -hero_size
        falling_objects.append([obj_x, obj_y])
        last_spawn_time = current_time

    # обновляем позиции падающих объектов
    for obj in falling_objects:
        obj[1] += falling_speed
        # проверяем столкновение с героем
        if hero_pos[0] < obj[0] < hero_pos[0] + hero_size or hero_pos[0] < obj[0] + hero_size < hero_pos[0] + hero_size:
            if hero_pos[1] < obj[1] < hero_pos[1] + hero_size or hero_pos[1] < obj[1] + hero_size < hero_pos[
                1] + hero_size:
                run = False
                game_over = True
    if current_time - start_time > game_duration:
        run = False
        victory = True

    mw.blit(background, (0, 0))

    mw.blit(hero, (hero_pos[0], hero_pos[1]))

    if mega_active:
        mw.blit(mega_meteor_img, (mega_meteor[0], mega_meteor[1]))

        if hero_pos[0] < mega_meteor[0] + width // 2 and hero_pos[0] + hero_size > mega_meteor[0]:
            if hero_pos[1] < mega_meteor[1] + height // 3 and hero_pos[1] + hero_size > mega_meteor[1]:
                run = False
                game_over = True

    # рисуем падающие объекты
    for obj in falling_objects:
        mw.blit(falling_objects_img, (obj[0], obj[1], hero_size, hero_size))

    clock.tick(30)
    display.update()

victory_png = image.load('image/pole.jpg')
victory_png = transform.scale(victory_png, (1200, 722))

game_over_png = image.load('image/ad.jpg')
game_over_png = transform.scale(game_over_png, (1200, 722))

if victory:
    mw.blit(victory_png, (0, 0))
    font.init()
    myfont = font.Font(None, 74)
    text = myfont.render('You Win!', True, (255, 255, 255))
    mw.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    display.update()
    time.wait(3000)

if game_over:
    mw.blit(game_over_png, (0, 0))
    font.init()
    myfont = font.Font(None, 74)
    text = myfont.render('GAME OVER', True, (255, 255, 0))
    mw.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    display.update()
    time.wait(3000)