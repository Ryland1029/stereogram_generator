from PIL import Image
import numpy as np
import maps

# SIRDS = single-image random dot stereogram
def generate_sirds(width=600, height=400, eye_sep=60, depth_scale=0.33):

    # creating random depth map
    #depth_map = np.random.rand(height, width) * depth_scale

    #calling rectangle map from maps.py
    depth_map = maps.rectangle_map(width, height, 150, 80, 200, 100, depth_value=0.7)

    #creating a pattern that will repeat horizontally with width of pattern = eye_sep for now
    pattern_width = eye_sep
    pattern = np.random.randint(0, 256, (height, pattern_width), dtype=np.uint8)

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

    return Image.fromarray(image)



