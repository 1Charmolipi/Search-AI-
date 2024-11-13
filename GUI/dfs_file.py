import time
import tracemalloc

# Đọc file input
def read_input_dfs(input):
    with open(input, 'r') as file:
        lines = file.readlines()
    
    # Lưu trọng lượng viên đá
    weight = list(map(int, lines[0].strip().split()))
    
    # Lưu mê cung
    maze = [list(line.rstrip()) for line in lines[1:]]
    
    # Tìm vị trí của Ares, viên đá và công tắc
    ares_pos = None
    stone_pos = []
    switch_pos = set()
    
    for i, row in enumerate(maze):
        for j, find in enumerate(row):
            if find == '@':
                ares_pos = (i, j)
            elif find == '$':
                stone_pos.append((i, j))
            elif find == '.':
                switch_pos.add((i, j))
            elif find == '*': 
                stone_pos.append((i, j))
                switch_pos.add((i, j))
            elif find == '+':
                ares_pos = (i, j)
                switch_pos.add((i, j))
    
    return weight, maze, ares_pos, stone_pos, switch_pos

# Hàm DFS
def dfs(start, goal, get_neighbors):
    stack = [(start, "", 0)] 
    visited = set()
    visited.add(start)
    count_node = 0
    start_time = time.perf_counter()  
    tracemalloc.start()
    
    while stack:
        cur_state, actions, total_weight = stack.pop()
        count_node += 1
        
        # Kiểm tra viên đá đã tới công tắc chưa
        if cur_state[1] == goal[1]:
            end_time = time.perf_counter()
            current, memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return actions, total_weight, count_node, (end_time - start_time) * 10**3, memory / 10**6
        
        for neighbor, action, weight in get_neighbors(cur_state):
            if neighbor not in visited:
                visited.add(neighbor)
                new_weight = total_weight + weight 
                stack.append((neighbor, actions + action, new_weight))
    
    end_time = time.perf_counter()
    current, memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return None, total_weight, count_node, (end_time - start_time) * 10**3, memory / 10**6

# Hàm tìm các node liền kề
def get_neighbors_dfs(state, maze, weight):
    neighbors = []
    ares_pos, stone_pos = state
    directions = [(-1, 0, 'u', 'U'), (1, 0, 'd', 'D'), (0, -1, 'l', 'L'), (0, 1, 'r', 'R')]
    
    for dx, dy, move, push in directions:
        new_pos = (ares_pos[0] + dx, ares_pos[1] + dy)
        
        # Ares di chuyển mà không đẩy đá
        if is_valid_dfs(new_pos, stone_pos, maze):
            neighbors.append(((new_pos, stone_pos), move, 0))
        
        # Ares cần đẩy đá
        if new_pos in stone_pos:
            new_stone_position = (new_pos[0] + dx, new_pos[1] + dy)
            if is_valid_dfs(new_stone_position, stone_pos, maze):
                new_stone_pos = set(stone_pos)
                new_stone_pos.remove(new_pos)
                new_stone_pos.add(new_stone_position)
                stone_weight = get_weight(new_pos, stone_pos, weight)
                neighbors.append(((new_pos, frozenset(new_stone_pos)), push, stone_weight))
    
    return neighbors

# Hàm lấy trọng lượng viên đá
def get_weight(pos, stone_pos, weight):
    stone_list = list(stone_pos)
    index = stone_list.index(pos)
    return weight[index]

# Hàm để xác định xem vị trí có thỏa mãn maze không
def is_valid_dfs(pos, stone_pos, maze):
    x, y = pos
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[x]):
        return False
    if maze[x][y] == '#':
        return False
    if pos in stone_pos:
        return False
    return True

# Ghi kết quả vào file output
# Ghi kết quả vào file output
def write_output_dfs(output, name, path, steps, total_weight, count_node, time, memory):
    with open(output,'a') as file:
        if path:
            file.write(f"{name}\n")
            file.write(f'Steps: {steps}, Weight: {total_weight}, Nodes: {count_node},')
            file.write(f' Time (ms): {round(time, 2)}, Memory (MB): {round(memory, 2)}\n')
            file.write(f'{path}\n')
        else:
            file.write(f"No path found")
        
# Hàm main
def DFS(input,output):
    weight, maze, ares_pos, stone_pos, switch_pos = read_input_dfs(input)
    start = (ares_pos, frozenset(stone_pos))
    goal = (ares_pos, frozenset(switch_pos))
    
    # Thuật toán DFS
    path, total_weight, count_node, time, memory = dfs(
        start, goal, lambda state: get_neighbors_dfs(state, maze, weight)
    )
    
    if path:
        steps = len(path)
        write_output_dfs(output, "DFS", path, steps, total_weight, count_node, time, memory)
    else:
        write_output_dfs(output, "DFS", path, 0, total_weight, count_node, time, memory)
        


