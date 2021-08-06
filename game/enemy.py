import pygame

class Enemy(pygame.sprite.Sprite):
	def __init__(self, color, x, y):
		super().__init__()
		file_path = '../graphics/' + color + '.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))
		if color == "red": self.value = 500
		if color == "yellow": self.value = 300
		if color == "green": self.value = 100

	def update(self, speed):
		self.rect.x += speed

class Extra(pygame.sprite.Sprite):
	def __init__(self, dir, screen_width):
		super().__init__()
		self.image = pygame.image.load("../graphics/extra.png").convert_alpha()

		if dir == "right":
			x = screen_width + 100
			self.speed = -5
		if dir == "left":
			x = -100
			self.speed = 5

		self.rect = self.image.get_rect(center=(x, 80))

	def update(self):
		self.rect.centerx += self.speed