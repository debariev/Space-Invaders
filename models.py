from utils import load_sprite

class GameObject:
    def __init__(self, position, sprite):
        self.x, self.y = position
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))
    
    def move(self, x, y):
        self.x += x
        self.y += y


class Cannon(GameObject):
    def __init__(self, position, sprite, create_bullet_callback):
        self.x, self.y = position
        self.sprite = sprite
        self.create_bullet_callback = create_bullet_callback

    def shoot(self):
        bullet_sprite = load_sprite("bullet")
        bullet = Bullet((self.x + self.sprite.get_rect().width/2-bullet_sprite.get_rect().width/2, self.y), bullet_sprite)
        self.create_bullet_callback(bullet)

class Bullet(GameObject):
    BULLET_SPEED = 5

    def move(self, up = True):
        if up:
            self.y -= self.BULLET_SPEED
        else:
            self.y += self.BULLET_SPEED

    def collides_with(self, obj):
        x, y= self.x, self.y
        x_obj, y_obj = obj.x, obj.y
        width, height = self.sprite.get_rect().width, self.sprite.get_rect().height
        width_obj, height_obj = obj.sprite.get_rect().width, obj.sprite.get_rect().height

        if (x < x_obj + width_obj) and (x_obj < x + width) and (y < y_obj + height_obj) and (y_obj < y + height_obj):
            return True
        return False


class Alien(GameObject):
    STRIKE_TIME = 60

    def __init__(self, position, sprite, create_bullet_callback):
        self.x, self.y = position
        self.sprite = sprite
        self.frames_from_last_strike = self.STRIKE_TIME+1
        self.create_bullet_callback = create_bullet_callback
    
    def drop(self):
        self.frames_from_last_strike = 0
        bullet_sprite = load_sprite("alien_bullet")
        bullet = Bullet((self.x + self.sprite.get_rect().width/2-bullet_sprite.get_rect().width/2, self.y), bullet_sprite)
        #self.create_bullet_callback(bullet)