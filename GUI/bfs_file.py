import time
import tracemalloc
from collections import deque

class Stone:
    def __init__(self, position, weight):
        self.position = position
        self.weight = weight

# Đọc file input
def read_input_bfs(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
    # Lưu trọng lượng viên đá
    weights = list(map(int, lines[0].strip().split()))
    
    # Lưu mê cung
    maze = [list(line.rstrip()) for line in lines[1:]]
    
    # Tìm vị trí của Ares, viên đá và công tắc
    stones = []
    ares_pos = None
    switch_pos = set()
    
    stone_index = 0
    for i, row in enumerate(maze):
        for j, find in enumerate(row):
            if find == '@':
                ares_pos = (i, j)
            elif find == '$':
                stones.append(Stone((i, j), weights[stone_index]))
                stone_index += 1
            elif find == '.':
                switch_pos.add((i, j))
            elif find == '*':  
                stones.append(Stone((i, j), weights[stone_index]))
                stone_index += 1
                switch_pos.add((i, j))
            elif find == '+':
                ares_pos = (i, j)
                switch_pos.add((i, j))

    return maze, ares_pos, stones, switch_pos


def bfs(start, goal, get_neighbors, maze):
    queue = deque([(start, "", 0)])
    visited = set()
    visited.add((start[0], tuple((stone.position, stone.weight) for stone in start[1])))
    count_node = 0
    start_time = time.perf_counter()
    tracemalloc.start()
    
    while queue:
        cur_state, actions, total_weight = queue.popleft()
        count_node += 1
        
        ares_pos, stones = cur_state
        
        # Điều kiện dừng: tất cả viên đá đã tới công tắc
        if all(stone.position in goal for stone in stones):
            end_time = time.perf_counter()
            current, memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return actions, total_weight, count_node, (end_time - start_time) * 10**3, memory / 10**6
        
        for neighbor, action, weight in get_neighbors(cur_state, maze):  
            state_key = (neighbor[0], tuple((stone.position, stone.weight) for stone in neighbor[1]))
            if state_key not in visited:
                visited.add(state_key)
                new_weight = total_weight + weight
                
                queue.append((neighbor, actions + action, new_weight))
    
    end_time = time.perf_counter()
    current, memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return None, total_weight, count_node, (end_time - start_time) * 10**3, memory / 10**6


# Tìm các node liền kề
def get_neighbors_bfs(state, maze):
    neighbors = []
    ares_pos, stones = state
    directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]
    
    for dx, dy, move, push in directions:
        new_pos = (ares_pos[0] + dx, ares_pos[1] + dy)
        
        # Ares di chuyển mà không đẩy đá
        if is_valid_bfs(new_pos, [stone.position for stone in stones], maze):
            neighbors.append(((new_pos, stones), move, 0))
        
        # Ares cần đẩy đá
        for stone in stones:
            if stone.position == new_pos:
                new_stone_position = (new_pos[0] + dx, new_pos[1] + dy)
                if is_valid_bfs(new_stone_position, [s.position for s in stones], maze):
                    new_stones = update_stone_pos(stones, stone.position, new_stone_position)
                    neighbors.append(((new_pos, new_stones), push, stone.weight)) 
    
    return neighbors



def update_stone_pos(stones, old_position, new_position):
    new_stones = [Stone(stone.position, stone.weight) for stone in stones] 
    for stone in new_stones:
        if stone.position == old_position:
            stone.position = new_position 
            break
    return new_stones



# Hàm để xác định xem vị trí có thỏa mãn maze không
def is_valid_bfs(pos, stone_pos, maze):
    x, y = pos
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[x]):
        return False
    if maze[x][y] == '#':
        return False
    if pos in stone_pos:
        return False
    return True

# Ghi kết quả vào file output
def write_output_bfs(output, name, path, steps, total_weight, count_node, time, memory):
    with open(output,'a') as file:
        if path:
            file.write(f"{name}\n")
            file.write(f'Steps: {steps}, Weight: {total_weight}, Nodes: {count_node},')
            file.write(f' Time (ms): {round(time, 2)}, Memory (MB): {round(memory, 2)}\n')
            file.write(f'{path}\n')
        else:
            file.write(f"No path found")

def BFS(input,output):
    maze, ares_pos, stones, switch_positions = read_input_bfs(input)
    start = (ares_pos, stones)
    goal = switch_positions
    # Chạy thuật toán BFS với maze được truyền vào như tham số
    path, total_weight, count_node, time, memory = bfs(start, goal, get_neighbors_bfs, maze)
    if path:
        steps = len(path)
        write_output_bfs(output, "BFS", path, steps, total_weight, count_node, time, memory)
    else:
        write_output_bfs(output, "BFS", path, 0 , total_weight, count_node, time, memory)

