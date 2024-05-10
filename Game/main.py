import pygame
import spriteSheet
import color

# Initialisation de Pygame
pygame.init()
pygame.display.set_caption("Dodge Game 2D")
FramePerSec = pygame.time.Clock()
w = 800
h = 600
FPS = 60
last_update = pygame.time.get_ticks()
screen = pygame.display.set_mode((w, h))
vec = pygame.math.Vector2
tile_size = 50
ground = h-160

bg_img = pygame.image.load('Game/assets/img/sky.png')
sun_img = pygame.image.load('Game/assets/img/sun.png')

doux_sheet_image = pygame.image.load('Game/assets/Sprites/doux.png').convert_alpha()
doux_sheet = spriteSheet.diviser_sprite_sheet(doux_sheet_image, 24, 24)


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (w, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, h))

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img = pygame.image.load('Game/assets/img/dirt.png')
        grass_img = pygame.image.load('Game/assets/img/grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
#img = pygame.image.load(f'Game/assets/img/{stand_animation[0]}')
#self.image = pygame.transform.scale(img, (40, 80))
class Player():
    def __init__(self, x, y):
        self.images_stand = []
        self.images_stand_left = []
        self.images_right = []
        self.images_left = []
        self.size = 70
        self.index = 0
        self.counter = 0

        for i in range(4):
            img = doux_sheet[i]
            img = pygame.transform.scale(img, (self.size, self.size))
            img_left = pygame.transform.flip(img, True, False)
            self.images_stand.append(img)
            self.images_stand_left.append(img_left)
        for u in range(10):
            img = doux_sheet[u+4]
            img = pygame.transform.scale(img, (self.size, self.size))
            img_left = pygame.transform.flip(img, True, False)
            self.images_right.append(img)
            self.images_left.append(img_left)

        self.image = self.images_stand[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 1

    def update(self):
        dx = 0
        dy = 0
        speed = 9
        walk_cooldown = 8
        
        self.counter += 1
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
        if self.index >= len(self.images_stand) or self.index >= len(self.images_right) or self.index >= len(self.images_left):
            self.index = 0

        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.jumped and self.rect.bottom == ground + self.size:  # Autorise le saut seulement si le joueur est au sol et n'a pas déjà sauté
            self.vel_y = -15
            self.jumped = True  # Met à jour la variable jumped

        if not key[pygame.K_UP] and self.rect.bottom == ground + self.size:  # Réinitialise la variable jumped lorsque le joueur touche le sol
            self.jumped = False

        if key[pygame.K_LEFT] and not self.rect.x <= -2: # aller à gauche sans sortir de l'écran
            dx -= speed
            self.index += 1
            self.direction = -2

        if key[pygame.K_RIGHT] and not self.rect.x >= w-self.size+10:  # aller à droite sans sortir de l'écran
            dx += speed
            self.index += 1
            self.direction = 2

        if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
            if self.direction == -2:
                self.direction = -1
            elif self.direction == 2:
                self.direction = 1

        #handle direction
        if self.direction == 1: self.image = self.images_stand[self.index]
        elif self.direction == -1: self.image = self.images_stand_left[self.index]
        elif self.direction == -2: self.image = self.images_left[self.index]
        elif self.direction == 2: self.image = self.images_right[self.index]

        #add gravity
        self.vel_y += 1
        if self.vel_y > 50:
            self.vel_y = 50
        dy += self.vel_y

        #check for collision

        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > ground+70:
            self.rect.bottom = ground+70
            dy = 0

        #draw player onto screen
        screen.blit(self.image, self.rect)

world_data = [
    [0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

player = Player(100, ground)
world = World(world_data)
    

# Game loop
def game():
    global frame, last_update
    while True:
        screen.blit(bg_img, (0, 0))
        screen.blit(sun_img, (100, 100))

        world.draw()
        #draw_grid()
        player.update()

        """current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(stand_animation):
                frame = 0

        screen.blit(stand_animation[frame], (100, ground))"""

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

        FramePerSec.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    game()

print(f'[Finished in {last_update/100}s]')
pygame.quit()