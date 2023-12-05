from bridson import poisson_disc_samples
from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
import numpy as np
import random

class World:
    def __init__(self, seedperm):
        self.seedperm = seedperm
        self.worlddata = self.generate_worldlayout(random.randint(40, 50), (random.randint(40, 50)), 10, 3, 2, seedperm)

    def normalize(value, min_value, max_value, new_min, new_max):
        return ((value - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min
    
    def generate_worldlayout(self, width, height, wavelength, octaves, power, seed):
        def generate_enoise(nx, ny):
            noise = OpenSimplex(seed)
            return noise.noise2(nx, ny)

        def generate_mnoise(nx, ny):
            noise = OpenSimplex(1 + seed)
            return noise.noise2(nx, ny)

        world = np.zeros((height, width))

        for y in range(height):
            for x in range(width):
                nx, ny = x / width - 0.5, y / height - 0.5

                # Frequency adjustment
                e = generate_enoise(x / wavelength, y / wavelength)
                m = generate_mnoise(x / wavelength, y / wavelength)

                # Octaves for fractal noise
                for octave in range(1, octaves + 1):
                    e += 0.5**octave * generate_enoise(2**octave * nx, 2**octave * ny)
                    m += 0.5**octave * generate_mnoise(2**octave * nx, 2**octave * ny)

                # Redistribution for terrain features
                e /= sum(0.5**octave for octave in range(octaves))
                e = e ** power
                e = self.normalize(e, 0, 0.15, -0.5, 0.5)

                m /= sum(0.5**octave for octave in range(octaves))
                m = m ** power
                m = self.normalize(m, 0, 0.15, -0.5, 0.5)

                # Handle toroidal (wrap-around) effect for x-axis
                wrapped_x = (x + width) % width

                # Assign biome based on thresholds
                world[y][wrapped_x] = self.assign_biome(e, m)

        upsampled_world = world.repeat(3, axis=0).repeat(3, axis=1)
        mountain_samples = poisson_disc_samples(width=world_width * 3, height=world_height * 3, r=1)

        # Add mountains after initial assignments and upsampling
        for sample in mountain_samples:
            x, y = int(sample[0]), int(sample[1])
        
        # Check if the location is above sea level
        if upsampled_world[y][x] < -.1:  # Sea level
            upsampled_world[y][x] = 8  # Assign mountain biome
        return upsampled_world

    #Biomes:
    #0 - deep ocean
    #1 - sea
    #2 - coastal desert
    #3 - coast
    #4 - desert
    #5 - plains
    #6 - forest
    #7 - rainforest
    #8 - mountain range
    #9 - extreme mountain


    def assign_biome(e, m):
        if e < -.3:
            return 0
        if e < -.2:
            return 1
        if e < -.1:
            if m < .3:
                return 2
            else:
                return 3
        if e < .35:
            if m < .3:
                return 4
            if m < 0:
                return 5
            if m < 3:
                return 6
            else:
                return 7
        if e < 4.5:
            return 8
        else:
            return 9

    def visualize_world(world):
        plt.imshow(world, cmap='terrain', interpolation='nearest')
        plt.colorbar(label='Biome')
        plt.title('World Biomes')
        plt.show()

world_width = 50
world_height = 50
wavelength = 10
octaves = 3
power = 2
test = World.generate_worldlayout(world_width, world_height, wavelength, octaves, power, 42)
print("world generated")

# Visualize the world
World.visualize_world(test)