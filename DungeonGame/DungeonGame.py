# Saturday 11th February 2017

from scene import *
from enum import Enum
from enum import IntEnum
import math
import pickle

"""
todo (No order):
	- create joystick*
	- create player moved by joystick (and other physics)*
	- create walls~
	- create idling and walking animations
	- create attack animations*
	- create health bar
	- create basic enemies
	- create doors
	- add sound effects
	
* Completed
~ Partially completed
"""

BUTTON_COLOUR = '#ffffff' # Colour of buttons
BUTTON_ALPHA = 0.2 # Button transparency
JOYSTICK_SIZE = 128
JOYSTICK_AREA = 2 # Area where the joystick can spawn, the larger the number, the smaller the area
KNOB_RESTRICTION = 11 # How far the knob can move away from its origin
KNOB_DEADZONE = 20 # Create a deadzone so controls aren't too sensitive
TILE_SIZE = 32 # The size for tiles
MAX_SPEED = 5 # Max speed the player can go

FLOOR_X = 2
FLOOR_Y = 7
FLOOR_W = 28
FLOOR_H = 15

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

class Tile (Enum):
	TILE_BASE = 0
	TILE_WALL_SIDE = 1

class TileFacing (IntEnum):
	UP = 000
	DOWN = 314
	LEFT = -157
	RIGHT = 157
	
class PlayerFacing (Enum):
	LEFT = 0
	RIGHT = 1
	UP = 2
	DOWN = 3

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
		
		self.floors = []
		self.walls = []
		
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
		
		self.background_color = '#000000'
		
		# Player Facing
		PlayerFacing.RIGHT
		
		# Return true if the player is attacking
		self.playerAttacking = False
		
		# The joystick isn't being used, so we tell the program to return a false boolean
		self.usingJoystick = False
		
		# Create player
		self.player = SpriteNode(PLAYER0_RIGHT_IDLE[0])
		self.player.position = (self.size.w / 2, self.size.h / 2)
		self.add_child(self.player)
		
		# Create the joystick base and knob
		self.joystickBase = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA, size=(JOYSTICK_SIZE, JOYSTICK_SIZE))
		
		self.joystickKnob = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA, size=(JOYSTICK_SIZE / 4, JOYSTICK_SIZE / 4))
		
		self.draw_room()
		
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
			
	def draw_tile(self, Tile, TileFacing, image, x, y):
		if Tile == Tile.TILE_BASE:
			floor = SpriteNode(texture=image, size=(TILE_SIZE, TILE_SIZE), position=(x, y))
			floor.rotation = TileFacing / 100
			self.add_child(floor)
			self.floors.append(floor)
		elif Tile == Tile.TILE_WALL_SIDE:
			wallSide = SpriteNode(texture=image, size=(TILE_SIZE, TILE_SIZE), position=(x, y))
			wallSide.rotation = TileFacing / 100
			self.add_child(wallSide)
			self.walls.append(wallSide)
		else:
			print("Invalid enum")
	
	def draw_room(self):
		# Place floor
		for x in range(FLOOR_W):
			for y in range(FLOOR_H):
				self.draw_tile(Tile.TILE_BASE, TileFacing.UP, FLOOR, (x * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * FLOOR_X, (y * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * FLOOR_Y)
				y += 1
			x += 1
			
		''' Place walls '''
		# Top wall		
		for x in range(FLOOR_W):
			self.draw_tile(Tile.TILE_WALL_SIDE, TileFacing.DOWN, WALL_SIDE, (x * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X), (TILE_SIZE * FLOOR_H + TILE_SIZE / 2) + TILE_SIZE * FLOOR_Y)
		
		# Bottom wall	
		for x in range(FLOOR_W):
			self.draw_tile(Tile.TILE_WALL_SIDE, TileFacing.UP, WALL_SIDE, (x * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X), (-TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * FLOOR_Y)
			
		# Left wall
		for y in range(FLOOR_H):
			self.draw_tile(Tile.TILE_WALL_SIDE, TileFacing.LEFT, WALL_SIDE, (-TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * FLOOR_X, (y * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X + 5))
			
		# Right wall	
		for y in range(FLOOR_H):
			self.draw_tile(Tile.TILE_WALL_SIDE, TileFacing.RIGHT, WALL_SIDE, (TILE_SIZE + (FLOOR_W - 1) * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * FLOOR_X, (y * TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X + 5))
		
		# Top Left Corner Wall
		self.draw_tile(Tile.TILE_BASE, TileFacing.LEFT, WALL_CORNER, (-TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X), TILE_SIZE * (FLOOR_Y + FLOOR_H) + TILE_SIZE / 2)
		
		# Top Right Corner Wall
		self.draw_tile(Tile.TILE_BASE, TileFacing.DOWN, WALL_CORNER, (-TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X + FLOOR_W + 1), TILE_SIZE * (FLOOR_Y + FLOOR_H) + TILE_SIZE / 2)
		
		# Bottom Left Corner Wall
		self.draw_tile(Tile.TILE_BASE, TileFacing.UP, WALL_CORNER, (-TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X), TILE_SIZE * (FLOOR_Y - 1) + TILE_SIZE / 2)
		
		# Bottom Right Corner Wall
		self.draw_tile(Tile.TILE_BASE, TileFacing.RIGHT, WALL_CORNER, (-TILE_SIZE + TILE_SIZE / 2) + TILE_SIZE * (FLOOR_X + FLOOR_W + 1), TILE_SIZE * (FLOOR_Y - 1) + TILE_SIZE / 2)
	
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
			
		
		# Slows player down
		self.xVel -= 0.1 * self.xVel
		self.yVel -= 0.1 * self.yVel
				
		
		# Set velocity to zero when going slow enough
		if self.xVel < 0.1 and self.xVel > -0.1:
			self.xVel = 0
		
		if self.yVel < 0.1 and self.yVel > -0.1:
			self.yVel = 0
		
		
		# Wall collision
		for w in self.walls:
			if self.playerHitbox.intersects(w.bbox):
				
				# Collision on down facing walls
				if w.rotation == TileFacing.DOWN / 100:
					self.move_player(0, -1)
					self.yVel = 0
				
				# Collision on top facing walls
				if w.rotation == TileFacing.UP / 100:
					self.move_player(0, 1)
					self.yVel = 0
				
				# Collision on right facing walls
				if w.rotation == TileFacing.RIGHT / 100:
					self.move_player(-1, 0)
					self.xVel = 0
					
				# Collision on left facing walls
				if w.rotation == TileFacing.LEFT / 100:
					self.move_player(1, 0)
					self.xVel = 0
	
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
		self.player.z_position = self.player.position.y
		
		# Flip image when going left and right
		if self.xVel > 0:
			self.player.x_scale = 1
		elif self.xVel < 0:
			self.player.x_scale = -1
					
	def move_player(self, x, y):
			self.player.position = (self.player.position.x + x, self.player.position.y + y)

if __name__ == '__main__':
	run(DungeonGame(), show_fps=True, orientation=LANDSCAPE)
