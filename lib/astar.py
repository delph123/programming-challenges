from abc import ABC, abstractmethod
from typing import Dict, Iterable, TypeVar, Generic
from .priorityq import MappedQueue

T = TypeVar("T")
C = TypeVar("C")  # type of cost
H = TypeVar("H")  # type of heuristic


class AStarNode(Generic[T]):
    """Represent a node manipulated by the A* algorithm."""

    def __init__(
        self, node: T, predecessor: "AStarNode[T]", cost: C, heuristic: H
    ) -> None:
        self.node = node
        self.cost = cost
        self.heuristic = heuristic
        self.predecessors = [predecessor] if predecessor is not None else []
        self.closed = False

    def __lt__(self, b: "AStarNode[T]") -> bool:
        """Nodes must be comparable on their heuristic value"""
        return self.heuristic < b.heuristic


class AStarSolution(Generic[T]):
    """Represent the solution to the A* algorithm."""

    def __init__(self, goal: AStarNode[T], explored: Dict[T, AStarNode[T]]):
        self.goal = goal
        self.explored = explored

    def reversed_path(self):
        current = self.goal
        while current:
            yield current.node
            current = current.predecessors[0] if current.predecessors else None

    def path(self):
        return reversed(list(self.reversed_path()))

    def cost(self):
        return self.goal.cost


class AStar(ABC, Generic[T]):
    @abstractmethod
    def heuristic_cost_estimate(self, current: T, cost: C, goal=None) -> H:
        """
        Computes the estimated (rough) distance between a node and the goal.
        The second parameter is the cost from the start to the node.
        This method must be return the estimated cost to the goal.
        heuristic = distance(current, goal) + cost
        """
        raise NotImplementedError

    @abstractmethod
    def cost_between(self, n1: T, n2: T) -> C:
        """
        Gives the real distance between two adjacent nodes n1 and n2 (i.e n2
        belongs to the list of n1's neighbors).
        n2 is guaranteed to belong to the list returned by the call to neighbors(n1).
        This method must return the real cost of traveling to n2 through n1:
        cost = n1_cost + distance(n1, n2)
        """
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, node: T) -> Iterable[T]:
        """
        For a given node, returns (or yields) the list of its neighbors.
        This method must be implemented in a subclass.
        """
        raise NotImplementedError

    def is_goal_reached(self, current: T, goal=None) -> bool:
        """
        Returns true when we can consider that 'current' is the goal.
        The default implementation simply compares `current == goal`, but this
        method can be overwritten in a subclass to provide more refined checks.
        """
        return current == goal

    def solve(self, start: T, goal=None):

        start_node = AStarNode(
            start,
            predecessor=None,
            cost=0,
            heuristic=self.heuristic_cost_estimate(start, 0, goal),
        )

        visited = {start: start_node}
        candidates = MappedQueue([start_node])

        while candidates:
            current = candidates.pop()

            if self.is_goal_reached(current.node, goal):
                return AStarSolution(current, visited)

            # For debug purpose only, we still visit closed nodes
            # to compute predecessors
            current.closed = True

            for neighbor in self.neighbors(current.node):
                explored = neighbor in visited

                cost = current.cost + self.cost_between(current.node, neighbor)
                heuristic = self.heuristic_cost_estimate(neighbor, cost, goal)

                if not explored:
                    visited[neighbor] = AStarNode(neighbor, current, cost, heuristic)
                    candidates.push(visited[neighbor])
                    continue

                neighbor_node = visited[neighbor]

                if explored and heuristic < neighbor_node.heuristic:
                    neighbor_node.cost = cost
                    neighbor_node.heuristic = heuristic
                    neighbor_node.predecessors = [current]
                    candidates.update(neighbor_node, neighbor_node)
                elif explored and heuristic == neighbor_node.heuristic:
                    neighbor_node.predecessors.append(current)

        return None
