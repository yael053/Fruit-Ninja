import pygame
import random
import math
pygame.mixer.init()
pygame.font.init()

WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FRUIT_WIDTH, FRUIT_HEIGHT = 100, 100

BOMB_WIDTH, BOMB_WIDTH = 100, 150
PINAPPLE_WIDTH, PINAPPLE_HEIGHT = 125, 160

score_font = pygame.font.SysFont("verdania", 60)
false_font = pygame.font.SysFont("verdania", 75)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


slice_sound = pygame.mixer.Sound("slice_sound.mpeg")
slice_bomb = pygame.mixer.Sound("slice_bomb_sound.mpeg")

SCREEN = pygame.transform.scale(pygame.image.load("wall_Eden.jpg"), (WIDTH, HEIGHT))

watermelon = pygame.transform.scale(pygame.image.load("melon.png"), (FRUIT_WIDTH, FRUIT_HEIGHT))
kiwi = pygame.transform.scale(pygame.image.load("kiwi.png"), (FRUIT_WIDTH, FRUIT_HEIGHT))
coconut = pygame.transform.scale(pygame.image.load("coconut.png"), (FRUIT_WIDTH, FRUIT_HEIGHT))
mango = pygame.transform.scale(pygame.image.load("mango.png"), (FRUIT_WIDTH, FRUIT_HEIGHT))
pinapple = pygame.transform.scale(pygame.image.load("pinapple.png"), (PINAPPLE_WIDTH, PINAPPLE_HEIGHT))
strawb = pygame.transform.scale(pygame.image.load("strawb.png"), (FRUIT_WIDTH, FRUIT_HEIGHT))

bomb = pygame.transform.scale(pygame.image.load("bomb.png"), (BOMB_WIDTH, BOMB_WIDTH))


def get_image_color(image):
    pixel_array = pygame.PixelArray(image)
    w, h = pixel_array.shape
    color_counters = [0, 0, 0]
    counter = 0
    for i in range(w):
        for j in range(h):
            if pixel_array[i, j] > 0:
                curr_color = pygame.Color(pixel_array[i, j])
                color_counters[0] += curr_color[1]
                color_counters[1] += curr_color[2]
                color_counters[2] += curr_color[3]
                counter += 1

    return [c // counter for c in color_counters][::-1]


get_image_color(strawb)
FRUITS = {"watermelon": watermelon,
          "kiwi": kiwi,
          "coconut": coconut,
          "mango": mango,
          "pinapple": pinapple,
          "strawb": strawb,
          "bomb": bomb}

def num_of_false(num_of_false):
    if num_of_false == 1:
        false_text = false_font.render("X    ", True, RED)
        screen.blit(false_text, (WIDTH - 150, 10))
    if num_of_false == 2:
        false_text = false_font.render("X X  ", True, RED)
        screen.blit(false_text, (WIDTH - 150, 10))
    if num_of_false == 3:
        false_text = false_font.render("X X X", True, RED)
        screen.blit(false_text, (WIDTH - 150, 10))





class Fruit:
    width = FRUIT_WIDTH
    height = FRUIT_WIDTH

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.acceleration = 0.8  # brex
        self.speed = random.randint(-25, -20)  # kamash
        self.fruit = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fruit_type = random.choice(list(FRUITS))
        self.sparkle_color = get_image_color(FRUITS[self.fruit_type])

    def get_fruit_type(self):
        return self.fruit_type

    def draw(self, screen):
        screen.blit(FRUITS[self.fruit_type], (self.x, self.y))

    def move(self):
        self.y += self.speed
        self.speed += self.acceleration

    def check_slice(self):
        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        dist = math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)
        return dist <= self.width


class Sparkle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.y_speed = random.random() * - 9
        self.x_speed = random.normalvariate(0, 3)
        self.acceleration = 0.1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.y_speed += self.acceleration


clock = pygame.time.Clock()
FPS = 60
DEFAULT_FRUIT_TIME = 400


def main():
    timer = 0
    fruits = []
    sparkles = []
    run = True
    count_slice_fruits = 0
    count_not_slice = 0

    while run:
        clock.tick(FPS)
        timer -= clock.tick(FPS)
        screen.blit(SCREEN, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if timer <= 0:
            fruits.append(Fruit(random.randint(FRUIT_WIDTH, WIDTH - FRUIT_WIDTH), HEIGHT))
            timer = DEFAULT_FRUIT_TIME

        score_text = score_font.render("Score " + str(count_slice_fruits), True, WHITE)
        screen.blit(score_text, (10, 10))
        num_of_false(count_not_slice)



        for i, fruit in enumerate(fruits):
            if 0 < fruit.x <= WIDTH and 0 < fruit.y <= HEIGHT:
                fruit.draw(screen)
                fruit.move()
                if fruit.check_slice():
                    if fruit.get_fruit_type() == "bomb":
                        slice_bomb.play()
                        run = False
                    slice_sound.play()
                    sparkles += [Sparkle(fruit.x, fruit.y, fruit.sparkle_color) for _ in range(50)]
                    fruits.remove(fruit)
                    count_slice_fruits += 1
            else:
                slice_bomb.play()
                count_not_slice += 1
                num_of_false(count_not_slice)
                if count_not_slice == 3:
                    run = False
                fruits.remove(fruit)

        for i, sparkle in enumerate(sparkles):
            if 0 < sparkle.x <= WIDTH and 0 <= sparkle.y < HEIGHT:
                sparkle.move()
                sparkle.draw(screen)
            else:
                sparkles.remove(sparkle)

        pygame.display.update()

    pygame.time.delay(2000)
    main()



if __name__ == '__main__':
    main()
