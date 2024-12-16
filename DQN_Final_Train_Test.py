import pygame
import random
import numpy as np
import tensorflow as tf
from collections import deque

# Constants
WIDTH, HEIGHT, FPS = 800, 800, 60
BLACK, WHITE, RED, BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255)

# DQN Hyperparameters
DQN_LEARNING_RATE = 0.001
DQN_DISCOUNT_FACTOR = 0.95
DQN_EXPLORATION_PROB = 0.1
DQN_BATCH_SIZE = 32
DQN_MEMORY_SIZE = 2000

# Define the Bus class
class Bus(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.route_index = 0
        self.state = 0
        self.model = self.build_model()
        self.can_move = True

    def build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(4,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(len(routes), activation='linear')
        ])
        optimizer = tf.keras.optimizers.Adam(learning_rate=DQN_LEARNING_RATE)
        model.compile(optimizer='adam', loss='mse')
        return model



    def move_along_route(self):
        global score 

        # Check if we've reached the target point
        target_point = routes[self.route_index][1]
        if self.rect.center == target_point:
            # Move to the next route index
            self.route_index = (self.route_index + 1) % len(routes)
            target_point = routes[self.route_index][1]
        
        # Move towards the target point
        self.move_towards_point(target_point)
        
        inside_routes = self.is_inside_routes()
        if not inside_routes:
            # Penalize for going outside the routes
            reward = -1
            score -= 1  # Decrease score for penalty
            print(f"Bus went outside the routes! Score penalty: {score}.")
        else:
            # Check for nearby passengers
            nearby_passengers = pygame.sprite.spritecollide(self, passengers, False)
            if nearby_passengers:
                for passenger in nearby_passengers:
                    if not passenger.picked_up:
                        # Provide a positive reward for picking up nearby passengers
                        reward = 2
                        passenger.picked_up = True
                        score += 2
                        print(f"Passenger picked up! Score: {score}")
                    else:
                        # Penalize for being near a passenger that has already been picked up
                        reward = -1
            else:
                # Penalize for not picking up any nearby passengers
                reward = -1  # Adjust the negative reward value as needed

        # Example: Update Q-values for reinforcement learning
        next_state = np.array([[self.state, self.route_index, 0, 0]])
        self.update_q_values(np.array([[self.state, self.route_index, 0, 0]]), self.route_index, reward, next_state, False)
   
    def collect_experience(self, reward, done):
        state = np.array([[self.state, self.route_index, 0, 0]])
        action = self.route_index
        next_state = np.array([[self.state, self.route_index, 0, 0]])
        replay_buffer.append((state, action, reward, next_state, done))

    def is_inside_routes(self):
        for start, end in routes:
            if pygame.draw.line(screen, BLACK, start, end, 5).colliderect(self.rect):
                return True  # The bus is inside the routes
        return False  # The bus is outside the routes

    def move_towards_point(self, target_point):
        dx, dy = target_point[0] - self.rect.centerx, target_point[1] - self.rect.centery
        distance = np.sqrt(dx**2 + dy**2)
        if distance > 0:
            # Normalize the direction vector and move towards the target point
            dx, dy = dx / distance, dy / distance
            self.rect.centerx += dx * 5  # Speed 
            self.rect.centery += dy * 5

    def choose_next_route(self):
        if np.random.rand() < DQN_EXPLORATION_PROB:
            # Explore: Choose a random action
            return random.choice(valid_next_routes)
        else:
            # Exploit: Choose the route with the most passengers waiting
            valid_next_routes = [i for i, route in enumerate(routes) if route[0] == routes[self.route_index][1]]
            passenger_counts = {route: 0 for route in valid_next_routes}
            for passenger in passengers:
                if passenger.route_index in valid_next_routes:
                    passenger_counts[passenger.route_index] += 1
            most_passengers = max(passenger_counts, key=passenger_counts.get)
            return most_passengers

    def update_q_values(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = (reward + DQN_DISCOUNT_FACTOR * np.amax(self.model.predict(next_state)[0]))
        target_f = self.model.predict(state)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=10000, verbose=0)

# Initialize a score variable
score = 0

# Define the Passenger class
class Passenger(pygame.sprite.Sprite):
    def __init__(self, x, y, route_index):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Size of passenger sprite
        self.image.fill(BLUE)  # Color of passenger sprite
        self.rect = self.image.get_rect(center=(x, y))
        self.route_index = route_index  # The route that the passenger is associated with
        self.picked_up = False  # Flag to check if the passenger has been picked up

    def update(self):
        if self.picked_up:
            # Logic to handle what happens when the passenger is picked up
            self.kill()

restricted_area = (300, 300, 400, 400)  # Replace with the actual coordinates

def generate_passengers():
    passengers.empty()  # Clear existing passengers
    for i, (start, end) in enumerate(routes):
        # Skip route 1
        if i == 0:
            continue

        # Randomly place a passenger along the route for all other routes
        rand_x = random.uniform(min(start[0], end[0]), max(start[0], end[0]))
        rand_y = random.uniform(min(start[1], end[1]), max(start[1], end[1]))
        passenger = Passenger(rand_x, rand_y, i)
        passengers.add(passenger)
        all_sprites.add(passenger)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bus Route Planning System")
clock = pygame.time.Clock()


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


# Initialize buses and passengers
bus = Bus(100, 100)
passengers = pygame.sprite.Group()

# Initialize all_sprites group
all_sprites = pygame.sprite.Group()
all_sprites.add(bus)  # Add the bus to the all_sprites group

# Generate initial passengers
generate_passengers()

# Generate some passengers and add them to the groups
for i, (start, end) in enumerate(routes):
    # Place a passenger at the end of each route
    passenger = Passenger(*end, i)
    passengers.add(passenger)
    all_sprites.add(passenger)

# Replay buffer
replay_buffer = deque(maxlen=DQN_MEMORY_SIZE)

# Main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    bus.move_along_route()
    collided_passengers = pygame.sprite.spritecollide(bus, passengers, dokill=True)  # Passengers are removed upon collision
    for passenger in collided_passengers:
        passenger.picked_up = True
        reward = 2  # Increase score as a reward for picking up a passenger
        done = False  # Set it to True if the episode ends
        bus.collect_experience(reward, done)
        # Increase score as a reward for picking up a passenger

    # Check if all passengers have been picked up and respawn them if true
    if not passengers:  # passengers group is empty
        generate_passengers()


    # Update game state
    all_sprites.update()

    # Clear the screen before drawing anything
    screen.fill(WHITE)

    # Draw the routes on each frame
    for start, end in routes:
        pygame.draw.line(screen, BLACK, start, end, 5)

    # Draw all sprites
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
