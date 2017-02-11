# Saturday 11th February 2017

from scene import *
import math
import random
import pickle

"""
todo (No order):
	- create joystick*
	- create player moved by joystick (and other physics)*
	- create walls*
	- create idling and walking animations*
	- create attack animations*
	- create health bar
	- create basic enemies
	- create doors~
	- add sound effects
	
* Completed
~ Partially completed
"""

BUTTON_COLOUR = '#000000' # Colour of buttons
BUTTON_ALPHA = 0.2 # Button transparency
JOYSTICK_AREA = 2 # Area where the joystick can spawn, the larger the number, the smaller the area
KNOB_RESTRICTION = 11 # How far the knob can move away from its origin
KNOB_DEADZONE = 20 # Create a deadzone so controls aren't too sensitive
TILE_SIZE = 64 # The size for tiles
MAX_SPEED = 5 # Max speed the player can go

NORTH_ROTATION = 3.14
SOUTH_ROTATION = 0
EAST_ROTATION = 1.57
WEST_ROTATION = -EAST_ROTATION

ANIM_SPEED = 0.2 # Controls animation speed (higher = faster)


## Images
FLOOR = 'assets/floor.png'
WALL_SIDE = 'assets/wall_side.png'
WALL_CORNER = 'assets/wall_corner.png'
DOOR_CLOSED = 'assets/door_closed.png'
DOOR_OPEN = 'assets/door_open.png'

# Idle animations
PLAYER0_RIGHT_IDLE = ['assets/player0_right_idle0.png', 'assets/player0_right_idle1.png', 'assets/player0_right_idle2.png', 'assets/player0_right_idle3.png']
PLAYER0_UP_IDLE = ['assets/player0_up_idle0.png', 'assets/player0_up_idle1.png', 'assets/player0_up_idle2.png', 'assets/player0_up_idle3.png']
PLAYER0_DOWN_IDLE = ['assets/player0_down_idle0.png', 'assets/player0_down_idle1.png', 'assets/player0_down_idle2.png', 'assets/player0_down_idle3.png']

# Moving animations
PLAYER0_RIGHT_MOVE = ['assets/player0_right_move0.png', 'assets/player0_right_move1.png', 'assets/player0_right_move2.png', 'assets/player0_right_move3.png']
PLAYER0_UP_MOVE = ['assets/player0_up_move0.png', 'assets/player0_up_move1.png', 'assets/player0_up_move2.png', 'assets/player0_up_move3.png']
PLAYER0_DOWN_MOVE = ['assets/player0_down_move0.png', 'assets/player0_down_move1.png', 'assets/player0_down_move2.png', 'assets/player0_down_move3.png']

# Attacking animations
PLAYER0_RIGHT_ATTACK = [['assets/player0_right_attack0_var0.png'], ['assets/player0_right_attack0_var1.png']]
PLAYER0_UP_ATTACK = [['assets/player0_up_attack0_var0.png'], ['assets/player0_up_attack0_var1.png']]
PLAYER0_DOWN_ATTACK = [['assets/player0_down_attack0_var0.png'], ['assets/player0_down_attack0_var1.png']]

