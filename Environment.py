import pygame

# Constants
WIDTH, HEIGHT, FPS = 800, 800, 60
BLACK, WHITE, RED, BLUE = (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 0, 255)

# Initialize Pygamekk
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

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the routes
    for start, end in routes:
        pygame.draw.line(screen, BLACK, start, end, 5)

    # Draw the bus (for simplicity, just a red rectangle representing the bus)
    pygame.draw.rect(screen, RED, (100, 90, 25, 25))  # Adjust coordinates and size as needed

    # Draw passengers (for simplicity, just a blue circle representing a passenger at a specific location)
    passenger_locations = [(100, 390), (390, 190)]  # Sample locations; adjust as needed
    for loc in passenger_locations:
        pygame.draw.rect(screen, BLUE, (loc[0], loc[1], 20, 20))  # Adjust radius as needed

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()