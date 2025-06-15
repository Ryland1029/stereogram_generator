from PIL import Image
import numpy as np
import maps
import noise
import coloring


# SIRDS = single-image random dot stereogram
def generate_sirds(width=800, height=600, eye_sep=100, depth_scale=0.7, depth_map = None, noise_pattern = None):

    height, width = depth_map.shape

    #creating a pattern that will repeat horizontally with width of pattern = eye_sep for now
    pattern_width = eye_sep

    # define the noise pattern as the one chosen
    pattern = noise_pattern(height, pattern_width)

    #output image, creates numpy array of zeros with height and width of input image
    #blank black canvas to fill with values eventually
    image = np.zeros((height, width), dtype=np.uint8)

    # indexing the image - all rows, all columns up to but not including pattern_width.
    # puts the base pattern to be repeated on L side of image.
    image[:, :pattern_width] = pattern

    #loop through each pixel left to right top to bottom, not including pattern_width that is already written
    for x in range(pattern_width, width):
        for y in range(height):

            #multiplying map by separation to shift pixels to create depth - closer pixel gets larger disparity to appear closer
            disparity = int(depth_map[y,x] * eye_sep)

            # give x coordinate to copy pixel color to new
            src_x = x - eye_sep + disparity

            #copy the pixel color from source to current position
            if 0 <= src_x < width:
                image[y, x] = image[y, src_x]

    # add color to image
    colored_image = coloring.greyscale_to_satscale(image)

    return Image.fromarray(colored_image)

