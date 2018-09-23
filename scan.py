import cv2
from skimage.filters import threshold_local
from transform import four_point_transform
import imutils



def apply_filter(image, block_size = 11, offset = 10, method = 'gaussian'):

    # Apply the 'black and white' effect

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = (image > threshold_local(image, block_size, offset = offset, method = method)). \
                       astype("uint8") * 255
    return image


def scan(image):

    # Decrease height for faster processing

    height_for_conversion = min(1000, image.shape[0])
    conversion_ratio = image.shape[0] / height_for_conversion
    image = imutils.resize(image, height = height_for_conversion)

    # Edge Detection

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 3, 75, 75)  # Tune parameters for better processing
    edged = cv2.Canny(gray, 75, 200)

    # Find contours

    (_, contours, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:min(3, len(contours))]

    flag = 0

    for contour in contours:

        perimeter = cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(polygon) == 4:
            flag = 1
            break

    if flag == 0:
        print("No contour found with 4 points")
        exit(1)

    # Change image perspective

    warped_image = four_point_transform(image, polygon.reshape(4, 2) * conversion_ratio)

    return warped_image

if __name__ == '__main__':
    image = cv2.imread(input('Enter image name/path: '))
    original_image = image.copy()

    warped_image = scan(image)

    warped_image = apply_filter(warped_image)

    cv2.imshow('Original', imutils.resize(original_image, height = 650))
    cv2.imshow('Transformed', imutils.resize(warped_image, height = 650))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
