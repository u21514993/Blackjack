import pygame
from card import Card, Deck, Hand, Chip, CARD_WIDTH, CARD_HEIGHT

class BlackjackGame:
    # Game states
    STATE_BETTING = 0
    STATE_PLAYER_TURN = 1
    STATE_DEALER_TURN = 2
    STATE_GAME_OVER = 3
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Initialize game components
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand(is_dealer=True)
        
        # Game state variables
        self.state = self.STATE_BETTING
        self.player_money = 1000
        self.current_bet = 0
        self.message = "Place your bet!"
        
        # Load button images and positions
        self.setup_buttons()
        
        # Initialize chips
        self.chips = {}
        self.setup_chips()
        
        # Start a new round
        self.new_round()
    
    def setup_buttons(self):
        # This will be implemented to create buttons for hit, stand, etc.
        self.buttons = {}
        
        # Define buttons (position, size, text, color)
        button_y = self.screen_height - 100
        
        self.buttons["deal"] = pygame.Rect(50, button_y, 100, 50)
        self.buttons["hit"] = pygame.Rect(170, button_y, 100, 50)
        self.buttons["stand"] = pygame.Rect(290, button_y, 100, 50)
        self.buttons["double"] = pygame.Rect(410, button_y, 100, 50)
        self.buttons["split"] = pygame.Rect(530, button_y, 100, 50)
        self.buttons["insurance"] = pygame.Rect(650, button_y, 100, 50)
        self.buttons["surrender"] = pygame.Rect(770, button_y, 100, 50)
        self.buttons["clear_bet"] = pygame.Rect(890, button_y, 100, 50)
    
    def setup_chips(self):
        # Define chip values and load images
        chip_info = [
            (25, "Assets_Folder/Chip-25.png"),
            (50, "Assets_Folder/Chip-50.png"),
            (100, "Assets_Folder/Chip-100.png"),
            (500, "Assets_Folder/Chip-500.png"),
            (1000, "Assets_Folder/Chip-1000.png")
        ]
        
        # Position chips along the bottom of the screen
        chip_spacing = 60
        starting_x = (self.screen_width - (len(chip_info) * chip_spacing)) // 2
        chip_y = self.screen_height - 180
        
        for i, (value, image_path) in enumerate(chip_info):
            chip = Chip(value, image_path)
            chip.rect.topleft = (starting_x + i * chip_spacing, chip_y)
            self.chips[value] = chip
    
    def new_round(self):
        # Reset for a new round
        self.deck = Deck()  # Create a new deck to ensure enough cards
        self.deck.shuffle()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.state = self.STATE_BETTING
        # Do not reset current_bet here to preserve bet amount for the round
        # self.current_bet = 0  # Removed reset here
        self.message = "Place your bet!"
        # Force redraw by clearing the screen (optional)
        self.screen.fill((0, 102, 0))  # Dark green background
        pygame.display.flip()
    
    def deal_initial_cards(self):
        # Deal 2 cards to player and 1 card to dealer (hide second dealer card)
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        # Do not deal second dealer card yet (hole card hidden)
        # self.dealer_hand.add_card(self.deck.deal_card())
        
        # Check for blackjack
        if self.player_hand.value == 21:
            # For blackjack check, we need to deal the second dealer card temporarily
            self.dealer_hand.add_card(self.deck.deal_card())
            if self.dealer_hand.value == 21:
                self.message = "Both have Blackjack! Push."
                self.state = self.STATE_GAME_OVER
            else:
                self.message = "Blackjack! You win!"
                # Add bet plus 1.5 times bet for blackjack payout
                self.player_money += int(self.current_bet * 2.5)
                self.state = self.STATE_GAME_OVER
            # Remove the temporarily added dealer card to keep it hidden
            self.dealer_hand.cards.pop()
            self.dealer_hand.value -= self.dealer_hand.cards[-1].value if self.dealer_hand.cards else 0
        else:
            self.state = self.STATE_PLAYER_TURN
            self.message = "Your turn! Hit or Stand?"
    
    def player_hit(self):
        if self.state == self.STATE_PLAYER_TURN:
            self.player_hand.add_card(self.deck.deal_card())
            
            if self.player_hand.value > 21:
                self.message = "Bust! You lose."
                self.player_money -= self.current_bet
                self.state = self.STATE_GAME_OVER
            elif self.player_hand.value == 21:
                self.player_stand()  # Automatically stand on 21
    
    def player_stand(self):
        if self.state == self.STATE_PLAYER_TURN:
            self.state = self.STATE_DEALER_TURN
            self.dealer_play()
    
    def player_double(self):
        if self.state == self.STATE_PLAYER_TURN and len(self.player_hand.cards) == 2:
            if self.current_bet <= self.player_money:
                self.current_bet *= 2
                self.player_hit()
                if self.state == self.STATE_PLAYER_TURN:  # If not bust
                    self.player_stand()
    
    def player_split(self):
        # Placeholder for split logic
        pass
    
    def player_insurance(self):
        # Placeholder for insurance logic
        pass
    
    def player_surrender(self):
        # Placeholder for surrender logic
        pass
    
    def dealer_play(self):
        # Deal the dealer's hole card (second card) now that player stands
        self.dealer_hand.add_card(self.deck.deal_card())
        
        # Dealer hits until 17 or higher
        while self.dealer_hand.value < 17:
            self.dealer_hand.add_card(self.deck.deal_card())
        
        # Determine winner
        if self.dealer_hand.value > 21:
            self.message = "Dealer busts! You win!"
            self.player_money += self.current_bet * 2
        elif self.dealer_hand.value > self.player_hand.value:
            self.message = "Dealer wins!"
            self.player_money -= self.current_bet
        elif self.dealer_hand.value < self.player_hand.value:
            self.message = "You win!"
            self.player_money += self.current_bet * 2
        else:
            self.message = "Push! It's a tie."
        
        self.state = self.STATE_GAME_OVER
    
    def handle_chip_click(self, value):
        """Handle when a player clicks on a chip to bet"""
        if self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER:
            if value <= self.player_money:
                # Add chip value to current bet
                self.current_bet += value
                self.player_money -= value
                self.message = f"Bet: ${self.current_bet}. Click 'Deal' to play or add more chips."
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Check if any button was clicked
            for button_name, button_rect in self.buttons.items():
                if button_rect.collidepoint(pos):
                    self.handle_button_click(button_name)
            
            # Check if any chip was clicked (only in betting state)
            if self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER:
                for value, chip in self.chips.items():
                    if chip.is_clicked(pos):
                        self.handle_chip_click(value)
                        break
    
    def handle_button_click(self, button_name):
        if button_name == "deal" and (self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER):
            if self.current_bet > 0:
                if self.state == self.STATE_GAME_OVER:
                    self.new_round()
                self.deal_initial_cards()
            else:
                self.message = "Please place a bet first!"
        elif button_name == "clear_bet" and (self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER):
            self.player_money += self.current_bet
            self.current_bet = 0
            self.message = "Bet cleared. Place your bet!"
        elif self.state == self.STATE_PLAYER_TURN:
            if button_name == "hit":
                self.player_hit()
            elif button_name == "stand":
                self.player_stand()
            elif button_name == "double":
                self.player_double()
            elif button_name == "split":
                self.player_split()
            elif button_name == "insurance":
                self.player_insurance()
            elif button_name == "surrender":
                self.player_surrender()
    
    def update(self):
        # Update game state if needed
        pass
    
    def draw(self):
        # Draw hands
        dealer_y = 150
        player_y = 400
        
        # Draw dealer's hand
        self.dealer_hand.draw(self.screen, self.screen_width // 2 - (len(self.dealer_hand.cards) * CARD_WIDTH // 2), dealer_y)
        
        # Draw player's hand
        self.player_hand.draw(self.screen, self.screen_width // 2 - (len(self.player_hand.cards) * CARD_WIDTH // 2), player_y)
        
        # Draw UI elements
        self.draw_ui()
    
    def draw_ui(self):
        # Draw game message
        font = pygame.font.SysFont(None, 36)
        message_surface = font.render(self.message, True, (255, 255, 255))
        message_rect = message_surface.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(message_surface, message_rect)
        
        # Draw player money and current bet
        money_text = f"Money: ${self.player_money}  Bet: ${self.current_bet}"
        money_surface = font.render(money_text, True, (255, 255, 255))
        self.screen.blit(money_surface, (20, 20))
        
        # Draw buttons
        for button_name, button_rect in self.buttons.items():
            # Different colors based on game state
            if button_name == "deal" and (self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER) and self.current_bet > 0:
                color = (100, 200, 100)  # Green for active
            elif button_name == "clear_bet" and (self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER) and self.current_bet > 0:
                color = (200, 100, 100)  # Red for active
            elif self.state == self.STATE_PLAYER_TURN and button_name in ["hit", "stand", "double", "split", "insurance", "surrender"]:
                color = (100, 200, 100)  # Green for active
            else:
                color = (100, 100, 100)  # Gray for inactive
            
            pygame.draw.rect(self.screen, color, button_rect)
            button_text = font.render(button_name.capitalize(), True, (0, 0, 0))
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
        
        # Draw chips
        if self.state == self.STATE_BETTING or self.state == self.STATE_GAME_OVER:
            for value, chip in self.chips.items():
                chip.draw(self.screen, chip.rect.x, chip.rect.y)
                
                # Draw chip value text
                font = pygame.font.SysFont(None, 20)
                value_text = font.render(f"${value}", True, (0, 0, 0))
                text_rect = value_text.get_rect(center=(chip.rect.centerx, chip.rect.bottom + 15))
                self.screen.blit(value_text, text_rect)