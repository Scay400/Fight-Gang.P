import pygame
import os
import random
import sys
import random

# Инициализация Pygame
pygame.init()

BLACK = (0,0,0)

# Настройки окна
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fight Gang")
background = pygame.transform.scale(pygame.image.load('assets/background.png'),(WIDTH,HEIGHT))


# ФПС
FPS = 120
clock = pygame.time.Clock()

class Character:
    def __init__(self, x, y,name,index):
        self.x = x
        self.y = y
        self.name = name
        self.width =330
        self.height = 394
        self.state = "idle"
        self.animation_count = 0
        self.animations = {
            "idle": [],
            "attack1": [],
            "attack2": [],
            "crouch": [],
            "block": [],
            "jump":[],
            "knife":[],
            "leg":[],
        }
        # Скорости анимаций
        self.animation_speeds = {
            "idle": 0.5,
            "attack1": 0.5,
            "attack2": 0.5,
            "leg":0.5,
            "jump":0.3,
            "knife":0.6
        }
  
        self.reverse_speeds = {
            "crouch": 0.8,
            "block": 0.8
        }
        self.Rattack = False
        self.Rblock = False
        self.Rcrouch = False
        self.Rjump = False
        self.Rknife = False
        self.Rleg = False
        self.load_animations()
        self.attacking = False
        self.crouching = False
        self.blocking = False
        self.jumping = False
        self.leg = False
        self.knife = False
        self.attack_cooldown = 0
        self.active_cooldown = 0
        self.invis_cooldown = 0
        self.attack_cooldown2 = 0
        self.last_state = None
        self.reverse_animation = False
        self.attacks = ['attack1','attack2']
        self.last_attack = None
        self.index = index


        self.hits_data = [

            {'Blue':{'attack1':1,'attack2':2,'block':1,'crouch':1,'jump':[1,2,3],'knife':[5,6],'leg':5}},

            {'Red':{'attack1':1,'attack2':2,'block':1,'crouch':1,'jump':[1,2,3],'knife':[5,6],'leg':5}}

        ]

        self.heroes_data = [

            {'Blue':{'name':'Tony','HP':290,'DEF':3,'DMG':2}},

            {'Red':{'name':'Ki Su','HP':140,'DEF':1,'DMG':5}}

        ]

        self.heroname = self.heroes_data[self.index][self.name]['name']
        self.fullhealth = self.heroes_data[self.index][self.name]['HP']
        self.defence = self.heroes_data[self.index][self.name]['DEF']
        self.damage = self.heroes_data[self.index][self.name]['DMG']
        self.health = self.fullhealth

    
    def load_animations(self):
        animation_data = {
            "idle": {"folder": "assets/heroes/"+self.name+"/idle", "frames": 13},
            "attack1": {"folder": "assets/heroes/"+self.name+"/attack1", "frames": 3},
            "attack2": {"folder": "assets/heroes/"+self.name+"/attack2", "frames": 4},
            "crouch": {"folder": "assets/heroes/"+self.name+"/crouch", "frames": 2},
            "block": {"folder": "assets/heroes/"+self.name+"/block", "frames": 2},
            "jump": {"folder": "assets/heroes/"+self.name+"/jump", "frames": 5},
            "knife": {"folder": "assets/heroes/"+self.name+"/knife", "frames": 8},
            "leg": {"folder": "assets/heroes/"+self.name+"/leg", "frames": 12},
        }
        
        for state, data in animation_data.items():
            folder = data["folder"]
            frame_count = data["frames"]
            
            
            for i in range(frame_count):
                file_path = os.path.join(folder, f"{i}.png")
                if os.path.exists(file_path):
                
                    img = pygame.image.load(file_path).convert_alpha()
                    original_width, original_height = img.get_size()
                    scale_factor = 7  
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    img = pygame.transform.scale(img, (new_width, new_height))
                    self.animations[state].append(img)
    
    def update(self,player2es):
 
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.active_cooldown > 0:
            self.active_cooldown -= 1
        if self.invis_cooldown > 0:
            self.invis_cooldown -= 1
        if self.attack_cooldown2 > 0:
            self.attack_cooldown2 -= 1
        
 
        if self.last_state != self.state:
            self.animation_count = 0
            self.last_state = self.state
            self.reverse_animation = False
        
        if self.state == 'attack1' and int(self.animation_count) == self.hits_data[self.index][self.name]['attack1']:

            self.Rattack = True

            self.Rblock = False
            self.Rcrouch = False
            self.Rjump = False
            self.Rknife = False
            self.Rleg = False

        elif self.state == 'attack2' and int(self.animation_count) == self.hits_data[self.index][self.name]['attack2']:

            self.Rattack = True

            self.Rblock = False
            self.Rcrouch = False
            self.Rjump = False
            self.Rknife = False
            self.Rleg = False

        elif self.state == 'block' and int(self.animation_count) == self.hits_data[self.index][self.name]['block']:

            self.Rblock = True

            self.Rattack = False
            self.Rcrouch = False
            self.Rjump = False
            self.Rknife = False
            self.Rleg = False

        elif self.state == 'crouch' and int(self.animation_count) == self.hits_data[self.index][self.name]['crouch']:

            self.Rcrouch = True

            self.Rattack = False
            self.Rblock = False
            self.Rjump = False
            self.Rknife = False
            self.Rleg = False

        elif self.state == 'jump' and int(self.animation_count) in self.hits_data[self.index][self.name]['jump']:

            self.Rjump = True

            self.Rcrouch = False
            self.Rattack = False
            self.Rblock = False
            self.Rknife = False
            self.Rleg = False

        elif self.state == 'knife' and int(self.animation_count) in self.hits_data[self.index][self.name]['knife']:

            self.Rknife = True

            self.Rattack = False
            self.Rblock = False
            self.Rcrouch = False
            self.Rjump = False
            self.Rleg = False

        elif self.state == 'leg' and int(self.animation_count) == self.hits_data[self.index][self.name]['leg']:

            self.Rleg = True

            self.Rattack = False
            self.Rblock = False
            self.Rcrouch = False
            self.Rjump = False
            self.Rknife = False
        
        else:
            self.Rleg = False
            self.Rattack = False
            self.Rblock = False
            self.Rcrouch = False
            self.Rjump = False
            self.Rknife = False

        
        speed = self.reverse_speeds.get(self.state, self.animation_speeds.get(self.state, 0.1))
        
        if self.state == "idle":
            if player2es:
                self.x = 630
                self.y = 250
            else:
                self.x = 315
                self.y = 237
        if self.state == "attack1":
            if player2es:
                self.x = 560
                self.y = 260
            else:
                self.x = 315
                self.y = 237
        if self.state == "attack2":
            if player2es:
                self.x = 560
                self.y = 260
            else:
                self.x = 315
                self.y = 237
        if self.state == "knife":
            if player2es:
                self.x = 540
                self.y = 250
            else:
                self.x = 315
                self.y = 237
        if self.state == "jump":
            if player2es:
                self.x = 630
                self.y = 200
            else:
                self.x = 315
                self.y = 180
        if self.state == "crouch":
            if player2es:
                self.x = 620
                self.y = 300
            else:
                self.x = 315
                self.y = 237


        if not self.reverse_animation:
            self.animation_count += speed
            max_frame = len(self.animations[self.state]) - 1
            if int(self.animation_count) >= max_frame:
                if self.state in ["attack1", "attack2","jump","knife","leg"]:
                    self.animation_count = max_frame
                    if self.attack_cooldown <= 0:
                        if self.state == 'attack1' or 'attack2':
                            self.attack_cooldown2 = 10
                        self.state = "idle"
                        self.attacking = False
                        self.jumping = False
                        self.leg = False
                        self.knife = False
                elif self.state == "idle":
                    self.animation_count = 0
                else: 
                    self.animation_count = max_frame
        else:
            self.animation_count -= speed
            if self.animation_count <= 0:
                self.animation_count = 0
                self.state = "idle"
                self.reverse_animation = False
    
    def draw(self, screen,player2es):
        if not self.animations[self.state]: 
            self.create_placeholder_frame(self.state)
            
        frame = min(int(self.animation_count), len(self.animations[self.state]) - 1)
        if player2es:
            flipped_image = pygame.transform.flip(self.animations[self.state][frame], True, False)
            screen.blit(flipped_image, (self.x, self.y))
        else:
            screen.blit(self.animations[self.state][frame], (self.x, self.y))
    
    def attack(self):
        if self.attack_cooldown <= 0 and not self.attacking and not self.blocking and not self.crouching and not self.jumping and not self.leg and not self.knife and self.attack_cooldown2 <= 0:
            self.state = random.choice(self.attacks)
            if self.state == 'attack1' and self.last_attack == 'attack1':
                self.state == 'attack2'
            if self.state == 'attack2' and self.last_attack == 'attack2':
                self.state == 'attack1'
            self.last_attack = self.state
            self.animation_count = 0
            self.attacking = True
            self.attack_cooldown = 10
           
        
    
    def crouch(self, is_crouching):
        if self.active_cooldown <= 0 and not self.attacking and not self.blocking and not self.jumping and not self.leg and not self.knife:
            self.crouching = is_crouching
            if is_crouching:
                self.state = "crouch"
                self.animation_count = 0
                self.reverse_animation = False
            elif self.state == "crouch":
                self.reverse_animation = True
                self.active_cooldown = 1
            
    
    def block(self, is_blocking):
        if self.active_cooldown <= 0 and not self.attacking and not self.crouching and not self.jumping and not self.leg and not self.knife:
            self.blocking = is_blocking
            if is_blocking:
                self.state = "block"
                self.animation_count = 0
                self.reverse_animation = False
            elif self.state == "block":
                self.reverse_animation = True
                self.active_cooldown = 1
    
    def jump(self):
        if self.active_cooldown <= 0 and not self.attacking and not self.blocking and not self.crouching and not self.jumping and not self.leg and not self.knife:
            self.state = "jump"
            self.animation_count = 0
            self.jumping = True
            self.active_cooldown = 1

    def legp(self):
        if self.attack_cooldown <= 0 and not self.attacking and not self.blocking and not self.crouching and not self.jumping and not self.leg and not self.knife and self.attack_cooldown2 <= 0:
            self.state = "leg"
            self.animation_count = 0
            self.leg = True
            self.attack_cooldown = 2

    def knifedd(self):
        if self.attack_cooldown <= 0 and not self.attacking and not self.blocking and not self.crouching and not self.jumping and not self.leg and not self.knife and self.attack_cooldown2 <= 0:
            self.state = "knife"
            self.animation_count = 0
            self.knife = True
            self.attack_cooldown = 2
    

