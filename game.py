import pygame
from random import randint

class Tube:
	def __init__(self, posx, posy, width, height, type):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.passed = False
		self.type = type
	def inv(self):
		return Tube(self.posx, self.height + TUBE_GAP, TUBE_WIDTH, HEIGHT - self.height - TUBE_GAP, 2)
	def draw(self):
		if self.type == 1:
			tube_down_img = pygame.image.load("tube_down.png")
			tube_down_img = pygame.transform.scale(tube_down_img, (self.width, self.height))
			return screen.blit(tube_down_img, (self.posx, self.posy))
		elif self.type == 2:
			tube_up_img = pygame.image.load("tube_up.png")
			tube_up_img = pygame.transform.scale(tube_up_img, (self.width, self.height))
			return screen.blit(tube_up_img, (self.posx, self.posy))
		else:
			return pygame.draw.rect(screen, BLUE, (self.posx, self.posy, self.width, self.height))

class Bird:
	def __init__(self):
		self.posx = 50
		self.posy = 400
		self.width = 35
		self.height = 35
		self.velocity = 0
	def draw(self):
		bird_image = pygame.image.load("bird.png")
		bird_image = pygame.transform.scale(bird_image, (self.width, self.height))
		return screen.blit(bird_image,(self.posx, self.posy))

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
background_image = pygame.image.load("background.png")

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('sans', 20)
score = 0 

TUBE_WIDTH = 50
TUBE_GAP = 150
TUBE_VELOCITY = 3

tube1 = Tube(500, 0, TUBE_WIDTH, randint(100,400), 1)
tube2 = Tube(700, 0, TUBE_WIDTH, randint(100,400), 1)
tube3 = Tube(900, 0, TUBE_WIDTH, randint(100,400), 1)
sol = Tube(0, 580, 400, 50, 3) #invisible tube

bird = Bird()

GRAVITATION = 0.5
running = True
finished = False
clock = pygame.time.Clock()

while running:
	clock.tick(60)
	screen.fill(GREEN)
	screen.blit(background_image, (0,0))
	#draw tubes
	tube1_rect = tube1.draw()
	tube2_rect = tube2.draw()
	tube3_rect = tube3.draw()

	tube1_inv_rect = tube1.inv().draw()
	tube2_inv_rect = tube2.inv().draw()
	tube3_inv_rect = tube3.inv().draw()

	sol_rect = sol.draw()

	#draw bird
	bird_rect = bird.draw()

	#show score
	score_txt = font.render("Score: " + str(score), True, BLACK)
	score_box = score_txt.get_rect()
 
	pygame.draw.rect(screen, WHITE,score_box) 
	screen.blit(score_txt, (0,0))

	#update tube
	for tube in [tube1, tube2, tube3]:
		tube.posx -= TUBE_VELOCITY
		if tube.posx + TUBE_WIDTH < 0:
			tube.posx = WIDTH + TUBE_GAP
			tube.height = randint(100,400)
			tube.passed = False 

	#update bird
	bird.posy += bird.velocity
	bird.velocity += GRAVITATION

	if bird.posy >= HEIGHT:
		finished = True

	#update score
	if tube1.posx < bird.posx < tube2.posx and not tube1.passed :
		score += 1
		tube1.passed = True
	if tube2.posx < bird.posx < tube3.posx and not tube2.passed :
		score += 1
		tube2.passed = True
	if tube3.posx < bird.posx < tube1.posx and not tube3.passed :
		score += 1
		tube3.passed = True
	
	#check collision
	for tube in [tube1_rect, tube2_rect, tube3_rect, tube1_inv_rect, tube2_inv_rect, tube3_inv_rect, sol_rect]:
		if bird_rect.colliderect(tube):
			finished = True
			TUBE_VELOCITY = 0
			bird.velocity = 0

			game_over_txt = font.render("Game over, score: {0}".format(score), True, BLACK)
			screen.blit(game_over_txt, (200,300))
			press_space_txt = font.render("Press Space to Continue", True, BLACK)
			screen.blit(press_space_txt, (200,350))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if finished:
					bird.posy = 400
					TUBE_VELOCITY = 3
					tube1.posx = 500
					tube2.posx = 700
					tube3.posx = 900
					score = 0
					pygame.time.wait(1000)
					finished = False
				bird.velocity = -10
						
	pygame.display.flip()

pygame.quit()
