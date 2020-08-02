# USAGE
# python example.py --source images/ocean_sunset.jpg --target images/ocean_day.jpg

# import the necessary packages
from color_transfer import color_transfer
import numpy as np
import argparse
import cv2
import os

def show_image(title, image, width = 300):
	# resize the image to have a constant width, just to
	# make displaying the images take up less screen real
	# estate
	r = width / float(image.shape[1])
	dim = (width, int(image.shape[0] * r))
	resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

	# show the resized image
	cv2.imshow(title, resized)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-s", "--source", required = True,
# 	help = "Path to the source image")
ap.add_argument("-t", "--target", required = True,
	help = "Path to the target image")
ap.add_argument("-m", "--mask", required = True,
	help = "Path to the target image")	
ap.add_argument("-c", "--clip", type = str2bool, default = 't',
	help = "Should np.clip scale L*a*b* values before final conversion to BGR? "
		   "Approptiate min-max scaling used if False.")
ap.add_argument("-p", "--preservePaper", type = str2bool, default = 't',
	help = "Should color transfer strictly follow methodology layed out in original paper?")
ap.add_argument("-o", "--output", help = "Path to the output image (optional)")
args = vars(ap.parse_args())

# # load the images
# source = cv2.imread(args["source"])
target = cv2.imread(args["target"])
mask = cv2.imread(args["mask"])

sourcepath = "shades"

for i in os.listdir(sourcepath):
	print(os.path.join(sourcepath,i))
	source = cv2.imread(os.path.join(sourcepath,i))

	# transfer the color distribution from the source image
	# to the target image
	final,transfer,fg = color_transfer(source, target,mask, clip=args["clip"], preserve_paper=args["preservePaper"])

	# check to see if the output image should be saved
	if args["output"] is not None:
		cv2.imwrite(args["output"]+i, final)
		cv2.imwrite("transfer1/"+i,transfer)
		
		cv2.imwrite("fg/"+i,fg)

# # show the images and wait for a key press
# show_image("Source", source)
# show_image("Target", target)
# show_image("Transfer", transfer)
# cv2.waitKey(0)