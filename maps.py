import numpy as np


# def rect_map(width, height):
#
#     # creating open meshgrid that uses 1D vectors to represent each pixel
#     y, x = np.ogrid[:height, :width]
#
#     # midpoint of the shape
#     cx, cy = width // 2, height // 2


def rectangle_map(width, height, rect_x, rect_y, rect_width, rect_height, depth_value=1.0):
    """
    Creates a depth map with a rectangle shape.

    Parameters:
    - width, height: size of the output depth map
    - rect_x, rect_y: top-left corner coordinates of the rectangle
    - rect_width, rect_height: size of the rectangle
    - depth_value: depth intensity inside the rectangle (default 1.0)

    Returns:
    - depth_map: 2D numpy array (height x width) with depth values
    """
    depth_map = np.zeros((height, width), dtype=float)

    # Clamp coordinates to image bounds
    x_start = max(0, rect_x)
    y_start = max(0, rect_y)
    x_end = min(width, rect_x + rect_width)
    y_end = min(height, rect_y + rect_height)

    # Set the rectangle area to depth_value
    depth_map[y_start:y_end, x_start:x_end] = depth_value

    return depth_map