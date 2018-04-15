'''
Student Name: Liyao Jiang
Student ID: 1512445
Section: EB1
Student Name: Xiaolei Zhang
Student ID: 1515335
Section: B1
Cmput 275 Project:
Link Picture Pairs

sidepan.py
contains a class 'Sidepan'
which is simply a side pannel for displaying
time remaining, score, and # of remaining picts
Also some instructions of game will be displayed
'''

import pygame

class Sidepan:
	# class attributes constants
	text_color = (127,255,0)
	circle_color = (47,79,79)
	s_width, s_height = 800, 800
	num_row = 12
	num_col = 12
	pict_width = int(s_width / num_col)
	pict_height = int(s_height/ num_row)


	# on __init__, Sidepan object takes display surface and font
	def __init__(self,_display_surf,font):
		pygame.init()
		self._display_surf = _display_surf
		self.font = font
		self.__on_init = True


	# called when main.py wants to initiated the side panel
	def on_init(self,score,count,time):
		self.update_score(score)
		self.update_count(count)
		self.update_time(time)
		self.instruction()
		self.__on_init = False


	# score is passed in, which is the score of the current game
	def update_score(self,score):
		pygame.draw.circle(self._display_surf,self.circle_color,(900,250),80,0)
		self._display_surf.blit(self.font.render("Score:",True,self.text_color), (850,200))
		self._display_surf.blit(self.font.render(str(score),True,self.text_color), (870,230))
		pygame.display.flip()


	# the time remaining is passed in
	def update_time(self,time):
		pygame.draw.circle(self._display_surf,self.circle_color,(900,450),80,0)
		self._display_surf.blit(self.font.render("Time:",True,self.text_color), (850,400))
		self._display_surf.blit(self.font.render(str(time),True,self.text_color), (870,430))
		pygame.display.flip()


	# the number of remaining picts is passed in
	def update_count(self,count):
		pygame.draw.circle(self._display_surf,self.circle_color,(900,650),80,0)
		self._display_surf.blit(self.font.render("Remain:",True,self.text_color), (850,600))
		self._display_surf.blit(self.font.render(str(count),True,self.text_color), (870,630))
		pygame.display.flip()


	# instruction strings 
	def instruction(self):
		self._display_surf.blit(self.font.render("[s] Shuffle:",True,self.text_color), (820,10))
		self._display_surf.blit(self.font.render("  cost 200",True,self.text_color), (820,40))
		self._display_surf.blit(self.font.render("[a] Add 10s:",True,self.text_color), (820,80))
		self._display_surf.blit(self.font.render("  cost 300",True,self.text_color), (820,110))
		pygame.display.flip()


	# redraw the 4 rectangular sides of the background
	def redraw_bg(self):
		image_menu = pygame.image.load("images/menu.jpg")
		image_menu = pygame.transform.scale(image_menu,(self.s_width,self.s_height))
		self._display_surf.blit(image_menu,(0,0),(0,0,800,self.pict_height))
		self._display_surf.blit(image_menu,(0,11*self.pict_height),\
			(0,11*self.pict_height,12*self.pict_width,self.pict_height))
		self._display_surf.blit(image_menu,(0,self.pict_height),\
			(0,self.pict_height,self.pict_width,10*self.pict_height))
		self._display_surf.blit(image_menu,(11*self.pict_width,self.pict_height),\
			(11*self.pict_width,self.pict_height,self.pict_width,10*self.pict_height))
		pygame.display.flip()
