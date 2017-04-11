import random
from random import randrange
from configobj import ConfigObj
from PIL import Image

def random_rotation(image):
	"""Returns a randomly rotated (possibly same) copy of an image"""
	return image.rotate(90*randrange(4))

# Read configuration
config = ConfigObj('config')

# The game board
tile_width = int(config['board']['tile_width'])
tile_height = int(config['board']['tile_height'])
board_width = int(config['board']['width'])
board_height = int(config['board']['height'])
board = Image.new(
	mode = 'RGBA', size=(board_width*tile_width,
		board_height*tile_height), color=(0, 0, 0, 0))

# Tiles
tiles = []
for tile in config['tiles'].items():
	sprite = Image.open(tile[1]['sprite'])
	count = int(tile[1]['count'])
	print "Adding", count, tile[0], "to tiles"
	tiles.extend([sprite] * count)
random.shuffle(tiles)

total_slots = board_height*board_width
assert len(tiles) >= total_slots, \
		"Not enough tiles to fill the board. Need " \
		+ str(total_slots - len(tiles)) \
		+ " more."

print "Discarding", len(tiles) - total_slots, "tiles"
for row in xrange(board_height):
	for column in xrange(board_width):
		tile = tiles[row*board_width + column]
		tile = random_rotation(tile)
		board.paste(tile, (row*tile_height, column*tile_width))

board.show()
