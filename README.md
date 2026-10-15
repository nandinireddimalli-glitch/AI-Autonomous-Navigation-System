# AI-Based Autonomous Navigation System

An industry-oriented, fully virtual autonomous navigation pipeline built in Python. It combines **computer-vision-style perception**, **A\* path planning**, **simulated LiDAR sensing**, and **reactive obstacle avoidance** inside a custom pygame simulation environment — no real robot hardware required.

> Designed as portfolio proof-of-work for placements, internships, and off-campus applications.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Industry Relevance](#industry-relevance)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Simulation Workflow](#simulation-workflow)
- [Results](#results)
- [Screenshots](#screenshots)
- [Learning Outcomes](#learning-outcomes)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

---

## Project Overview

This project simulates how an autonomous robot (think warehouse AGV, delivery robot, or self-driving car in a simplified grid world) navigates from a start point to a goal while avoiding obstacles it discovers along the way.

The robot **does not know the full map in advance**. It uses a simulated sensor to perceive its surroundings, an A\* planner to compute an obstacle-free path, and a reactive control loop that **re-plans in real time** when new obstacles block the current route — exactly how real autonomous systems operate.

### Simple-language explanation

Imagine you're in a maze. You can see a few steps ahead, but not the whole maze. You plan a route toward the exit, but if you suddenly spot a wall in your way, you change your route. That's what this system does — automatically, on a virtual grid, with code you can see and run.

### Technical explanation

The system implements a classic **sense-plan-act** autonomy loop:

| Stage | What happens | Module |
|-------|-------------|--------|
| **Perception** | A simulated 8-direction LiDAR scans for obstacles within sensor range | `src/sensors.py`, `src/perception.py` |
| **Path Planning** | A\* search with an octile-distance heuristic finds the shortest free path on the 8-connected grid | `src/path_planner.py` |
| **Decision Making** | The navigator checks whether newly discovered obstacles block the current path and triggers re-planning if so | `src/navigator.py` |
| **Control** | The robot follows the path one cell per simulation step | `src/robot.py` |
| **Simulation** | A pygame window renders the grid, obstacles, sensor rays, robot, and path in real time | `src/simulation.py` |
| **Visualization** | Matplotlib generates static path images and animated GIFs for documentation | `src/visualizer.py` |

---

## Problem Statement

Real autonomous vehicles and robots need to:

1. **Perceive** their environment using sensors (cameras, LiDAR, radar).
2. **Plan** a safe, efficient route to their destination.
3. **React** to unexpected obstacles in real time.
4. **Navigate** reliably without human intervention.

Building and testing these systems on real hardware is expensive, dangerous, and inaccessible to most students. This project solves that gap by providing a **fully virtual testbed** where the entire perception-planning-navigation pipeline can be developed, tested, and demonstrated on a laptop.

---

## Industry Relevance

This project models the same software architecture used across the autonomous systems industry:

| Industry | Application | How this project relates |
|----------|------------|------------------------|
| **Autonomous vehicles** | Tesla, Waymo, Cruise | Path planning + obstacle avoidance on a grid is the 2D simplification of what self-driving cars do in continuous space |
| **Warehouse automation** | Amazon Kiva, Grey Orange, Locus Robotics | AGVs navigate warehouse floors using grid-based maps and reactive re-planning |
| **Delivery robots** | Starship Technologies, Nuro | Last-mile delivery robots use the same sense-plan-act loop |
| **Drones** | Skydio, Zipline | UAVs plan paths around obstacles — the 2D version is directly transferable |
| **Industrial safety** | Mobile robots in factories | Obstacle avoidance prevents collisions with workers and equipment |
| **Smart mobility** | Campus shuttles, parking robots | Route planning + dynamic obstacle detection is the core capability |

Companies hiring for robotics, AV, and automation roles look for candidates who understand **perception → planning → control** pipelines. This project demonstrates exactly that.

---

## Tech Stack

| Tool | Role |
|------|------|
| **Python 3.9+** | Core programming language |
| **NumPy** | Grid manipulation, array operations |
| **OpenCV** | Computer-vision-style obstacle detection (contour-based blob detection) |
| **Matplotlib** | Static path plots, animated GIF generation |
| **pygame** | Real-time interactive simulation window |
| **pytest** | Unit testing for the path planner and navigation loop |

> No GPU required. No deep-learning model training needed. Runs on any laptop with Python 3.9+.

---

## Architecture

### Block Diagram

```
                    ┌──────────────────────────────────────────────┐
                    │              CONFIG (config.py)               │
                    │  grid size, sensor range, colors, speeds      │
                    └──────────────────┬───────────────────────────┘
                                       │
                    ┌──────────────────▼───────────────────────────┐
                    │            GRID MAP (grid_map.py)             │
                    │  2D occupancy grid, obstacles, start, goal    │
                    └──────┬──────────────────────┬────────────────┘
                           │                      │
           ┌───────────────▼───┐      ┌───────────▼──────────────┐
           │   SENSOR (sensors) │      │  PATH PLANNER (A*)        │
           │  8-dir LiDAR rays  │      │  octile heuristic search  │
           │  detects obstacles │      │  shortest free path       │
           └───────┬───────────┘      └───────────┬──────────────┘
                   │                              │
          ┌────────▼──────────┐                   │
          │  PERCEPTION        │                   │
          │  accumulates known  │    re-plan?      │
          │  obstacles, checks  │◄─────────────────┘
          │  path-blocked       │
          └────────┬───────────┘
                   │
          ┌────────▼───────────┐
          │   NAVIGATOR         │
          │  sense → plan → act │
          │  reactive re-plan   │
          └────────┬───────────┘
                   │
          ┌────────▼───────────┐
          │     ROBOT           │
          │  follows path,      │
          │  logs trail/steps   │
          └────────┬───────────┘
                   │
          ┌────────▼───────────┐    ┌─────────────────────┐
          │  SIMULATION (pygame)│    │  VISUALIZER (mpl)    │
          │  real-time render   │    │  path PNG + GIF      │
          └────────────────────┘    └─────────────────────┘
```

### Data Flow

1. **GridMap** is created with obstacles, start, and goal positions.
2. **A\* Planner** computes an initial path from start to goal.
3. **Navigator** begins the sense-plan-act loop:
   - **Sensor** scans 8 directions from the robot's current cell.
   - **Perception** merges any new obstacles into the known set.
   - If the current path is blocked, **A\*** re-plans around the known obstacles.
   - **Robot** moves one step along the (updated) path.
4. Loop repeats until the robot reaches the goal or no path exists.
5. **Simulation** renders every step in pygame; **Visualizer** saves PNG/GIF.

---

## Folder Structure

```
AI-Autonomous-Navigation-System/
│
├── config.py                  # Central configuration (grid size, sensor, colors)
├── main.py                    # Entry point: sim / run / animate / test
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files to exclude from git
├── README.md                  # This file
│
├── src/                       # All source modules
│   ├── __init__.py
│   ├── grid_map.py            # 2D occupancy grid world
│   ├── path_planner.py        # A* algorithm with octile heuristic
│   ├── sensors.py             # Simulated 8-direction LiDAR
│   ├── perception.py          # Obstacle accumulation + CV detection
│   ├── robot.py               # Robot agent that follows a path
│   ├── navigator.py           # Sense-plan-act controller
│   ├── simulation.py          # Pygame real-time simulator
│   └── visualizer.py          # Matplotlib path plots + GIF animation
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test_path_planner.py   # Tests for A*, navigator, heuristics
│
├── outputs/                   # Generated results (PNG, GIF)
│   ├── .gitkeep
│   ├── path_plot.png          # (generated by --mode run)
│   └── navigation_demo.gif    # (generated by --mode animate)
│
├── docs/                      # Documentation
│   └── PROJECT_GUIDE.md       # Complete build + portfolio strategy guide
│
└── images/                    # Screenshots for README
    └── .gitkeep
```

### File Purposes

| File | Purpose |
|------|---------|
| `config.py` | Single source of truth for grid size, sensor range, colors, FPS |
| `main.py` | CLI entry point with 4 modes: `sim`, `run`, `animate`, `test` |
| `src/grid_map.py` | Defines the virtual world: obstacles, start, goal, neighbors |
| `src/path_planner.py` | A\* search with octile heuristic on an 8-connected grid |
| `src/sensors.py` | Simulated LiDAR — casts 8 rays, reports first obstacle hit |
| `src/perception.py` | Accumulates obstacle knowledge + OpenCV contour detection |
| `src/robot.py` | Agent state: position, path, trail, step counter |
| `src/navigator.py` | The brain — orchestrates sense → plan → act with reactive re-planning |
| `src/simulation.py` | Pygame window with real-time rendering of everything |
| `src/visualizer.py` | Static PNG path plots + animated GIF for documentation |
| `tests/test_path_planner.py` | 5 unit tests covering heuristics, pathfinding, navigation |

---

## Installation

### Prerequisites

- **Python 3.9 or newer** (3.11+ recommended)
- pip (comes with Python)

### Step-by-step

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/AI-Autonomous-Navigation-System.git
cd AI-Autonomous-Navigation-System
```

**2. Create a virtual environment**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Verify installation**
```bash
python main.py --mode test
```

You should see:
```
============================== 5 passed in 0.4s ==============================
```

---

## How to Run

The project has **four modes**, all launched from `main.py`:

### Mode 1: Interactive Simulation (pygame window)
```bash
python main.py --mode sim
```
Opens a real-time pygame window. You watch the robot navigate the grid, detect obstacles via sensor rays (yellow lines), and follow the A\* path (yellow dots). The HUD shows step count, replans, and mission status. Press `ESC` or close the window to quit.

### Mode 2: Headless Run (no window, saves PNG)
```bash
python main.py --mode run
```
Runs a complete mission in the terminal, prints a status report, and saves `outputs/path_plot.png`.

**Sample terminal output:**
```
==============================
 AI AUTONOMOUS NAVIGATION - RUN COMPLETE
==============================
  Mission success : True
  Steps taken     : 27
  Replans         : 0
  Obstacles known : 35
  Event log:
    - Initial path planned: 28 steps.
    - Detected 2 new obstacle(s) near (1, 1).
    - Detected 1 new obstacle(s) near (2, 1).
    ...
    - Goal reached successfully!
  Path image saved: outputs/path_plot.png
==============================
```

### Mode 3: Animated GIF (for GitHub / LinkedIn)
```bash
python main.py --mode animate --out outputs/navigation_demo.gif
```
Runs a full mission and saves an animated GIF showing the robot navigating step-by-step. Perfect for embedding in your README and LinkedIn posts.

### Mode 4: Unit Tests
```bash
python main.py --mode test
# or
python -m pytest tests/ -v
```

### What success looks like

- Terminal prints `Mission success : True` and `Goal reached successfully!`
- `outputs/path_plot.png` shows a clear yellow path from green start to red goal
- `outputs/navigation_demo.gif` shows the robot moving along the path
- All 5 tests pass

---

## Simulation Workflow

The simulation uses a **custom-built pygame environment** — no external simulator installation needed. Here's the step-by-step of what happens when you run it:

### Step 1: World creation
`GridMap.build_demo_map()` creates a 30x20 grid with warehouse-style walls and 25 scattered obstacles. Start is at the top-left, goal at the bottom-right.

### Step 2: Initial path planning
A\* runs on the known (static) map and computes a 28-step path from start to goal. This path may pass through cells that hide obstacles the robot hasn't detected yet.

### Step 3: Sensor scan
At each step, the simulated LiDAR casts 8 rays from the robot's current position. Each ray travels up to 6 cells and reports the first obstacle it hits.

### Step 4: Perception update
Newly discovered obstacles are merged into the `known_obstacles` set. The perception module checks whether any of these sit on the remaining path.

### Step 5: Reactive re-planning
If the path is blocked, A\* re-plans from the robot's **current position** to the goal, treating all known obstacles as off-limits. The robot seamlessly switches to the new path.

### Step 6: Movement
The robot advances one cell along the path. The trail is logged for visualization.

### Step 7: Goal check
The loop repeats until the robot reaches the goal cell or no valid path exists.

### Step 8: Visualization
- **pygame**: renders grid, obstacles, sensor rays, path, robot, and HUD in real time
- **matplotlib**: saves static PNG and animated GIF for documentation

---

## Results

| Metric | Value |
|--------|-------|
| Grid size | 30 x 20 cells |
| Total obstacles | ~35 (walls + scattered) |
| Sensor range | 6 cells, 8 directions |
| Path length | ~28 steps |
| Replans (typical run) | 0-3 |
| Mission success rate | 100% (with valid maps) |
| Tests | 5 / 5 passing |

The robot consistently reaches the goal while discovering and avoiding obstacles it didn't know about at the start — demonstrating true autonomous reactive navigation.

---

## Screenshots

### Path Planning Output
![Path Planning](outputs/path_plot.png)

### Animated Navigation Demo
![Navigation Demo](outputs/navigation_demo.gif)

> If the images don't load above, run `python main.py --mode run` and `python main.py --mode animate` to generate them, then commit the outputs.

---

## Learning Outcomes

By building this project you will demonstrate understanding of:

- **Autonomous system architecture** — the sense-plan-act loop used across the robotics and AV industry
- **A\* path planning** — one of the most widely used graph search algorithms in robotics and game AI
- **Sensor modeling** — how LiDAR/rangefinder sensors work and how to simulate them
- **Reactive re-planning** — handling dynamic obstacles in real time
- **Computer vision basics** — OpenCV contour-based object detection on grid data
- **Simulation environments** — building a virtual testbed without hardware
- **Software engineering practices** — modular code, unit tests, configuration management, documentation
- **Data visualization** — matplotlib animation and real-time pygame rendering

---

## Future Improvements

- **Real-time camera input** — replace the simulated sensor with a webcam feed and real computer vision
- **ROS/ROS2 integration** — port the pipeline to the Robot Operating System for real-robot compatibility
- **CARLA integration** — upgrade to the CARLA autonomous driving simulator for 3D realistic scenarios
- **Lane detection** — add OpenCV-based lane detection for road-following scenarios
- **Reinforcement learning** — train an RL agent to learn navigation policies instead of hard-coded A\*
- **SLAM** — implement Simultaneous Localization and Mapping for unknown environments
- **Multi-agent** — coordinate multiple robots on the same grid
- **Dijkstra / RRT / BFS comparison** — add multiple planners and benchmark them
- **Drone navigation** — extend to 3D path planning for UAV scenarios
- **Cloud dashboard** — stream navigation data to a web dashboard for remote monitoring

---

## Author

**Your Name**
- GitHub: [https://github.com/your-username](https://github.com/your-username)
- LinkedIn: [https://linkedin.com/in/your-name](https://linkedin.com/in/your-name)
- Email: your.email@example.com

> Replace the above with your real links before pushing to GitHub.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```
