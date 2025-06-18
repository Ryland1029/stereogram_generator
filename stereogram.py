from PIL import Image
import numpy as np
import maps
import noise
import coloring


# SIRDS = single-image random dot stereogram
def generate_sirds(
        width=800,
        height=600,
        pattern_width=100,
        depth_scale=0.7,
        depth_map=None,
        noise_pattern=None,
        color_option=None,
        hue=None,
        smoothing=False
):

    height, width = depth_map.shape

    # define the noise pattern as the one chosen
    pattern = noise_pattern(height, pattern_width)

    #output image, creates numpy array of zeros with height and width of input image
    #blank black canvas to fill with values eventually
    image = np.zeros((height, width), dtype=np.uint8)

    # indexing the image - all rows, all columns up to but not including pattern_width.
    # puts the base pattern to be repeated on L side of image.
    # (got rid of this to make pattern a reference only, not part of image)
    #image[:, :pattern_width] = pattern

    # normalize to always 0-1 (moved to generate_and_display in gui.py)
    #depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

    assert pattern_width < width

    #loop through each pixel left to right top to bottom
    for x in range(width):
        for y in range(height):

            # multiplying map by separation to shift pixels to create depth - closer pixel gets larger disparity to appear closer
            # also clamps disparity to be between 0 and pattern_width - 1 to prevent wraparound artifact
            disparity = min((depth_map[y,x] * pattern_width), pattern_width - 1)

            if not smoothing:
                disparity = int(disparity)

            # give x coordinate to copy pixel color to new
            src_x = x - pattern_width + disparity

            if not smoothing:
                # copy the pixel color from source to current position, modified so pattern is just a reference
                if src_x < 0:
                    image[y, x] = pattern[y, x % pattern_width]
                elif src_x < width:
                    image[y, x] = image[y, src_x]
            if smoothing:
                image[y, x] = interpolate_pixel(x,y, src_x, image, pattern, pattern_width, width)
                # (linear interpolation to smooth depth)
                # x0 = int(np.floor(src_x))
                # x1 = x0 + 1
                # alpha = src_x - x0
                #
                # if x0 < 0:
                #     image[y, x] = pattern[y, x % pattern_width]
                # elif x0 < pattern_width:
                #     left = pattern[y, x0 % pattern_width]
                #     right = pattern[y, x1 % pattern_width]
                #     image[y, x] = int((1 - alpha) * left + alpha * right)
                # elif x1 >= width:
                #     continue # prevents breaking on right side of image
                # else:
                #     # Normal interpolation in image
                #     left = image[y, x0]
                #     right = image[y, x1]
                #     image[y, x] = int((1 - alpha) * left + alpha * right)



                # if 0 < x0 and 0 < x1:
                #     left = image[y, x0]
                #     right = image[y, x1]
                #     image[y, x] = int((1 - alpha) * left + alpha * right)



    # add color to image (or leave greyscale)
    if color_option is not None:
        if color_option == coloring.greyscale_to_satscale:
            image = color_option(image, hue=hue)
        else:
            image = color_option(image)

    return Image.fromarray(image)


def interpolate_pixel(x, y, src_x, image, pattern, pattern_width, width):
    x0 = int(np.floor(src_x))
    x1 = x0 + 1
    alpha = src_x - x0

    # make sure x0 and x1 are in the image
    if 0 <= x0 < width - 1:
        left = image[y, x0]
        right = image[y, x1]
        return int((1 - alpha) * left + alpha * right) # avg weighted by alpha
    elif x0 < 0:
        # ?use pattern ref for first part of image
        return pattern[y, x % pattern_width]
    elif x1 >= width:
        # avoid out of bounds
        return image[y, x0]
    else:
        return 0 # prevent none returned
