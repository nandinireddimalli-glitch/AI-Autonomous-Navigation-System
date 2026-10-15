"""
Central configuration for the AI-Based Autonomous Navigation System.

All tunable parameters live here so every module reads from one place.
Edit the values below to change grid size, sensor range, or colors.
"""

# ---------------------------------------------------------------------------
# Grid / map settings
# ---------------------------------------------------------------------------
GRID_W = 30          # number of columns in the grid
GRID_H = 20          # number of rows in the grid
CELL_SIZE = 28       # pixel size of one grid cell in the pygame window

# ---------------------------------------------------------------------------
# Cell values used inside the grid (0 = free, 1 = obstacle, 2 = start, 3 = goal)
# ---------------------------------------------------------------------------
FREE = 0
OBSTACLE = 1
START = 2
GOAL = 3

# ---------------------------------------------------------------------------
# Sensor settings (the simulated LiDAR / ultrasonic sensor)
# ---------------------------------------------------------------------------
SENSOR_RANGE = 6     # how many cells the sensor can see in each direction
SENSOR_RAYS = 8      # number of directional rays (N, NE, E, SE, S, SW, W, NW)

# ---------------------------------------------------------------------------
# Robot settings
# ---------------------------------------------------------------------------
ROBOT_SPEED = 1      # cells per simulation step
ROBOT_CLEARANCE = 1  # safety margin kept from detected obstacles

# ---------------------------------------------------------------------------
# Colors used by both the pygame simulator and matplotlib (R, G, B)
# ---------------------------------------------------------------------------
COLORS = {
    "background": (18, 18, 24),
    "grid_line": (40, 40, 52),
    "free": (245, 245, 248),
    "obstacle": (60, 60, 70),
    "start": (46, 204, 113),       # green
    "goal": (231, 76, 60),         # red
    "robot": (52, 152, 219),       # blue
    "path": (241, 196, 15),        # yellow
    "explored": (155, 89, 182),    # purple-ish, used for visited cells
    "sensor": (255, 255, 0, 80),   # semi-transparent yellow
    "text": (236, 240, 241),
    "danger": (231, 76, 60),
}

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
FPS = 10             # simulation frames per second
HEADLESS = False     # set True to run without a window (for CI / screenshots)
