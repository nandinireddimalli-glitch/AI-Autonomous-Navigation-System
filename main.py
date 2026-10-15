#!/usr/bin/env python3
"""
AI-Based Autonomous Navigation System - main entry point.

Usage examples
--------------
Interactive pygame simulator:
    python main.py --mode sim

Headless navigation run (prints status + saves a path PNG):
    python main.py --mode run

Generate an animated GIF of a full mission (great for GitHub):
    python main.py --mode animate --out outputs/navigation_demo.gif

Run unit tests:
    python main.py --mode test
"""
from __future__ import annotations

import argparse
import os
import sys

# Make ``src`` importable when running this file directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import GRID_H, GRID_W, SENSOR_RANGE
from src.grid_map import GridMap
from src.navigator import Navigator
from src.visualizer import save_path_plot, animate_run


def run_headless() -> int:
    """Run one mission without any GUI and save a static path image."""
    grid = GridMap(GRID_W, GRID_H)
    grid.build_demo_map()
    nav = Navigator(grid, sensor_range=SENSOR_RANGE)

    success = nav.run_until_done(max_steps=400)

    out_path = os.path.join("outputs", "path_plot.png")
    os.makedirs("outputs", exist_ok=True)
    save_path_plot(grid, nav.robot.path, out_path, visited=nav.visited_cells)

    status = nav.status()
    print("\n==============================")
    print(" AI AUTONOMOUS NAVIGATION - RUN COMPLETE")
    print("==============================")
    print(f"  Mission success : {status['success']}")
    print(f"  Steps taken     : {status['steps']}")
    print(f"  Replans         : {status['replans']}")
    print(f"  Obstacles known : {status['obstacles_known']}")
    print("  Event log:")
    for line in status["log"]:
        print(f"    - {line}")
    print(f"  Path image saved: {out_path}")
    print("==============================\n")
    return 0 if success else 1


def run_sim() -> int:
    from src.simulation import Simulator
    sim = Simulator()
    sim.run()
    return 0


def run_animate(out_path: str) -> int:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    animate_run(out_path)
    return 0


def run_tests() -> int:
    import pytest
    return pytest.main(["-q", os.path.join(os.path.dirname(__file__), "tests")])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AI-Based Autonomous Navigation System")
    parser.add_argument("--mode", default="sim",
                        choices=["sim", "run", "animate", "test"],
                        help="sim = pygame window, run = headless, "
                             "animate = GIF, test = unit tests")
    parser.add_argument("--out", default="outputs/navigation_demo.gif",
                        help="output path for animate mode")
    args = parser.parse_args()

    if args.mode == "sim":
        return run_sim()
    if args.mode == "run":
        return run_headless()
    if args.mode == "animate":
        return run_animate(args.out)
    if args.mode == "test":
        return run_tests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
