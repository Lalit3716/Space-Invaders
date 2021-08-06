import pygame
from laser import Laser
pygame.init()
laser_sound = pygame.mixer.Sound("../audio/laser.wav")
laser_sound.set_volume(0.5)

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load("../graphics/player.png")
		self.rect = self.image.get_rect(midbottom=pos)
		self.speed = 5
		self.lasers = pygame.sprite.Group()
		self.ready = True
		self.cooldown = 600
		self.shoot_time = 0

	def update(self, screen_width):
		self.move(screen_width)
		self.recharge()

	def move(self, screen_width):
		keys = pygame.key.get_pressed()
		
		if keys[pygame.K_LEFT]:
			if self.rect.left <= 0:
				self.rect.left = 0
			else:	
				self.rect.left -= self.speed

		if keys[pygame.K_RIGHT]:
			if self.rect.right >= screen_width:
				self.rect.right = screen_width
			else:
				self.rect.right += self.speed

		if keys[pygame.K_SPACE] and self.ready:
			laser_sound.play()
			self.shoot()
			self.shoot_time = pygame.time.get_ticks()
			self.ready = False

	def shoot(self):
		laser_sprite = Laser((self.rect.centerx, self.rect.centery), -8)
		self.lasers.add(laser_sprite)

	def recharge(self):
		if pygame.time.get_ticks() - self.shoot_time >= 600:
			self.ready = True
