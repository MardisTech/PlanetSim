from ctypes.wintypes import POINT
from turtle import width
import pygame
import math
pygame.init()

# julie wants to zoom in
# place planet somewhere in system statically. onclick button, wait for input mouseclick grab x,y create object at the grabbed x,y
# could seperate planets into 4 spheres that act as 1 when close together but can seperate and act seperately if gravity force is strong enough
# add a reset method
# add a slow time function

WIDTH, HEIGHT = 1600, 1000 # originally at  800 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #want to implement pygame.RESIZABLE but sim doesnt rescale itself to fit the new resolution
pygame.display.set_caption("Planet Orbits Simulation (To Scale)")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
DARK_GRAY = (80, 78, 81)
ORANGE = (255, 165, 0)
TAN = (188,152,126)
BABY_BLUE = (137, 207, 240)
DARK_BLUE =  (32, 42, 68)
BLACK = (0,0,0)
FONT = pygame.font.SysFont("comic sans", 15)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 25 / AU   # 1 AU = 100 PIXELS @  250 / AU
    TIMESTEP = 3600*24 # 1 DAY IN SECONDS, each frame update will represent 1 day of movement in orbit

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y 
        self.radius = radius 
        self.color = color 
        self.mass = mass
        self.name = name

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = [] #this is a list of x,y position values for each planet so we can draw a line at those positions
                        #a problem with this is that it slows the program down after a while because how big he lists get
        
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2 #adding half the screen dimensions makes our values of 0,0 at the middle of the WIN, instead of 0,0 being at the top left corner
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
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))

        pygame.draw.circle(win, self.color, (x, y), self.radius) #drawing planets as circles

    def attraction(self, other):
        other_x, other_y = other.x, other.y #other planets distance from current planet
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2 #  F =(GmM)/r**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets: # ITERATING through the planets in planets[] to add all forces from other objects into total_f
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP # V = F/M * T
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP # X = V * T
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()
    frames = 0
    

    sun = Planet(0, 0, 7.5, YELLOW, 1.98892 * 10**30, "Sun") #(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 4, BLUE, 5.9742 * 10**24, "Earth") #(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 3, RED, 6.39 * 10**23, "Mars") #(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 2, DARK_GRAY, 3.30 * 10**23, "Mercury") #0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 3.5, WHITE, 4.8685 * 10**24, "Venus") #0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24
    venus.y_vel = -35.02 * 1000
    
    jupiter = Planet(-5.2 * Planet.AU, 0, 14, ORANGE, 1898.13 * 10**24, "Jupiter")
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 12, TAN, 5.683 * 10**26, "Saturn")
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(-19.8 * Planet.AU, 0, 10, BABY_BLUE, 8.6 * 10**25, "Uranus")
    uranus.y_vel = 6.8 * 1000

    neptune = Planet(30 * Planet.AU, 0, 9,  DARK_BLUE, 1.024 * 10**24, "Neptune") #
    neptune.y_vel = -5.43 * 1000
    
#Next is list of optional 'planets' that user can choose to add to game by clicking the corresponding button
    black_hole = Planet(15* Planet.AU, 20 * Planet.AU, 2, WHITE, 5* sun.mass, "Black Hole") # trying to change y pos to bottom of screen, not working for some reason
    black_hole.y_vel = -6 * 1000

    second_sun = Planet(15* Planet.AU, 20 * Planet.AU, 7.5, YELLOW, 1.98892 * 10**30, "Sun") #(0, 0, 30, YELLOW, 1.98892 * 10**30)
    second_sun.y_vel = -6 * 1000

    second_jupiter = Planet(15 * Planet.AU, 20* Planet.AU, 5, ORANGE, 1898.13 * 10**24, "Jupiter")
    second_jupiter.y_vel = -6 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
    
    def create_button(msg, button_x, button_y, button_w, button_h, inactive_color, active_color, add_planet = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if button_x + button_w > mouse[0] > button_x and button_y + button_h > mouse[1] > button_y:
            pygame.draw.rect(WIN, active_color, (button_x, button_y, button_w, button_h))

            if click[0] == 1 and add_planet != None:
                planets.append(add_planet)

        else:
            pygame.draw.rect(WIN, inactive_color, (button_x, button_y, button_w, button_h))

        button_text = FONT.render(msg, True, BLACK)
        textRect = button_text.get_rect()
        textRect.center = ( (button_x+(button_w/2)), (button_y + (button_h/2)) )
        WIN.blit(button_text, textRect)
    
    def timeElapsedBox(frames):
        if frames > 365:
            days = frames % 365
            years = frames // 365
            timeText = FONT.render(f'Time Elapsed: {years} Years {days} Days', True, WHITE, DARK_GRAY)
        else:
            timeText = FONT.render(f'Time Elapsed: {frames} Days', True, WHITE, DARK_GRAY)
        timeTextBox = timeText.get_rect()
        timeTextBox.center = (WIDTH // 2, HEIGHT // 2 - 300)
        WIN.blit(timeText, timeTextBox)

    
        



    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        
        

        create_button("Black Hole", 50, 250, 100, 50, WHITE, YELLOW, black_hole)
        create_button("Star", 50, 190, 100, 50, WHITE, YELLOW, second_sun)
        create_button("Planet", 50, 130, 100, 50, WHITE, YELLOW, second_jupiter)
        create_button("Quit", 50, 500, 100, 50, WHITE, YELLOW, pygame.QUIT)
        
        frames += 1
        timeElapsedBox(frames)
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    
    pygame.quit()

main() 
