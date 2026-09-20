# agent.py
import heapq
import random

from collections import deque

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

# Added by IT2460787
class SimpleReflexAgent:
    
    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here') or percept.get('smells_food'):
            return 'Suck'
        elif percept.get('wall_ahead'):
            return 'Left'
        else:
            return 'Up'

# Added by IT24610787 for Lab3
class SearchAgent:
    """Problem-Solving Agent implementing BFS, DFS and UCS"""

    def __init__(self):
        self.plan = []               # offline plan: list of actions still to execute
        self.active_algo = 'BFS'     # 'BFS', 'DFS' or 'UCS'

    def bfs_search(self, start_pos: tuple, goal_pos: tuple, walls: list, grid_size: tuple):
        width, height = grid_size
        wall_set = set(walls)

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        queue = deque([(start_pos, [])])
        reached = {start_pos}

        while queue:
            (curr_x, curr_y), path = queue.popleft()

            if (curr_x, curr_y) == goal_pos:
                return path

            for action_name, (dx, dy) in directions:
                nx, ny = curr_x + dx, curr_y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height:
                    if next_pos not in wall_set and next_pos not in reached:
                        reached.add(next_pos)
                        queue.append((next_pos, path + [action_name]))

        return None

    def dfs_search(self, start_pos: tuple, goal_pos: tuple, walls: list, grid_size: tuple):
        width, height = grid_size
        wall_set = set(walls)

        directions = [
            ('Up', (0,1)),
            ('Down', (0,-1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0)),
        ]

        stack = [(start_pos, [])]
        reached = {start_pos}

        while stack:
            (curr_x, curr_y), path = stack.pop()

            if(curr_x, curr_y) == goal_pos:
                return path

            for action_name, (dx, dy) in directions:
                nx, ny = curr_x + dx, curr_y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height:
                    if next_pos not in wall_set and next_pos not in reached:
                        reached.add(next_pos)
                        stack.append((next_pos, path + [action_name]))

        return None

    def ucs_search(self, start_pos: tuple, goal_pos: tuple, walls: list, grid_size: tuple):
        width, height = grid_size
        wall_set = set(walls)

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0)),
        ]

        step_cost = 1      # every move costs 1 in this grid
        order = 0          # tie-breaker so heapq never has to compare paths

        # Frontier is a priority queue ordered by g(n) = total path cost so far
        frontier = [(0, order, start_pos, [])]
        # reached maps each state to the cheapest cost found so far
        reached = {start_pos: 0}

        while frontier:
            cost, _, (curr_x, curr_y), path = heapq.heappop(frontier)

            if (curr_x, curr_y) == goal_pos:
                return path

            # Skip stale entries (a cheaper route to this cell was found later)
            if cost > reached[(curr_x, curr_y)]:
                continue

            for action_name, (dx, dy) in directions:
                nx, ny = curr_x + dx, curr_y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height and next_pos not in wall_set:
                    new_cost = cost + step_cost
                    if next_pos not in reached or new_cost < reached[next_pos]:
                        reached[next_pos] = new_cost
                        order += 1
                        heapq.heappush(frontier, (new_cost, order, next_pos, path + [action_name]))

        return None

    def _make_plan(self, percept: dict) -> list:
        """Pick the closest food (Manhattan distance) and search for a path to it."""
        searches = {
            'BFS': self.bfs_search,
            'DFS': self.dfs_search,
            'UCS': self.ucs_search,
        }
        if self.active_algo not in searches:
            raise ValueError(f"Unknown algorithm '{self.active_algo}'. Use 'BFS', 'DFS' or 'UCS'.")
        search = searches[self.active_algo]

        start = tuple(percept['agent_pos'])
        walls = percept['walls']
        grid_size = percept['grid_size']
        foods = [tuple(f) for f in percept['all_food']]

        # Closest first; if that food is unreachable, fall back to the next closest
        for goal in sorted(foods, key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1])):
            path = search(start, goal, walls, grid_size)
            if path:
                return path
        return []

    def sense_and_act(self, percept: dict) -> str:
        # Only plan when the previous plan has been fully executed
        if not self.plan:
            self.plan = self._make_plan(percept)

        if not self.plan:
            return 'Stay'   # no food left, or none reachable

        return self.plan.pop(0)