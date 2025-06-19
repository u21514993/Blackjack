import pygame
import os
import random

CARD_WIDTH = 71
CARD_HEIGHT = 96

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = None
        self.face_up = True
    
    def load_image(self):
        # Convert rank for face cards and aces
        rank_name = self.rank
        if self.rank == 'A':
            rank_name = 'ace'
        elif self.rank == 'K':
            rank_name = 'king'
        elif self.rank == 'Q':
            rank_name = 'queen'
        elif self.rank == 'J':
            rank_name = 'jack'
        
        if self.face_up:
            file_name = f"Assets_Folder/cards/{rank_name}_of_{self.suit}.png"
        else:
            file_name = "Assets_Folder/cards/back.png"  # Make sure you have this file
        
        try:
            self.image = pygame.image.load(file_name)
            self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        except pygame.error:
            print(f"Error loading image: {file_name}")
            # Create placeholder
            self.image = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
            self.image.fill((200, 200, 200))
    
    def draw(self, screen, x, y):
        if self.image is None:
            self.load_image()
        screen.blit(self.image, (x, y))

class Deck:
    def __init__(self):
        self.cards = []
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop() if self.cards else None

class Hand:
    def __init__(self, is_dealer=False):
        self.cards = []
        self.value = 0
        self.is_dealer = is_dealer
    
    def add_card(self, card):
        self.cards.append(card)
        self.update_value()
    
    def reveal(self):
        for card in self.cards:
            card.face_up = True
        self.update_value()
    
    def update_value(self):
        self.value = 0
        aces = 0
        for card in self.cards:
            if not card.face_up:
                continue
            if card.rank in ['J', 'Q', 'K']:
                self.value += 10
            elif card.rank == 'A':
                self.value += 11
                aces += 1
            else:
                self.value += int(card.rank)
        while self.value > 21 and aces:
            self.value -= 10
            aces -= 1
    
    def clear(self):
        """Clear the hand for a new round."""
        self.cards = []
        self.value = 0
    
    def draw(self, screen, x, y):
        for i, card in enumerate(self.cards):
            # If it's the dealer's hand and the first card and not all cards are face up
            if self.is_dealer and i == 0 and not all(card.face_up for card in self.cards):
                card.face_up = False
            else:
                card.face_up = True
            card.draw(screen, x + i * (CARD_WIDTH + 10), y)

class Chip:
    def __init__(self, value, image_path):
        self.value = value
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Adjust size as needed
        self.rect = self.image.get_rect()
    
    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)