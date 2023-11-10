import numpy as np
from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
from scipy import ndimage
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

# Create a structuring element for dilation
selem = ndimage.generate_binary_structure(2, 2)

# Iterate over each region
for feature in range(1, num_features + 1):
    # Create a mask for the current region
    mask = labels == feature

    # Apply dilation to the mask
    dilated_mask = ndimage.binary_dilation(mask, structure=selem)

    # Check if the dilated region touches the border
    if np.any(dilated_mask[0, :]) or np.any(dilated_mask[-1, :]) or np.any(dilated_mask[:, 0]) or np.any(dilated_mask[:, -1]):
        continue

    # If it doesn't touch the border, change it to category 2
    categories[mask] = 2

print("continents generated: ", time.time() - inittime)

# Create a larger map and place the generated map in the center
larger_rows, larger_cols = 1300, 1300
larger_categories = np.ones((larger_rows, larger_cols)) # Fill with category 1 noise
start_row, start_col = (larger_rows - rows) // 2, (larger_cols - cols) // 2
larger_categories[start_row:start_row+rows, start_col:start_col+cols] = categories

print("ocean expanded: ", time.time() - inittime)

# Visualize with matplotlib
plt.imshow(larger_categories, cmap='viridis')
plt.colorbar(ticks=[0, 1, 2, 3, 4, 5], label='Categories')
plt.show()
