"""
Module for game stages, including both menu
screens and play stages 
Written Dec 19, 2015 by Benjamin Reed
Version 0.0.1-alpha
	
Credit for original implementation goes to
Paul Vincent Craven at
programarcadegames.com
"""
import pygame as pyg
import constants as con
from game_surface import *

class Stage(object):
	"""
	Stage superclass, to be overridden
	"""
	background = pyg.Surface([con.SCREEN_WIDTH, con.SCREEN_HEIGHT])
	background.fill(con.BG_COLOR)
	
	def draw(self, screen):
		"""
		Wipe contents of previous frame and 
		blit background
		"""
		screen.fill(con.BLACK)
		screen.blit(self.background,[0,0])

class PlayStage(Stage):
	"""
	A Stage that features gameplay-oriented features 
	and functionality, as opposed to MenuStages
	"""
	def __init__(self, player):
		"""
		Create a sprite group for game surfaces in 
		the level and adds a reference to any and 
		all players in the level
		"""
		super(PlayStage, self).__init__()
		self.surface_list = pyg.sprite.Group()
		self.player = player
		
	def update(self):
		"""
		Update members of the surface list
		"""
		self.surface_list.update()
	
	def draw(self, screen):
		"""
		Wipe contents of previous frame, blit 
		background, and draw game surfaces 
		"""
		screen.fill(con.BLACK)
		screen.blit(self.background,[0,0])
		self.surface_list.draw(screen)
		
class PlayStage_01(PlayStage):
	"""
	Debug class for a "box" level with 2 walls, a
	ceiling, and a floor boxing the whole screen
	"""
	def __init__(self, player):
		"""
		Call superconstructor and populate stage 
		with four wall game surfaces
		"""
		super(PlayStage_01, self).__init__(player)
		level = [ [con.SCREEN_WIDTH, 15, 0, (con.SCREEN_HEIGHT-15)],
				  [con.SCREEN_WIDTH, 15, 0, 0],
				  [15, con.SCREEN_HEIGHT, 0, 0],
				  [15, con.SCREEN_HEIGHT, (con.SCREEN_WIDTH-15), 0]
		]
		
		# Construct surfaces using dimension/coord arguments,
		#   then add a reference to the player for collision
		#   detection
		for surface in level:
			wall = GameSurface(surface[0], surface[1])
			wall.rect.x = surface[2]
			wall.rect.y = surface[3]
			wall.player = self.player
			self.surface_list.add(wall)