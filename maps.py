import numpy as np

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

# create horizontal gradient map
def horizontal_gradient_map(width, height):
    depth_map = np.tile(np.linspace(0,0.7,width),(height,1))
    return depth_map

def hori_sine_map(width, height, freq = 2, amp = 0.5, phase = 0.5):

    x = np.linspace(0, 1, width)
    wave = 0.5 * (1 + np.sin(2 * np.pi * freq * x + phase)) * amp
    depth_map = np.tile(wave, (height, 1))

    return depth_map

#has to be bottom
# map registry
available_maps = {
    "rectangle": rectangle_map,
    "horizontal gradient": horizontal_gradient_map,
    "horizontal sine": hori_sine_map,
}



