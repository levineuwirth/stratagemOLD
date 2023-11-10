import numpy as np
from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import gaussian_filter
import time
import random

inittime = time.time()
# Generate 1000x1000 noise
noise = OpenSimplex(seed=random.randint(0, 100000000))
rows, cols = 1000, 1000
world = np.zeros((rows, cols))
for i in range(rows):
    for j in range(cols):
        world[i][j] = noise.noise2(i/100, j/100)

# Divide noise into six categories using numpy's digitize function
bins = [-np.inf, -0.2, -0.1, 0.1, 0.2, 0.5, np.inf]
categories = np.digitize(world, bins)
print("map generated: ", time.time() - inittime)

# Label regions in category 1
labels, num_features = ndimage.label(categories == 1)

# Define the boundaries of the middle third of the map
third_rows = rows // 3
two_third_rows = 2 * rows // 3

# Iterate over each region
for feature in range(1, num_features + 1):
    # Create a mask for the current region
    mask = labels == feature

    # Check if the region touches the border
    if np.any(mask[0, :]) or np.any(mask[-1, :]) or np.any(mask[:, 0]) or np.any(mask[:, -1]):
        continue

    # If it doesn't touch the border and is within the middle third of the map,
    # change it to category 7; otherwise change it to category 2
    if third_rows <= np.min(np.nonzero(mask)[0]) <= two_third_rows:
        categories[mask] = 7
    else:
        categories[mask] = 2

print("continents generated: ", time.time() - inittime)

# Create a larger map and place the generated map in the center
larger_rows, larger_cols = 1300, 1300
larger_categories = np.ones((larger_rows, larger_cols)) # Fill with category 1 noise
start_row, start_col = (larger_rows - rows) // 2, (larger_cols - cols) // 2
larger_categories[start_row:start_row+rows, start_col:start_col+cols] = categories

print("ocean expanded: ", time.time() - inittime)

# Define the region of interest
roi = larger_categories[start_row:start_row+rows, start_col:start_col+cols]

# Apply Gaussian filter to smooth the results in the region of interest
smooth_roi = gaussian_filter(roi, sigma=2)

# Replace the region of interest with the smoothed data
larger_categories[start_row:start_row+rows, start_col:start_col+cols] = smooth_roi

# Set the corners of the 1000x1000 map to category one
larger_categories[:start_row, :] = 1
larger_categories[start_row+rows:, :] = 1
larger_categories[:, :start_col] = 1
larger_categories[:, start_col+cols:] = 1


# Visualize with matplotlib
plt.imshow(larger_categories, cmap='viridis')
plt.colorbar(ticks=[0, 1, 2, 3, 4, 5], label='Categories')
plt.show()
