import random
import numpy as np
from PIL import Image, ImageDraw
from src.curves import create_bell_bezier


def generate_grid_corners(width, height, num_pieces):
    # Calculate the number of rows and columns in the grid based on the aspect ratio
    aspect_ratio = width / height

    # Calculate the number of rows and columns
    num_cols = int(np.sqrt(num_pieces * aspect_ratio))
    num_rows = int(np.ceil(num_pieces / num_cols))

    # Calculate the size of each grid cell
    cell_width = width / num_cols
    cell_height = height / num_rows

    # Generate the corner points for the grid
    corners = []
    for i in range(num_rows + 1):  # Include the last row
        for j in range(num_cols + 1):  # Include the last column
            x = j * cell_width
            y = i * cell_height
            corners.append((x, y))

    return corners, num_rows, num_cols


def create_grid_image(width, height, corners, num_rows, num_cols):
    # Create a blank white image
    img = Image.new("RGB", (int(width), int(height)), "white")
    draw = ImageDraw.Draw(img)

    # Draw the boundary of the rectangle
    draw.rectangle([0, 0, width, height], outline="black")

    # Draw the corner points
    radius = 0
    for x, y in corners:
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill="red", outline="black")

    draw_puzzle_knobs(draw, corners, num_rows, num_cols)
    img.show()


def draw_puzzle_knobs(draw, corners, num_rows, num_cols,
                      color="black", line_width=2,
                      neck_factor=1.6, width_factor=0.8,
                      height_factor=0.3, vertical_pull=0.2):
    # Draw horizontal knobs
    for row in range(1, num_rows):
        start_index = row * (num_cols + 1)
        for col in range(num_cols):
            point1 = corners[start_index + col]
            point2 = corners[start_index + col + 1]

            flip = random.choice([0, 1])
            curve_x, curve_y = create_bell_bezier(point1, point2, neck_factor, width_factor, height_factor,
                                                  vertical_pull)

            if flip == 0:  # Flip the knob horizontally
                point1_y = point1[1]
                curve_y = [2 * point1_y - y for y in curve_y]  # Reflect the y points over point1[1]

            for i in range(len(curve_x) - 1):
                draw.line([curve_x[i], curve_y[i], curve_x[i + 1], curve_y[i + 1]], fill=color, width=line_width)

    # Draw vertical knobs
    for col in range(1, num_cols):
        for row in range(num_rows):
            point1 = corners[row * (num_cols + 1) + col]
            point2 = corners[(row + 1) * (num_cols + 1) + col]

            flip = random.choice([0, 1])
            v_curve_x, v_curve_y = create_bell_bezier((point1[1], point1[0]), (point2[1], point2[0]),
                                                      neck_factor, width_factor, height_factor, vertical_pull)

            if flip == 0:  # Flip the knob vertically
                point1_x = point1[0]
                v_curve_y = [2 * point1_x - x for x in v_curve_y]  # Reflect the x points over point1[0]

            for i in range(len(v_curve_x) - 1):
                draw.line([v_curve_y[i], v_curve_x[i], v_curve_y[i + 1], v_curve_x[i + 1]], fill=color,
                          width=line_width)


if __name__ == '__main__':
    ''' Custom Image Underlay '''
    image_path = "../results/wave.jpg"
    img = Image.open(image_path)
    width, height = img.size
    num_pieces = 1000

    corners, num_rows, num_cols = generate_grid_corners(width, height, num_pieces)
    draw_puzzle_knobs(ImageDraw.Draw(img), corners, num_rows, num_cols)
    img.show()
    # img.save("out.jpg")

    ''' Puzzle Skeleton on White Canvas '''
    width, height = 4000, 3000
    num_pieces = 1000

    corners, num_rows, num_cols = generate_grid_corners(width, height, num_pieces)
    create_grid_image(width, height, corners, num_rows, num_cols)
