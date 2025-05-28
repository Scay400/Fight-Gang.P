import pygame
import os
import random
import sys


pygame.init()


WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FightGang")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
clock = pygame.time.Clock()

class Character:
    def __init__(self, x, y):
        self.x = 300
        self.y = 150
        self.width =200
        self.height = 263
        self.state = "idle"
        self.animation_count = 0
        self.last_attack = None
        self.animations = {
            "idle": [],
            "attack1": [],
            "attack2": [],
            "crouch": [],
            "block": []
        }
    
        self.animation_speeds = {
            "idle": 0.2,
            "attack1": 0.3,
            "attack2": 0.3,
            "crouch": 0.3,
            "block": 0.3
        }
  
        self.reverse_speeds = {
            "crouch": 0.3,
            "block": 0.3
        }
        self.load_animations()
        self.attacking = False
        self.crouching = False
        self.blocking = False
        self.attack_cooldown = 0
        self.last_state = None
        self.reverse_animation = False
        self.attacks = ["attack1", "attack2"]
    
    def load_animations(self):
        animation_data = {
            "idle": {"folder": "idle", "frames": 13},
            "attack1": {"folder": "attack1", "frames": 3},
            "attack2": {"folder": "attack2", "frames": 4},
            "crouch": {"folder": "crouch", "frames": 2},
            "block": {"folder": "block", "frames": 2}
        }
        
        for state, data in animation_data.items():
            folder = data["folder"]
            frame_count = data["frames"]
            
            if not os.path.exists(folder):
                print(f"Внимание: Папка '{folder}' не найдена! Создаю placeholder-анимацию.")
                for _ in range(frame_count):
                    self.create_placeholder_frame(state)
                continue
            
            for i in range(frame_count):
                file_path = os.path.join(folder, f"{i}.png")
                try:
                    img = pygame.image.load(file_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.width, self.height))
                    self.animations[state].append(img)
                except:
                    print(f"Ошибка загрузки кадра {i} для анимации {state}")
                    self.create_placeholder_frame(state)
    
    def create_placeholder_frame(self, state):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        color = {
            "idle": (100, 150, 200),
            "attack1": (200, 100, 100),
            "attack2": (100, 200, 100),
            "crouch": (150, 150, 100),
            "block": (100, 100, 200)
        }.get(state, (150, 150, 150))
        
        pygame.draw.rect(surf, color, (0, 0, self.width, self.height))
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{state}", True, BLACK)
        surf.blit(text, (10, 10))
        self.animations[state].append(surf)
    
    def update(self):
 
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
 
        if self.last_state != self.state:
            self.animation_count = 0
            self.last_state = self.state
            self.reverse_animation = False
        

        speed = self.reverse_speeds.get(self.state, self.animation_speeds.get(self.state, 0.1))

        if not self.reverse_animation:
            self.animation_count += speed
            max_frame = len(self.animations[self.state]) - 1
            if int(self.animation_count) >= max_frame:
                if self.state in ["attack1", "attack2"]:
                    self.animation_count = max_frame
                    if self.attack_cooldown <= 0:
                        self.state = "idle"
                        self.attacking = False
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
    
    def draw(self, screen):
        if not self.animations[self.state]: 
            self.create_placeholder_frame(self.state)
            
        frame = min(int(self.animation_count), len(self.animations[self.state]) - 1)
        screen.blit(self.animations[self.state][frame], (self.x, self.y))
    
    def attack(self):
        if self.attack_cooldown <= 0 and not self.attacking and not self.blocking and not self.crouching:
            self.state = random.choice(self.attacks)
            # for i in range(len(self.attacks)):
            #     if self.state == self.attacks[i] and self.last_attack == self.attacks[i]:
            #         if i != len(self.attacks)-1:
            #             self.state == self.attacks[i+1]
            #         else:
            #             self.state == self.attacks[i-1]
            if self.state == 'attack1' and self.last_attack == 'attack1':
                self.state == 'attack2'
            if self.state == 'attack2' and self.last_attack == 'attack2':
                self.state == 'attack1'
            self.last_attack = self.state
            self.animation_count = 0
            self.attacking = True
            self.attack_cooldown = 30
        
    
    def crouch(self, is_crouching):
        if self.attack_cooldown <= 0 and not self.attacking and not self.blocking:
            self.crouching = is_crouching
            if is_crouching:
                self.state = "crouch"
                self.animation_count = 0
                self.reverse_animation = False
            elif self.state == "crouch":
                self.reverse_animation = True
                self.attack_cooldown = 10
            
    
    def block(self, is_blocking):
        if self.attack_cooldown <= 0 and not self.attacking and not self.crouching:
            self.blocking = is_blocking
            if is_blocking:
                self.state = "block"
                self.animation_count = 0
                self.reverse_animation = False
            elif self.state == "block":
                self.reverse_animation = True
                self.attack_cooldown = 10


player = Character(0, 0)


running = True
space_pressed = False
ctrl_pressed = False
shift_pressed = False

while running:
    screen.fill(WHITE)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_pressed = True
                player.attack()
            elif event.key == pygame.K_LCTRL:
                ctrl_pressed = True
                player.crouch(True)
            elif event.key == pygame.K_LSHIFT:
                shift_pressed = True
                player.block(True)
            elif event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False
            elif event.key == pygame.K_LCTRL:
                ctrl_pressed = False
                player.crouch(False)
            elif event.key == pygame.K_LSHIFT:
                shift_pressed = False
                player.block(False)

    player.update() 

    player.draw(screen)

    font = pygame.font.SysFont(None, 30)
    instructions = [
        f"Текущее состояние: {player.state}",
        f"Атака (SPACE): {'Да' if space_pressed else 'Нет'}",
        f"Присед (CTRL): {'Да' if ctrl_pressed else 'Нет'}",
        f"Блок (SHIFT): {'Да' if shift_pressed else 'Нет'}"
    ]
    
    for i, text in enumerate(instructions):
        rendered = font.render(text, True, BLACK)
        screen.blit(rendered, (20, 20 + i * 30))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()