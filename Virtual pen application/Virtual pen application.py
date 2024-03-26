import cv2
import numpy as np

# Initialize the canvas as a black image
canvas = None
# The [x, y] coordinates of where the pen is
x1, y1 = 0, 0
# The value of the pen thickness
pen_thickness = 5
# Initialize the webcam
cap = cv2.VideoCapture(0)

# This function is needed to initialize the canvas to the same size as the video frame
def initialize_canvas():
    global canvas
    _, frame = cap.read()
    canvas = np.zeros_like(frame)

# The main loop
while True:
    # Read the frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break
    
    # Initialize the canvas
    if canvas is None:
        initialize_canvas()

    # Flip the frame horizontally for a laterally correct mirror image
    frame = cv2.flip(frame, 1)

    # # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # # Define the HSV range for the blue color of the pen
    # lower_blue = np.array([100, 60, 60])
    # upper_blue = np.array([140, 255, 255])
    # # Create a mask for detecting the blue color in the frame
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Adjusted HSV range for grey
    lower_grey = np.array([0, 0, 40])
    upper_grey = np.array([180, 50, 220])

    # Later in the code, when creating the mask
    mask = cv2.inRange(hsv, lower_grey, upper_grey)


    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > 500:
        c = max(contours, key=cv2.contourArea)
        x2, y2, w, h = cv2.boundingRect(c)
        
        # If there was a previous point then draw a line from it to this point
        if x1 != 0 and y1 != 0:
            canvas = cv2.line(canvas, (x1, y1), (x2, y2), [255, 0, 0], pen_thickness)
        
        x1, y1 = x2, y2
    else:
        # If there were no contours detected then make x1,y1 = 0
        x1, y1 = 0, 0

    # Merge the canvas and the frame.
    frame = cv2.add(frame, canvas)
    
    # Optionally, show the mask and canvas for debugging purposes
    # cv2.imshow("mask", mask)
    # cv2.imshow("canvas", canvas)

    cv2.imshow("Virtual Pen", frame)
    
    # If the 'q' key is pressed, quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
