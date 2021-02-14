from args import args
from PIL import ImageDraw, Image
import numpy as np


image_file = f"./Mazes/{args.Image}.png"

# setup the file

maze_im = Image.open(image_file)
maze_data = np.reshape(maze_im.getdata(), maze_im.size)
qet = maze_im.convert('RGB')
im = ImageDraw.Draw(qet)


#check the image
