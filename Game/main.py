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


sprite_sheet_img = pygame.image.load('Game/assets/Sprites/doux.png')
sprite_sheet = spriteSheet.SpriteSheet(sprite_sheet_img)

bg_img = pygame.image.load('Game/assets/img/sky.png')
sun_img = pygame.image.load('Game/assets/img/sun.png')

# Animation list
stand_animation = []
animation_cooldown = 200
frame = 0
for i in range(4):
    stand_animation.append(sprite_sheet.get_image(i, 24, 24, 3, color.black))
    

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
        self.images_right = []
        self.images_left = []
        self.images_stand = []
        self.index = 0
        self.counter = 0
        for num in range(4):
            img_stand = pygame.image.load(f'Game/assets/doux/doux{num+1}.png')
            img_stand = pygame.transform.scale(img_stand, (70, 70))
            self.images_stand.append(img_stand)
        for i in range(10):
            img_right = pygame.image.load(f'Game/assets/doux/doux{num+5}.png')
            img_right = pygame.transform.scale(img_right, (70, 70))
            img_left = pygame.transform.flip(img_right, True, False) # flip(img, x axis, y axis)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        print(self.images_stand)
        print(self.images_right)
        print(self.images_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self):
        dx = 0
        dy = 0
        speed = 9
        walk_cooldown = 8
        
        #get keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and not self.jumped:
            self.vel_y = -15
            self.jumped = True
        if not key[pygame.K_UP]:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= speed
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += speed
            self.counter += 1
            self.direction = 1
        if not(key[pygame.K_LEFT] and key[pygame.K_RIGHT]):
            self.counter = 0
            self.index = 0
            #self.image = self.images_stand[self.index]

        #handle animation
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
            if self.direction == 0:
                self.image = self.images_stand(self.index)
        
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