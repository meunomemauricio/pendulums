"""Simple Example Pymunk + Pyglet Application."""

import time

import pymunk


def main():
    space = pymunk.Space()
    space.gravity = 0, -1000

    body = pymunk.Body(mass=1, moment=1666)
    body.position = 50, 100  # x, y

    space.add(body)

    try:
        while True:
            space.step(0.02)  # 1/50 (50 FPS)
            print(body.position)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Canceled.")
