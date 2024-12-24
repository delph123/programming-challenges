# Import some utilities
from lib.tools import *
from lib.math import *
from lib.grid import Point, Grid
from lib.astar import AStar

# Import advent of code tooling
from lib.aoc.printing import part_one, part_two, preview
from lib.aoc.parsing import read, read_lines, read_grid

# Useful tools from standard library
import re
from collections import deque, Counter, defaultdict
from itertools import pairwise, groupby, combinations, product, zip_longest, batched
from functools import cache, reduce, cmp_to_key, partial
from math import sqrt, prod, floor, ceil
from copy import deepcopy
