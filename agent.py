# agent.py
import random

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

# Added by IT24610787
class ModelBasedAgent:

    def __init__(self):
        self.last_percept = None
        self.last_action = None
        self.actions_pool = ['Up', 'Right', 'Down', 'Left']
        self.action_index = 0

    def sense_and_act(self, percept: dict) -> str:
        is_stuck_in_loop = (self.last_percept == percept)
        
        if percept.get('food_here'):
            action = 'Suck'
        elif percept.get('wall_ahead') or is_stuck_in_loop:
            self.action_index = (self.action_index + 1) % len(self.actions_pool)
            action = self.actions_pool[self.action_index]
        else:
            action = self.actions_pool[self.action_index]

        self.last_percept = dict(percept)
        self.last_action = action
        
        return action

# Added by IT24610787 as a placeholder until Lab3
class SearchAgent:
    """Problem-Solving Agent implementing Breadth-First Search (BFS)."""

    def bfs_search(self, start_pos: tuple, goal_pos: tuple, walls: list, grid_size: tuple):
        width, height = grid_size
        wall_set = set(walls)

        directions = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        queue = [(start_pos, [])]
        visited = {start_pos}

        while queue:
            (curr_x, curr_y), path = queue.pop(0)

            if (curr_x, curr_y) == goal_pos:
                return path

            for action_name, (dx, dy) in directions:
                nx, ny = curr_x + dx, curr_y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height:
                    if next_pos not in wall_set and next_pos not in visited:
                        visited.add(next_pos)
                        queue.append((next_pos, path + [action_name]))

        return None