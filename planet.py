from static import *
import math 
import pygame
from collections import deque

pygame.init()

WIN = pygame.display.set_mode(
    (WIDTH, HEIGHT), flags=pygame.RESIZABLE
)  
pygame.display.set_caption("sol_sys")
FONT = pygame.font.SysFont("comic sans", 15)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 25 / AU  # 1 AU = 100 PIXELS @  250 / AU
    MAX_ORBIT_POINTS = 500  # Maximum number of points to keep in the orbit list

    global TIMESTEP

    def __init__(self, x, y, radius, color, mass, name, x_vel = 0, y_vel = 0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.TIMESTEP = TIMESTEP
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.orbit = deque(maxlen=self.MAX_ORBIT_POINTS)  # Use deque for efficient orbit management

        self.x0 = x
        self.y0 = y
        self.radius0 = radius
        self.color0 = color
        self.mass0 = mass
        self.name0 = name
        self.TIMESTEP0 = TIMESTEP
        self.sun0 = False
        self.distance_to_sun0 = 0
        self.x_vel0 = x_vel
        self.y_vel0 = y_vel
        self.orbit0 = (
            []
        )

    def reset(self):
        self.x = self.x0
        self.y = self.y0
        self.radius = self.radius0
        self.color = self.color0
        self.mass = self.mass0
        self.name = self.name0
        self.TIMESTEP = self.TIMESTEP0
        self.sun = self.sun0
        self.distance_to_sun = self.distance_to_sun0
        self.x_vel = self.x_vel0
        self.y_vel = self.y_vel0
        self.orbit = self.orbit0

    def update_timestep(self, new_timestep):
        self.TIMESTEP = new_timestep


    def draw(self, win):
        x = (
            self.x * self.SCALE + WIDTH / 2
        )  # adding half the screen dimensions makes our values of 0,0 at the middle of the WIN, instead of 0,0 being at the top left corner
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = [
                (point[0] * self.SCALE + WIDTH / 2, point[1] * self.SCALE + HEIGHT / 2)
                for point in self.orbit
            ]
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
        self.orbit.append((self.x, self.y))  # Automatically handles maxlen with deque

