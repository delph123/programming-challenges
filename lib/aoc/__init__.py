# Import some utilities
from lib.tools import *
from lib.math import *
from lib.grid import Point, Grid
from lib.graph import Graph, group_adjacent, adjacent
from lib.astar import AStar

# Import advent of code tooling
from lib.aoc.printing import part_one, part_two, preview, print_error
from lib.aoc.parsing import read, read_lines, read_grid, create_matcher

# Useful tools from standard library
import re
from collections import deque, Counter, defaultdict
from itertools import count, accumulate, batched, groupby, islice, pairwise, zip_longest
from itertools import product, permutations, combinations, combinations_with_replacement
from functools import cache, reduce, cmp_to_key, partial
from operator import itemgetter, attrgetter
from math import sqrt, prod, floor, ceil, copysign, gcd
from hashlib import md5
from dataclasses import dataclass
from copy import deepcopy