# Создание персонажа
player1 = Character(315, 250,'Blue',0)
player2 = Character(630, 250,'Red',1)

running = True
space_pressed = False
ctrl_pressed = False
shift_pressed = False

while running:
    # screen.fill((255,255,255))
    # pygame.draw.rect(screen,(255,0,0),rect_pos_RED1)
    # pygame.draw.rect(screen,(0,255,0),rect_pos_GREEN1)
    # pygame.draw.rect(screen,(255,0,0),rect_pos_RED2)
    # pygame.draw.rect(screen,(0,255,0),rect_pos_GREEN2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
              
                player1.attack()
            elif event.key == pygame.K_w:
                
                player1.jump()
            elif event.key == pygame.K_f:
               
                player1.legp()
            elif event.key == pygame.K_r:
                
                player1.knifedd()
            elif event.key == pygame.K_s:
                
                player1.crouch(True)
            elif event.key == pygame.K_a:
                
                player1.block(True)
            elif event.key == pygame.K_ESCAPE:
                running = False
            #player2
            if event.key == pygame.K_LEFT:
              
                player2.attack()
            elif event.key == pygame.K_UP:
                
                player2.jump()
            elif event.key == pygame.K_l:
               
                player2.legp()
            elif event.key == pygame.K_k:
                
                player2.knifedd()
            elif event.key == pygame.K_DOWN:
                
                player2.crouch(True)
            elif event.key == pygame.K_RIGHT:
                
                player2.block(True)
            elif event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.KEYUP:
            # if event.key == pygame.K_d:
            #     space_pressed = False      
            # elif event.key == pygame.K_w:
            #     space_pressed = False    
            # elif event.key == pygame.K_f:
            #     space_pressed = False  
            # elif event.key == pygame.K_r:
            #     space_pressed = False
            if event.key == pygame.K_s:
                player1.crouch(False)
            elif event.key == pygame.K_a:
                player1.block(False)
            elif event.key == pygame.K_ESCAPE:
                running = False
            #player2
            # if event.key == pygame.K_UP:
            #     space_pressed = False
            elif event.key == pygame.K_DOWN:

                player2.crouch(False)
            elif event.key == pygame.K_RIGHT:

                player2.block(False)
            
    if player1.Rattack and not player2.Rblock and not player2.Rcrouch and player2.invis_cooldown == 0:
            player2.health -= int((random.randint(2,7)*player1.damage)/random.choice([1,player2.defence]))
            player2.invis_cooldown = 15

    if player2.Rattack and not player1.Rblock and not player1.Rcrouch and player1.invis_cooldown == 0:
            player1.health -= int((random.randint(2,7)*player2.damage)/random.choice([1,player2.defence]))
            player1.invis_cooldown = 15

    if player1.Rknife and not player2.Rcrouch and player2.invis_cooldown == 0:
        if player2.state == 'block':
            player2.state = 'idle'
        player2.health -= int((random.randint(1,4)*player1.damage)/random.choice([1,player2.defence]))
        player2.invis_cooldown = 15

    if player2.Rknife and not player1.Rcrouch and player1.invis_cooldown == 0:
        if player1.state == 'block':
            player1.state = 'idle'
        player1.health -= int((random.randint(1,4)*player2.damage)/random.choice([1,player1.defence]))
        player1.invis_cooldown = 15

    if player1.Rleg and not player2.Rjump and player2.invis_cooldown == 0:
        if player2.state == 'crouch':
            player2.state = 'idle'
        player2.health -= int((random.randint(1,2)*player1.damage)/random.choice([1,player2.defence]))
        player2.invis_cooldown = 15
    
    if player2.Rleg and not player1.Rjump and player1.invis_cooldown == 0:
        if player1.state == 'crouch':
            player1.state = 'idle'
        player1.health -= int((random.randint(1,2)*player2.damage)/random.choice([1,player1.defence]))
        player1.invis_cooldown = 15





        
    screen.blit(background,(0,0))
    player1.update(False) 

    player1.draw(screen,False)

    player2.update(True)

    player2.draw(screen,True)

    font = pygame.font.SysFont(None, 30)
    instructions = [
        f"HP: {player1.health,player1.fullhealth}",
    ]
    instructions2 = [
        f"HP: {player2.health,player2.fullhealth}",
    ]
    
    for i, text in enumerate(instructions):
        rendered = font.render(text, True, (0,255,0))
        screen.blit(rendered, (20, 20 + i * 30))
    for i, text in enumerate(instructions2):
        rendered = font.render(text, True, (0,255,0))
        screen.blit(rendered, (560, 20 + i * 30))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
