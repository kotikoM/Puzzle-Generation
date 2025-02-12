import numpy as np

def create_bell_bezier(start_point, end_point,
                       neck_factor=1.6, width_factor=0.8,
                       height_factor=0.3, vertical_pull=0.2):
    # Extract coordinates
    x1, y1 = start_point
    x2, y2 = end_point

    num_points = 100

    # Calculate midpoint for connecting the two curves
    mid_x = (x1 + x2) / 2
    mid_y = max(y1, y2) + abs(x2 - x1) * height_factor  # Peak of the bell

    # Control points for first curve (bottom to top)
    ctrl1_x = x1 + (mid_x - x1) * neck_factor  # Close to start for narrow neck
    ctrl1_y = y1 + (mid_y - y1) * vertical_pull

    ctrl2_x = mid_x - (mid_x - x1) * width_factor  # Wide curve for bell shape
    ctrl2_y = mid_y - (mid_y - y1) * 0.1

    # Control points for second curve (top to bottom)
    ctrl3_x = mid_x + (x2 - mid_x) * width_factor  # Wide curve for bell shape
    ctrl3_y = mid_y - (mid_y - y2) * 0.1

    ctrl4_x = x2 - (x2 - mid_x) * neck_factor  # Close to end for narrow neck
    ctrl4_y = y2 + (mid_y - y2) * vertical_pull

    # Generate points for first curve
    t = np.linspace(0, 1, num_points)
    curve1_x = (1 - t) ** 3 * x1 + 3 * (1 - t) ** 2 * t * ctrl1_x + 3 * (1 - t) * t ** 2 * ctrl2_x + t ** 3 * mid_x
    curve1_y = (1 - t) ** 3 * y1 + 3 * (1 - t) ** 2 * t * ctrl1_y + 3 * (1 - t) * t ** 2 * ctrl2_y + t ** 3 * mid_y

    # Generate points for second curve
    curve2_x = (1 - t) ** 3 * mid_x + 3 * (1 - t) ** 2 * t * ctrl3_x + 3 * (1 - t) * t ** 2 * ctrl4_x + t ** 3 * x2
    curve2_y = (1 - t) ** 3 * mid_y + 3 * (1 - t) ** 2 * t * ctrl3_y + 3 * (1 - t) * t ** 2 * ctrl4_y + t ** 3 * y2

    # Combine the curves
    x_points = np.concatenate([curve1_x, curve2_x])
    y_points = np.concatenate([curve1_y, curve2_y])

    return x_points, y_points
