import heapq
import math
from collections import defaultdict

class PathFinder:
    @staticmethod
    def astar(start, goal, passable_func, max_range=None, diagonal=True):
        def heuristic(a, b):
            return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if diagonal:
            neighbors += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        frontier = [(0, 0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        counter = 1
        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current == goal:
                break
            if max_range and cost_so_far[current] >= max_range:
                continue
            for dx, dy in neighbors:
                next_pos = (current[0] + dx, current[1] + dy)
                if not passable_func(next_pos[0], next_pos[1]):
                    continue
                move_cost = 1.414 if dx != 0 and dy != 0 else 1.0
                new_cost = cost_so_far[current] + move_cost
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    counter += 1
                    heapq.heappush(frontier, (priority, counter, next_pos))
                    came_from[next_pos] = current
        if goal not in came_from:
            return None
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
    
    @staticmethod
    def bfs(start, passable_func, max_range):
        from collections import deque
        visited = set([start])
        queue = deque([(start, 0)])
        reachable = set()
        while queue:
            pos, dist = queue.popleft()
            if dist >= max_range:
                continue
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                new_pos = (pos[0]+dx, pos[1]+dy)
                if new_pos not in visited and passable_func(new_pos[0], new_pos[1]):
                    visited.add(new_pos)
                    queue.append((new_pos, dist+1))
                    reachable.add(new_pos)
        return reachable

pathfinder = PathFinder()