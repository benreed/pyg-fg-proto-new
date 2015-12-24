"""
Module for platforms and physical surfaces
Written Dec 19, 2015 by Benjamin Reed
Version 0.0.1-alpha

Credit for original implementation goes to
Paul Vincent Craven at
programarcadegames.com
"""
import pygame as pyg
import constants as con

class GameSurface(pyg.sprite.Sprite):
	"""
	Generic game surface superclass.
	"""
	def __init__(self, width, height):
		"""
		DEBUG: Instantiate a basic debug
		platform of dimensions (width, 
		height) as a green rectangle
		"""
		super(GameSurface, self).__init__()
		
		self.image = pyg.Surface([width, height])
		self.image.fill(con.GREEN)
		
		self.rect = self.image.get_rect()