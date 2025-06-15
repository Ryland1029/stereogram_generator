import numpy as np
import colorsys

# convert values to different rgb colors, gives rainbow spectrum
# uses nested loops, very slow
def greyscale_to_rgb(grey_array, sat = 1.0, val = 1.0):

    # 2D greyscale array
    height, width = grey_array.shape

    # 3D array init with RGB dimension
    rgb_array = np.zeros((height,width,3), dtype=np.uint8)

    # iterate through each pixel to
    for y in range (height):
        for x in range (width):

            #convert to range 0-1 expected by next step
            hue = grey_array[y,x] / 255.0

            # convert hue sat val to rgb
            r, g, b = colorsys.hsv_to_rgb(hue, sat, val)

            rgb_array[y,x] = [int(r*255), int(g*255), int(b*255)]

    return rgb_array


# convert greyscale to constant color but changing saturation
def greyscale_to_satscale(grey_array, hue = 0.8, val = 1.0):

    # 2D greyscale array
    height, width = grey_array.shape

    #0-255 to 0-1 scale (float) and invert to make black = full color
    grey_norm = grey_array.astype(np.float32) / 255.0                                          #
    saturation = 1.0 - grey_norm

    # convert saturation to 1D vector by flattening. hue and val will be constant (full_like fills entire array with constant)
    sat_flat = saturation.flatten()
    hue_flat = np.full_like(sat_flat, hue)
    val_flat = np.full_like(sat_flat, val)

    #convert hsv to rgb array of correct shape
    rgb_flat = np.array([colorsys.hsv_to_rgb(hue, sat, val) for hue, sat, val in zip(hue_flat, sat_flat, val_flat)])
    rgb_array = (rgb_flat.reshape((height, width,3))*255).astype(np.uint8)

    return rgb_array

