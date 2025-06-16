import matplotlib.pyplot as plt
import numpy as np

def plot_depth_map(depth_map=None):

    plt.figure("Depth Map")
    plt.imshow(depth_map, cmap='grey', origin='upper')
    plt.title("Depth Map")
    plt.colorbar(label='Depth value')
    plt.show()

def plot_disparity_map(depth_map=None, pattern_width=None):
    disparity_map = (depth_map * pattern_width).astype(int)
    plt.figure("Disparity Map")
    plt.imshow(disparity_map, cmap='gray', origin='upper')
    plt.title("Disparity Map")
    plt.colorbar(label='Disparity')
    plt.show()