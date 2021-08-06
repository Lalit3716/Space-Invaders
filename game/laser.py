import pygame

class Laser(pygame.sprite.Sprite):
	def __init__(self, pos, speed):
		super().__init__()
		self.image = pygame.Surface((3, 20))
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect(center=pos)
		self.speed = speed

	def update(self, screen_height):
		self.rect.y += self.speed
		self.destroy(screen_height)

	def destroy(self, screen_height):
		if self.rect.top <= 0 or self.rect.bottom >= screen_height: 
			self.kill()