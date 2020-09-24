# Game imports

import pygame
import random
import sys
import math

# Initiallizing pygame
pygame.init()

# Creating the game screen - X = (800) LEFT TO RIGHT. Y = (600) TOP TO BOTTOM
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Game caption and Icon
pygame.display.set_caption("Stefs Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player (Image) - playerX = the coordinates of the X value. playerY = the coordinates of the Y value
playerImg = pygame.image.load("xwing.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load("spaceenemy.png"))
	enemyX.append(random.randint(0, 735))
	enemyY.append(random.randint(50, 150))
	enemyX_change.append(1)
	enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("laser.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

# Font

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255, 0, 0))
	screen.blit(over_text, (200, 250))

def show_score(x, y):
	score = font.render("Score: " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

# Drawing (blit) the image of the player and enemy on the screen
def player(x, y):
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))

# fire_bullet - Displays bullet img and declares a "fire" string so that when we later call this, pressing spacebar 
#will make the state "fire"

def fire_bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):

	# distance/collision = the midpoint between the bullet and the enemy. So the average x + average y of the
	# bullet and enemy = the midpoint/colission point.
	distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))

	# this is essentially the space of the hitbox/the px that counts as a collission (almost the width/size of the enemy)
	if distance < 27:
		return True
	else:
		return False
	




# Game loop
running = True
while running:

	#RGB - Red, Green, BLue
	screen.fill((0, 0, 0))
	# Background Image
	screen.blit(background, (0, 0,))
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -2
			elif event.key == pygame.K_RIGHT:
				playerX_change = 2

			# When you shoot, the x coordinate of the bullet will be saved and therefore the same as the x coordinate of the ship
			# Also checks IF the bullet state is ready before being able to shoot it again
			elif event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					# Gets the current x coordinate of the space
					bulletX = playerX
					fire_bullet(playerX, bulletY)



		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0

	playerX += playerX_change

	# Player Boundary limit - 736px because the ship is 64px and the screen boundary is 800. 800 - 64.
	#The way the mechanic is working here is as soon as the ship touches the boundary, it is immediately
	#sent back to just before the boundary. (its basically resetting the position really quick but unseen)
	#to the eye
	if playerX <=0:
		playerX = 0
	elif playerX >= 736:
		playerX = 736

	# Enemy Movement
	for i in range(num_of_enemies):

		# Game Over
		if enemyY[i] > 440:
			for j in range(num_of_enemies):
				enemyY[j] = 2000

			game_over_text()
			break



		if enemyX[i] <=0:
			enemyX_change[i] = 1.5
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -1.5
			enemyY[i] += enemyY_change[i]
		
	
		

		enemyX[i] += enemyX_change[i]


		# Collision - when there is a collision, the bullet location gets set back to the ship and the state 
	# goes back to ready, the score is printed and updated by 1, and the enemy respawns.
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0, 735)
			enemyY[i] = random.randint(50, 150)

		enemy(enemyX[i], enemyY[i], i)

	# Bullet Movement - when spacebar is pressed, state is changed to fire and the bullet is displayed and shot from ship
	if bulletY <= 0:
		bulletY = 480
		bullet_state = "ready"


	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change



	player(playerX, playerY)
	show_score(textX, textY)

	pygame.display.update()





