from ctypes.wintypes import POINT
from turtle import width
import pygame
import math

pygame.init()

# julie wants to zoom in
# add custom object input for place button
# look into hooking in nasa API for real initial positions when launched instead of initializing on x axis
# add planet info box - user will be able to inspect an object to see its velocity and other props
# add a slow or fastforward frames/sim option, possibly a rewind option that draws from reversed list of orbit
# add acceleration vection arrow to see orbit disturbance better!

WIDTH, HEIGHT = 1600, 1000  # originally at  800 800
WIN = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)  # want to implement pygame.RESIZABLE but sim doesnt rescale itself to fit the new resolution
pygame.display.set_caption("Planet Orbits Simulation (To Scale)")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARK_GRAY = (80, 78, 81)
ORANGE = (255, 165, 0)
TAN = (188, 152, 126)
BABY_BLUE = (137, 207, 240)
DARK_BLUE = (32, 42, 68)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("comic sans", 15)
frames = 0
pause = False
place_active = False


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 25 / AU  # 1 AU = 100 PIXELS @  250 / AU
    TIMESTEP = (
        3600 * 24
    )  # 1 DAY IN SECONDS, each frame update will represent 1 day of movement in orbit

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = (
            []
        )  # this is a list of x,y position values for each frame for each planet so we can draw the planet and calculate distance from other planets through the pixel/distance ratio

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = (
            self.x * self.SCALE + WIDTH / 2
        )  # adding half the screen dimensions makes our values of 0,0 at the middle of the WIN, instead of 0,0 being at the top left corner
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{self.name}", 1, WHITE)
            win.blit(
                distance_text,
                (x - distance_text.get_width() / 2, y - distance_text.get_width() / 2),
            )

        pygame.draw.circle(
            win, self.color, (x, y), self.radius
        )  # drawing planets as circles

    def attraction(self, other):
        other_x, other_y = (
            other.x,
            other.y,
        )  # other planets distance from current planet
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2  #  F =(GmM)/r**2
        theta = math.atan2(
            distance_y, distance_x
        )  # split the force vector into its x and y components
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for (
            planet
        ) in (
            planets
        ):  # ITERATING through the planets in planets[] to add all forces from other objects into total_f
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP  # V = F/M * T
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP  # X = V * T
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(
        0, 0, 7.5, YELLOW, 1.98892 * 10**30, "Sun"
    )  # (0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(
        -1 * Planet.AU, 0, 4, BLUE, 5.9742 * 10**24, "Earth"
    )  # (-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(
        -1.524 * Planet.AU, 0, 3, RED, 6.39 * 10**23, "Mars"
    )  # (-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(
        0.387 * Planet.AU, 0, 2, DARK_GRAY, 3.30 * 10**23, "Mercury"
    )  # 0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23
    mercury.y_vel = -47.4 * 1000

    venus = Planet(
        0.723 * Planet.AU, 0, 3.5, WHITE, 4.8685 * 10**24, "Venus"
    )  # 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(-5.2 * Planet.AU, 0, 14, ORANGE, 1898.13 * 10**24, "Jupiter")
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 12, TAN, 5.683 * 10**26, "Saturn")
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(-19.8 * Planet.AU, 0, 10, BABY_BLUE, 8.6 * 10**25, "Uranus")
    uranus.y_vel = 6.8 * 1000

    neptune = Planet(30 * Planet.AU, 0, 9, DARK_BLUE, 1.024 * 10**24, "Neptune")  #
    neptune.y_vel = -5.43 * 1000

    #   optional objects that user can choose to add to game by clicking the corresponding button
    black_hole = Planet(
        15 * Planet.AU, 20 * Planet.AU, 2, WHITE, 5 * sun.mass, "Black Hole"
    )
    black_hole.y_vel = -6 * 1000

    second_sun = Planet(
        15 * Planet.AU, 20 * Planet.AU, 7.5, YELLOW, 1.98892 * 10**30, "Sun"
    )  # (0, 0, 30, YELLOW, 1.98892 * 10**30)
    second_sun.y_vel = -6 * 1000

    second_jupiter = Planet(
        15 * Planet.AU, 20 * Planet.AU, 5, ORANGE, 1898.13 * 10**24, "Jupiter"
    )
    second_jupiter.y_vel = -6 * 1000

    user_object = Planet(
        5 * Planet.AU, 5 * Planet.AU, 3, WHITE, 10 * sun.mass, "Custom"
    )

    #   main() iterates through this list of objects and updates each position. optional objects get entered here when clicked
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    def reset_button(
        msg, button_x, button_y, button_w, button_h, inactive_color, active_color
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            button_x + button_w > mouse[0] > button_x
            and button_y + button_h > mouse[1] > button_y
        ):
            pygame.draw.rect(
                WIN, active_color, (button_x, button_y, button_w, button_h)
            )
            if click[0] == 1:
                sun.orbit = []
                sun.x, sun.y = 0, 0
                sun.x_vel = 0
                sun.y_vel = 0

                earth.y_vel = 29.783 * 1000
                earth.orbit = []
                earth.x = -1 * Planet.AU
                earth.y = 0
                earth.x_vel = 0

                mars.y_vel = 24.077 * 1000
                mars.orbit = []
                mars.x = -1.524 * Planet.AU
                mars.y = 0
                mars.x_vel = 0

                mercury.y_vel = -47.4 * 1000
                mercury.orbit = []
                mercury.x = 0.387 * Planet.AU
                mercury.y = 0
                mercury.x_vel = 0

                venus.y_vel = -35.02 * 1000
                venus.orbit = []
                venus.x = 0.723 * Planet.AU
                venus.y = 0
                venus.x_vel = 0

                jupiter.y_vel = 13.07 * 1000
                jupiter.orbit = []
                jupiter.x = -5.2 * Planet.AU
                jupiter.y = 0
                jupiter.x_vel = 0

                saturn.y_vel = -9.68 * 1000
                saturn.orbit = []
                saturn.x = 9.5 * Planet.AU
                saturn.y = 0
                saturn.x_vel = 0

                uranus.y_vel = 6.8 * 1000
                uranus.orbit = []
                uranus.x = -19.8 * Planet.AU
                uranus.y = 0
                uranus.x_vel = 0

                neptune.y_vel = -5.43 * 1000
                neptune.orbit = []
                neptune.x = 30 * Planet.AU
                neptune.y = 0
                neptune.x_vel = 0

                global frames
                frames = 0
                if black_hole in planets:
                    black_hole.x_vel = 0
                    black_hole.y_vel = -6 * 1000
                    black_hole.x = 15 * Planet.AU
                    black_hole.y = 20 * Planet.AU
                    black_hole.orbit = []
                    planets.remove(black_hole)

                if second_sun in planets:
                    second_sun.x_vel = 0
                    second_sun.y_vel = -6 * 1000
                    second_sun.x = 15 * Planet.AU
                    second_sun.y = 20 * Planet.AU
                    second_sun.orbit = []
                    planets.remove(second_sun)

                if second_jupiter in planets:
                    second_jupiter.x_vel = 0
                    second_jupiter.y_vel = -6 * 1000
                    second_jupiter.x = 15 * Planet.AU
                    second_jupiter.y = 20 * Planet.AU
                    second_jupiter.orbit = []
                    planets.remove(second_jupiter)

                if user_object in planets:
                    user_object.orbit = []
                    user_object.x_vel = 0
                    user_object.y_vel = 0
                    planets.remove(user_object)

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    def add_planet_button(
        msg,
        button_x,
        button_y,
        button_w,
        button_h,
        inactive_color,
        active_color,
        add_planet=None,
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            button_x + button_w > mouse[0] > button_x
            and button_y + button_h > mouse[1] > button_y
        ):
            pygame.draw.rect(
                WIN, active_color, (button_x, button_y, button_w, button_h)
            )

            if click[0] == 1 and add_planet != None:
                planets.append(add_planet)

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    # working but want to add several object if clicked again, currently updates object position
    def place_planet_button(
        msg, button_x, button_y, button_w, button_h, inactive_color, active_color
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        global place_active

        if (
            button_x + button_w > mouse[0] > button_x
            and button_y + button_h > mouse[1] > button_y
        ) or place_active == True:
            pygame.draw.rect(
                WIN, active_color, (button_x, button_y, button_w, button_h)
            )

            if click[0] == 1:
                place_active = True

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    # update user object
    def update_object():
        global place_active
        mouse = pygame.mouse.get_pos()
        user_object.x = (mouse[0] - (WIDTH / 2)) / Planet.SCALE
        user_object.y = (mouse[1] - (HEIGHT / 2)) / Planet.SCALE
        planets.append(user_object)
        place_active = False
        # x = self.x * self.SCALE + WIDTH / 2

    #        x - width/2    /    self.SCALE = self.x

    def pause_button(
        msg, button_x, button_y, button_w, button_h, inactive_color, active_color
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            button_x + button_w > mouse[0] > button_x
            and button_y + button_h > mouse[1] > button_y
        ):
            pygame.draw.rect(
                WIN, active_color, (button_x, button_y, button_w, button_h)
            )

            if click[0] == 1:
                paused()

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    def paused():
        WIN.fill(BLACK)
        global pause
        pause = True

        while pause:
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pause = False

            resume_button("Resume", 200, 730, 100, 50, RED, YELLOW)

            for planet in planets:
                planet.draw(WIN)
            timeElapsedBox(frames)
            pygame.display.update()
            clock.tick(15)

    def resume_button(
        msg, button_x, button_y, button_w, button_h, inactive_color, active_color
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            button_x + button_w > mouse[0] > button_x
            and button_y + button_h > mouse[1] > button_y
        ):
            pygame.draw.rect(
                WIN, active_color, (button_x, button_y, button_w, button_h)
            )
            if click[0] == 1:
                global pause
                pause = False

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    def quit_button(
        msg, button_x, button_y, button_w, button_h, inactive_color, active_color
    ):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (
            button_x + button_w > mouse[0] > button_x
            and button_y + button_h > mouse[1] > button_y
        ):
            pygame.draw.rect(
                WIN, active_color, (button_x, button_y, button_w, button_h)
            )

            if click[0] == 1:
                pygame.quit()
        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    # takes in the number of frames generated since start and shows the simulated time that has passed. 1 frame = 1 day
    def timeElapsedBox(frames):
        if frames > 365:
            days = frames % 365
            years = frames // 365
            timeText = FONT.render(
                f"Time Elapsed: {years} Year(s) {days} Days", True, WHITE, DARK_GRAY
            )
        else:
            timeText = FONT.render(
                f"Time Elapsed: {frames} Days", True, WHITE, DARK_GRAY
            )
        timeTextBox = timeText.get_rect()
        timeTextBox.center = (WIDTH // 2, HEIGHT // 2 - 300)
        WIN.blit(timeText, timeTextBox)

    # can be used to quickly make text boxes
    def create_instruction_box(msg, x_pos, y_pos):
        instructionText = FONT.render(msg, True, WHITE, DARK_GRAY)
        instructionTextBox = instructionText.get_rect()
        instructionTextBox.center = (x_pos, y_pos)
        WIN.blit(instructionText, instructionTextBox)

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        # buttons
        add_planet_button("Black Hole", 50, 250, 100, 50, WHITE, YELLOW, black_hole)
        add_planet_button("Star", 50, 190, 100, 50, WHITE, YELLOW, second_sun)
        add_planet_button("Planet", 50, 130, 100, 50, WHITE, YELLOW, second_jupiter)
        place_planet_button("Place BH", 50, 450, 100, 50, WHITE, YELLOW)

        pause_button("Pause", 100, 730, 100, 50, YELLOW, RED)

        reset_button("Reset", 50, 790, 100, 50, RED, RED)
        quit_button("Quit", 50, 850, 100, 50, WHITE, YELLOW)

        # text box
        create_instruction_box(
            "Choose an option below. It will enter from bottom right", 225, 100
        )
        create_instruction_box("----- OR ------", 100, 375)
        create_instruction_box(
            'Click "Place BH" then click anywhere on screen', 210, 425
        )

        global frames, place_active
        frames += 1
        timeElapsedBox(frames)

        # event listeners
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and place_active == True:
                update_object()

        # draw the planets updrated positions and velocidies every frame
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
