import pygame

class Obstacle(pygame.sprite.Sprite):
	def __init__(self, size, pos, color):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.image.fill(color)
		self.rect = self.image.get_rect(center=pos)


shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx'
]