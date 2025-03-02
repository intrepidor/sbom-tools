#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Template Python Script
Author: Your Name
Date: YYYY-MM-DD
Description: Brief description of what this script does.
"""

import sys

# a dict with 10 elements, each containing a key named after a fruit, and a value indicating the color of the fruit
fruits = {
    "apple": "red",
    "banana": "yellow",
    "cherry": "red",
    "grape": "purple",
    "kiwi": "green",
    "lemon": "yellow",
    "lime": "green",
    "orange": "orange",
    "pear": "green",
    "strawberry": "red"
}

# A CyloneDX JSON structure encoded into a Python dictionary. The structure contains a list of components, each with a type, name, and version.
cyclonedx = {
    "components": [
        {
            "type": "library",
            "name": "requests",
            "version": "2.26.0"
        },
        {
            "type": "library",
            "name": "flask",
            "version": "2.0.1"
        },
        {
            "type": "library",
            "name": "sqlalchemy",
            "version": "1.4.23"
        }
    ]
}




# A function that accepts a string indicating the color of a fruit and returns a tuple containing each fruit with that color.
def get_fruit_by_color(color):
    """
    Get fruit by color
    """
    return tuple(fruit for fruit, fruit_color in fruits.items() if fruit_color == color)


if __name__ == "__main__":
    print(get_fruit_by_color("green"))
