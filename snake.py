import pygame
import sys
import random
import numpy as np
block_width= 32
width_blocks= 20
height_blocks= 20
size= width, height= block_width * width_blocks, block_width* height_blocks
snake_color= (255, 0, 0)
background_color= (0, 0, 0)
food_color= (0, 255, 0)
food_sprite= pygame.image.load('Sprites/Food.png')
background_sprite= pygame.image.load('Sprites/Background.png')
background_sprite= pygame.transform.scale(background_sprite, size)
start_sprite= pygame.image.load('Sprites/Start.png')
start_pressed_sprite= pygame.image.load('Sprites/Start_pressed.png')
# empty_squares= []
time= 100

# class Coord:
# 	def __init__(self, x, y):
# 		self[0]= x
# 		self[1]= y

class Snake:
	def __init__(self, screen, last_direction):
		self.data= [np.array([ (width_blocks//2 -3 ) ,  (height_blocks//2- 1)] ),
					np.array([ (width_blocks//2 -2 ) ,  (height_blocks//2- 1)] ),
					np.array([ (width_blocks//2 -1 ) ,  (height_blocks//2- 1)] )]
		self.screen= screen
		self.last_direction= last_direction
		self.tail={}
		self.body={}
		self.head={}
		self.load_images()

	def load_images(self):
		self.tail[str(np.array([0, -1]))]= pygame.image.load('Sprites/Tail.png')
		self.tail[str(np.array([0, 1]))]= pygame.transform.rotate(self.tail[str(np.array([0, -1]))], 180)
		self.tail[str(np.array([1, 0]))]= pygame.transform.rotate(self.tail['[0 1]'], 90)
		self.tail[str(np.array([-1, 0]))]= pygame.transform.rotate(self.tail['[0 1]'], -90)

		self.head[str(np.array([0, 1]))]= pygame.image.load('Sprites/Head.png')
		self.head[str(np.array([0, -1]))]= pygame.transform.rotate(self.head[str(np.array([0, 1]))], 180)
		self.head[str(np.array([1, 0]))]= pygame.transform.rotate(self.head['[0 1]'], 90)
		self.head[str(np.array([-1, 0]))]= pygame.transform.rotate(self.head['[0 1]'], -90)

		self.body[str(np.array([[0, 1], [0, 1]]))]= self.body[str(np.array([[0, -1], [0, -1]]))]= pygame.image.load('Sprites/Body.png')
		self.body[str(np.array([[-1, 0], [-1, 0]]))]=  self.body[str(np.array([[1, 0], [1, 0]]))]= pygame.transform.rotate(self.body[str(np.array([[0, 1], [0, 1]]))], 90)


		self.body[str(np.array([[0, 1], [1, 0]]))]= self.body[str(np.array([[-1, 0], [0, -1]]))]= pygame.image.load('Sprites/Body_turn.png')
		self.body[str(np.array([[0, -1], [1, 0]]))]= self.body[str(np.array([[-1, 0], [0, 1]]))]= pygame.transform.rotate(self.body[str(np.array([[0, 1], [1, 0]]))],  -90)
		self.body[str(np.array([[0, -1], [-1, 0]]))]= self.body[str(np.array([[1, 0], [0, 1]]))]= pygame.transform.rotate(self.body[str(np.array([[0, 1], [1, 0]]))],  180)
		self.body[str(np.array([[0, 1], [-1, 0]]))]= self.body[str(np.array([[1, 0], [0, -1]]))]= pygame.transform.rotate(self.body[str(np.array([[0, 1], [1, 0]]))],  90)


	def draw(self):
		diff= np.subtract(self.data[1:], self.data[:-1])
		self.screen.blit(self.tail[str(diff[0])], self.data[0]*block_width)
		for index in range(len(diff)-1):
			# print(val)
			self.screen.blit(self.body[str(diff[index: index +2])],  self.data[index+1]*block_width) #str(diff[index + 1])

		self.screen.blit(self.head[str(self.last_direction)], self.data[-1]*block_width)

	def move(self, next_direction, food): # we can use numpy
		if (np.array_equal(next_direction+ self.last_direction, [0,0]) ):
			 next_direction= self.last_direction

		next_block= (self.data[-1] + next_direction )
		if self.data[-1][0] >= width_blocks or self.data[-1][1] >= height_blocks or self.data[-1][0] < 0 or self.data[-1][1] < 0 or (self.data[-1].tolist() in np.array(self.data[:-1]).tolist()) : # kinda sloppy
			return 0
		ev= 1 ## food not eaten
		if not np.array_equal(next_block, food) :
			del self.data[0]
		else:
			ev= 2 # food eaten
		self.data.append(next_block)
		self.last_direction= next_direction ## update !!!
		return ev

def draw_background(screen):
	screen.blit(background_sprite, (0, 0)) # background_sprite

def draw_food(screen, food):
	screen.blit(food_sprite, food*block_width)

def start_screen(screen):
	start_rect= start_sprite.get_rect()
	start_rect.center= (width//2, height//2)
	screen.blit(start_sprite, start_rect )
	return start_rect

def start_screen_pressed(screen):
	start_rect= start_pressed_sprite.get_rect()
	start_rect.center= (width//2, height//2)
	screen.blit(start_pressed_sprite, start_rect )
	return start_rect

def get_empty_squares(snake):
	empty_squares= []
	for i in range(width_blocks):
		for j in range(height_blocks):
			block= np.array([i , j ])
			if [0, 0] not in (snake.data-block).tolist():
				empty_squares.append(block)
	return empty_squares


def get_food(snake):
	empty_squares= get_empty_squares(snake)
	return random.choice(empty_squares)

def main ():
	clock= pygame.time.Clock()
	pygame.init()

	pygame.display.set_caption('Snike')
	screen= pygame.display.set_mode(size)
	while True:
		draw_background(screen)
		start_rect= start_screen(screen)
		# start screen
		start= True
		while start:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					cursor_pos= pygame.mouse.get_pos()
					if start_rect.collidepoint(cursor_pos):
						start= False
			pygame.display.update()
		draw_background(screen)
		start_screen_pressed(screen)
		pygame.display.update()
		pygame.time.wait(50)

		next_direction= np.array([1, 0])
		snake= Snake(screen, next_direction)

		food= get_food(snake)

		draw_background(screen)
		draw_food(screen, food)
		snake.draw()

		# 1st frame
		pygame.display.update()
		pygame.time.wait(time)


		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			pressed_keys= pygame.key.get_pressed()

			if pressed_keys[pygame.K_UP] :
				next_direction= np.array([0, -1])
			elif pressed_keys[pygame.K_DOWN] :
				next_direction= np.array([0, 1])
			elif pressed_keys[pygame.K_RIGHT] :
				next_direction= np.array([1, 0])
			elif pressed_keys[pygame.K_LEFT] :
				next_direction= np.array([-1, 0])


			ev= snake.move(next_direction, food)

			if ev== 0:
				break
			elif ev== 1:
				pass
			elif ev== 2:
				food= get_food(snake)
			draw_background(screen)
			draw_food(screen, food)
			snake.draw()
			pygame.display.update()
			# clock.tick(time)
			pygame.time.wait(time)


if __name__ == '__main__':
	main()
