# Friday 2nd December 2016

from scene import *
import math
import pickle

"""
todo (No order):
	- create joystick*
	- create player moved by joystick (and other physics)*
	- create walls*
	- create idling and walking animations*
	- create attack animations~
	- create health bar
	- create basic enemies
	- create doors~
* Completed
~ Partially completed
"""

BUTTON_COLOUR = '#000000'
BUTTON_ALPHA = 0.2
JOYSTICK_AREA = 2 # Area where the joystick can spawn, the larger the number, the smaller the area
KNOB_RESTRICTION = 11 # How far the knob can move away from its origin
KNOB_DEADZONE = 20 # Create a deadzone so controls aren't too sensitive
TILE_SIZE = 64 # The size for tiles
MAX_SPEED = 5 # Max speed the player can go

ANIM_SPEED = 0.2 # Controls animation speed (higher = faster)

## Images
FLOOR = 'assets/floor.png'
WALL_SIDE = 'assets/wall_side.png'
WALL_CORNER = 'assets/wall_corner.png'

# Idle animations
PLAYER0_RIGHT_IDLE = ['assets/player0_right_idle0.png', 'assets/player0_right_idle1.png', 'assets/player0_right_idle2.png', 'assets/player0_right_idle3.png']
PLAYER0_UP_IDLE = ['assets/player0_up_idle0.png', 'assets/player0_up_idle1.png', 'assets/player0_up_idle2.png', 'assets/player0_up_idle3.png']
PLAYER0_DOWN_IDLE = ['assets/player0_down_idle0.png', 'assets/player0_down_idle1.png', 'assets/player0_down_idle2.png', 'assets/player0_down_idle3.png']

# Moving animations
PLAYER0_RIGHT_MOVE = ['assets/player0_right_move0.png', 'assets/player0_right_move1.png', 'assets/player0_right_move2.png', 'assets/player0_right_move3.png']
PLAYER0_UP_MOVE = ['assets/player0_up_move0.png', 'assets/player0_up_move1.png', 'assets/player0_up_move2.png', 'assets/player0_up_move3.png']
PLAYER0_DOWN_MOVE = ['assets/player0_down_move0.png', 'assets/player0_down_move1.png', 'assets/player0_down_move2.png', 'assets/player0_down_move3.png']

# Attacking animations
PLAYER0_RIGHT_ATTACK_VAR0 = ['assets/player0_right_attack0_var0.png']
PLAYER0_RIGHT_ATTACK_VAR1 = ['assets/player0_right_attack0_var1.png']
PLAYER0_UP_ATTACK_VAR0 = ['assets/player0_up_attack0_var0.png']
PLAYER0_UP_ATTACK_VAR1 = ['assets/player0_up_attack0_var1.png']
PLAYER0_DOWN_ATTACK_VAR0 = ['assets/player0_down_attack0_var0.png']
PLAYER0_DOWN_ATTACK_VAR1 = ['assets/player0_down_attack0_var1.png']

