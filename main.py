import pygame
import os
import random
import sys
import random

# Инициализация Pygame
pygame.init()

BLACK = (0,0,0)

font1 = pygame.font.SysFont(None, 30)

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
        self.index = index

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
        self.Rrage = False

        self.load_animations()

        self.attacking = False
        self.crouching = False
        self.blocking = False
        self.jumping = False
        self.leg = False
        self.knife = False

        self.win = False
        self.lose = False

        self.attack_cooldown = 0
        self.active_cooldown = 0
        self.invis_cooldown = 0
        self.attack_cooldown2 = 0
        self.ragecooldown = 0
        self.count = 0


        self.last_state = None
        self.reverse_animation = False
        self.attacks = ['attack1','attack2']
        self.last_attack = None

        self.rage = 0

        self.hits_data = [

            {'Blue':{'attack1':2,'attack2':2,'block':1,'crouch':1,'jump':[1,2,3],'knife':[5,6],'leg':5}},

            {'Red':{'attack1':2,'attack2':2,'block':1,'crouch':1,'jump':[1,2,3],'knife':[5,6],'leg':5}}

        ]

        self.heroes_data = [

            {'Blue':{'name':'Tony','HP':220,'DEF':3,'DMG':2,'RAGE':2}},

            {'Red':{'name':'Ki Su','HP':180,'DEF':1,'DMG':10,'RAGE':1}}

        ]

        self.heroname = self.heroes_data[self.index][self.name]['name']
        self.fullhealth = self.heroes_data[self.index][self.name]['HP']
        self.defence = self.heroes_data[self.index][self.name]['DEF']
        self.damage = self.heroes_data[self.index][self.name]['DMG']
        self.ragex = self.heroes_data[self.index][self.name]['RAGE']

        self.health = self.fullhealth
        
        self.rect_pos_RED = [0,0,0,0]
        self.rect_pos_GREEN = [0,0,0,0]

        self.rect_pos_RAGE1 = [0,0,0,0]
        self.rect_pos_RAGE2 = [0,0,0,0]

    
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
        if self.ragecooldown > 0:
            self.ragecooldown -= 1
        if self.count > 0:
            self.count -= 1

        if self.rage > 0 and self.ragecooldown <= 0 and self.rage != 200 and not self.Rrage:
            self.rage -= 2/self.ragex
            self.ragecooldown = 10

        if self.rage>200:
            self.rage = 200

        if self.Rrage and self.rage > 0 and self.ragecooldown <= 0:
            self.rage -= 16/self.ragex
            self.ragecooldown = 5
            if self.rage == 0:
                self.Rrage = False

        
        if self.win:
            ko_label = pygame.transform.scale(pygame.image.load('assets/heroes/'+str(self.name)+'/KO.png'),(300,300))
            screen.blit(ko_label,(490,210))
        
        if self.lose:
            if self.x < 1300 and self.x > -300:
                if player2es:
                    if self.x >720:
                        if self.count <= 0:
                            self.x+=150
                            self.count = 1
                    else:
                        if self.count <= 0:
                            self.x+=5
                            self.count = 1
                else:
                    if self.x < 200:
                        if self.count <= 0:
                            self.x-=150
                            self.count = 1
                    else:
                        if self.count <= 0:
                            self.x-=5
                            self.count = 1
 
        if self.last_state != self.state:
            self.animation_count = 0
            self.last_state = self.state
            self.reverse_animation = False

        if player2es:
            self.rect_pos_RED = [WIDTH-self.fullhealth,680,self.fullhealth,20]
            self.rect_pos_GREEN = [1280,680,-self.health,20]
        else:
            self.rect_pos_RED = [0,680,self.fullhealth,20]
            self.rect_pos_GREEN = [0,680,self.health,20]

        if player2es:
            self.rect_pos_RAGE1 = [WIDTH-100*2,650,100*2,20]
            self.rect_pos_RAGE2 = [1280,650,-self.rage,20]
        else:
            self.rect_pos_RAGE1 = [0,650,100*2,20]
            self.rect_pos_RAGE2 = [0,650,self.rage,20]

        if gameplay:
        
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
                    self.x = 530
                    self.y = 250
                else:
                    self.x = 315
                    self.y = 237
            if self.state == "attack2":
                if player2es:
                    self.x = 580
                    self.y = 250
                else:
                    self.x = 315
                    self.y = 237
            if self.state == "knife":
                if player2es:
                    self.x = 580
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
                    self.y = 195
            if self.state == "crouch":
                if player2es:
                    self.x = 620
                    self.y = 257
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
    def win1(self,player2es):
        self.win = True
        # for i in range(20):
        #     if player2es:
        #         self.x+=
            
    def lose1(self,player2es):
        self.lose = True

