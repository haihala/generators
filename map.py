import pygame, argparse, os, math
from random import random

DEEP_SEA = (0, 0, 100)
SHALLOW_SEA = (80, 80, 200)
MOUNTAIN = (151,124,83) 
GRASS = (40, 150, 40)
BEACH = (223,193,99)
SUMMIT = (240, 240, 240)

def smooth(source, window, power):
    for i in range(window, len(source)-window):
        for j in range(window, len(source[0])-window):
            avg = sum(sum(column for column in row[j-window:j+window]) for row in source[i-window:i+window])/((1+2*window)**2)
            source[i][j] = power*avg + (1-power)*source[i][j]

def color_lerp(a, b, ratio):
    ratio = min(1, max(0, ratio))
    return tuple(int(a[i]*ratio+b[i]*(1-ratio)) for i in range(3))

def generate(
        fname, 
        size, 
        view_result, 
        height_offset, 
        height_delta, 
        height_points,
        height_smooth_size, 
        height_smooth_power,
        height_smooth_rounds,
        beach_height,
        mountain_height,
        summit_height
        ):
    pygame.init()
    height_map = [[height_offset for i in range(size[1]+2*height_smooth_size)] for j in range(size[0]+2*height_smooth_size)]
    surf = pygame.Surface(size)

    # Random points for altitude
    points = []
    for _ in range(int(height_points*size[0]*size[1])):
        i = int(random()*size[0])
        j = int(random()*size[1])
        points.append((i, j))
        height_map[i][j] += height_delta*(0.5-random())

    print("Randomness generated")

    # Smooth out data
    for i in range(height_smooth_rounds):
        print("Beginning height smoothing round {}".format(i+1))
        smooth(height_map, height_smooth_size, height_smooth_power)
    print("Smoothing done")

    # Remove original points
    for point in points:
        i, j = point
        height_map[i][j] = (sum(sum(column for column in row[j-1:j+1]) for row in height_map[i-1:i+1])-height_map[i][j])/8

    # Crop to size. Do it this way to ignore edge when smoothing.
    height_map = [row[height_smooth_size:-height_smooth_size] for row in height_map[height_smooth_size:-height_smooth_size]]
    print("Cropping done")

    # Map to colors
    for i in range(size[0]):
        for j in range(size[1]):
            height = height_map[i][j]
            height_scaler = abs(5000*height/height_delta)

            if height < 0:
                # Water
                surf.set_at((i, j), color_lerp(DEEP_SEA, SHALLOW_SEA, height_scaler))
            else:
                # Land
                color = (0, 0, 0)
                if height < beach_height:
                    # Beach
                    color = BEACH
                elif height < mountain_height:
                    # Grassland/forest
                    color = color_lerp(MOUNTAIN, GRASS, height/mountain_height)
                elif height < summit_height:
                    # Mountain
                    color = MOUNTAIN
                else:
                    # Snowy summit
                    color = SUMMIT
                surf.set_at((i, j), color)
                

    # Display if flag given
    if view_result:
        display = pygame.display.set_mode(size)
        pygame.display.set_caption("Preview. Escape to exit.")
        display.blit(surf, (0, 0))
        pygame.display.flip()
        
        closed = False
        while not closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        closed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print("Clicked position data:")
                    print("Elevation: {}".format(height_map[pos[0]][pos[1]]))
      
    # Write to file if flag given
    if fname:
        if not os.path.isdir("images"):
            os.mkdir("images")
        if '.' not in fname:
            fname += ".png"
        pygame.image.save(surf, os.path.join("images", fname))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a world map image")
    parser.add_argument("-file", type=str, default=False, nargs="?",
        help="Name of file to save the map to")
    parser.add_argument("width", type=int,
        help="Width of image")
    parser.add_argument("height", type=int,
        help="Height of image")
    parser.add_argument("-view", const=True, default=False, nargs='?',
        help="View map after generating")

    parser.add_argument("-height_offset", type=float, default=50,
        help="How high is sea level")
    parser.add_argument("-height_delta", type=float, default=800000,
        help="Height delta. How tall should the summits of mountains be.")
    parser.add_argument("-height_points", type=int, default=0.001,
        help="How many random points should random values be applied to per pixel")
    parser.add_argument("-height_smooth_size", type=int, default=20,
        help="How much should smoothing influence(1 is total offset, 0 is no smoothing)")
    parser.add_argument("-height_smooth_power", type=float, default=0.7,
        help="How much should smoothing influence(1 is total offset, 0 is no smoothing)")
    parser.add_argument("-height_smooth_rounds", type=int, default=6,
        help="How many times should the smoothing be ran")
    parser.add_argument("-beach_height", type=float, default=5,
        help="Maximum height for 'beach'")
    parser.add_argument("-mountain_height", type=float, default=100,
        help="Minimum height for 'mountain'")
    parser.add_argument("-summit_height", type=float, default=180,
        help="Minimum height for 'summit'")

    args = parser.parse_args()
    generate(
        args.file, 
        (args.width, args.height),
        args.view,
        args.height_offset, 
        args.height_delta, 
        args.height_points,
        args.height_smooth_size, 
        args.height_smooth_power,
        args.height_smooth_rounds,
        args.beach_height,
        args.mountain_height,
        args.summit_height
        )


