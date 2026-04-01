'''Module 3: count black and white pixels and compute the percentage of white pixels in a .jpg image and extrapolate points'''

# Code optimized with assistance from Claude (Anthropic, 2026) — claude.ai
from termcolor import colored
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd
import time 
start = time.time()

filenames = [
    r"images/MASK_SK658 Llobe ch010039.jpg",
    r"images/MASK_SK658 Llobe ch010030.jpg",
    r"images/MASK_SK658 Llobe ch010171.jpg",
    r"images/MASK_SK658 Slobe ch010142.jpg",
    r"images/MASK_SK658 Slobe ch010060.jpg",
    r"images/MASK_SK658 Slobe ch010098.jpg",
]

depths = [15, 200, 810, 7100, 8400, 10000]

# Load images and compute pixel counts in one pass
white_counts, black_counts, white_percents = [], [], []

for filename in filenames:
    binary = cv2.threshold(cv2.imread(filename, 0), 127, 255, cv2.THRESH_BINARY)[1]
    white = int(np.sum(binary == 255))
    black = int(np.sum(binary == 0))
    white_counts.append(white)
    black_counts.append(black)
    white_percents.append(100 * white / (white + black))

# Print pixel counts
print(colored("Counts of pixel by color in each image", "yellow"))
for x, (w, b) in enumerate(zip(white_counts, black_counts)):
    print(colored(f"White pixels in image {x}: {w}", "white"))
    print(colored(f"Black pixels in image {x}: {b}", "black"))
    print()

# Print percentages
print(colored("Percent white px:", "yellow"))
for filename, pct, depth in zip(filenames, white_percents, depths):
    print(colored(f'{filename}:', "red"))
    print(f'{pct:.2f}% White | Depth: {depth} microns\n')

# Write to CSV
df = pd.DataFrame({
    'Filenames': filenames,
    'Depths': depths,
    'White percents': white_percents
})
df.to_csv('Percent_White_Pixels.csv', index=False)



# LECTURE 2: UNCOMMENT BELOW

# Interpolate a point: given a depth, find the corresponding white pixel percentage

interpolate_depth = float(input(colored("Enter the depth at which you want to interpolate a point (in microns): ", "yellow")))

x = depths
y = white_percents

# You can also use 'quadratic', 'cubic', etc.
i = interp1d(x, y, kind='quadratic')
interpolate_point = i(interpolate_depth)
print(colored(f'The interpolated point is at the x-coordinate {interpolate_depth} and y-coordinate {interpolate_point}.', "green"))

depths_i = depths[:]
depths_i.append(interpolate_depth)
white_percents_i = white_percents[:]
white_percents_i.append(interpolate_point)


# make two plots: one that doesn't contain the interpolated point, just the data calculated from your images, and one that also contains the interpolated point (shown in red)
fig, axs = plt.subplots(2, 1)

axs[0].scatter(depths, white_percents, marker='o', linestyle='-', color='blue')
axs[0].set_title('Plot of depth of image vs percentage white pixels')
axs[0].set_xlabel('depth of image (in microns)')
axs[0].set_ylabel('white pixels as a percentage of total pixels')
axs[0].grid(True)


axs[1].scatter(depths_i, white_percents_i, marker='o', linestyle='-', color='blue')
axs[1].set_title('Plot of depth of image vs percentage white pixels with interpolated point (in red)')
axs[1].set_xlabel('depth of image (in microns)')
axs[1].set_ylabel('white pixels as a percentage of total pixels')
axs[1].grid(True)
axs[1].scatter(depths_i[len(depths_i)-1], white_percents_i[len(white_percents_i)-1], color='red', s=100, label='Highlighted point')


# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()


#to test accuracy of interpolation, we can load the image at depth = 9000 microns and compute the percentage of white pixels, then compare it to the interpolated point at depth = 9000 microns
# Load the image at depth = 9000 microns
filename_9000 = r"images/MASK_SK658 Llobe ch010121.jpg"

# Convert to binary (black and white)
binary_9000 = cv2.threshold(cv2.imread(filename_9000, 0), 127, 255, cv2.THRESH_BINARY)[1]

# Count white and black pixels
white_9000 = int(np.sum(binary_9000 == 255))
black_9000 = int(np.sum(binary_9000 == 0))

# Compute percent white pixels
percent_white_9000 = 100 * white_9000 / (white_9000 + black_9000)

# Print results
print(colored("Actual data at depth = 9000 microns:", "yellow"))
print(f"White pixels: {white_9000}")
print(f"Black pixels: {black_9000}")
print(f"Percent white (fibrosis): {percent_white_9000:.2f}%")