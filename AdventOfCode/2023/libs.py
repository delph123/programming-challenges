import sys

# HACK: Add root repository directory in the path to be able to
# load libraries in case the scripts are not called as a module
sys.path.append(__file__[: __file__.index("AdventOfCode") - 1])

from lib.aoc import *