# Создание персонажа
player1 = Character(315, 250,'Blue',0)
player2 = Character(630, 250,'Red',1)

start_menu = True
choose_menu = True
gamerun = True
gameplay = True
running = True
space_pressed = False
ctrl_pressed = False
shift_pressed = False

while running:

    screen.fill((255,255,255))

    if gamerun:
        if gameplay:  
            if player1.Rattack:
                if not player2.Rblock and not player2.Rcrouch:
                    if player2.invis_cooldown == 0:
                        if player1.Rrage:
                            player2.health -= int((random.randint(2,7)*player1.damage))*3
                        else:
                            player2.health -= int((random.randint(2,7)*player1.damage)/random.choice([1,player2.defence]))
                        player2.invis_cooldown = 15
                        player2.ragecooldown = 40
                        player2.rage += random.randint(7,15)*player2.ragex
                        if not player1.Rrage:
                            player1.ragecooldown = 20
                            player1.rage += random.randint(5,10)*player1.ragex
                else:
                    player2.rage += random.randint(4,7)*player2.ragex
            

            if player2.Rattack:
                if not player1.Rblock and not player1.Rcrouch:
                    if player1.invis_cooldown == 0:
                        if player2.Rrage:
                            player1.health -= int((random.randint(1,2)*player2.damage))*3
                        else:
                            player1.health -= int((random.randint(1,2)*player2.damage)/random.choice([1,player1.defence]))
                        player1.invis_cooldown = 15
                        player1.ragecooldown = 40
                        player1.rage += random.randint(5,15)*player1.ragex
                        if not player2.Rrage:
                            player2.ragecooldown = 20
                            player2.rage += random.randint(7,15)*player2.ragex
                else:
                    player1.rage += random.randint(4,7)*player1.ragex

            if player1.Rknife:
                if not player2.Rcrouch:
                    if player2.invis_cooldown == 0:
                        if player2.state == 'block':
                            player2.state = 'idle'
                        if player1.Rrage:
                            player2.health -= int((random.randint(2,7)*player1.damage))*3
                        else:
                            player2.health -= int((random.randint(2,7)*player1.damage)/random.choice([1,player2.defence]))
                        player2.invis_cooldown = 15
                        player2.ragecooldown = 40
                        player2.rage += random.randint(5,15)*player2.ragex
                        if not player1.Rrage:
                            player1.ragecooldown = 20
                            player1.rage += random.randint(5,10)*player1.ragex
                else:
                    player2.rage += random.randint(4,7)*player2.ragex

            if player2.Rknife:
                if not player1.Rcrouch:
                    if player1.invis_cooldown == 0:
                        if player1.state == 'block':
                            player1.state = 'idle'
                        if player2.Rrage:
                            player1.health -= int((random.randint(1,2)*player2.damage))*3
                        else:
                            player1.health -= int((random.randint(1,2)*player2.damage)/random.choice([1,player1.defence]))
                        player1.invis_cooldown = 15
                        player1.ragecooldown = 40
                        player1.rage += random.randint(5,15)*player1.ragex
                        if not player2.Rrage:
                            player2.ragecooldown = 20
                            player2.rage += random.randint(7,15)*player2.ragex
                else:
                    player1.rage += random.randint(4,7)*player1.ragex

            if player1.Rleg:
                if not player2.Rjump:
                    if player2.invis_cooldown == 0:
                        if player2.state == 'crouch':
                            player2.state = 'idle'
                        if player1.Rrage:
                            player2.health -= int((random.randint(2,7)*player1.damage))*3
                        else:
                            player2.health -= int((random.randint(2,7)*player1.damage)/random.choice([1,player2.defence]))
                        player2.invis_cooldown = 15
                        player2.ragecooldown = 40
                        player2.rage += random.randint(5,15)*player2.ragex
                        if not player1.Rrage:
                            player1.ragecooldown = 20
                            player1.rage += random.randint(5,10)*player1.ragex
                else:
                    player2.rage += random.randint(4,7)*player2.ragex

            if player2.Rleg:
                if not player1.Rjump:
                    if player2.invis_cooldown == 0:
                        if player1.state == 'crouch':
                            player1.state = 'idle'
                        if player2.Rrage:
                            player1.health -= int((random.randint(1,2)*player2.damage))*3
                        else:
                            player1.health -= int((random.randint(1,2)*player2.damage)/random.choice([1,player1.defence]))
                        player1.invis_cooldown = 15
                        player1.ragecooldown = 40
                        player1.rage += random.randint(5,15)*player1.ragex
                        if not player2.Rrage:
                            player2.ragecooldown = 20
                            player2.rage += random.randint(7,15)*player2.ragex
                else:
                    player1.rage += random.randint(4,7)*player1.ragex

            if player1.health <= 0:
                player1.lose1(False)
                player2.win1(True)
                gameplay = False
            elif player2.health <=0:
                player1.win1(False)
                player2.lose1(True)
                gameplay = False

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if gameplay:
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
                        elif event.key == pygame.K_t:
                            if player1.rage == 200:
                                player1.Rrage = True
                        elif event.key == pygame.K_ESCAPE:
                            running = False


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
                        elif event.key == pygame.K_j:
                            if player2.rage == 200:
                                player2.Rrage = True
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    
            
                if event.type == pygame.KEYUP:
                    if gameplay:
                        if event.key == pygame.K_s:
                            player1.crouch(False)
                        elif event.key == pygame.K_a:
                            player1.block(False)
                        elif event.key == pygame.K_DOWN:
                            player2.crouch(False)
                        elif event.key == pygame.K_RIGHT:
                            player2.block(False)
                    elif event.key == pygame.K_ESCAPE:
                        running = False
        
        screen.blit(background,(0,0))

        player1.draw(screen,False)
        player2.draw(screen,True)

        player1.update(False) 
        player2.update(True)

        pygame.draw.rect(screen,(255,0,0),player1.rect_pos_RED)
        pygame.draw.rect(screen,(0,255,0),player1.rect_pos_GREEN)
        #player2
        pygame.draw.rect(screen,(255,0,0),player2.rect_pos_RED)
        pygame.draw.rect(screen,(0,255,0),player2.rect_pos_GREEN)

        pygame.draw.rect(screen,(255,128,0),player1.rect_pos_RAGE1)
        pygame.draw.rect(screen,(255,128,0),player2.rect_pos_RAGE1)

        if player1.rage != 200:
            pygame.draw.rect(screen,(255,51,51),player1.rect_pos_RAGE2)
        else:
            pygame.draw.rect(screen,(255,0,127),player1.rect_pos_RAGE2)
        if player2.rage != 200:
            pygame.draw.rect(screen,(255,51,51),player2.rect_pos_RAGE2)
        else:
            pygame.draw.rect(screen,(255,0,127),player2.rect_pos_RAGE2)

        HP = font1.render('HP:'+str(player1.health)+'/'+str(player1.fullhealth),True,(0,100,0))
        screen.blit(HP,(5,682))
        HP = font1.render('HP:'+str(player2.health)+'/'+str(player2.fullhealth),True,(0,100,0))
        screen.blit(HP,(1170,682))

    # else:
    #     if choose_menu:
    #         pygame.draw.rect(screen,(96,96,96),[0,0,WIDTH,HEIGHT])




    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()
