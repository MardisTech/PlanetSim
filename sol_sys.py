import pygame
from planet import *
from static import *

pygame.init()

# julie wants to zoom in
# add custom object input for place button
# look into hooking in nasa API for real initial positions when launched instead of initializing on x axis
# add planet info box - user will be able to inspect an object to see its velocity and other props
# add a slow or fastforward frames/sim option, possibly a rewind option that draws from reversed list of orbit
# add acceleration vector arrow to see orbit disturbance better!
# Should I zoom in?




def main():
    run = True
    clock = pygame.time.Clock()
    

    sun = Planet(
        0, 0, 7.5, YELLOW, 1.98892 * 10**30, "Sun"
    )  # (0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(
        -1 * Planet.AU, 0, 4, BLUE, 5.9742 * 10**24, "Earth", y_vel = 29.783 * 1000
    )  # (-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(
        -1.524 * Planet.AU, 0, 3, RED, 6.39 * 10**23, "Mars", y_vel = 24.077 * 1000
    )  # (-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(
        0.387 * Planet.AU, 0, 2, DARK_GRAY, 3.30 * 10**23, "Mercury", y_vel = -47.4 * 1000
    )  # 0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23
    mercury.y_vel = -47.4 * 1000

    venus = Planet(
        0.723 * Planet.AU, 0, 3.5, WHITE, 4.8685 * 10**24, "Venus", y_vel = -35.02 * 1000
    )  # 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(-5.2 * Planet.AU, 0, 14, ORANGE, 1898.13 * 10**24, "Jupiter", y_vel = 13.07 * 1000)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 12, TAN, 5.683 * 10**26, "Saturn", y_vel = -9.68 * 1000)
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(-19.8 * Planet.AU, 0, 10, BABY_BLUE, 8.6 * 10**25, "Uranus", y_vel = 6.8 * 1000)
    uranus.y_vel = 6.8 * 1000

    neptune = Planet(30 * Planet.AU, 0, 9, DARK_BLUE, 1.024 * 10**24, "Neptune", y_vel = -5.43 * 1000)  #
    neptune.y_vel = -5.43 * 1000

    #   optional objects that user can choose to add to game by clicking the corresponding button
    black_hole = Planet(
        15 * Planet.AU, 20 * Planet.AU, 2, WHITE, 5 * sun.mass, "BH", y_vel = -6 * 1000
    )
    black_hole.y_vel = -6 * 1000

    second_sun = Planet(
        15 * Planet.AU, 20 * Planet.AU, 7.5, YELLOW, 1.98892 * 10**30, "Sun 2.0", y_vel = -6 * 1000
    )  # (0, 0, 30, YELLOW, 1.98892 * 10**30)
    second_sun.y_vel = -6 * 1000

    second_jupiter = Planet(
        15 * Planet.AU, 20 * Planet.AU, 5, ORANGE, 1898.13 * 10**24, "Jupiter 2.0", y_vel = -6 * 1000
    )
    second_jupiter.y_vel = -6 * 1000

    user_object = Planet(
        5 * Planet.AU, 5 * Planet.AU, 3, WHITE, 10 * sun.mass, "BH"
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
                for planet in planets:
                    planet.reset()
                    if planet.name in PLACEABLE_OBJECT_NAMES:
                        planets.remove(planet)

                
                global frames
                frames = 0

                global TIMESTEP, TIMESTEP_MULTIPLIER
                TIMESTEP = (3600 * 24)
                TIMESTEP_MULTIPLIER = 1

                

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


    def speed_up_button(
        msg,
        button_x,
        button_y,
        button_w,
        button_h,
        inactive_color,
        active_color,
    ):
        global TIMESTEP, TIMESTEP_MULTIPLIER
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
                TIMESTEP_MULTIPLIER = TIMESTEP_MULTIPLIER * 2
                TIMESTEP = TIMESTEP*TIMESTEP_MULTIPLIER
                for planet in planets:
                    planet.update_timestep(new_timestep=TIMESTEP)

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

    def slow_button(
        msg,
        button_x,
        button_y,
        button_w,
        button_h,
        inactive_color,
        active_color,
    ):
        global TIMESTEP, TIMESTEP_MULTIPLIER
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
                TIMESTEP_MULTIPLIER = 1/2
                TIMESTEP = TIMESTEP*TIMESTEP_MULTIPLIER
                for planet in planets:
                    planet.update_timestep(new_timestep=TIMESTEP)

        else:
            pygame.draw.rect(
                WIN, inactive_color, (button_x, button_y, button_w, button_h)
            )

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ((button_x + (button_w / 2)), (button_y + (button_h / 2)))
        WIN.blit(button_text, textRect)

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
        global pause,TIMESTEP_MULTIPLIER
        pause = True

        while pause:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pause = False

            resume_button("Paused", 200 * BUTTON_WIDTH_RATIO, 730 * BUTTON_HEIGHT_RATIO, BUTTON_WIDTH, BUTTON_HEIGHT, RED, YELLOW)

            for planet in planets:
                planet.draw(WIN)
            timeElapsedBox(frames*TIMESTEP_MULTIPLIER)
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

        global BUTTON_WIDTH, BUTTON_HEIGHT, current_window_w, current_window_h, SCREEN_CHANGE_RATIO_W, SCREEN_CHANGE_RATIO_H

        # text box
        create_instruction_box(
            "Interstellar Visitor", 100 * SCREEN_CHANGE_RATIO_W, 80 * SCREEN_CHANGE_RATIO_H
        )

        # buttons
        add_planet_button("Planet", 25 * SCREEN_CHANGE_RATIO_W, 130 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, YELLOW, second_jupiter)
        add_planet_button("Star", 25 * SCREEN_CHANGE_RATIO_W, 190 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, YELLOW, second_sun)
        add_planet_button("Black Hole", 25 * SCREEN_CHANGE_RATIO_W, 250 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, YELLOW, black_hole)
        


        
        create_instruction_box(
            'Point and Click', 100 * SCREEN_CHANGE_RATIO_W, 400 * SCREEN_CHANGE_RATIO_H
        )

        place_planet_button("Place BH", 25 * SCREEN_CHANGE_RATIO_W, 450 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, YELLOW)

        speed_up_button(">>>", 25 * SCREEN_CHANGE_RATIO_W, 610 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, YELLOW, RED)
        slow_button(">", 25 * SCREEN_CHANGE_RATIO_W, 670 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, YELLOW, RED)

        pause_button("Pause", 25 * SCREEN_CHANGE_RATIO_W, 730 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, YELLOW, RED)
        reset_button("Reset", 25 * SCREEN_CHANGE_RATIO_W, 790 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, RED, RED)
        quit_button("Quit", 25 * SCREEN_CHANGE_RATIO_W, 850 * SCREEN_CHANGE_RATIO_H, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, YELLOW)




        global frames, place_active
        frames += 1
        timeElapsedBox(frames*TIMESTEP_MULTIPLIER)

        # event listeners
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and place_active == True:
                update_object()

            if event.type == pygame.VIDEORESIZE:
                current_window_w, current_window_h = pygame.display.get_surface().get_size()

                BUTTON_WIDTH = current_window_w * BUTTON_WIDTH_RATIO

                BUTTON_HEIGHT = current_window_h * BUTTON_HEIGHT_RATIO

                SCREEN_CHANGE_RATIO_W = current_window_w / WIDTH

                SCREEN_CHANGE_RATIO_H = current_window_h / HEIGHT

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
