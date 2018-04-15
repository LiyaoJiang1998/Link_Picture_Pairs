'''
Student Name: Liyao Jiang
Student ID: 1512445
Section: EB1
Student Name: Xiaolei Zhang
Student ID: 1515335
Section: B1
Cmput 275 Project:
Link Picture Pairs

main.py
the game class handles the game itself
and puts everything toghether
'''

import pygame,sys,random
import pygame.font
from pict import Pict
from sidepan import Sidepan

class game:
	# constant class attributes
	s_width, s_height = 800, 800
	window_width, window_height = 1000, 800
	color_background = (0,0,0)

	num_row = 12
	num_col = 12
	pict_total = 10
	pict_width = int(s_width / num_col)
	pict_height = int(s_height/ num_row)
	# the total time for each round
	total_time = 100


	# init the necessary instance attributes
	def __init__(self):
		self._running = True # flag for game running
		self._display_surf = None
		self._image_surf = None
		self.prev_coord = None
		self._notime = False # flag for no time losing condition
		self._win = False # flag for win by no pict remains


	# all the game initialize work is inside
	def on_init(self):
		global restart, first
		self._display_surf = pygame.display.set_mode([self.window_width,self.window_height])
		self._running = True
		self._display_surf.fill(self.color_background)
		self.font = pygame.font.SysFont('Arial',30)
		# menu mode at the first time
		if first:
			while self._running:
				self.menu()
			first = False
			if (not self._running) and (not restart):
				self.on_cleanup()
			else:
				self._running = True
				restart = True
		image_menu = pygame.image.load("images/menu.jpg")
		image_menu = pygame.transform.scale(image_menu,(self.s_width,self.s_height))
		self._display_surf.blit(image_menu,(0,0))
		pygame.display.update()
		# dic_initialize will create and show all the random picts 
		self.dic = self.dic_initialize()
		self.score = 0
		# initialize the sidepan
		self.pan = Sidepan(self._display_surf,self.font)
		self.start_time = pygame.time.get_ticks() # record the start time
		self.bonus_time = 0 # this records the added bonus time
		self.pan.on_init(self.score,len(self.dic),0)
		# init music player
		pygame.mixer.init()
		self.remove = pygame.mixer.Sound("remove.wav") # load the remove sound
 
	# event will check for user input
	# mousebutton for linking
	# keyboard s key for shuffle (cost 200 score)
	# keyborad a key for adding bonus time (cost 300 score)
	# clikc on quit button will quit the game
	def on_event(self, event):
		global restart
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.check_mouse(event) # let check_mouse handle linking
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s and self.score >= 200:
				self.shuffle()
				self.score -= 200
			if event.key == pygame.K_a and self.score >= 300:
				self.score -= 300
				self.bonus_time += 10 
		if event.type == pygame.QUIT:
			self._running = False
			restart = False


	# excuted in between frames, updates the sidepanel and background
	def on_loop(self):
		self.pan.redraw_bg()
		# account for the bonus_time
		time = self.total_time + self.bonus_time - int((pygame.time.get_ticks()-self.start_time)*0.001)
		self.pan.update_time(time)
		self.pan.update_count(len(self.dic))
		self.pan.update_score(self.score)
		# flag notime for game over
		if time <= 0:
			self._notime = True
	

	# menu mode that handles in between rounds
	# press r for a new game
	# press q for quit
	# shows different prompt for win or loose
	def menu(self):
		global restart,first
		restart = False
		image_menu = pygame.image.load("images/menu.jpg")
		image_menu = pygame.transform.scale(image_menu,(self.s_width,self.s_height))
		self._display_surf.blit(image_menu,(0,0))
		str1 = "[r]--Press r to start a new game"
		str2 = "[q]--Press q to quit game"
		str_win = "Congratulations! You linked all the pictures!"
		str_lose = "Time is up! Good luck on next time!"
		str_welcome = "Welcome to Link Picture Pairs! Enjoy!"
		if first:
			self._display_surf.blit(self.font.render(str_welcome,True,(0,0,0)), (100,150))
		elif self._win:
			self._display_surf.blit(self.font.render(str_win,True,(0,0,0)), (100,150))
		elif self._notime:
			self._display_surf.blit(self.font.render(str_lose,True,(0,0,0)), (100,150))
		self._display_surf.blit(self.font.render(str1,True,(0,0,0)), (250,400))
		self._display_surf.blit(self.font.render(str2,True,(0,0,0)), (250,500))
		pygame.display.update()

			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self._running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					self._running = False
				if event.key == pygame.K_r:
					self._running = False
					restart = True


	# quit the program
	def on_cleanup(self):
		pygame.quit()
		sys.exit()
 	

 	# the execution of the game loop
 	# tick(60) restrict the while loop to be 60fps
	def on_execute(self):
		c = pygame.time.Clock()
		if self.on_init() == False:
			self._running = False
 
		while self._running:
			# winning check
			if len(self.dic) == 0:
				self._win = True
				self.menu()
			# losing check
			elif self._notime:
				self.menu()
			# handle user inputs
			else:
				for event in pygame.event.get():
					self.on_event(event)
				self.on_loop()
				c.tick(60) # avoid busy loop
		global restart
		if restart == False:
			self.on_cleanup()


	# O(pict_total*width*(width*height)) = O(n^4)
	# initalize a dic containing num_row*num_col random picts
	def dic_initialize(self):
		dic = {}
		coord_list = []
		# list of coordinates in the grid
		for i in range(1,self.num_row-1):
			for j in range(1,self.num_col-1):
				coord_list.append((i, j))

		# for each pict, randomly assign it to 10 different positions
		for i in range(self.pict_total):
			for j in range(10):
				coord = random.choice(coord_list)
				coord_list.remove(coord) # remove from list take O(lengthoflist)
				# add the coord as key and add the Pict object as value
				dic[coord] = Pict(coord[0],coord[1],i)
				# display each pict
				jpg = pygame.image.load('images/%d.jpg' %i)
				jpg = pygame.transform.scale(jpg,(self.pict_width,self.pict_height))
				self._display_surf.blit(jpg, dic[coord].pixel())
		
		pygame.display.update()
		return dic

	# O(1)
	# remove the pict at coord, draw a white rect over it
	# also remove it from the dic, play the remove sound
	def remove_pict(self,coord):
		pixel = self.dic[coord].pixel()
		parameter = [pixel[0],pixel[1],self.pict_width,self.pict_height]
		pygame.draw.rect(self._display_surf,(255,255,255),parameter,0)
		pygame.display.flip()
		del self.dic[coord]
		self.remove.play()

	# O(n^2) since called two_turn
	def check_mouse(self,event):
		if pygame.mouse.get_pressed()[0]:
			# covert the pixel to coord and check
			pixel_x,pixel_y = pygame.mouse.get_pos()
			new_coord = (pixel_x//self.pict_width, pixel_y//self.pict_height)
			# case of not clicking on a valid block
			if new_coord not in self.dic:
				self.prev_coord = None
				return
			# case of no previous coord
			elif self.prev_coord == None:
				self.prev_coord = new_coord
				return
			# case of clicking on the same position as prev
			elif self.prev_coord == new_coord:
				return
			# case of valid click on a pict, determine which kind of link to prev
			# zero_turn will be checked first, and then one_turn, two_turn
			if self.dic[new_coord].zero_turn(self.dic,self.dic[self.prev_coord],self._display_surf):
				self.remove_pict(new_coord)
				self.remove_pict(self.prev_coord)
				self.score += 10
			elif self.dic[new_coord].one_turn(self.dic,self.dic[self.prev_coord],self._display_surf):
				self.remove_pict(new_coord)
				self.remove_pict(self.prev_coord)
				self.score += 20
			elif self.dic[new_coord].two_turn(self.dic,self.dic[self.prev_coord],self._display_surf):
				self.remove_pict(new_coord)
				self.remove_pict(self.prev_coord)
				self.score += 30
			# set this clicked coord as the prev coord
			else:
				self.prev_coord = new_coord
				return
			# at this point, a pair of picts is linked, reset click
			self.prev_coord = None



	# O(n^4)
	# put all keys in dic into list, assign each to a random coord
	# and redraw them
	def shuffle(self):
		# draw white rectangle background
		parameter = [self.pict_width,self.pict_height,10*self.pict_width,10*self.pict_height]
		pygame.draw.rect(self._display_surf,(255,255,255),parameter,0)
		# dic.values take O(n)
		values = list(self.dic.values())
		size = len(self.dic)
		coord_list = []
		self.dic = {}
		# this loop takes O(n^2), get all the coordinates
		for i in range(1,self.num_row-1):
			for j in range(1,self.num_col-1):
				coord_list.append((i, j))

		# assign each pict to a random coord and add to dic and display
		for i in range(size):
			coord = random.choice(coord_list)
			val = random.choice(values)
			coord_list.remove(coord)
			values.remove(val) # remove takes O(length of list) = O (n^2)
			self.dic[coord] = Pict(coord[0],coord[1],val.pict_num)
			jpg = pygame.image.load('images/%d.jpg' %val.pict_num)
			jpg = pygame.transform.scale(jpg,(self.pict_width,self.pict_height))
			self._display_surf.blit(jpg,self.dic[coord].pixel())
		pygame.display.update()
		self.prev_coord = None


if __name__ == "__main__" :
	restart = True
	first = True
	while restart == True:
		pygame.init()
		restart = False
		Game = game()
		Game.on_execute()
	pygame.quit()