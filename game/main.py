import pygame, sys, random
from player import Player
from obstacle import Obstacle, shape
from enemy import Enemy, Extra
from laser import Laser


def show_text(message, pos, color=(255, 255, 255), size=20, anti_alias=False):
	font = pygame.font.Font("../font/Pixeled.ttf", size)
	font = font.render(message, anti_alias, color)
	screen.blit(font, pos)

class Game:
	def __init__(self):

		# Cheat
		self.cheat_enabled = False 

		# Player Setup
		self.player = pygame.sprite.GroupSingle(Player((screen_width//2, screen_height)))
		
		# Score
		self.player_score = 0

		# Health
		self.player_lives = 5
		self.hearts = pygame.image.load("../graphics/heart.png")
		self.hearts_offset_x = screen_width - self.hearts.get_width() * 5 + 40 

		# Obstacles Setup
		self.obstacle_size = 6
		self.obstacles = pygame.sprite.Group()
		self.obstacles_num = 4
		gaps = [i * (screen_width/self.obstacles_num) for i in range(self.obstacles_num)]
		self.create_obstacles(*gaps, offset_x=screen_width / 15, offset_y=550, color=(241,79,80))

		# Enemy Setup
		self.enemies = pygame.sprite.Group()
		self.enemies_speed = 1
		self.create_enemies(rows=8, cols=10)
		self.enemy_lasers = pygame.sprite.Group()

		# Extra Setup
		self.extra_direction = random.choice(["right", "left"])
		self.extra_timer = random.randint(50, 80)
		self.extra = pygame.sprite.GroupSingle()

	def create_obstacle(self, offset_x, offset_y, gap_x, color):
		for row_index, row in enumerate(shape):
			for col_index, col in enumerate(row):
				if col == "x":
					x = col_index * self.obstacle_size + offset_x + gap_x
					y = row_index * self.obstacle_size + offset_y
					self.obstacles.add(Obstacle(self.obstacle_size, (x, y), color=color))

	def create_obstacles(self, *gaps_between, offset_x, offset_y, color):
		for gap in gaps_between:
			self.create_obstacle(offset_x=offset_x, offset_y=offset_y, gap_x=gap, color=color)

	def create_enemies(self,rows,cols,x_distance = 60, y_distance = 48, x_offset = 160, y_offset = 90):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index == 0: enemy_sprite = Enemy('red',x,y)
				elif 1 <= row_index <= 2: enemy_sprite = Enemy('yellow',x,y)
				else: enemy_sprite = Enemy('green',x,y)
				self.enemies.add(enemy_sprite)

	def enemy_movement(self):
		for enemy in self.enemies.sprites():
			if enemy.rect.left <= 0:
				self.enemies_speed = +1
				self.enemies_move_down()
			if enemy.rect.right >= screen_width:
				self.enemies_speed = -1
				self.enemies_move_down()

	def enemies_move_down(self):
		if self.enemies:
			for enemy in self.enemies.sprites():
				enemy.rect.y += 1			
			
	def extra_appear_timer(self):
		self.extra_timer -= 1
		if self.extra_timer <= 0:
			self.extra_direction = random.choice(["right", "left"])
			self.extra = pygame.sprite.GroupSingle(Extra(self.extra_direction, screen_width))
			self.extra_timer = random.randint(400, 800)

	def collision(self):
		# Player Lasers
		if self.player.sprite.lasers:
			for curr_laser in self.player.sprite.lasers:
				if pygame.sprite.spritecollide(curr_laser, self.obstacles, True):
					explosion_sound.play()
					if not self.cheat_enabled:
						curr_laser.kill()

				enemies_hit = pygame.sprite.spritecollide(curr_laser, self.enemies, True)
				if enemies_hit:
					for enemy in enemies_hit:
						self.player_score += enemy.value
							
					explosion_sound.play()
					if not self.cheat_enabled:
						curr_laser.kill()

				if pygame.sprite.spritecollide(curr_laser, self.extra, True):
					explosion_sound.play()
					self.player_score += 1000


		# Enemies
		if self.enemies:
			for curr_enemy in  self.enemies:
				if pygame.sprite.spritecollide(curr_enemy, self.obstacles, True):
					explosion_sound.play()

				if pygame.sprite.spritecollide(curr_enemy, self.player, False):
					explosion_sound.play()
					return True

		# Enemies Laser
		if self.enemy_lasers:
			for laser in  self.enemy_lasers.sprites():
				if pygame.sprite.spritecollide(laser, self.obstacles, True):
					explosion_sound.play()
					laser.kill()

				if pygame.sprite.spritecollide(laser, self.player, False):
					explosion_sound.play()
					laser.kill()
					self.player_lives -= 1
					if self.player_lives <= 0:
						return True

	def enemy_shoot(self):
		if self.enemies:
			enemy = random.choice(self.enemies.sprites())
			self.enemy_lasers.add(Laser(enemy.rect.center, 8))
			laser_sound.play()

	def show_health(self):
		for i in range(self.player_lives):
			screen.blit(self.hearts, (self.hearts_offset_x + i*40, 10))
				
	def show_score(self):
		show_text(f"SCORE: {self.player_score}", (10, 5), (255, 0, 255), 20)

	def activate_cheat(self):
		self.cheat_enabled = not self.cheat_enabled

	def check_victory(self):
		if not self.enemies:
			return True
		else:
			False

	def run(self):
		# Player Rendering
		self.player.update(screen_width)
		self.player.draw(screen)

		# Lasers Rendering
		self.player.sprite.lasers.update(screen_height)
		self.player.sprite.lasers.draw(screen)
		self.enemy_lasers.draw(screen)
		self.enemy_lasers.update(screen_height)

		# Obstacles Rendering
		self.obstacles.draw(screen)

		# Enemies Rendering
		self.enemy_movement()
		self.enemies.update(self.enemies_speed)
		self.enemies.draw(screen)
		self.extra.draw(screen)
		self.extra_appear_timer()
		self.extra.update()

		# Display Healt & Score
		self.show_health()
		self.show_score()
		
		# Collision's Logic
		return {"game_over": self.collision(),"victory": self.check_victory() }

	def over(self):
		show_text("GAME OVER", (screen_width//2 - 80, screen_height//2 - 50))
		show_text(f"SCORE: {self.player_score}", (screen_width//2 - 80, screen_height//2))

	def loading(self):
		show_text("Hit Enter To Play", (screen_width // 2 - 130, screen_height//2 - 50))

	def victory(self):
		show_text("VICTORY", (screen_width//2-80, screen_height//2-50))
		show_text(f"SCORE: {self.player_score}", (screen_width//2-80, screen_height//2))
		
	def reset(self):
		self.__init__()
		self.run()



class Overlay:
	def __init__(self):
		self.image = pygame.image.load("../graphics/tv.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (screen_width, screen_height))

	def lines(self):
		lines = screen_height // 3
		for line in range(lines):
			pygame.draw.line(self.image, (0, 0, 0), (0, line * 3), (screen_width, line*3), 1)

	def draw(self):
		self.image.set_alpha(random.randint(90, 100))
		self.lines()
		screen.blit(self.image, (0, 0))

if __name__ == "__main__":
	# Init Pygame
	pygame.init()
	screen_width = 800
	screen_height = 700
	screen = pygame.display.set_mode((screen_width,screen_height))
	pygame.display.set_caption("Space Invaders")
	clock = pygame.time.Clock()
	
	# Game Variables
	GAME_OVER = False 
	LOADING = True
	VICTORY = False

	# Audio
	explosion_sound = pygame.mixer.Sound("../audio/explosion.wav")
	music_sound = pygame.mixer.Sound("../audio/music.wav")
	laser_sound = pygame.mixer.Sound("../audio/laser.wav")
	music_sound.play(loops=-1)
	music_sound.set_volume(0.2)
	laser_sound.set_volume(0.5)
	explosion_sound.set_volume(0.3)

	# Initiate Game Class
	game = Game()

	# Overlay
	overlay = Overlay()

	# Timer 
	ENEMY_LASER_TIMER = pygame.USEREVENT
	pygame.time.set_timer(ENEMY_LASER_TIMER, 1000)

	
# Main Game Loop
while True:
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN and LOADING:
					LOADING = False
				if event.key == pygame.K_LCTRL and not GAME_OVER and not LOADING and not VICTORY:
					game.activate_cheat()
				if event.key == pygame.K_RETURN and (GAME_OVER or VICTORY):
					game.reset()
					GAME_OVER = False
					VICTORY = False	

			if event.type == ENEMY_LASER_TIMER and not GAME_OVER and not LOADING and not VICTORY:
				game.enemy_shoot()

	
	screen.fill((30, 30, 30))

	if LOADING:
		game.loading()
	
	elif not GAME_OVER and not VICTORY:
		res = game.run()
		GAME_OVER = res["game_over"]
		VICTORY = res["victory"]
	elif not GAME_OVER and VICTORY:
		game.victory()
	else:
		game.over()

	overlay.draw()
	pygame.display.update()
	clock.tick(60)