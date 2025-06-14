import numpy as np

# depth map of a rectangle (creates numpy array with depth values)
def rectangle_map(width, height, rect_x=300, rect_y=300, rect_width=200, rect_height=100, depth_value=0.7):
    # width, height: size of the output depth map
    # rect_x, rect_y: top-left corner coordinates of rectangle
    # rect_width, rect_height: length and width of rectangle
    # depth_value: depth intensity

    # array with all zeros
    depth_map = np.zeros((height, width), dtype=float)

    # Clamp coordinates to image bounds
    x_start = max(0, rect_x)
    y_start = max(0, rect_y)
    x_end = min(width, rect_x + rect_width)
    y_end = min(height, rect_y + rect_height)

    # Set the rectangle area to depth_value, gets called to tell how much the pixels get shifted during gen (in the for loop)
    depth_map[y_start:y_end, x_start:x_end] = depth_value

    return depth_map

# create horizontal gradient map
def horizontal_gradient_map(width, height):
    depth_map = np.tile(np.linspace(0,0.7,width),(height,1))
    return depth_map

def hori_sine_map(width, height, freq = 10, amp = 0.7, phase = 0.0):

    x = np.linspace(0, 1, width)
    wave = 0.5 * (1 + np.sin(2 * np.pi * freq * x + phase)) * amp
    depth_map = np.tile(wave, (height, 1))

    return depth_map



#has to be bottom
available_maps = {
    "rectangle": rectangle_map,
    "horizontal gradient": horizontal_gradient_map,
    "horizontal sine": hori_sine_map,
}

    # creating random depth map
    #depth_map = np.random.rand(height, width) * depth_scale

    # calling rectangle map from maps.py
    #depth_map = maps.rectangle_map(width, height, 150, 80, 200, 100, depth_value=0.7)

    # horizontal gradient
    #depth_map = maps.horizontal_gradient_map(width, height)

    # horizontal sine wave
    #depth_map = maps.hori_sine_map(width, height, freq=10, amp=0.6)


