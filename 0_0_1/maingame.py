"""
Main game module with modified architecture for 
increased encapsulation of main game loop logic
Written Dec 18, 2015 by Benjamin Reed
Version 0.0.1-alpha
	
Credit for this implementation goes to Sean J. McKiernan
(Mekire) at /r/pygame
https://github.com/Mekire
"""
import sys
import pygame as pyg
import constants as con
from stage import *
from game_object import *

class App:
	"""
	A class to cleanly encapsulate main game loop phases,
	including initialization, event handling, and state 
	updates
	"""
	def __init__(self):
		"""
		Get a reference to the display surface; set up required attributes;
		and instantiate player objects
		"""
		self.screen = pyg.display.get_surface()
		self.screen_rect = self.screen.get_rect()
		self.clock = pyg.time.Clock()
		self.fps = con.TARGET_FPS
		self.done = False
		self.keys = pyg.key.get_pressed()
		
		# Initialize player object
		self.player = Player()
		
		# Initialize stage list and current level
		self.test_stage = PlayStage_01(self.player)
		self.stage_list = []
		self.stage_list.append(self.test_stage)
		self.current_stage_no = 0
		self.current_stage = self.stage_list[self.current_stage_no]
		
		# Set up sprite group for game object sprites
		self.active_sprite_list = pyg.sprite.Group()
		self.player.stage = self.current_stage
		self.active_sprite_list.add(self.player)
		
	def event_loop(self):
		"""
		Method encompassing one trip through the event queue
		Called within main_loop()
		"""
		for event in pyg.event.get():
			if event.type == pyg.QUIT:
				self.done = True
			elif event.type in (pyg.KEYUP, pyg.KEYDOWN):
				self.keys = pyg.key.get_pressed()
				
	def render(self):
		"""
		Draws to the screen and updates the display
		"""
		self.current_stage.draw(self.screen)
		self.active_sprite_list.draw(self.screen)
		pyg.display.flip()
		
	def main_loop(self):
		"""
		Performs the main game loop
		"""
		while not self.done:
			self.event_loop()
			self.active_sprite_list.update(self.keys)
			self.render()
			self.clock.tick(self.fps)
		
def main():
	"""
	Main program function. Performs Pygame initialization,
	starts the app, and exits the program upon main loop
	break.
	"""
	pyg.init()
	pyg.display.set_caption(con.WINDOW_CAPTION)
	pyg.display.set_mode(con.SCREEN_SIZE)
	App().main_loop()
	pyg.quit()
	sys.exit()
	
if __name__ == "__main__":
	main()