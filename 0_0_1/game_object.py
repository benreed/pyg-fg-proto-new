"""
Module for game objects with physical properties
Includes characters, projectiles, etc
Written Dec 19, 2015 by Benjamin Reed
Version 0.0.1-alpha

Credit for original implementation goes to
Paul Vincent Craven at
programarcadegames.com
"""
import Queue
import pygame as pyg
import constants as con
from spritesheet import *
from input import *

class PhysObject(pyg.sprite.Sprite):
	"""
	Generic physical object class extending Sprite.
	Meant as a debug object to be overridden, has 
	few members other than superclass members and
	deltaX/deltaY members. A glorified AABB, essentially.
	"""
	
	deltaX = 0
	deltaY = 0
	
	def __init__(self, color=con.RED, width=30, height=50):
		"""
		Calls superconstructor and initializes drawing 
		coordinates and a 30x50 red rectangle for the
		sake of visibility when debugging
		"""
		super(PhysObject, self).__init__()
		self.image = pyg.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = 40
		self.rect.y = 40
		
class Player(PhysObject):
	"""
	Player class that extends PhysObject and contains 
	all methods and members specific to a playable 
	game character
	"""
	# -------- Movement attributes --------
	run_speed = 6
	air_steer_speed = 3
	movement_speed = run_speed
	jump_force = -10
	gravity_force = .35
	
	# -------- Input event queue --------
	input_queue = Queue.Queue()
	
	# -------- State variables --------
	keys = None
	direction = "R"
	airborne = True
	air_jumped = False
	
	# -------- Lists for animation frames --------
	idle_frames_R = []
	idle_frames_L = []
	running_frames_R = []
	running_frames_L = []
	jumping_frames_R = []
	jumping_frames_L = []
	
	# Reference to current stage player inhabits
	stage =  None
	
	def __init__(self):
		"""
		Call superconstructor and load animation frames
		"""
		super(Player, self).__init__()
		self.init_frames()
		self.image = self.idle_frames_R[0]
		self.rect = self.image.get_rect()
		self.rect.x = 40
		self.rect.y = 40
			
	def update(self, keys):
		"""
		Update player attributes based on game events
		(input, collision detection, etc)
		"""
		# Apply gravity
		self.calc_grav()
				
		# Update keystate and handle input
		self.keys = keys
		self.handle_input(self.keys)
		
		# Apply deltaX
		self.rect.x += self.deltaX
		
		# Set running frame
		if self.direction == "R":
			frame = (self.rect.x // 30) % len(self.running_frames_R)
			self.image = self.running_frames_R[frame]
		else:
			frame = (self.rect.x // 30) % len(self.running_frames_L)
			self.image = self.running_frames_L[frame]
		
		# Check for collisions with surfaces (x-axis)
		surface_col_list = pyg.sprite.spritecollide(self, self.stage.surface_list, False)
		for surface in surface_col_list:
			# If character is moving right, adjust character's
			#   right edge to the left edge of the game surface
			if self.deltaX > 0:
				self.rect.right = surface.rect.left
			# Otherwise, adjust character's left edge to the
			#   right edge of the game surface
			elif self.deltaX < 0:
				self.rect.left = surface.rect.right
		
		# Apply deltaY
		self.rect.y += self.deltaY
		
		# Check for collisions with surfaces (y-axis)
		surface_col_list = pyg.sprite.spritecollide(self, self.stage.surface_list, False)
		for surface in surface_col_list:
			# If character is falling, land on the top of the platform
			if self.deltaY > 0:
				self.rect.bottom = surface.rect.top
				self.land()
			# If character is rising, bump their head on the bottom of
			#   the platform
			if self.deltaY < 0:
				self.rect.top = surface.rect.bottom
				self.stop_rising()
				
		# If character is rising, display jumping animation
		if self.deltaY < 0:
			if self.direction == "R":
				self.image = self.jumping_frames_R[0]
			else:
				self.image = self.jumping_frames_L[0]
				
		# If character is falling, display falling animation
		if self.deltaY > 0:
			if self.direction == "R":
				if self.deltaY < 1.6:
					self.image = self.jumping_frames_R[1]
				elif self.deltaY < 3.3:
					self.image = self.jumping_frames_R[2]
				else:
					self.image = self.jumping_frames_R[3]
			else:
				if self.deltaY < 1.6:
					self.image = self.jumping_frames_L[1]
				elif self.deltaY < 3.3:
					self.image = self.jumping_frames_L[2]
				else:
					self.image = self.jumping_frames_L[3]
					
		# If not airborne or moving horizontally, display
		#   idle standing animation (currently 1 frame)
		if not self.airborne and self.deltaX == 0:
			if self.direction == "R":
				self.image = self.idle_frames_R[0]
			else:
				self.image = self.idle_frames_L[0]
				
	def air_jump(self):
		"""
		Causes character to jump while airborne
		"""
		if self.airborne and not self.air_jumped:
			self.air_jumped = True
			self.deltaY = self.jump_force
	
	def calc_grav(self):
		"""
		Applies character-specific gravity to the
		player character
		"""
		if self.deltaY == 0:
			self.deltaY = 1
		else:
			self.deltaY += self.gravity_force
		
	def handle_input(self, keys):
		"""
		Handles input by checking keystates to drive
		movement, possibly other stuff as well
		(will revisit in later versions)
		"""
		# (Left held but not right)
		#   Move left
		if keys[pyg.K_LEFT] and not keys[pyg.K_RIGHT]:
			if not self.airborne:
				self.deltaX = -self.movement_speed
			else:
				if not self.direction == "L":
					self.deltaX = -self.air_steer_speed
			if not self.airborne:
				self.direction = "L"
		
		# (Right held but not left)
		#   Move right
		if keys[pyg.K_RIGHT] and not keys[pyg.K_LEFT]:
			if not self.airborne:
				self.deltaX = self.movement_speed
			else:
				if not self.direction == "R":
					self.deltaX = self.air_steer_speed
			if not self.airborne:
				self.direction = "R"
		
		# (Left and right both held)
		#   Resolve to no horizontal movement
		if keys[pyg.K_LEFT] and keys[pyg.K_RIGHT]:
			self.deltaX = 0
			
		# (Neither left nor right held)
		#   Resolve to no horizontal movement (duh)
		if not keys[pyg.K_LEFT] and not keys[pyg.K_RIGHT]:
			self.deltaX = 0
		
		# If there's anything in the input event queue,
		#   we pop the top element and handle what we
		#   find within
		if not self.input_queue.empty():
			event = self.input_queue.get()
			
			if event.type == pyg.KEYDOWN:
				# Up pressed: Character jumps
				if event.key == pyg.K_UP:
					if not self.airborne:
						self.jump()
					else:
						self.air_jump()
			
			elif event.type == pyg.KEYUP:
				# Up released: Stop jumping if released 
				#   fast enough
				if event.key == pyg.K_UP:
					# If up is released within 10f of press,
					#   stop_rising() causes a short jump
					if event.timestamp <= 10:
						self.stop_rising()
						
	def init_frames(self):
		"""
		Load spritesheet as a SpriteSheet object
		and use class methods to slice out individual
		frames
		"""
		sprite_sheet = SpriteSheet("img/nov2015_spritesheet_2.png")
		originX = 0
		originY = 0
		image_width = 120
		image_height = 114
		
		# Initialize right-facing frames
		# (Right idle frames)
		image = sprite_sheet.get_image(originX, originY, image_width, image_height)
		self.idle_frames_R.append(image)
		
		# (Right running frames)
		originX = 240
		for x in range (0,6):
			image = sprite_sheet.get_image(originX, originY, image_width, image_height)
			self.running_frames_R.append(image)
			originX += image_width
		
		# (Right jumping frames)
		for x in range (0,4):
			image = sprite_sheet.get_image(originX, originY, image_width, image_height)
			self.jumping_frames_R.append(image)
			originX += image_width
			
		# Load right-facing images again and flip them to face left
		# (Left idle frames)
		originX = 0
		image = sprite_sheet.get_image(originX, originY, image_width, image_height)
		image = pyg.transform.flip(image, True, False)
		self.idle_frames_L.append(image)
		
		# (Left running frames)
		originX = 240
		for x in range (0,6):
			image = sprite_sheet.get_image(originX, originY, image_width, image_height)
			image = pyg.transform.flip(image, True, False)
			self.running_frames_L.append(image)
			originX += image_width
			
		# (Left jumping frames)
		for x in range (0,4):
			image = sprite_sheet.get_image(originX, originY, image_width, image_height)
			image = pyg.transform.flip(image, True, False)
			self.jumping_frames_L.append(image)
			originX += image_width
			
	def jump(self):
		"""
		Applies jump force to deltaY to make character
		jump into the air
		"""
		# Check 2px below character for a surface to jump 
		#   off of, then readjust rect y
		self.rect.y += 2
		surface_col_list = pyg.sprite.spritecollide(self, self.stage.surface_list, False)
		self.rect.y -= 2
		
		# If a surface is available, apply jump force and 
		#   declare the character airborne
		if len(surface_col_list) > 0:
			self.deltaY = self.jump_force
			self.airborne = True
			#self.movement_speed = self.air_steer_speed
			
		
	def land(self):
		"""
		Readjusts deltaY, movement speed, and
		airborne state flags when character lands
		"""
		self.deltaY = 0
		self.airborne = False
		self.air_jumped = False
		self.movement_speed = self.run_speed
		
		if self.deltaX < 0:
			self.deltaX = -self.movement_speed
			self.direction = "L"
		if self.deltaX > 0:
			self.deltaX = self.movement_speed
			self.direction = "R"
			
	def stop_rising(self):
		"""
		Causes character to stop rising from a jump
		"""
		# deltaY value of -3 chosen to prevent 
		#   unintentional stop_rising() calls
		#   at positive deltaY values, resulting
		#   in an unintentional "fastfall"
		# Value chosen based on the average deltaY at
		#   which stop_rising() was being called 
		#   from a short jump before this restriction
		#   was implemented
		if self.deltaY <= -3:
			self.deltaY += -0.5*self.jump_force