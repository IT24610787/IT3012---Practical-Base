# agent.py
import heapq
import math
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

# Added by IT24610787 for Lab3 & modified for Lab4
class SearchAgent:
    """Problem-Solving Agent implementing BFS, DFS and UCS"""

    def __init__(self):
        self.plan = []               # offline plan: list of actions still to execute
        self.active_algo = 'BFS'     # 'BFS', 'DFS', 'UCS' or 'AStar'
        self.heuristic_type = 'manhattan'   # used by A*: 'manhattan' or 'euclidean'

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

    # Lab 4, Step 1.1 - heuristic functions
    def manhattan_distance(self, pos, goal):
        """h(n) = |x1 - x2| + |y1 - y2|"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)"""
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

    # Lab 4, Step 1.2 - A* search
    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        width, height = grid_size
        wall_set = set(walls)

        if heuristic_type == 'manhattan':
            heuristic = self.manhattan_distance
        elif heuristic_type == 'euclidean':
            heuristic = self.euclidean_distance
        else:
            raise ValueError(f"Unknown heuristic '{heuristic_type}'. Use 'manhattan' or 'euclidean'.")

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0)),
        ]

        reached_states = set()

        # Tuple format: (f_cost, g_cost, current_pos, path_taken)
        h_start = heuristic(start_pos, goal_pos)
        frontier = [(0 + h_start, 0, start_pos, [])]

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)

            if current_pos == goal_pos:
                return path_taken

            # The same cell can be pushed more than once; skip stale copies
            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)

            curr_x, curr_y = current_pos
            for action_name, (dx, dy) in directions:
                nx, ny = curr_x + dx, curr_y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height:
                    if next_pos not in wall_set and next_pos not in reached_states:
                        g_new = g_cost + 1
                        h_new = heuristic(next_pos, goal_pos)
                        f_new = g_new + h_new
                        heapq.heappush(frontier, (f_new, g_new, next_pos, path_taken + [action_name]))

        return None

    def _make_plan(self, percept: dict) -> list:
        """Pick the closest food (Manhattan distance) and search for a path to it."""
        searches = {
            'BFS': self.bfs_search,
            'DFS': self.dfs_search,
            'UCS': self.ucs_search,
            'AStar': lambda s, g, w, gs: self.astar_search(s, g, w, gs, self.heuristic_type),
        }
        if self.active_algo not in searches:
            raise ValueError(f"Unknown algorithm '{self.active_algo}'. Use 'BFS', 'DFS', 'UCS' or 'AStar'.")
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

if __name__ == "__main__":
    # Lab 4 - Step 1.1 testing checkpoint
    _agent = SearchAgent()
    print("Manhattan:", _agent.manhattan_distance((0, 0), (3, 4)))   # expected 7
    print("Euclidean:", _agent.euclidean_distance((0, 0), (3, 4)))   # expected 5.0