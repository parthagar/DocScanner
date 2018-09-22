import cv2
import numpy as np

def order_points(points):

    # ordered[] will have coordinates in the order (top-left, top-right, bottom-right, bottom-left)
    ordered = np.zeros((4, 2), dtype = np.float32)

    sum = np.sum(points, axis = 1)
    ordered[0] = points[np.argmin(sum)] # x + y will be very low
    ordered[2] = points[np.argmax(sum)] # x + y will be very high

    diff = np.diff(points, axis = 1)
    ordered[1] = points[np.argmin(diff)] # x - y will be very less or -ve
    ordered[3] = points[np.argmax(diff)] # x - y will be very high

    return ordered

def four_point_transform(image, points):

    ordered = order_points(points)

    tl, tr, br, bl = ordered

    top_width = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    bottom_width = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))

    width = int(np.max([top_width, bottom_width]))

    left_height = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    right_height = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))

    height = int(np.max([left_height, right_height]))

    # Redefining points to store points
    points = np.array([[0, 0],
                       [width - 1, 0],
                       [width - 1, height - 1],
                       [0, height - 1]], dtype = np.float32)
    M = cv2.getPerspectiveTransform(ordered, points)
    warped_image = cv2.warpPerspective(image, M, (width, height))

    return warped_image
