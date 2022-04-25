èimport pygame

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Flappy Bird')
running = True
GREEN = (0, 200, 0)
clock = pygame.time.Clock()

while running:		
	clock.tick(60)
	screen.fill(GREEN)
	screen.blit(background_image, (0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
				
	pygame.display.flip()

pygame.quit()


	# draw sand
	sand_rect = pygame.draw.rect(screen, YELLOW, (0,550,400,50))

	# draw bird
	bird_rect = screen.blit(bird_image, (BIRD_X, bird_y))