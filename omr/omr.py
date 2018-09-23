import sys, os

sys.path.append('..')

from scan import scan
import cv2
import numpy as np
from imutils.contours import sort_contours

def readAnswerKey():
    try:
        with open('answer_key.txt', 'r') as file:
            dict = {}
            for line in file:
                values = line.split(' ')
                dict[int(values[0])] = int(values[1])
            return dict
    except:
        print('Answer key file incorrectly placed!!! Please place it in omr directory')

# I/O

image_path = input('Enter the image name/path: ')
if 'images' not in image_path:
    image_path = os.path.join('..', 'images', image_path)

try:
    image = cv2.imread(image_path)
except:
    print('Image path incorrect!!! Re-run program with correct path')

original_image = image.copy()
answer_key = readAnswerKey()

# Convert image to top-down view

image = scan(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresholded_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)


(_, contours, _) = cv2.findContours(thresholded_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
bubble_contours = []


for contour in contours:

    (x, y, w, h) = cv2.boundingRect(contour)

    aspect_ratio = float(w) / h

    if w >= 20 and h >= 20 and aspect_ratio >= 0.85 and aspect_ratio <= 1.15:
        bubble_contours.append(contour)

bubble_contours, _ = sort_contours(bubble_contours, method = 'top-to-bottom')

# Number of correct answers
score = 0

no_of_options = int(input('Enter the number of options per question: '))

for i in np.arange(0, len(bubble_contours), no_of_options):

    row_contours, _ = sort_contours(bubble_contours[i : i + no_of_options])

    bubbled = None

    for (j, contour) in enumerate(row_contours):

        mask = np.zeros(thresholded_image.shape, dtype = 'uint8')

        # Draw option's contour
        cv2.drawContours(mask, [contour], -1, 255, -1)

        # Take only one option from the thresholded image
        mask = cv2.bitwise_and(thresholded_image, thresholded_image, mask = mask)

        # Find number of pixels filled/white/marked in option
        no_of_pixels_active = cv2.countNonZero(mask)

        # Store filled bubble's filled area and index
        if bubbled is None or no_of_pixels_active > bubbled[0]:
            bubbled = (no_of_pixels_active, j)

    # Colour red for incorrect answer
    colour = (0, 0, 255)
    if bubbled[1] == answer_key[i // no_of_options]:

        # Colour green for correct answer
        colour = (0, 255, 0)
        score += 1

    cv2.drawContours(image, [row_contours[answer_key[i // no_of_options]]], -1, colour, 2)

percentage = (score / float(len(bubble_contours) / no_of_options)) * 100

cv2.putText(image, "{:.2f}%".format(percentage), (10, 10), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 0), 2)

cv2.imshow('Original', original_image)
cv2.imshow('Sheet', image)
cv2.waitKey(0)
cv2.destroyAllWindows()










