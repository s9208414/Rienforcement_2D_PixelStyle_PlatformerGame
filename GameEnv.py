import os
os.environ['SDL_VIDEODRIVER']='dummy'

import pygame
import random

import numpy as np
from gym import Env
from gym.spaces import Box, Discrete, MultiBinary
import random




# Set up window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
RED = (255,0,0)

# Set up player dimensions
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32

# Set up platform dimensions
PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 32


# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, role, platforms, walls):
        super().__init__()
        self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.player_on_platformer = False
        self.role = role
        self.platforms = platforms
        self.walls = walls

    def update(self, walls, platforms):
        self.rect.x += self.vel_x

        # Check for collisions in x direction
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for wall in collisions:
            if self.vel_x > 0:
                self.rect.right = wall.rect.left
            elif self.vel_x < 0:
                self.rect.left = wall.rect.right

        self.rect.y += self.vel_y

        # Check for collisions in y direction
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collisions:
            if self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.player_on_platformer = True
            elif self.vel_y < 0:
                self.rect.top = platform.rect.bottom
                self.vel_y = 0
                self.player_on_platformer = False

        # Apply gravity
        self.vel_y += 1
        if self.vel_y > 10 and self.player_on_platformer == False:
            self.vel_y = 10


        # Check for collisions in y direction
        collisions = pygame.sprite.spritecollide(self, walls, False)
        for wall in collisions:
            if self.vel_y > 0:
                self.rect.bottom = wall.rect.top
                self.vel_y = 0
                print('站在地板')
            elif self.vel_y < 0:
                self.rect.top = wall.rect.bottom
                self.vel_y = 0
                print('碰到天花板')


    def jump(self):
        self.rect.y += 2
        hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
        hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2
        if hits_walls:
            self.vel_y = -20
        if hits_platforms:
            self.vel_y = -20

    def move(self,key):
        if (self.role == "p1"):
            if key == "left":
                self.vel_x = -5
            elif key == "right":
                self.vel_x = 5
            else:
                self.vel_x = 0
        else:
            if key == "left":
                self.vel_x = -5
            elif key == "right":
                self.vel_x = 5
            else:
                self.vel_x = 0 

    def move_jump(self,key):
        if (self.role == "p1"):
            if key == "left":
                self.vel_x = -5
                self.rect.y += 2
                hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
                hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
                self.rect.y -= 2
                if hits_walls:
                    self.vel_y = -20
                if hits_platforms:
                    self.vel_y = -20
            elif key == "right":
                self.vel_x = 5
                hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
                hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
                self.rect.y -= 2
                if hits_walls:
                    self.vel_y = -20
                if hits_platforms:
                    self.vel_y = -20
            else:
                self.vel_x = 0
                hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
                hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
                self.rect.y -= 2
                if hits_walls:
                    self.vel_y = -20
                if hits_platforms:
                    self.vel_y = -20
        else:
            if key == "left":
                self.vel_x = -5
                hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
                hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
                self.rect.y -= 2
                if hits_walls:
                    self.vel_y = -20
                if hits_platforms:
                    self.vel_y = -20
            elif key == "right":
                self.vel_x = 5
                hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
                hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
                self.rect.y -= 2
                if hits_walls:
                    self.vel_y = -20
                if hits_platforms:
                    self.vel_y = -20
            else:
                self.vel_x = 0 
                hits_walls = pygame.sprite.spritecollide(self, self.walls, False)
                hits_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
                self.rect.y -= 2
                if hits_walls:
                    self.vel_y = -20
                if hits_platforms:
                    self.vel_y = -20

# Define wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Define key class
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([32, 32])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collect = False


# Define door class
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([32, 64])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y