class DungeonGame (Scene):
	def setup(self):
		
		'''
		Just played around with pickling, left the code for future reference (saving files, etc.)
		
		store = ['Yo wattup', 3, (2, 4)]
		
		with open('dungeon.pickle', 'w') as file:
			pickle.dump(store, file)
		
		with open('dungeon.pickle', 'r') as file:
			asd = pickle.load(file)
			print(asd[2]) <<<--- This will print (2, 4)
		'''
		
		# Player physics variables
		self.x_vel = 0
		self.y_vel = 0
		# Joystick origin variables
		self.x = 0
		self.y = 0
		# Movement
		self.x_move = 0
		self.y_move = 0
		# Animation
		self.anim_counter = 0
		
		# Player direction
		self.player_direction = "side"
		
		# Decide if the player is attacking
		self.player_attacking = False
		# The joystick isn't being used, so we tell the program to return a false boolean
		self.using_joystick = False
		
		# Create background
		self.setup_floor()
		self.setup_walls()
		
		# Create player
		self.player = SpriteNode(PLAYER0_RIGHT_IDLE[0])
		self.player.position = self.size.w / 2, self.size.h / 2
		self.add_child(self.player)
		
		# Shows the player's hitbox outline
		self.player_hitbox_test = SpriteNode(texture=('assets/outline.png'), anchor_point=(0,0), size=(TILE_SIZE, TILE_SIZE/2))
		self.add_child(self.player_hitbox_test)
		
		# Create the joystick base and knob
		self.joystickbase = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA, size=(self.size.h / 4, self.size.h / 4))
		self.joystickknob = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA, size=(self.size.h / (4 * 4), self.size.h / (4 * 4)))
		
		'''
		# Create buttons
		self.button_a = SpriteNode(color=BUTTON_COLOUR, alpha=BUTTON_ALPHA)
		self.button_a.size = (self.size.h / 12, self.size.h / 12)
		self.button_a.position = (self.size.w / 1.2, self.size.h / 5)
		self.add_child(self.button_a)
		'''
	
	def update(self):
		self.player_physics()
		self.player_input()
		self.player_texture()
		
		# Updates player hitbox outline
		self.player_hitbox_test.position = (self.player_hitbox.x,self.player_hitbox.y)
		
		# If the joystick isn't being used, remove it
		if self.using_joystick == False:
			self.joystickbase.remove_from_parent()
			self.joystickknob.remove_from_parent()
			# Reset variables
			self.joystickknob.position = (0, 0)
			self.x = 0
			self.y = 0
	
	def touch_began(self, touch):
		x, y = touch.location
			
		""" Add joytick """
		# Check if the user is touching within the bottom-left quadrant..
		if x < self.size.w / JOYSTICK_AREA and y < self.size.h / JOYSTICK_AREA:
			# Create a new variable to use the quadrant value
			self.x, self.y = x, y
			''' Create the joystick at the new position '''
			self.joystickbase.position = (self.x, self.y)
			self.add_child(self.joystickbase)
			self.joystickknob.position = (self.x, self.y)
			self.add_child(self.joystickknob)
			
			# Tell the program the joystick is being used
			self.using_joystick = True
		else:
			# Player attack animation
			self.player_attacking = True
	
	def touch_moved(self, touch):
		x, y = touch.location
		
		""" Move joystick knob """
		# If the touched location is inside the bottom-left quadrant...
		if x < self.size.w / JOYSTICK_AREA and y < self.size.h / JOYSTICK_AREA:
			x_moved, y_moved = x, y # Only allows certain coordinates to pass
			
			''' if the touch has moved past the right side joystick base limit... '''
			if x_moved > self.x + self.size.h / KNOB_RESTRICTION:
				# Set the knob's x-coordinate to the right side joystick base limit
				knob_x = self.x + self.size.h / KNOB_RESTRICTION
				''' else if the touch has moved past the left side joystick base limit... '''
			elif x_moved < self.x - self.size.h / KNOB_RESTRICTION:
				# Set the knob's x-coordinate to the left side joystick base limit
				knob_x = self.x - self.size.h / KNOB_RESTRICTION
				''' else keep it where it is (which is inside the horizontal joystick base limits) '''
			else:
				knob_x = x_moved
			
			''' if the touch has moved past the top joystick base limit... '''
			if y_moved > self.y + self.size.h / KNOB_RESTRICTION:
				# Set the knob's y-coordinate to the top joystick base limit
				knob_y = self.y + self.size.h / KNOB_RESTRICTION
				''' if the touch has moved past the bottom joystick base limit... '''
			elif y_moved < self.y - self.size.h / KNOB_RESTRICTION:
				# Set the knob's y-coordinate to the bottom joystick base limit
				knob_y = self.y - self.size.h / KNOB_RESTRICTION
				''' else keep it where it is (which is inside the vertical joystick base limits) '''
			else:
				knob_y = y_moved
			
			# Set the joystick position to the previous calculations
			self.joystickknob.position = (knob_x, knob_y)
				
	def touch_ended(self, touch):
		x, y = touch.location
		
		# If the player stops touching inside the left half of the screen, tell the program the joystick isn't being used
		# Used to later remove the joystick in 'remove_joystick(self)''
		if x < self.size.w / JOYSTICK_AREA and y < self.size.h:
			self.using_joystick = False
		else:
			self.player_attacking = False
			
	def setup_floor(self):
		# Create an empty Node to contain floor SpriteNodes
		self.floors = Node(parent=self)
		# Place floor
		for x in range(int(self.size.w / TILE_SIZE)):
			for y in range(int(self.size.h / TILE_SIZE)):
				floor = SpriteNode(texture=FLOOR, position=(x*TILE_SIZE+TILE_SIZE/2,y*TILE_SIZE+TILE_SIZE/2))
				self.floors.add_child(floor)
				y += 1
			x += 1
	
	def setup_walls(self):
		''' North wall '''
		# Create an empty Node to contain north wall SpriteNodes
		self.wall_north = Node(parent=self)
		self.walls_north = []
		# Place north outer walls
		for x in range(int(self.size.w / TILE_SIZE)):
			wall_side = SpriteNode(texture=(WALL_SIDE))
			wall_side.rotation = 3.14
			wall_side.position = (TILE_SIZE * (x + 0.5), self.size.h - TILE_SIZE / 2)
			self.wall_north.add_child(wall_side)
			self.walls_north.append(wall_side)
			x += 1
		
		''' South wall '''
		# Create an empty Node to contain south wall SpriteNodes
		self.wall_south = Node(parent=self)
		# Place south walls
		for x in range(int(self.size.w / TILE_SIZE)):
			wall_side = SpriteNode(texture=(WALL_SIDE))
			wall_side.position = (TILE_SIZE * (x + 0.5), TILE_SIZE / 2)
			self.wall_south.add_child(wall_side)
			x += 1
		
		''' East wall '''
		# Create an empty Node to contain east wall SpriteNodes
		self.wall_east = Node(parent=self)
		# Place east walls
		for y in range(int(self.size.h / TILE_SIZE)):
			wall_side = SpriteNode(texture=(WALL_SIDE))
			wall_side.rotation = 1.57
			wall_side.position = (self.size.w - TILE_SIZE / 2, TILE_SIZE * (y + 0.5))
			self.wall_east.add_child(wall_side)
			y += 1
		
		''' West wall '''
		# Create an empty Node to contain west wall SpriteNodes
		self.wall_west = Node(parent=self)
		# Place west walls
		for y in range(int(self.size.h / TILE_SIZE)):
			wall_side = SpriteNode(texture=(WALL_SIDE))
			wall_side.rotation = -1.57
			wall_side.position = (TILE_SIZE / 2, TILE_SIZE * (y + 0.5))
			self.wall_west.add_child(wall_side)
			y += 1
			
		''' Corner walls '''
		# Create an empty Node to contain corner wall SpriteNodes
		self.wall_corners = Node(parent=self)
		
		# Bottom-left corner
		wall_corner = SpriteNode(texture=WALL_CORNER)
		wall_corner.position = (TILE_SIZE / 2, TILE_SIZE / 2)
		self.wall_corners.add_child(wall_corner)
		
		# Bottom-right corner
		wall_corner = SpriteNode(texture=WALL_CORNER)
		wall_corner.position = (self.size.w - TILE_SIZE / 2, TILE_SIZE / 2)
		wall_corner.rotation = 1.57
		self.wall_corners.add_child(wall_corner)
		
		# Top-left corner
		wall_corner = SpriteNode(texture=WALL_CORNER)
		wall_corner.position = (TILE_SIZE / 2, self.size.h - TILE_SIZE / 2)
		wall_corner.rotation = 1.57
		self.wall_corners.add_child(wall_corner)
		
		# Top-right corner
		wall_corner = SpriteNode(texture=WALL_CORNER)
		wall_corner.position = (self.size.w - TILE_SIZE / 2, self.size.h - TILE_SIZE / 2)
		self.wall_corners.add_child(wall_corner)
		
	def player_physics(self):
		self.player.position = (self.player.position.x + self.x_vel, self.player.position.y + self.y_vel)
		self.player_hitbox = Rect(self.player.position.x - self.player.size.w / 2, self.player.position.y - self.player.size.h / 2, TILE_SIZE, TILE_SIZE/2)
		
		# Set x movement limit	
		if self.x_vel > MAX_SPEED:
			self.x_vel = MAX_SPEED
		elif self.x_vel < -MAX_SPEED:
			self.x_vel = -MAX_SPEED
		
		# Set y movement limit
		if self.y_vel > MAX_SPEED:
			self.y_vel = MAX_SPEED
		elif self.y_vel < -MAX_SPEED:
			self.y_vel = -MAX_SPEED
		
		# Prevent speed boost from diagonal movement
		if abs(self.x_move) == abs(self.y_move):
			self.x_vel += (math.sqrt(self.x_move**2 + self.y_move**2) / 2) * self.x_move
			self.y_vel += (math.sqrt(self.x_move**2 + self.y_move**2) / 2) * self.y_move
		else:
			self.x_vel += self.x_move
			self.y_vel += self.y_move
		
		# Friction
		if self.player_hitbox.intersects(self.floors.bbox):
			self.x_vel -= 0.1 * self.x_vel
			self.y_vel -= 0.1 * self.y_vel
		
		# Set velocity to zero when going slow enough
		if self.x_vel < 0.1 and self.x_vel > -0.1:
			self.x_vel = 0
		if self.y_vel < 0.1 and self.y_vel > -0.1:
			self.y_vel = 0
		
		# Collision for north wall
		if self.player_hitbox.y + self.player_hitbox.h > self.size.h - TILE_SIZE:
			if self.player_hitbox.x < 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.y_vel = 0
			if self.player_hitbox.x > 8.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.y_vel = 0
			if self.player_hitbox.x < 7 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.x_vel = 0
			if self.player_hitbox.x > 8 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.x_vel = 0
			
			
		# Collision for south wall
		if self.player_hitbox.y < TILE_SIZE:
			if self.player_hitbox.x < 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.y_vel = 0
			if self.player_hitbox.x > 8.5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.y_vel = 0
			if self.player_hitbox.x < 7 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.x_vel = 0
			if self.player_hitbox.x > 8 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.x_vel = 0
		
		# Collision for east wall
		if self.player_hitbox.x + self.player_hitbox.w > self.size.w - TILE_SIZE:
			if self.player_hitbox.y < 4.5 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.x_vel = 0
			if self.player_hitbox.y > 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x - 1, self.player.position.y)
				self.x_vel = 0
			if self.player_hitbox.y < 5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.y_vel = 0
			if self.player_hitbox.y > 6 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.y_vel = 0
		
		# Collision for west wall
		if self.player_hitbox.x < TILE_SIZE:
			if self.player_hitbox.y < 4.5 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.x_vel = 0
			if self.player_hitbox.y > 6.5 * TILE_SIZE:
				self.player.position = (self.player.position.x + 1, self.player.position.y)
				self.x_vel = 0
			if self.player_hitbox.y < 5 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y + 1)
				self.y_vel = 0
			if self.player_hitbox.y > 6 * TILE_SIZE:
				self.player.position = (self.player.position.x, self.player.position.y - 1)
				self.y_vel = 0
	
	def player_input(self):
		x_difference = int(self.joystickknob.position.x - self.x)
		y_difference = int(self.joystickknob.position.y - self.y)
		
		# Move left and right
		if x_difference > KNOB_DEADZONE:
			self.x_move = 1
		elif x_difference < -KNOB_DEADZONE:
			self.x_move = -1
		else:
			self.x_move = 0
		
		# Move up and down
		if y_difference > KNOB_DEADZONE:
			self.y_move = 1
		elif y_difference < -KNOB_DEADZONE:
			self.y_move = -1
		else:
			self.y_move = 0
		
	def player_texture(self):
		# Flip image when going left and right
		if self.x_vel > 0:
			self.player.x_scale = 1
		elif self.x_vel < 0:
			self.player.x_scale = -1
		
		# Determine the direction of the player		
		if abs(self.x_vel) > abs(self.y_vel):
			self.player_direction = "side"
		elif self.y_vel > 0:
			self.player_direction = "up"
		elif  self.y_vel < 0:
			self.player_direction = "down"
		
		# Attacking animation
		if self.player_attacking == True:
			if self.player_direction == "side":
				if self.anim_counter < len(PLAYER0_RIGHT_ATTACK_VAR0):
					self.player.texture = Texture(PLAYER0_RIGHT_ATTACK_VAR0[int(self.anim_counter)])
					self.anim_counter += ANIM_SPEED
				elif self.anim_counter >= len(PLAYER0_RIGHT_ATTACK_VAR0):
					self.anim_counter = 0
			elif self.player_direction == "up":
				if self.anim_counter < len(PLAYER0_UP_ATTACK_VAR0):
					self.player.texture = Texture(PLAYER0_UP_ATTACK_VAR0[int(self.anim_counter)])
					self.anim_counter += ANIM_SPEED
				elif self.anim_counter >= len(PLAYER0_UP_ATTACK_VAR0):
					self.anim_counter = 0
			elif self.player_direction == "down":
				if self.anim_counter < len(PLAYER0_DOWN_ATTACK_VAR0):
					self.player.texture = Texture(PLAYER0_DOWN_ATTACK_VAR0[int(self.anim_counter)])
					self.anim_counter += ANIM_SPEED
				elif self.anim_counter >= len(PLAYER0_DOWN_ATTACK_VAR0):
					self.anim_counter = 0
		
		if self.player_attacking == False:
			# Player idle animation
			if self.x_vel == 0 and self.y_vel == 0:
				if self.player_direction == "up":
					if self.anim_counter < len(PLAYER0_UP_IDLE):
						self.player.texture = Texture(PLAYER0_UP_IDLE[int(self.anim_counter)])
						self.anim_counter += ANIM_SPEED
					elif self.anim_counter >= len(PLAYER0_UP_IDLE):
						self.anim_counter = 0
				elif self.player_direction == "down":
					if self.anim_counter < len(PLAYER0_DOWN_IDLE):
						self.player.texture = Texture(PLAYER0_DOWN_IDLE[int(self.anim_counter)])
						self.anim_counter += ANIM_SPEED
					elif self.anim_counter >= len(PLAYER0_DOWN_IDLE):
						self.anim_counter = 0
				elif self.player_direction == "side":
					if self.anim_counter < len(PLAYER0_RIGHT_IDLE):
						self.player.texture = Texture(PLAYER0_RIGHT_IDLE[int(self.anim_counter)])
						self.anim_counter += ANIM_SPEED
					elif self.anim_counter >= len(PLAYER0_RIGHT_IDLE):
						self.anim_counter = 0
						
			# Player movement animation
			if self.player_direction == "side" and self.x_vel != 0:
				if self.anim_counter < len(PLAYER0_RIGHT_MOVE):
					self.player.texture = Texture(PLAYER0_RIGHT_MOVE[int(self.anim_counter)])
					self.anim_counter += ANIM_SPEED
				elif self.anim_counter >= len(PLAYER0_RIGHT_MOVE):
					self.anim_counter = 0
			elif self.player_direction == "up" and self.y_vel != 0:
				if self.anim_counter < len(PLAYER0_UP_MOVE):
					self.player.texture = Texture(PLAYER0_UP_MOVE[int(self.anim_counter)])
					self.anim_counter += ANIM_SPEED
				elif self.anim_counter >= len(PLAYER0_UP_MOVE):
					self.anim_counter = 0
			elif self.player_direction == "down" and self.y_vel != 0:
				if self.anim_counter < len(PLAYER0_DOWN_MOVE):
					self.player.texture = Texture(PLAYER0_DOWN_MOVE[int(self.anim_counter)])
					self.anim_counter += ANIM_SPEED
				elif self.anim_counter >= len(PLAYER0_DOWN_MOVE):
					self.anim_counter = 0

if __name__ == '__main__':
	run(DungeonGame(), show_fps=True, orientation=LANDSCAPE)