class DungeonGame (Scene):
	def setup(self):
		
		# Just playing around with pickling, left the code for future reference (saving game, etc.)
		'''
		store = ['Yo wattup', 3, (2, 4)]
		
		with open('dungeon.pickle', 'w') as file:
			pickle.dump(store, file)
		
		with open('dungeon.pickle', 'r') as file:
			store = pickle.load(file)
			print(store[2]) # >>> (2, 4
		'''
		
		# Player physics variables
		self.xVel = 0
		self.yVel = 0
		
		# Joystick origin variables
		self.x = 0
		self.y = 0
		
		# Movement
		self.xMove = 0
		self.yMove = 0
		
		# Animation
		self.animCounter = 0
		self.playerCooldown = 0.0
		self.playerAttackVar = 0.0
		
		# Player direction
		self.playerDirection = "side"
		
		# Decide if the player is attacking
		self.playerAttacking = False
		
		# The joystick isn't being used, so we tell the program to return a false boolean
		self.usingJoystick = False
		
		# Create enviroment
		self.draw_floor()
		self.draw_walls()
		self.draw_doors()
		
		# Create player
		self.player = SpriteNode(PLAYER0_RIGHT_IDLE[0])
		self.player.position = self.size.w / 2, self.size.h / 2
		self.add_child(self.player)
		
		# Create the joystick base and knob
		self.joystickBase = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA, size=(self.size.h / 4, self.size.h / 4))
		self.joystickKnob = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA, size=(self.size.h / (4 * 4), self.size.h / (4 * 4)))
		
		'''
		# Create buttons
		self.buttonA = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA)
		self.buttonA.size = (self.size.h / 12, self.size.h / 12)
		self.buttonA.position = (self.size.w / 1.2, self.size.h / 5)
		self.add_child(self.buttonA)
		'''
	
	def update(self):
		self.player_physics()
		self.player_input()
		self.player_texture()
		
		# If the joystick isn't being used, remove it
		if self.usingJoystick == False:
			self.joystickBase.remove_from_parent()
			self.joystickKnob.remove_from_parent()
			# Reset variables
			self.joystickKnob.position = (0, 0)
			self.x = 0
			self.y = 0
			
		# Reset player cooldown
		if self.playerCooldown > 0:
			self.playerAttacking = True
			self.playerCooldown -= 1
			
	def touch_began(self, touch):
		x, y = touch.location
			
		""" Add joytick """
		# Check if the user is touching within the bottom-left quadrant..
		if x < self.size.w / JOYSTICK_AREA and y < self.size.h / JOYSTICK_AREA:
			# Create a new variable to use the quadrant value
			self.x, self.y = x, y
			''' Create the joystick at the new position '''
			self.joystickBase.position = (self.x, self.y)
			self.add_child(self.joystickBase)
			self.joystickKnob.position = (self.x, self.y)
			self.add_child(self.joystickKnob)
			
			# Tell the program the joystick is being used
			self.usingJoystick = True
		
		# If a touch is detected elsewhere and self.playerCooldown <= 0 a player must be attacking
		elif self.playerCooldown <= 0:
			self.playerCooldown = 5
			self.playerAttackVar += 1
			
			if self.playerAttackVar > len(PLAYER0_RIGHT_ATTACK) - 1:
				self.playerAttackVar = 0
	
	def touch_moved(self, touch):
		x, y = touch.location
		
		""" Move joystick knob """
		# If the touched location is inside the bottom-left quadrant...
		if x < self.size.w / JOYSTICK_AREA and y < self.size.h / JOYSTICK_AREA:
			xMoved, yMoved = x, y # Only allows certain coordinates to pass
			
			''' if the touch has moved past the right side joystick base limit... '''
			if xMoved > self.x + self.size.h / KNOB_RESTRICTION:
				# Set the knob's x-coordinate to the right side joystick base limit
				knobX = self.x + self.size.h / KNOB_RESTRICTION
				''' else if the touch has moved past the left side joystick base limit... '''
			elif xMoved < self.x - self.size.h / KNOB_RESTRICTION:
				# Set the knob's x-coordinate to the left side joystick base limit
				knobX = self.x - self.size.h / KNOB_RESTRICTION
				''' else keep it where it is (which is inside the horizontal joystick base limits) '''
			else:
				knobX = xMoved
			
			''' if the touch has moved past the top joystick base limit... '''
			if yMoved > self.y + self.size.h / KNOB_RESTRICTION:
				# Set the knob's y-coordinate to the top joystick base limit
				knobY = self.y + self.size.h / KNOB_RESTRICTION
				''' if the touch has moved past the bottom joystick base limit... '''
			elif yMoved < self.y - self.size.h / KNOB_RESTRICTION:
				# Set the knob's y-coordinate to the bottom joystick base limit
				knobY = self.y - self.size.h / KNOB_RESTRICTION
				''' else keep it where it is (which is inside the vertical joystick base limits) '''
			else:
				knobY = yMoved
			
			# Set the joystick position to the previous calculations
			self.joystickKnob.position = (knobX, knobY)
				
	def touch_ended(self, touch):
		x, y = touch.location
		
		# If the player stops touching inside the left half of the screen, tell the program the joystick isn't being used
		# Used to later remove the joystick in 'remove_joystick(self)''
		if x < self.size.w / JOYSTICK_AREA and y < self.size.h:
			self.usingJoystick = False
			
	def draw_floor(self):
		# Create an empty Node to contain floor SpriteNodes
		self.floors = Node(parent=self)
		# Place floor
		for x in range(int(self.size.w / TILE_SIZE)):
			for y in range(int(self.size.h / TILE_SIZE)):
				floor = SpriteNode(texture=FLOOR, position=(x * TILE_SIZE + TILE_SIZE / 2, y * TILE_SIZE + TILE_SIZE / 2))
				self.floors.add_child(floor)
				y += 1
			x += 1
	
	def draw_walls(self):
		''' North wall '''
		# Create an empty Node to contain north wall SpriteNodes
		self.wallNorth = Node(parent=self)
		self.wallsNorth = []
		# Place north outer walls
		for x in range(int(self.size.w / TILE_SIZE)):
			wallSide = SpriteNode(texture=(WALL_SIDE))
			wallSide.rotation = NORTH_ROTATION
			wallSide.position = (TILE_SIZE * (x + 0.5), self.size.h - TILE_SIZE / 2)
			self.wallNorth.add_child(wallSide)
			self.wallsNorth.append(wallSide)
			x += 1
		
		''' South wall '''
		# Create an empty Node to contain south wall SpriteNodes
		self.wallSouth = Node(parent=self)
		# Place south walls
		for x in range(int(self.size.w / TILE_SIZE)):
			wallSide = SpriteNode(texture=(WALL_SIDE))
			wallSide.position = (TILE_SIZE * (x + 0.5), TILE_SIZE / 2)
			self.wallSouth.add_child(wallSide)
			x += 1
		
		''' East wall '''
		# Create an empty Node to contain east wall SpriteNodes
		self.wallEast = Node(parent=self)
		# Place east walls
		for y in range(int(self.size.h / TILE_SIZE)):
			wallSide = SpriteNode(texture=(WALL_SIDE))
			wallSide.rotation = EAST_ROTATION
			wallSide.position = (self.size.w - TILE_SIZE / 2, TILE_SIZE * (y + 0.5))
			self.wallEast.add_child(wallSide)
			y += 1
		
		''' West wall '''
		# Create an empty Node to contain west wall SpriteNodes
		self.wallWest = Node(parent=self)
		# Place west walls
		for y in range(int(self.size.h / TILE_SIZE)):
			wallSide = SpriteNode(texture=(WALL_SIDE))
			wallSide.rotation = WEST_ROTATION
			wallSide.position = (TILE_SIZE / 2, TILE_SIZE * (y + 0.5))
			self.wallWest.add_child(wallSide)
			y += 1
			
		''' Corner walls '''
		# Create an empty Node to contain corner wall SpriteNodes
		self.wallCorners = Node(parent=self)
		
		# Bottom-left corner
		wallCorner = SpriteNode(texture=WALL_CORNER)
		wallCorner.position = (TILE_SIZE / 2, TILE_SIZE / 2)
		self.wallCorners.add_child(wallCorner)
		
		# Bottom-right corner
		wallCorner = SpriteNode(texture=WALL_CORNER)
		wallCorner.position = (self.size.w - TILE_SIZE / 2, TILE_SIZE / 2)
		wallCorner.rotation = EAST_ROTATION
		self.wallCorners.add_child(wallCorner)
		
		# Top-left corner
		wallCorner = SpriteNode(texture=WALL_CORNER)
		wallCorner.position = (TILE_SIZE / 2, self.size.h - TILE_SIZE / 2)
		wallCorner.rotation = EAST_ROTATION
		self.wallCorners.add_child(wallCorner)
		
		# Top-right corner
		wallCorner = SpriteNode(texture=WALL_CORNER)
		wallCorner.position = (self.size.w - TILE_SIZE / 2, self.size.h - TILE_SIZE / 2)
		self.wallCorners.add_child(wallCorner)
	
	def draw_doors(self):
		self.doors = Node(parent=self)
		
		''' North doors '''
		# Left north door
		self.doorNorth1 = SpriteNode(texture=DOOR_CLOSED)
		self.doorNorth1.position = (TILE_SIZE * 7.5, self.size.h - TILE_SIZE / 2)
		self.doorNorth1.rotation = NORTH_ROTATION
		self.doorNorth1.x_scale = -1
		self.doors.add_child(self.doorNorth1)
		
		# Right north door
		self.doorNorth2 = SpriteNode(texture=DOOR_CLOSED)
		self.doorNorth2.position = (TILE_SIZE * 8.5, self.size.h - TILE_SIZE / 2)
		self.doorNorth2.rotation = NORTH_ROTATION
		self.doors.add_child(self.doorNorth2)
		
		''' South doors '''
		# Left south door
		self.doorSouth1 = SpriteNode(texture=DOOR_CLOSED)
		self.doorSouth1.position = (TILE_SIZE * (7.5), TILE_SIZE / 2)
		self.doors.add_child(self.doorSouth1)
		
		# Right south door
		self.doorSouth2 = SpriteNode(texture=DOOR_CLOSED)
		self.doorSouth2.position = (TILE_SIZE * (8.5), TILE_SIZE / 2)
		self.doorSouth2.x_scale = -1
		self.doors.add_child(self.doorSouth2)
		
		''' East doors '''
		# Left east door
		self.doorEast1 = SpriteNode(texture=DOOR_CLOSED)
		self.doorEast1.position = (self.size.w - TILE_SIZE / 2, TILE_SIZE * 5.5)
		self.doorEast1.rotation = EAST_ROTATION
		self.doors.add_child(self.doorEast1)
		
		# Right east door
		self.doorEast2 = SpriteNode(texture=DOOR_CLOSED)
		self.doorEast2.position = (self.size.w - TILE_SIZE / 2, TILE_SIZE * 6.5)
		self.doorEast2.rotation = EAST_ROTATION
		self.doorEast2.x_scale = -1
		self.doors.add_child(self.doorEast2)
		
		''' West doors '''
		# Left west door
		self.doorWest1 = SpriteNode(texture=DOOR_CLOSED)
		self.doorWest1.position = (TILE_SIZE / 2, TILE_SIZE * 5.5)
		self.doorWest1.rotation = WEST_ROTATION
		self.doorWest1.x_scale = -1
		self.doors.add_child(self.doorWest1)
		
		# Right west door
		self.doorWest2 = SpriteNode(texture=DOOR_CLOSED)
		self.doorWest2.position = (TILE_SIZE / 2, TILE_SIZE * 6.5)
		self.doorWest2.rotation = WEST_ROTATION
		self.doors.add_child(self.doorWest2)
		
	def player_physics(self):
		# Player pos
		self.player.position = (self.player.position.x + self.xVel, self.player.position.y + self.yVel)
		# Hitbox pos
		self.playerHitbox = Rect(self.player.position.x - self.player.size.w / 2, self.player.position.y - self.player.size.h / 2, TILE_SIZE, TILE_SIZE/2)
		
		
		# Set x movement limit	
		if self.xVel > MAX_SPEED:
			self.xVel = MAX_SPEED - self.playerCooldown
		
		elif self.xVel < -MAX_SPEED:
			self.xVel = -MAX_SPEED + self.playerCooldown
		
		
		# Set y movement limit
		if self.yVel > MAX_SPEED:
			self.yVel = MAX_SPEED - self.playerCooldown
		
		elif self.yVel < -MAX_SPEED:
			self.yVel = -MAX_SPEED + self.playerCooldown
			
		
		# Prevent speed boost from diagonal movement using Pythagoras' Theorem
		if abs(self.xMove) == abs(self.yMove):
			self.xVel += (math.sqrt(self.xMove**2 + self.yMove**2) / 2) * self.xMove
			self.yVel += (math.sqrt(self.xMove**2 + self.yMove**2) / 2) * self.yMove
		
		else:
			self.xVel += self.xMove
			self.yVel += self.yMove
			
		
		# Friction
		if self.playerHitbox.intersects(self.floors.bbox):
			self.xVel -= 0.1 * self.xVel
			self.yVel -= 0.1 * self.yVel
			
		
		# Set velocity to zero when going slow enough
		if self.xVel < 0.1 and self.xVel > -0.1:
			self.xVel = 0
		
		if self.yVel < 0.1 and self.yVel > -0.1:
			self.yVel = 0
			
		
		# Collision for north wall
		if self.playerHitbox.y + self.playerHitbox.h > self.size.h - TILE_SIZE:
			
			if self.playerHitbox.x < 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.yVel = 0
			
			if self.playerHitbox.x > 8.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.yVel = 0
			
			if self.playerHitbox.x < 7 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.xVel = 0
			
			if self.playerHitbox.x > 8 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.xVel = 0
			
			
		# Collision for south wall
		if self.playerHitbox.y < TILE_SIZE:
			
			if self.playerHitbox.x < 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.yVel = 0
			
			if self.playerHitbox.x > 8.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.yVel = 0
			
			if self.playerHitbox.x < 7 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.xVel = 0
			
			if self.playerHitbox.x > 8 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.xVel = 0
		
		
		# Collision for east wall
		if self.playerHitbox.x + self.playerHitbox.w > self.size.w - TILE_SIZE:
			
			if self.playerHitbox.y < 4.5 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.xVel = 0
			
			if self.playerHitbox.y > 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.xVel = 0
			
			if self.playerHitbox.y < 5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.yVel = 0
			
			if self.playerHitbox.y > 6 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.yVel = 0
		
		
		# Collision for west wall
		if self.playerHitbox.x < TILE_SIZE:
			
			if self.playerHitbox.y < 4.5 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.xVel = 0
			
			if self.playerHitbox.y > 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.xVel = 0
			
			if self.playerHitbox.y < 5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.yVel = 0
			
			if self.playerHitbox.y > 6 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.yVel = 0
	
	def player_input(self):
		# Calculates the distance from the area touched and the origin (self.joystickKnob.position.*)
		xDifference = int(self.joystickKnob.position.x - self.x)
		yDifference = int(self.joystickKnob.position.y - self.y)
		
		# Move player left and right if the knob is outside the deadzone
		# The deadzone allows the player to stop moving even if they aren't exactly at origin
		if xDifference > KNOB_DEADZONE:
			self.xMove = 1
		elif xDifference < -KNOB_DEADZONE:
			self.xMove = -1
		else:
			self.xMove = 0
		
		# Move up and down if the knob is outside the deadzone
		if yDifference > KNOB_DEADZONE:
			self.yMove = 1
		elif yDifference < -KNOB_DEADZONE:
			self.yMove = -1
		else:
			self.yMove = 0
		
	def player_texture(self):
		# Flip image when going left and right
		if self.xVel > 0:
			self.player.x_scale = 1
		elif self.xVel < 0:
			self.player.x_scale = -1
		
		# Determine the direction of the player		
		if abs(self.xVel) > abs(self.yVel):
			self.playerDirection = "side"
		elif self.yVel > 0:
			self.playerDirection = "up"
		elif  self.yVel < 0:
			self.playerDirection = "down"
		
		''' Attacking animation '''
		if self.playerAttacking == True:
			
			# Play attack animation for appropriate direction
			
			if self.playerDirection == "side":
					
				if self.animCounter < len(PLAYER0_RIGHT_ATTACK[int(self.playerAttackVar)]):
					self.player.texture = Texture(PLAYER0_RIGHT_ATTACK[int(self.playerAttackVar)][int(self.animCounter)])
					self.animCounter += ANIM_SPEED
			
			elif self.playerDirection == "up":
				
				if self.animCounter < len(PLAYER0_UP_ATTACK[int(self.playerAttackVar)]):
					self.player.texture = Texture(PLAYER0_UP_ATTACK[int(self.playerAttackVar)][int(self.animCounter)])
					self.animCounter += ANIM_SPEED
			
			elif self.playerDirection == "down":
				
				if self.animCounter < len(PLAYER0_DOWN_ATTACK[int(self.playerAttackVar)]):
					self.player.texture = Texture(PLAYER0_DOWN_ATTACK[int(self.playerAttackVar)][int(self.animCounter)])
					self.animCounter += ANIM_SPEED
			
			# ... else reset the variables		
			if self.animCounter >= len(PLAYER0_RIGHT_ATTACK[int(self.playerAttackVar)]):
				self.playerAttacking = False
				self.animCounter = -1
		
		''' Player idle animation '''
		if self.playerAttacking == False:
			
			# If the animCounter is too big for PLAYER0_UP_IDLE, reset animCounter
			if self.animCounter >= len(PLAYER0_UP_IDLE):
					self.animCounter = 0
			
			if self.xVel == 0 and self.yVel == 0:
				
				if self.playerDirection == "up":
					
					if self.animCounter < len(PLAYER0_UP_IDLE):
						self.player.texture = Texture(PLAYER0_UP_IDLE[int(self.animCounter)])
						self.animCounter += ANIM_SPEED
				
				elif self.playerDirection == "down":
					
					if self.animCounter < len(PLAYER0_DOWN_IDLE):
						self.player.texture = Texture(PLAYER0_DOWN_IDLE[int(self.animCounter)])
						self.animCounter += ANIM_SPEED
				
				elif self.playerDirection == "side":
					
					if self.animCounter < len(PLAYER0_RIGHT_IDLE):
						self.player.texture = Texture(PLAYER0_RIGHT_IDLE[int(self.animCounter)])
						self.animCounter += ANIM_SPEED
						
			''' Player movement animation '''
			if self.playerDirection == "side" and self.xVel != 0:
				
				if self.animCounter < len(PLAYER0_RIGHT_MOVE):
					self.player.texture = Texture(PLAYER0_RIGHT_MOVE[int(self.animCounter)])
					self.animCounter += ANIM_SPEED
			
			elif self.playerDirection == "up" and self.yVel != 0:
				
				if self.animCounter < len(PLAYER0_UP_MOVE):
					self.player.texture = Texture(PLAYER0_UP_MOVE[int(self.animCounter)])
					self.animCounter += ANIM_SPEED
			
			elif self.playerDirection == "down" and self.yVel != 0:
				
				if self.animCounter < len(PLAYER0_DOWN_MOVE):
					self.player.texture = Texture(PLAYER0_DOWN_MOVE[int(self.animCounter)])
					self.animCounter += ANIM_SPEED

if __name__ == '__main__':
	run(DungeonGame(), show_fps=True, orientation=LANDSCAPE)