# 繼承openai gym的環境類別並覆寫他的方法
class CustomEnv(Env):
    def __init__(self):
        # Initialize pygame and create window
        pygame.init()
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        pygame.display.set_caption("Two-Player Platformer")

        # Create walls and floor
        walls = pygame.sprite.Group()
        walls.add(Wall(0, 0, WINDOW_WIDTH, 10, BLACK))
        walls.add(Wall(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10, BLACK))
        walls.add(Wall(0, 10, 10, WINDOW_HEIGHT - 20, BLACK))
        walls.add(Wall(WINDOW_WIDTH - 10, 10, 10, WINDOW_HEIGHT - 20, BLACK))

        # Create platforms
        platforms = pygame.sprite.Group()
        platforms.add(Wall(200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(400, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(600, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(150, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(350, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))

        # Create key and door

        #key = Key(650, 50)
        keyList = [Key(random.randint(10,790),random.randint(10,590))for i in range(4)]
        door = Door(700, 200)

        self.keyNum = len(keyList)

        self.collect = 0
        # Create players
        player1 = Player(100, 300, BLUE, "p1", platforms, walls)

        # Add sprites to groups
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player1)
        all_sprites.add(walls)
        all_sprites.add(platforms)

        #all_sprites.add(key)
        for i in keyList:
            all_sprites.add(i)
        all_sprites.add(door)

        self.openDoor = False
        self.player = player1
        self.keylist = keyList
        self.door = door
        self.platforms = platforms
        self.walls = walls
        self.all_sprites = all_sprites
        self.action_space = Discrete(3) # 3個動作: 左、跳、右
        low = np.array([42, 42])   # 最小值(視窗左上角，不包含牆壁)
        high = np.array([558, 758])   # 最大值(視窗右下角，不包含牆壁)
        self.observation_space = Box(low=low, high=high, dtype=np.float32)
        self.state = [300, 100]
        self.game_time = 60 # 一場遊戲的時間


    def step(self, action):
        # Set up clock
        clock = pygame.time.Clock()
        if (action == 0):
            self.player.move("left")
            # Update sprites
            self.all_sprites.update(self.walls,self.platforms)

            # Check for platform collision for player 1
            self.player.on_ground = False
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self.player, platform):
                    if self.player.rect.bottom > platform.rect.bottom and self.player.vel_y >= 0:
                        self.player.rect.bottom = platform.rect.top
                        self.player.vel_y = 0
                        self.player.on_ground = True
                    elif self.player.rect.top < platform.rect.top and self.player.vel_y <= 0:
                        self.player.rect.top = platform.rect.bottom
                        self.player.vel_y = 0               

            self.all_sprites.update(self.walls,self.platforms)
            # Check for key collection
            for i in self.keylist:
                if pygame.sprite.collide_rect(self.player, i):
                    i.collect = True
                    self.keylist.remove(i)
                    i.kill()

            # Check for door unlock
            if pygame.sprite.collide_rect(self.player, self.door) and len(self.keylist) == 0:
                done = True

            # Limit to 60 frames per second
            clock.tick(60)
            self.state[0] =  self.player.rect.y
            self.state[1] =  self.player.rect.x

        elif (action == 1):
            self.player.jump()
            # Update sprites
            self.all_sprites.update(self.walls,self.platforms)

            # Check for platform collision for player 1
            self.player.on_ground = False
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self.player, platform):
                    if self.player.rect.bottom > platform.rect.bottom and self.player.vel_y >= 0:
                        self.player.rect.bottom = platform.rect.top
                        self.player.vel_y = 0
                        self.player.on_ground = True
                    elif self.player.rect.top < platform.rect.top and self.player.vel_y <= 0:
                        self.player.rect.top = platform.rect.bottom
                        self.player.vel_y = 0               

            self.all_sprites.update(self.walls,self.platforms)
            # Check for key collection
            for i in self.keylist:
                if pygame.sprite.collide_rect(self.player, i):
                    i.collect = True
                    self.keylist.remove(i)
                    i.kill()

            # Check for door unlock
            if pygame.sprite.collide_rect(self.player, self.door) and len(self.keylist) == 0:
                done = True


            # Limit to 60 frames per second
            clock.tick(60)
            self.state[0] =  self.player.rect.y
            self.state[1] =  self.player.rect.x

        elif (action == 2):
            self.player.move("right")
            # Update sprites
            self.all_sprites.update(self.walls,self.platforms)

            # Check for platform collision for player 1
            self.player.on_ground = False
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self.player, platform):
                    if self.player.rect.bottom > platform.rect.bottom and self.player.vel_y >= 0:
                        #print(self.player.rect.bottom==platform.rect.top)
                        self.player.rect.bottom = platform.rect.top
                        self.player.vel_y = 0
                        self.player.on_ground = True
                    elif self.player.rect.top < platform.rect.top and self.player.vel_y <= 0:
                        self.player.rect.top = platform.rect.bottom
                        self.player.vel_y = 0               

            self.all_sprites.update(self.walls,self.platforms)
            # Check for key collection
            for i in self.keylist:
                if pygame.sprite.collide_rect(self.player, i):
                    i.collect = True
                    self.keylist.remove(i)
                    i.kill()

            # Check for door unlock
            if pygame.sprite.collide_rect(self.player, self.door) and len(self.keylist) == 0:
                done = True


            # Limit to 60 frames per second
            clock.tick(60)
            self.state[0] =  self.player.rect.y
            self.state[1] =  self.player.rect.x

        elif (action == 3):
            self.player.move_jump("left")
            # Update sprites
            self.all_sprites.update(self.walls,self.platforms)

            # Check for platform collision for player 1
            self.player.on_ground = False
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self.player, platform):
                    if self.player.rect.bottom > platform.rect.bottom and self.player.vel_y >= 0:
                        self.player.rect.bottom = platform.rect.top
                        self.player.vel_y = 0
                        self.player.on_ground = True
                    elif self.player.rect.top < platform.rect.top and self.player.vel_y <= 0:
                        self.player.rect.top = platform.rect.bottom
                        self.player.vel_y = 0               

            self.all_sprites.update(self.walls,self.platforms)
            # Check for key collection
            for i in self.keylist:
                if pygame.sprite.collide_rect(self.player, i):
                    i.collect = True
                    self.keylist.remove(i)
                    i.kill()

            # Check for door unlock
            if pygame.sprite.collide_rect(self.player, self.door) and len(self.keylist) == 0:
                done = True


            # Limit to 60 frames per second
            clock.tick(60)
            self.state[0] =  self.player.rect.y
            self.state[1] =  self.player.rect.x

        elif (action == 4):
            self.player.move_jump("right")
            # Update sprites
            self.all_sprites.update(self.walls,self.platforms)

            # Check for platform collision for player 1
            self.player.on_ground = False
            for platform in self.platforms:
                if pygame.sprite.collide_rect(self.player, platform):
                    if self.player.rect.bottom > platform.rect.bottom and self.player.vel_y >= 0:
                        self.player.rect.bottom = platform.rect.top
                        self.player.vel_y = 0
                        self.player.on_ground = True
                    elif self.player.rect.top < platform.rect.top and self.player.vel_y <= 0:
                        self.player.rect.top = platform.rect.bottom
                        self.player.vel_y = 0               

            self.all_sprites.update(self.walls,self.platforms)
            # Check for key collection
            for i in self.keylist:
                if pygame.sprite.collide_rect(self.player, i):
                    i.collect = True
                    self.keylist.remove(i)
                    i.kill()

            # Check for door unlock
            if pygame.sprite.collide_rect(self.player, self.door) and len(self.keylist) == 0:
                done = True


            # Limit to 60 frames per second
            clock.tick(60)
            self.state[0] =  self.player.rect.y
            self.state[1] =  self.player.rect.x

            
        # 每0.1秒做一個動作，等於每一個step的時間為0.1秒    
        self.game_time -= 0.1 


        # Calculating the reward

        reward = self.keyNum - len(self.keylist)
        if len(self.keylist) == 0 and (self.state[1] == self.door.rect.x and self.state[0] == self.door.rect.y):
            reward += 5
        elif len(self.keylist) != 0 and (self.state[1] == self.door.rect.x and self.state[0] == self.door.rect.y):
            reward -= 10

        # Checking if game is done
        if self.game_time <= 0: 
            done = True
        else:
            done = False
        
        # Setting the placeholder for info
        info = {}
        
        
        print('動作: {} , X座標: {} ,Y座標: {} ,獎勵: {} ,鑰匙列表: {}\n'.format(action,self.state[1],self.state[0] , reward, len(self.keylist)))

        self.show(self.all_sprites,self.player,self.platforms,self.walls,self.keylist,self.door,self.state[1],self.state[0])

        # 回傳該step的狀態、動作、獎勵，及其他資訊
        return self.state, reward, done, info
    
    # 這個function還無法用
    def show(self,AS,P,PF,W,K,D,Sx,Sy):
        pygame.init()
        screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        pygame.display.set_caption("Two-Player Platformer")
        # Update sprites
        AS.update(W,PF)
        # Check for platform collision for player 1
        P.on_ground = False
        for platform in PF:
            if pygame.sprite.collide_rect(P, platform):
                if P.rect.bottom > platform.rect.bottom and P.vel_y >= 0:
                    print(P.rect.bottom==platform.rect.top)
                    P.rect.bottom = platform.rect.top
                    P.vel_y = 0
                    P.on_ground = True
                elif P.rect.top < platform.rect.top and P.vel_y <= 0:
                    P.rect.top = platform.rect.bottom
                    P.vel_y = 0               
                    

        # Check for key collection
        for i in K:
            if pygame.sprite.collide_rect(P, i):
                i.collect = True
                K.remove(i)
                i.kill()

        # Check for door unlock
        if pygame.sprite.collide_rect(P, D) and len(K) == 0:
            done = True

        # Limit to 60 frames per second
        Sy =  P.rect.y
        Sx =  P.rect.x


        # Draw everything
        screen.fill(WHITE)
        AS.draw(screen)
        pygame.display.flip()

        pygame.quit()

    def render(self):
        return None


    def reset(self):

        pygame.init()
        self.screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
        pygame.display.set_caption("Two-Player Platformer")

        # Create walls and floor
        walls = pygame.sprite.Group()
        walls.add(Wall(0, 0, WINDOW_WIDTH, 10, BLACK))
        walls.add(Wall(0, WINDOW_HEIGHT - 10, WINDOW_WIDTH, 10, BLACK))
        walls.add(Wall(0, 10, 10, WINDOW_HEIGHT - 20, BLACK))
        walls.add(Wall(WINDOW_WIDTH - 10, 10, 10, WINDOW_HEIGHT - 20, BLACK))

        # Create platforms
        platforms = pygame.sprite.Group()
        platforms.add(Wall(200, 500, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(400, 350, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(600, 200, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(150, 150, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        platforms.add(Wall(350, 250, PLATFORM_WIDTH, PLATFORM_HEIGHT, BLACK))
        # Create key and door

        #key = Key(650, 50)
        keyList = [Key(random.randint(10,790),random.randint(10,590))for i in range(4)]
        door = Door(700, 200)

        self.collect = 0
        # Create players
        player1 = Player(100, 300, BLUE, "p1", platforms, walls)

        # Add sprites to groups
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player1)
        all_sprites.add(walls)
        all_sprites.add(platforms)

        for i in keyList:
            all_sprites.add(i)
        all_sprites.add(door)

        self.openDoor = False
        self.player = player1
        self.keylist = keyList
        self.door = door
        self.platforms = platforms
        self.walls = walls
        self.all_sprites = all_sprites
        self.action_space = Discrete(5) # 3個動作: 左、跳、右
        low = np.array([42, 42])   # 最小值(視窗左上角，不包含牆壁)
        high = np.array([558, 758])   # 最大值(視窗右下角，不包含牆壁)
        self.observation_space = Box(low=low, high=high, dtype=np.float32)
        self.state = [300, 100]
        self.game_time = 60 # 一場遊戲的時間
        return self.state
    
    # 自定義monitor函數
    def custom_monitor_function(self, model):  
        if self.state[0] < 10 or self.state[1] < 10 or self.state[0] > 590 or self.state[1] > 790:
            print('超出視窗')
            model.stop_training = True