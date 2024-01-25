import pygame
import random
import math

# Constants
WIDTH = 1600
HEIGHT = 900
G = 6.67430e-7  # Universal gravitational constant

# Colors
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MOVE_SPEED = 15
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Circle:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.radius = int(math.sqrt(mass) / 1000)
        self.x = int(x)
        self.y = int(y)
        self.color = WHITE
        self.vx = random.randrange(-1, 1)
        self.vy = random.randrange(-1, 1)

    def draw(self):
        pygame.draw.circle(
            screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_gravity(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = max(math.sqrt(dx**2 + dy**2), 1)  # Avoid division by zero
        force = (G * self.mass * other.mass) / (distance * distance)
        angle = math.atan2(dy, dx)
        acceleration = force / self.mass
        self.vx += acceleration * math.cos(angle)
        self.vy += acceleration * math.sin(angle)

    def update(self):
        self.x += self.vx
        self.y += self.vy

# Generate random circles


def generate_circles(num_circles):
    xs = (int)((WIDTH/2) * 2)
    ys = (int)((HEIGHT/2) * 2)
    masss = 1000000000000000000000000000000000000000000000
    circles = []

    c1 = Circle(masss, xs, ys)
    c1.color = RED
    c1.radius = 100

    for nothing in range(num_circles):
        mass = random.randint(10, 1000000000)
        x = random.randint(0, WIDTH) * 5
        y = random.randint(0, HEIGHT) * 5
        circle = Circle(mass, x, y)
        circle.color = (random.randint(100, 255), random.randint(
            100, 255), random.randint(100, 255))
        circles.append(circle)

    return circles

# Simulation loop


zoomoutThreshold = 1.1

eatOnCollision = False


def simulation(num_circles):
    circles = generate_circles(num_circles)

    running = True
    while running:
        circles[len(circles)-1].vx = 0
        circles[len(circles)-1].vy = 0

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            for circle in circles:
                circle.y -= MOVE_SPEED
        if keys[pygame.K_w]:
            for circle in circles:
                circle.y += MOVE_SPEED
        if keys[pygame.K_d]:
            for circle in circles:
                circle.x -= MOVE_SPEED
        if keys[pygame.K_a]:
            for circle in circles:
                circle.x += MOVE_SPEED

        # Apply gravity to each circle
        for i, circle in enumerate(circles):
            for other in circles[i+1:]:
                circle.apply_gravity(other)

        # Update positions and draw circles

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    for circle in circles:
                        circle.x = (circle.x - WIDTH / 2) * \
                            zoomoutThreshold + WIDTH / 2
                        circle.y = (circle.y - HEIGHT / 2) * \
                            zoomoutThreshold + HEIGHT / 2
                        circle.radius *= zoomoutThreshold
                elif event.button == 5:  # Scroll down
                    for circle in circles:
                        circle.x = (circle.x - WIDTH / 2) / \
                            zoomoutThreshold + WIDTH / 2
                        circle.y = (circle.y - HEIGHT / 2) / \
                            zoomoutThreshold + HEIGHT / 2
                        circle.radius /= zoomoutThreshold
                # Collision detection and merging
        for circle in circles:
            circle.update()
            circle.draw()

        # Collision detection and merging
        if eatOnCollision == True:
            circles_to_remove = []
            i = 0
            k = 0
            for circle in circles:
                for j, other in enumerate(circles[:i]):
                    dx = other.x - circle.x
                    dy = other.y - circle.y
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < circle.radius + other.radius:
                        # Collision detected
                        if circle.mass >= other.mass:
                            # Circle absorbs other and gains mass
                            circle.mass += other.mass

                            circles.pop(i)
                        else:
                            # Other absorbs circle and gains mass
                            other.mass += circle.mass
                            circles.pop(k)
                i = i + 1
                k = k + 1

        circles[len(circles)-1].vx = 0
        circles[len(circles)-1].vy = 0
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


# Specify the number of circles to spawn
num_circles = 100  # Change this to the desired number of circles
simulation(num_circles)
