import pygame

from models import Cannon, Bullet, Alien

from utils import load_sprite, print_text

from random import randrange

class SpaceInvaders:
    CANNON_SPEED = 2
    ALIEN_DROP_SPEED = 20

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))

        self.bullets = []
        self.bullet_shot = False

        self.alien_bullets = []

        self.alien_cluster = [Alien((50 + (50+10)*k, 100), load_sprite("alien"), self.alien_bullets.append) for k in range(12)] +\
                            [Alien((50 + (50+10)*k, 150), load_sprite("alien"), self.alien_bullets.append) for k in range(12)] +\
                            [Alien((50 + (50+10)*k, 200), load_sprite("alien"), self.alien_bullets.append) for k in range(12)]

        canon_sprite = load_sprite("cannon")
        self.cannon = Cannon((self.screen.get_rect().width/2-canon_sprite.get_rect().width/2,
                self.screen.get_rect().height - canon_sprite.get_rect().height - 10), canon_sprite, self.bullets.append)

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 64)
        self.message = ""
    
    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Invaders")

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if self.cannon:
            is_key_pressed = pygame.key.get_pressed()
            if is_key_pressed[pygame.K_RIGHT]:
                if self.cannon.x + self.cannon.sprite.get_rect().width < self.screen.get_rect().width:
                    self.cannon.move(self.CANNON_SPEED, 0)
            elif is_key_pressed[pygame.K_LEFT]:
                if self.cannon.x > 0:
                    self.cannon.move(-self.CANNON_SPEED, 0)

            if is_key_pressed[pygame.K_SPACE]:
                if not self.bullet_shot:
                    self.cannon.shoot()
                    self.bullet_shot = True
            else:
                self.bullet_shot = False

    def _process_game_logic(self):
        for bullet in self.bullets:
            bullet.move()
        
        if self.alien_cluster:
            free_aliens = []
            last_strikes = []
            for alien in self.alien_cluster:
                last_strikes.append(alien.frames_from_last_strike)
                if alien.frames_from_last_strike > alien.STRIKE_TIME:
                    alien.sprite = load_sprite("alien")
                    free_aliens.append(alien)
                else:
                    alien.sprite = load_sprite("alien_dropped")
                alien.frames_from_last_strike+=1
            
            if free_aliens:
                if min(last_strikes) > self.ALIEN_DROP_SPEED:
                    free_aliens[randrange(len(free_aliens))].drop()
        
        for alien_bullet in self.alien_bullets:
            alien_bullet.move(up=False)

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint((bullet.x, bullet.y)):
                self.bullets.remove(bullet)

        for alien_bullet in self.alien_bullets[:]:
            if not self.screen.get_rect().collidepoint((alien_bullet.x, alien_bullet.y)):
                self.alien_bullets.remove(alien_bullet)
        
        if self.alien_cluster:
            for bullet in self.bullets[:]:
                for alien in self.alien_cluster[:]:
                    if bullet.collides_with(alien):
                        self.bullets.remove(bullet)
                        self.alien_cluster.remove(alien)
        
        if self.cannon:
            for alien_bullet in self.alien_bullets[:]:
                if alien_bullet.collides_with(self.cannon):
                    self.alien_bullets.remove(alien_bullet)
                    self.cannon = None
                    self.message = "You lost"
                    self.color = "tomato"
                    break

        if not self.alien_cluster and self.cannon:
            self.message = "You won"
            self.color = "green"
    
    def _draw(self):
        self.screen.fill((0,0,0))

        if self.cannon:
            self.cannon.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        if self.alien_cluster:
            for alien in self.alien_cluster:
                alien.draw(self.screen)

        for alien_bullet in self.alien_bullets:
            alien_bullet.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font, self.color)
                
        pygame.display.flip()
        self.clock.tick(60)