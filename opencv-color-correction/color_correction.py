# USAGE
# python color_correction.py --reference reference.jpg --input examples/01.jpg

# import the necessary packages
from imutils.perspective import four_point_transform
from skimage import exposure
import numpy as np
import argparse
import imutils
import cv2
import sys

def find_color_card(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection or contour detection to find the card's contour
    edged = cv2.Canny(gray, 30, 150)  # Adjust parameters as needed
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it's the color card)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)

        # Extract the color card by cropping the region of interest
        x, y, w, h = cv2.boundingRect(max_contour)
        card = image[y:y+h, x:x+w]

        return card

    # If no color card is found, return None
    return None

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-r", "--reference", required=True,
    help="path to the input reference image")
ap.add_argument("-i", "--input", required=True,
    help="path to the input image to apply color correction to")
args = vars(ap.parse_args())

# load the reference image and input images from disk
print("[INFO] loading images...")
ref = cv2.imread(args["reference"])
image = cv2.imread(args["input"])

# resize the reference and input images
ref = imutils.resize(ref, width=600)
image = imutils.resize(image, width=600)

# display the reference and input images to our screen
cv2.imshow("Reference", ref)
cv2.imshow("Input", image)

# find the color matching card in each image
print("[INFO] finding color matching cards...")
refCard = find_color_card(ref)
imageCard = find_color_card(image)

# if the color matching card is not found in either the reference
# image or the input image, gracefully exit
if refCard is None or imageCard is None:
    print("[INFO] could not find color matching card in both images")
    sys.exit(0)

# show the color matching card in the reference image and input image,
# respectively
cv2.imshow("Reference Color Card", refCard)
cv2.imshow("Input Color Card", imageCard)

# apply histogram matching from the color matching card in the
# reference image to the color matching card in the input image
print("[INFO] matching images...")
imageCard = exposure.match_histograms(imageCard, refCard,
    multichannel=True)

# show our input color matching card after histogram matching
cv2.imshow("Input Color Card After Matching", imageCard)
cv2.waitKey(0)
