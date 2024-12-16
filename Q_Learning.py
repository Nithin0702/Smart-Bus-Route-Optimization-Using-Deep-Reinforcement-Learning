import pygame
import random
import numpy as np

# Constants
WIDTH = 800
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define the Bus class
class Bus(pygame.sprite.Sprite):
    def __init__(self, x, y, q_table):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.route_index = 0
        self.q_table = q_table
        self.state = 0
        self.alpha = 0.1
        self.gamma = 0.9

    def update(self):
        self.move_along_route()

    def move_along_route(self):
        current_route = routes[self.route_index]
        target_point = current_route[1]
        dx = target_point[0] - self.rect.centerx
        dy = target_point[1] - self.rect.centery
        distance = np.hypot(dx, dy)

        if distance > 1:  # Adjust the threshold as needed
            speed = 2
            vx = dx / distance * speed
            vy = dy / distance * speed
            self.rect.centerx += vx
            self.rect.centery += vy
        else:
            next_route_index = self.choose_next_route()
            if next_route_index is not None:
                self.route_index = next_route_index
            else:
                self.route_index = 0

    def choose_next_route(self):
        current_state = self.state
        q_values = self.q_table[current_state]
        valid_routes = [i for i, route in enumerate(routes) if route[0] == routes[current_state][1]]
        if len(valid_routes) == 0:
            # No more routes to explore
            return None
        
        passengers_per_route = [len([p for p in passengers if p.route_index == i]) for i in valid_routes]
        max_passengers = max(passengers_per_route)
        max_passenger_routes = [route for route, passengers_count in zip(valid_routes, passengers_per_route) if
                                passengers_count == max_passengers]
        return random.choice(max_passenger_routes)

    def update_q_table(self, reward, next_state):
        current_state = self.state
        q_values = self.q_table[current_state]
        max_q_value = np.max(self.q_table[next_state])
        q_values[self.route_index] += self.alpha * (reward + self.gamma * max_q_value - q_values[self.route_index])
        self.state = next_state  # Update the current state to the next state

        # Print the state, action, next state, and reward
        print("State: {}, Action: {}, Next state: {}, Reward: {}".format(current_state, self.route_index, next_state, reward))
        self.state = next_state

    def print_q_table_format(self):
        for state, q_values in enumerate(self.q_table):
            for action, reward in enumerate(q_values):
                next_state = action
                print("State: {}, Action: {}, Next state: {}, Reward: {}".format(state, action, next_state, reward))

    def calculate_total_distance(self):
        total_distance = 0
        for i in range(self.route_index, len(routes) - 1):
            start_point = routes[i][0]
            end_point = routes[i + 1][1]
            dx = end_point[0] - start_point[0]
            dy = end_point[1] - start_point[1]
            distance = np.hypot(dx, dy)
            total_distance += distance
        return total_distance



# Define the Passenger class

class Passenger(pygame.sprite.Sprite):
    def __init__(self, x, y, route_index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.route_index = route_index

    def update(self):
        pass





# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bus Route Planning System")
clock = pygame.time.Clock()

# Sprite groups
all_sprites = pygame.sprite.Group()
buses = pygame.sprite.GroupSingle()
passengers = pygame.sprite.Group()  # Create the passengers group

# Define the routes
route1 = [(100, 100), (350, 100)]
route2 = [(350, 100), (350, 200)]
route3 = [(350, 200), (500, 200)]
route4 = [(500, 200), (500, 400)]
route5 = [(500, 400), (650, 400)]
route6 = [(650, 400), (650, 500)]
route7 = [(650, 500), (550, 500)]
route8 = [(550, 500), (550, 700)]
route9 = [(550, 700), (350, 700)]
route10 = [(350, 700), (350, 500)]
route11 = [(350, 500), (100, 500)]
route12 = [(100, 500), (100, 400)]
route13 = [(100, 400), (200, 400)]
route14 = [(200, 400), (200, 200)]
route15 = [(200, 200), (450, 200)]
route16 = [(450, 200), (450, 300)]
route17 = [(450, 300), (550, 300)]
route18 = [(550, 300), (550, 500)]
route19 = [(550, 500), (450, 500)]
route20 = [(450, 500), (450, 300)]
routes = [route1, route2, route3, route4, route5, route6, route7, route8, route9, route10, route11, route12, route13, route14, route15, route16, route17, route18, route19, route20]

# Create the Q-table

num_states = len(routes)
num_actions = len(routes)
q_table = np.zeros((num_states, num_actions))

# Create the bus
bus = Bus(100, 100, q_table)
all_sprites.add(bus)
buses.add(bus)

# Create passengers along the routes
for route_index, route in enumerate(routes):
    passenger_x = random.randint(min(route[0][0], route[1][0]), max(route[0][0], route[1][0]))
    passenger_y = random.randint(min(route[0][1], route[1][1]), max(route[0][1], route[1][1]))
    passenger = Passenger(passenger_x, passenger_y, route_index)
    all_sprites.add(passenger)
    passengers.add(passenger)  # Add the passenger to the passengers group


# Game loop
running = True
previous_passenger_count = 0
previous_time = pygame.time.get_ticks()
episode = 0
print_q_table = True  # Enable printing of Q-table
MAX_EPISODES = 3  # Define the maximum number of episodes as needed
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collision between bus and passengers
    bus_passenger_collision = pygame.sprite.spritecollide(bus, passengers, True)
    for passenger in bus_passenger_collision:
        print("Bus reached a passenger!")
        bus.update_q_table(1, passenger.route_index)

    # Count the number of remaining passengers
    current_passenger_count = len(passengers)
    current_time = pygame.time.get_ticks()

    if current_passenger_count < previous_passenger_count:
        bus.update_q_table(1, bus.route_index)
    elif current_passenger_count == previous_passenger_count:
        time_difference = current_time - previous_time
        if time_difference >= 5000:  # Increase the threshold as needed
            bus.update_q_table(-1, bus.route_index)
            previous_time = current_time

    previous_passenger_count = current_passenger_count

    # Render
    screen.fill(WHITE)
    for route in routes:
        pygame.draw.line(screen, BLACK, route[0], route[1], 2)

    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

    # Check if all passengers have been picked up
    if current_passenger_count == 0:
        episode += 1
        if episode > MAX_EPISODES:  # Define the maximum number of episodes as needed
            running = False
        else:
            # Reset passengers
            for route_index, route in enumerate(routes):
                passenger_x = random.randint(min(route[0][0], route[1][0]), max(route[0][0], route[1][0]))
                passenger_y = random.randint(min(route[0][1], route[1][1]), max(route[0][1], route[1][1]))
                passenger = Passenger(passenger_x, passenger_y, route_index)
                all_sprites.add(passenger)
                passengers.add(passenger)

    # Quit the game
pygame.quit()
