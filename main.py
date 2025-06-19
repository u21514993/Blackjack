import pygame
import sys
from game import BlackjackGame

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
BACKGROUND_COLOR = (0, 102, 0)  # Dark green table

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# Initialize the game
game = BlackjackGame(screen)

def main():
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to game for processing
            game.handle_event(event)
        
        # Update game state
        game.update()
        
        # Render the game
        screen.fill(BACKGROUND_COLOR)
        game.draw()
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()