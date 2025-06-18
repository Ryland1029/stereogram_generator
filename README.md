# Stereogram Generator

A Python application for generating single-image random dot stereograms (SIRDS) from a variety of depth maps. The app allows control of noise type, pattern width, hue adjustment, depth, and smoothing.

## Features

* Generate stereograms using available depth maps, including sine, checkerboard, Chladni-style standing waves, gradients, etc.
* Choose from different noise patterns for base texture.
* Greyscale, RGB, or Hue coloring, with hue slider (only if using saturation-based coloring).
* Toggleable depth smoothing via linear interpolation.
* Slider to control max effective depth.
* Benchmark time to generate image.
* Optional matplotlib depth map visualization.
* Ability to download generated image.
* Light/Dark themes (using Sun Valley ttk theme).

## Requirements

* Python 3.8+
* Dependencies:

  * matplotlib>=3.10.3
  * numpy>=2.3.0
  * pillow>=11.2.1
  * sv_ttk>=2.6.1

Install required packages:

```bash
pip install numpy pillow matplotlib sv-ttk
```

## Usage

Run the application:

```bash
python main.py
```

From the GUI:

* Select a depth map, noise pattern, and color option
* Click "Generate" or press Enter/space
* Experiment with pattern width, depth, and hue
* Toggle smoothing (for smoother depth mapping)
* View benchmark time and optionally download the result
* Click Depth Map to help visualize the stereogram you should be seeing

## File Structure

* `main.py`: Entry point
* `gui.py`: GUI layout and logic
* `stereogram.py`: Core stereogram generation algorithm
* `coloring.py`: Coloring functions
* `noise.py`: Pattern generators
* `maps.py`: Depth map functions
* `plotting.py`: Matplotlib depth and disparity visualizer functions

## Notes

* Smoothing interpolates across subpixel disparities for continuous depth using linear blending. Progressive blurring as the image generates rightward is intrinsic to the stereogram generation.
* Different types o depth maps are better visualized with different pattern width and depth settings. Experiment with these sliders if the illusion is not working. 
* rainbow coloring does not work well with Gaussian noise

## TODO

* Add support for custom user-uploaded depth maps
* More available depth map options
* More noise pattern types (Perlin)
* Web-based port
* Sound effects/background music
* improve algorithm efficiency (nested for loops -> vectors)

## License

MIT License

---

Feel free to fork and contribute
