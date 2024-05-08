import pygame
from pygame.locals import QUIT

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("Jeu de BlackJack")
FramePerSec = pygame.time.Clock()
WIDTH = 800
HEIGHT = 600
FPS = 60
GameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
vec = pygame.math.Vector2

def background():
    ground_rect = pygame.Rect(0, HEIGHT, WIDTH, 100)
    ground = pygame.Surface((ground_rect.width, ground_rect.height))
    ground.fill((19,133,16))
    GameDisplay.blit(ground, ground_rect)
    GameDisplay.fill((130,201,230))
    GameDisplay.blit(ground, (0, HEIGHT-100))

# Boucle de jeu
def main():
    background()
    while True:
        FramePerSec.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        
        pygame.display.update()    
    return

if __name__ == "__main__":
    main()

pygame.quit()
quit()