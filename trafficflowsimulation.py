import pygame
import random
import sys
import time

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_DARK = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define classes
class Car:
    def __init__(self, name, position, speed, lane):
        self.name = name
        self.position = position
        self.speed = speed
        self.lane = lane

class Road:
    def __init__(self, road_length, num_lanes, intersections):
        self.road_length = road_length
        self.num_lanes = num_lanes
        self.traffic_light = TrafficLight()
        self.intersections = intersections
        self.cars = []

    def draw(self, screen):
        for i in range(len(self.intersections)):
            pygame.draw.rect(screen, GRAY_DARK, [0, i * 200, self.road_length * 20, 50])  # Upper Boundary
            pygame.draw.rect(screen, GRAY_DARK, [0, 150 + i * 200, self.road_length * 20, 50])  # Lower Boundary
            pygame.draw.line(screen, GRAY_DARK, (0, 75 + i * 200), (self.road_length * 20, 75 + i * 200), 2)  # Middle Divider
            pygame.draw.line(screen, GRAY_DARK, (0, 125 + i * 200), (self.road_length * 20, 125 + i * 200), 2)  # Lower Divider
            pygame.draw.line(screen, GRAY_DARK, (0, 50 + i * 200), (self.road_length * 20, 50 + i * 200), 4)  # Road Boundary
            pygame.draw.line(screen, GRAY_DARK, (0, 150 + i * 200), (self.road_length * 20, 150 + i * 200), 4)  # Road Boundary
            pygame.draw.line(screen, GRAY_DARK, (self.road_length * 10, 50 + i * 200), (self.road_length * 10, 150 + i * 200), 2)  # Center Divider
            # Draw intersections
            for intersection in self.intersections[i]:
                pygame.draw.circle(screen, GRAY_DARK, intersection, 5)

        if self.traffic_light.color == RED:
            pygame.draw.circle(screen, RED, (750, 25), 10)
        else:
            pygame.draw.circle(screen, GREEN, (750, 25), 10)

class TrafficLight:
    def __init__(self):
        self.color = GREEN
        self.green_duration = 200  # Number of frames for green light
        self.red_duration = 100  # Number of frames for red light
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.color == GREEN:
            if self.timer >= self.green_duration:
                self.color = RED
                self.timer = 0
        else:
            if self.timer >= self.red_duration:
                self.color = GREEN
                self.timer = 0

class TrafficSimulation:
    def __init__(self, roads, num_cars, max_speed):
        self.roads = roads
        self.num_cars = num_cars
        self.max_speed = max_speed
        self.generate_cars()
        self.start_time = time.time()
        self.cars_crossed = 0

    def generate_cars(self):
        for road in self.roads:
            road.cars = []
            for _ in range(self.num_cars):
                lane = random.randint(0, road.num_lanes - 1)
                speed = random.uniform(1, self.max_speed)
                car = Car(name=f"Car {len(road.cars) + 1}", position=0, speed=speed, lane=lane)
                road.cars.append(car)

    def update(self):
        for road in self.roads:
            if road.traffic_light.color == GREEN:
                for car_index, car in enumerate(road.cars):
                    if car_index != 0:
                        car.speed = min(car.speed, road.cars[car_index - 1].speed)
                    car.speed = min(car.speed, self.max_speed)
                    car.position += car.speed
                    car.position %= road.road_length
                    car.lane %= road.num_lanes

                    # Check if car has crossed the road
                    if car.position >= road.road_length - 1:
                        self.cars_crossed += 1

        # Update traffic light after updating all roads
        for road in self.roads:
            road.traffic_light.update()

    def get_update_time(self):
        return int(time.time() - self.start_time)

def main():
    pygame.init()

    # Set up the screen
    screen_width = 800
    screen_height = 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Traffic Simulation")

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Define roads and intersections
    intersections = [
        [(100, 100), (200, 100)],
        [(100, 300), (200, 300)]
    ]
    road1 = Road(40, 2, intersections)
    road2 = Road(40, 2, intersections)
    roads = [road1, road2]

    # Create a traffic simulation
    sim = TrafficSimulation(roads, num_cars=5, max_speed=5)

    # Fonts for text display
    font = pygame.font.Font(None, 24)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the traffic simulation
        sim.update()

        # Draw everything
        screen.fill(WHITE)
        for road in roads:
            road.draw(screen)
            for car in road.cars:
                pygame.draw.rect(screen, BLACK, [car.position * 20, car.lane * 200 + 75, 20, 50])  # Draw cars

        # Draw text at the bottom of the screen
        update_time_text = font.render(f"Time: {sim.get_update_time()} seconds", True, BLACK)
        cars_crossed_text = font.render(f"Cars Crossed: {sim.cars_crossed} per minute", True, BLACK)
        if sim.cars_crossed > 100:
            over_traffic_text = font.render("Over Traffic!", True, RED)
            screen.blit(over_traffic_text, (screen_width - 150, screen_height - 25))
        screen.blit(update_time_text, (10, screen_height - 50))
        screen.blit(cars_crossed_text, (10, screen_height - 25))

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
