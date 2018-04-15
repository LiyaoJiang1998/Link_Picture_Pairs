'''
Student Name: Liyao Jiang
Student ID: 1512445
Section: EB1
Student Name: Xiaolei Zhang
Student ID: 1515335
Section: B1
Cmput 275 Project:
Link Picture Pairs

pict.py contains a class "Pict"
In the main game, each small picture block will be an instance of Pict
this class also have methods for checking different types of linking.
Eg. zero_turn, one_turn, two_turn
Note: inside these methods, they will also draw a black line to show the links
on the display when they are linkable.
'''

import pygame

class Pict:
	# constant class attributes
	s_width, s_height = 800, 800
	num_row = 12
	num_col = 12
	pict_width = int(s_width / num_col)
	pict_height = int(s_height/ num_row)
	pygame.init()

	# instance members: coord - coordinate(x,y) 
	# pict_num - corresponds to which picture
	def __init__(self,x,y,index):
		self.coord = (x,y)
		self.pict_num = index
	

	# calculate the pixel x y on the display
	# when want to get pixel of center to draw line
	# pass True as an argument
	def pixel(self,center = None):
		# return the top left pixel of the pict
		if not center:
			pixel_x = self.pict_width * self.coord[0]
			pixel_y = self.pict_height * self.coord[1]
			return (pixel_x,pixel_y)
		# return the center pixel of the pict	
		elif center:
			pixel_x = int (self.pict_width * (self.coord[0] + 0.5))
			pixel_y = int (self.pict_height * (self.coord[1] + 0.5))
			return (pixel_x,pixel_y)


	'''
	'same_line' returns True if self and pict2
	on the same line with no obstruction
	Input arguments:
		dic - the dict contains all instances of pict
		pict2 - the other pict want to check with
	Running time:
		O(n),worst case there are num_col(or num_row)-2 blocks to check
	'''
	def same_line(self, dic, pict2):
		# if they are on the same line?
		if self.coord[0] != pict2.coord[0] and self.coord[1] != pict2.coord[1]:
			return False

		# are they the same pict?
		elif self.coord == pict2.coord:
			return False

		# only share the x (horizontal) coordinate
		# check all block in between are empty
		elif self.coord[0] == pict2.coord[0]:
			y_max = max(self.coord[1],pict2.coord[1])
			y_min = min(self.coord[1],pict2.coord[1])+1
			for y in range(y_min,y_max):
				if (self.coord[0],y) in dic:
					return False

		# only share the y (vertical) coordinate
		# check all block in between are empty
		elif self.coord[1] == pict2.coord[1]:
			x_max = max(self.coord[0],pict2.coord[0])
			x_min = min(self.coord[0],pict2.coord[0])+1
			for x in range(x_min,x_max):
				if (x,self.coord[1]) in dic:
					return False
		return True # on the same line with no obstruction


	'''
	helper function for drawing link lines
	point_list is a list of pixel coordinates
	lines connect these points will be drawn by pygame.draw.lines
	'''
	def drawlines(self,_display_surf,point_list):
		pygame.draw.lines(_display_surf,(0,0,0),False,point_list,2)
		pygame.display.flip()
		pygame.time.wait(300)
		pygame.draw.lines(_display_surf,(255,255,255),False,point_list,2)
		pygame.display.flip()


	'''
	'zero_turn' returns True if self and pict2
	on the same line with no obstruction, or next to each other
	Input arguments:
		dic - the dict contains all instances of pict
		pict2 - the other pict want to check with
		_display_surf - the drawing surface
	Running time:
		O(n),since it calls same_line once
	'''
	def zero_turn(self,dic,pict2,_display_surf):
		if self.pict_num == pict2.pict_num:
			# one line situation
			if self.same_line(dic,pict2):
				point_list = [self.pixel(True),pict2.pixel(True)]
				self.drawlines(_display_surf,point_list)
				return True
			# neighbors situation
			elif (abs(self.coord[1] - pict2.coord[1]) == 1) and (self.coord[0] == pict2.coord[0]):
				return True
			elif (abs(self.coord[0] - pict2.coord[0]) == 1) and (self.coord[1] == pict2.coord[1]):
				return True
		return False


	'''
	'one_turn' returns True if self and pict2
	can be linked with 2 lines (one turn)
	Input arguments:
		dic - the dict contains all instances of pict
		pict2 - the other pict want to check with
		_display_surf - the drawing surface
		two_turn_pixel - will be passed if two_turn situation
	Running time:
		since called same_line constant times
		O(max(width,height))= O(n)
	'''
	def one_turn(self,dic,pict2,_display_surf,two_turn_pixel = None):
		# different pict, can't be linked
		if self.pict_num != pict2.pict_num:
			return False
		# two possible intersects, see if one is same line (no obstrution)
		# with both self and pict2, and itself is empty
		intersect1 = Pict(self.coord[0],pict2.coord[1],None)
		intersect2 = Pict(pict2.coord[0],self.coord[1],None)
		line_1 = self.same_line(dic,intersect1) and pict2.same_line(dic,intersect1)
		line_2 = self.same_line(dic,intersect2) and pict2.same_line(dic,intersect2)
		# try one of the intersect
		if line_1 and (intersect1.coord not in dic):
			point_list = [self.pixel(True),intersect1.pixel(True),pict2.pixel(True)]
			if two_turn_pixel != None:
				point_list.append(two_turn_pixel)
			self.drawlines(_display_surf,point_list)
			return True
		# try the other intersect
		elif line_2 and (intersect2.coord not in dic):
			point_list = [self.pixel(True),intersect2.pixel(True),pict2.pixel(True)]
			if two_turn_pixel != None:
				point_list.append(two_turn_pixel)
			self.drawlines(_display_surf,point_list)
			return True
		else:
			return False


	'''
	'two_turn' returns True if self and pict2
	can be linked with 3 lines (two turn)
	Input arguments:
		dic - the dict contains all instances of pict
		pict2 - the other pict want to check with
		_display_surf - the drawing surface
	Running time:
		O(n^2) worst case check for all points with the same y coord, or the same x-coord
		which is a total of 2n points, and test each point for both same_line and one_turn.
		the two methods are both O(n), so the total running time is O(n^2)
	'''
	def two_turn(self,dic,pict2,_display_surf):
		# different pict_num cannot be linked
		# The idea is that the intersect should same_line with self
		# and one_turn with pict2 at the same time
		if self.pict_num == pict2.pict_num:
			# check for possible same_line intersect across the row
			for x in range(0,self.num_col):
				intersect = Pict(x,self.coord[1],pict2.pict_num)
				if intersect.coord not in dic:
					# self.pixel(True) is passed to one_turn to draw
					if self.same_line(dic,intersect) and \
					pict2.one_turn(dic,intersect,_display_surf,self.pixel(True)):
						return True
			# check for possible same_line intersect across the column
			for y in range(0,self.num_row):
				intersect = Pict(self.coord[0],y,pict2.pict_num)
				if intersect.coord not in dic:
					# self.pixel(True) is passed to one_turn to draw
					if self.same_line(dic,intersect) and \
					pict2.one_turn(dic,intersect,_display_surf,self.pixel(True)):
						return True
		return False
		