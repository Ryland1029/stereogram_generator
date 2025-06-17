import numpy as np
import matplotlib.pyplot as plt


# depth map of a rectangle (creates numpy array with depth values)
def rectangle_map(width, height, rect_x=200, rect_y=200, rect_width=200, rect_height=200, depth_value=0.15):
    # width, height: size of the output depth map
    # rect_x, rect_y: top-left corner coordinates of rectangle
    # rect_width, rect_height: length and width of rectangle

    # array with all zeros
    depth_map = np.zeros((height, width), dtype=float)

    #set bounds of depth mapping to size and location of the rectangle
    depth_map[rect_x:rect_x + rect_width, rect_y:rect_y + rect_height] = depth_value

    return depth_map

# checkerboard map
def checkerboard_map(width, height, rect_width=100, rect_height=100, depth_value=0.15):
    depth_map = np.zeros((height, width), dtype=float)

    for y in range(0, height, rect_height):
        for x in range(0, width, rect_width):
            if (x//rect_width + y//rect_height) % 2 == 0:
                depth_map[y:y + rect_height, x: x + rect_width] = depth_value

    return depth_map

# create horizontal gradient map
def horizontal_gradient_map(width, height):
    depth_map = np.tile(np.linspace(0,0.7,width),(height,1))
    return depth_map

# create horizontal sine wave map
def hori_sine_map(width, height, freq = 2, amp = 0.3, phase = 0.5):

    x = np.linspace(0, 1, width)
    wave = 0.5 * (1 + np.sin(2 * np.pi * freq * x + phase)) * amp

    depth_map = np.tile(wave, (height, 1))

    return depth_map

def two_sine_map(width, height, freq = 4, amp = 0.3, phase = 0.5):
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)

    wave = wave = (np.sin(x ** 2 + y ** 2)) / (x ** 2 + y ** 2) * amp
    depth_map = np.tile(wave, (height, 1))

    return depth_map

def standing_wave_map(width, height, mode_x=5, mode_y=3, amplitude=0.1):
    x = np.linspace(0, np.pi, width)
    y = np.linspace(0, np.pi, height)
    xv, yv = np.meshgrid(x, y)

    # Standing wave pattern (sin(nπx/L) * sin(mπy/L))
    # depth_map = amplitude * np.sin(mode_x * xv) * np.sin(mode_y * yv)
    depth_map = (amplitude * np.sin(mode_x * xv) * np.sin(mode_y * yv)) + (amplitude * np.sin(mode_x * yv) * np.sin(mode_y * xv))

    # Normalize
    depth_map = 0.5 * (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

    return depth_map

# create tunnel map
def tunnel_map(width, height, depth_value=0.25):

    # 2D array with coordingates y and x for each pixel
    y,x = np.indices((height, width))
    # center of the tunnel
    center_x = width // 2
    center_y = height // 2
    # distance of pixel from center of tunnel in 2 separate dimensions
    dx = x - center_x
    dy = y - center_y

    # Euclidian norm, gives pixel's distance from tunnel center (by calculating hypotenuse b/w center and pixel)
    distance_from_center = np.hypot(dx, dy)

    max_distance = np.hypot(center_x, center_y)
    depth_map = np.exp(distance_from_center/max_distance)
    depth_map*=depth_value

    return depth_map


# map registry (must be below all functions)
available_maps = {
    "rectangle": rectangle_map,
    "checkerboard": checkerboard_map,
    "horizontal gradient": horizontal_gradient_map,
    "horizontal sine": hori_sine_map,
    "standing wave": standing_wave_map,
    "tunnel": tunnel_map,
}



