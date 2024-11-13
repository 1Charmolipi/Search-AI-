import pygame, sys
import heapq
from pygame.locals import *
import time
import threading
import os
import tracemalloc
from collections import deque
import bfs_file
import dfs_file
import a_file
import ucs_file
#file in và out chung cho các thuật toán
input = 'input-01.txt'
output = 'output-01.txt'
algorithm = 'bfs'
speed = 1000
total_weight_gui = 0
state_pause = 'pausing'
highlight_input = 1
algorithm_running = True
x2 = 1
# Hàm đọc file input
def read_file_to_2d_array(filename):
        x = []
        try:
            with open(filename, 'r') as file:
                # Bỏ qua dòng đầu tiên
                file.readline()
                # Đọc phần còn lại của file và lưu vào mảng 2 chiều
                for line in file:
                    # Thay khoảng trắng bằng '0' và lưu từng dòng vào mảng
                    row = [char if char != ' ' else '0' for char in line.rstrip()]
                    x.append(row)
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except IOError:
            print("An error occurred while reading the file.")
        return x 
# Hàm in mảng cho dễ kiểm tra
def print_array(a):
    for row in a:
        print(' '.join(str(cell) for cell in row))
    print()  # Dòng trống để ngăn cách mỗi lần in
#==============================TẤT CẢ HÀM NÀY PHỤC VỤ CHO HÀM GUI()==================================================================
# Hàm vẽ map
def default_map(input,num,arr_input):
            x = [
                    [0, 0, 0, 'in1', 'in2', 'in3', 'in4', 'in5', 'in6', 'in7', 'in8', 'in9','in10', 0, 'x2', 0, 'c', 0, 'r', 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ] +[
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ] +[
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ] +[
                    ['bfs', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ]+[
                    ['dfs', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ] +[
                    ['ucs', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ] +[
                    ['a_star', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0],  # Hàng đầu tiên
                ] + [[0] * 36 for _ in range(15)]  # 12 hàng còn lại, mỗi hàng có 26 cột
            
            f_highlight_input(x,num,arr_input)
            # Gọi hàm và in kết quả
            b = read_file_to_2d_array(input)
            print_array(b)
            # Sửa lại mảng b trước khi dán vào a
            # Xử lý mảng b
            c = [] # mảng c là mảng sau khi sửa của b
            for line in b:
                # Chuyển danh sách thành chuỗi
                line_string = ''.join(line)
                # Nếu có "#" ở đầu và cuối dòng, thay thế tất cả các 0 giữa chúng bằng 1
                if line_string.startswith('#') and line_string.endswith('#'):
                    line_string = line_string.replace('0', '1')  # Thay thế 0 bằng 1
                c.append(line_string)
            
            print_array(c)
            # Kích thước của mảng c
            rows_c = len(c)
            cols_c = len(c[0]) if rows_c > 0 else 0

            # Vị trí bắt đầu trong mảng a
            start_row = 3
            start_col = 3

            # Thay thế phần tử trong mảng a bằng phần tử trong mảng c
            for i in range(rows_c):
                for j in range(cols_c):
                    # Kiểm tra nếu vị trí không vượt quá kích thước của mảng a
                    # if start_row + i < len(x) and start_col + j < len(x[start_row]):
                        x[start_row + i][start_col + j] = c[i][j]
            return x
 
#Hàm đặt highlight cho input khi vẽ map
def f_highlight_input(x,num,arr_input):
    x[0][3]='in1'
    x[0][4]='in2'
    x[0][5]='in3'
    x[0][6]='in4'
    x[0][7]='in5'
    x[0][8]='in6'
    x[0][9]='in7'
    x[0][10]='in8'
    x[0][11]='in9'
    x[0][12]='in10'
    
    x[0][num+2]=arr_input[num-1]
 #Hàm vẽ map cho gui
def draw_map(a,DISPLAYSURF, TILESIZE):
    # Tải hình ảnh cho các đối tượng
    nen_img = pygame.image.load("./image/wall.jpg").convert() # nền đen
    gach_img = pygame.image.load("./image/gach.jpg").convert() # gạch nâu
    dat_img = pygame.image.load("./image/dat.jpg").convert() # nền trắng
    da_img = pygame.image.load("./image/da.jpg").convert() # đá
    nv_img = pygame.image.load("./image/nv.jpg").convert() # nhân vật
    den_img =  pygame.image.load("./image/den.jpg").convert() # đích đến
    pause_img =  pygame.image.load("./image/pausing.jpg").convert() # đích đến
    play_img =  pygame.image.load("./image/playing.jpg").convert() # đích đến
    reset_img = pygame.image.load("./image/reset.jpg").convert() # reset
    
    in1_img = pygame.image.load("./image/1.jpg").convert() # trungtam
    in2_img = pygame.image.load("./image/2.jpg").convert() # trungtam
    in1_hover_img = pygame.image.load("./image/1_hover.jpg").convert() # trungtam
    in2_hover_img = pygame.image.load("./image/2_hover.jpg").convert() # trungtam
    in3_img = pygame.image.load("./image/3.jpg").convert() # trungtam
    in4_img = pygame.image.load("./image/4.jpg").convert() # trungtam
    in3_hover_img = pygame.image.load("./image/3_hover.jpg").convert() # trungtam
    in4_hover_img = pygame.image.load("./image/4_hover.jpg").convert() # trungtam
    in5_img = pygame.image.load("./image/5.jpg").convert() # trungtam
    in6_img = pygame.image.load("./image/6.jpg").convert() # trungtam
    in5_hover_img = pygame.image.load("./image/5_hover.jpg").convert() # trungtam
    in6_hover_img = pygame.image.load("./image/6_hover.jpg").convert() # trungtam
    in7_img = pygame.image.load("./image/7.jpg").convert() # trungtam
    in8_img = pygame.image.load("./image/8.jpg").convert() # trungtam
    in7_hover_img = pygame.image.load("./image/7_hover.jpg").convert() # trungtam
    in8_hover_img = pygame.image.load("./image/8_hover.jpg").convert() # trungtam
    in9_img = pygame.image.load("./image/9.jpg").convert() # trungtam
    in10_img = pygame.image.load("./image/10.jpg").convert() # trungtam
    in9_hover_img = pygame.image.load("./image/9_hover.jpg").convert() # trungtam
    in10_hover_img = pygame.image.load("./image/10_hover.jpg").convert() # trungtam
    
    bfs_img = pygame.image.load("./image/BFS.jpg").convert() # trungtam
    dfs_img = pygame.image.load("./image/DFS.jpg").convert() # trungtam
    ucs_img = pygame.image.load("./image/UCS.jpg").convert() # trungtam
    a_img = pygame.image.load("./image/A.jpg").convert() # trungtam
    bfs_hover_img = pygame.image.load("./image/BFS_hover.jpg").convert() # trungtam
    dfs_hover_img = pygame.image.load("./image/DFS_hover.jpg").convert() # trungtam
    ucs_hover_img = pygame.image.load("./image/UCS_hover.jpg").convert() # trungtam
    a_hover_img = pygame.image.load("./image/A_hover.jpg").convert() # trungtam
    x2_img = pygame.image.load("./image/x2.jpg").convert() 

    pygame.display.set_caption("GUI SEARCH")
    for row in range(len(a)):  # Lặp qua tất cả các hàng trong mảng a
                for col in range(len(a[row])):  # Lặp qua tất cả các cột trong hàng hiện tại
                    tile = a[row][col]  # Lấy giá trị của ô hiện tại
                    x, y = col * TILESIZE, row * TILESIZE  # Tính toán vị trí vẽ
                    if tile == 0:
                        DISPLAYSURF.blit(nen_img, (x, y))
                    elif tile == '#':
                        DISPLAYSURF.blit(gach_img, (x, y))
                    elif tile == '0':  
                        DISPLAYSURF.blit(nen_img, (x, y))
                    elif tile == '$':
                        DISPLAYSURF.blit(da_img, (x, y))
                    elif tile == '@' or tile == '+':
                        DISPLAYSURF.blit(nv_img, (x, y))
                    elif tile == '.' or tile == '*': 
                        DISPLAYSURF.blit(den_img, (x, y))
                    elif tile == '1': 
                        DISPLAYSURF.blit(dat_img, (x, y))
                    elif tile == 'p': # p là pause
                        DISPLAYSURF.blit(pause_img, (x, y))
                    elif tile == 'c': # c là play
                        DISPLAYSURF.blit(play_img, (x, y))
                    elif tile == 'r': # r là reset
                        DISPLAYSURF.blit(reset_img, (x, y))
                    elif tile == 'in1': 
                        DISPLAYSURF.blit(in1_img, (x, y))
                    elif tile == 'in2': 
                        DISPLAYSURF.blit(in2_img, (x, y))
                    elif tile == 'in3': 
                        DISPLAYSURF.blit(in3_img, (x, y))
                    elif tile == 'in4': 
                        DISPLAYSURF.blit(in4_img, (x, y))
                    elif tile == 'in5': 
                        DISPLAYSURF.blit(in5_img, (x, y))
                    elif tile == 'in6': 
                        DISPLAYSURF.blit(in6_img, (x, y))
                    elif tile == 'in7': 
                        DISPLAYSURF.blit(in7_img, (x, y))
                    elif tile == 'in8': 
                        DISPLAYSURF.blit(in8_img, (x, y))
                    elif tile == 'in9': 
                        DISPLAYSURF.blit(in9_img, (x, y))
                    elif tile == 'in10': 
                        DISPLAYSURF.blit(in10_img, (x, y))
                    elif tile == 'in1_hover': 
                        DISPLAYSURF.blit(in1_hover_img, (x, y))
                    elif tile == 'in2_hover': 
                        DISPLAYSURF.blit(in2_hover_img, (x, y))
                    elif tile == 'in3_hover': 
                        DISPLAYSURF.blit(in3_hover_img, (x, y))
                    elif tile == 'in4_hover': 
                        DISPLAYSURF.blit(in4_hover_img, (x, y))
                    elif tile == 'in5_hover': 
                        DISPLAYSURF.blit(in5_hover_img, (x, y))
                    elif tile == 'in6_hover': 
                        DISPLAYSURF.blit(in6_hover_img, (x, y))
                    elif tile == 'in7_hover': 
                        DISPLAYSURF.blit(in7_hover_img, (x, y))
                    elif tile == 'in8_hover': 
                        DISPLAYSURF.blit(in8_hover_img, (x, y))
                    elif tile == 'in9_hover': 
                        DISPLAYSURF.blit(in9_hover_img, (x, y))
                    elif tile == 'in10_hover': 
                        DISPLAYSURF.blit(in10_hover_img, (x, y))
                    elif tile == 'bfs': 
                        DISPLAYSURF.blit(bfs_img, (x, y))
                    elif tile == 'dfs': 
                        DISPLAYSURF.blit(dfs_img, (x, y))
                    elif tile == 'ucs': 
                        DISPLAYSURF.blit(ucs_img, (x, y))
                    elif tile == 'a_star': 
                        DISPLAYSURF.blit(a_img, (x, y))
                    elif tile == 'bfs_hover': 
                        DISPLAYSURF.blit(bfs_hover_img, (x, y))
                    elif tile == 'dfs_hover': 
                        DISPLAYSURF.blit(dfs_hover_img, (x, y))
                    elif tile == 'ucs_hover': 
                        DISPLAYSURF.blit(ucs_hover_img, (x, y))
                    elif tile == 'a_hover': 
                        DISPLAYSURF.blit(a_hover_img, (x, y))
                    elif tile == 'x2': 
                        DISPLAYSURF.blit(x2_img, (x, y))

# Tìm vị trí của đá trong mảng a[]
def find_position_stone(a):
    # Tạo danh sách để lưu tọa độ của đá
    positions = []
    
    # Duyệt qua từng dòng trong mảng
    for i in range(len(a)):
        # Duyệt qua từng cột trong dòng hiện tại
        for j in range(len(a[i])):
            # Kiểm tra xem giá trị tại (i, j) có phải là '$' không
            if a[i][j] == '$':
                positions.append((i, j))  # Thêm tọa độ vào danh sách
    
    return positions  # Trả về danh sách tọa độ

# Hàm tìm tất cả vị trí của tất cả switch
def find_position_switch (a):
        # Tạo danh sách để lưu tọa độ của đá
    positions = []
    
    # Duyệt qua từng dòng trong mảng
    for i in range(len(a)):
        # Duyệt qua từng cột trong dòng hiện tại
        for j in range(len(a[i])):
            # Kiểm tra xem giá trị tại (i, j) có phải là '$' không
            if a[i][j] == '.' or a[i][j] == '*' or a[i][j] == '+':
                positions.append((i, j))  # Thêm tọa độ vào danh sách
    
    return positions  # Trả về danh sách tọa độ
          
    # Hàm trả về mảng vị trí các viên đá trong map a[]
# Hàm check xem Ares or Stone có đang đứng trên switch hay không 
def check_position(row,col,arr_position_switch):
    point =( row,col)
    if point in arr_position_switch:
        return True
    else:
        return False
def arr_stone_pos(a):
    # Tạo danh sách để lưu tọa độ của đá
    arr_stone_positions = []

    # Gọi hàm tìm tọa độ của đá
    coordinates = find_position_stone(a)

    # Thêm các cặp tọa độ vào danh sách
    for dx, dy in coordinates:
        arr_stone_positions.append((dx, dy))

    return arr_stone_positions


 # đọc thông tin output của thuật toán
def extract_path_from_file(filename):
    last_line = None
    try:
        with open(filename, 'r') as file:
            for line in file:
                last_line = line.strip()  # Cập nhật last_line cho mỗi dòng
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except IOError:
        print("An error occurred while reading the file.")

    return last_line                          
#Hàm tính total_weight và update lại tọa độ trong mảng stone
def get_update_stone_position(arrow,arr_stone_positions, arr_weight, new_row, new_col):
            # Kiểm tra xem cặp tọa độ (new_row, new_col) có trong arr_stone_positions hay không
            for index, (dx, dy) in enumerate(arr_stone_positions):
                if dx == new_row and dy == new_col:
                    # Nếu tìm thấy, lấy trọng lượng viên đá
                    stone_weight = arr_weight[index]
                    # Kiểm tra kiểu dữ liệu
                    if not isinstance(stone_weight, (int, float)):
                        print(f"Error: stone_weight is not a number: {stone_weight}")
                    # Cập nhật lại tọa độ viên đá
                    if arrow == 'U':
                        arr_stone_positions[index] = (dx -1, dy)  # Giảm dx đi 1
                    if arrow == 'D':
                        arr_stone_positions[index] = (dx +1, dy)  # Giảm dx đi 1
                    if arrow == 'L':
                        arr_stone_positions[index] = (dx, dy-1)  # Giảm dx đi 1
                    if arrow == 'R':
                        arr_stone_positions[index] = (dx, dy +1)  # Giảm dx đi 1
                    return stone_weight
            
            return None, 0, stone_weight  # Trả về None nếu không tìm thấy 

# Tìm vị trí của nhân vật
def find_player_position(a):
    for row in range(len(a)):
        for col in range(len(a[row])):
            if a[row][col] == '@':  # Kiểm tra nếu ô hiện tại là vị trí của Ares
                return row, col  # Trả về hàng và cột
    return None  # Trả về None nếu không tìm thấy

def move_player(direction,a,arr_stones,arr_weight_stone,arr_switch):
            global total_weight_gui
            row, col = find_player_position(a)
            new_row, new_col = row, col  # Khởi tạo new_row và new_col
            stone_row = row
            stone_col = col
            if direction == 'u' or direction == 'U' :  # Up
                new_row -= 1
            elif direction == 'd' or direction == 'D':  # Down
                new_row += 1
            elif direction == 'l' or direction == 'L':  # Left
                new_col -= 1
            elif direction == 'r' or direction == 'R':  # Right
                new_col += 1
            
            # chạm vào đá    
            if direction == 'U':  
                stone_row = row-2
                stone_col = col
                a[stone_row][stone_col] = '$'
                total_weight_gui += get_update_stone_position(direction,arr_stones, arr_weight_stone, new_row, new_col)
                print('total_weight: ', total_weight_gui)
                print('arr: ', arr_stones)
            elif direction == 'D':
                stone_row = row +2
                stone_col = col
                a[stone_row][stone_col] = '$'
                total_weight_gui += get_update_stone_position(direction,arr_stones, arr_weight_stone, new_row, new_col)
                print('total_weight: ', total_weight_gui)
                print('arr: ', arr_stones)
            elif direction == 'L':
                stone_row = row
                stone_col = col -2
                a[stone_row][stone_col] = '$'
                total_weight_gui += get_update_stone_position(direction,arr_stones, arr_weight_stone, new_row, new_col)
                print('total_weight: ', total_weight_gui)
                print('arr: ', arr_stones)
            elif direction == 'R':
                stone_row = row
                stone_col = col +2
                a[stone_row][stone_col] = '$'
                total_weight_gui += get_update_stone_position(direction,arr_stones, arr_weight_stone, new_row, new_col)
                print('total_weight: ', total_weight_gui)
                print('arr: ', arr_stones)
            # Cập nhật vị trí của nhân vật
            if check_position(row,col,arr_switch):
                a[row][col] = '.' 
                a[new_row][new_col] = '@'
            else :
                a[row][col] = '1' 
                a[new_row][new_col] = '@'

# Lấy weight của các viên đá
def get_weight_from(filename):
    numbers = []  # Khởi tạo danh sách để lưu các số
    try:
        with open(filename, 'r') as file:
            first_line = file.readline()  # Đọc dòng đầu tiên
            # Tách các số từ dòng đầu tiên
            numbers = [int(num) for num in first_line.split() if num.isdigit()]
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except IOError:
        print("An error occurred while reading the file.")
    except ValueError:
        print("Error converting a string to an integer.")
    return numbers  # Trả về danh sách các số

def draw_button(DISPLAYSURF,button_rect,button_color,font):
    # Vẽ nút
    pygame.draw.rect(DISPLAYSURF, button_color, button_rect)
    # Vẽ văn bản trên nút
    text_surface = font.render("BFS", True, (0,0,0))  # Màu chữ trắng
    text_rect = text_surface.get_rect(center=button_rect.center)  # Đặt văn bản ở giữa nút
    DISPLAYSURF.blit(text_surface, text_rect)
def display_step(DISPLAYSURF, step,elapsed_time,font):
                step_text = font.render(f"Steps: {step}", True, (255, 255, 255))  # Màu chữ trắng
                time_text = font.render(f"Time (s): {int(elapsed_time)}", True, (255, 255, 255))  # Màu chữ trắng
                weight = font.render(f"Weight : {int(total_weight_gui)}", True, (255, 255, 255))  # Màu chữ trắng
                DISPLAYSURF.blit(step_text, (10, 10))  # Hiển thị ở góc trái trên cùng (10, 10)
                DISPLAYSURF.blit(time_text, (10, 40))  # Hiển thị thời gian bên dưới số bước
                DISPLAYSURF.blit(weight, (10, 70))  # Hiển thị thời gian bên dưới số bước

#Hàm hiển thị file input ban đầu
def get_input_file(num_input):
    global highlight_input
    global input
    global output
    if num_input == 1:
        highlight_input =1
        input = 'input-01.txt'
        output = 'output-01.txt'
    elif num_input == 2:
        highlight_input =2
        input = 'input-02.txt'
        output = 'output-02.txt'
    elif num_input == 3:
        highlight_input =3
        input = 'input-03.txt'
        output = 'output-03.txt'
    elif num_input == 4:
        highlight_input =4
        input = 'input-04.txt'
        output = 'output-04.txt'
    elif num_input == 5:
        highlight_input =5
        input = 'input-05.txt'
        output = 'output-05.txt'
    elif num_input == 6:
        highlight_input =6
        input = 'input-06.txt'
        output = 'output-06.txt'
    elif num_input == 7:
        highlight_input =7
        input = 'input-07.txt'
        output = 'output-07.txt'
    elif num_input == 8:
        highlight_input =8
        input = 'input-08.txt'
        output = 'output-08.txt'
    elif num_input == 9:
        highlight_input =9
        input = 'input-09.txt'
        output = 'output-09.txt'
    elif num_input == 10:
        highlight_input =10
        input = 'input-10.txt'
        output = 'output-10.txt'
        
        

#Hàm hiển thị trong sự kiện chọn thuật toán 
def seen_algorithm(algorithm,a):
    if algorithm == 'bfs':
        a[3][0]= 'bfs_hover'
        a[4][0]= 'dfs'
        a[5][0]= 'ucs'
        a[6][0]= 'a_star'
    elif algorithm =='dfs':
        a[3][0] ='bfs'
        a[4][0]= 'dfs_hover'
        a[5][0]= 'ucs'
        a[6][0]= 'a_star'
    elif algorithm =='ucs':
        a[3][0]= 'bfs'
        a[4][0]= 'dfs'
        a[5][0]= 'ucs_hover'
        a[6][0]= 'a_star'
    elif algorithm =='a*':
        a[3][0]= 'bfs'
        a[4][0]= 'dfs'
        a[5][0]= 'ucs'
        a[6][0]= 'a_hover'
#Hàm get và highlight thuật toán
def get_algorithm(alrogithm,a):
    global algorithm_running
    if algorithm == 'bfs':
        bfs_file.BFS(input,output)
        a[3][0]= 'bfs_hover'
        a[4][0]= 'dfs'
        a[5][0]= 'ucs'
        a[6][0]= 'a_star'
    elif algorithm =='dfs':
        dfs_file.DFS(input,output)
        a[3][0] ='bfs'
        a[4][0]= 'dfs_hover'
        a[5][0]= 'ucs'
        a[6][0]= 'a_star'
    elif algorithm =='ucs':
        ucs_file.UCS(input,output)
        a[3][0]= 'bfs'
        a[4][0]= 'dfs'
        a[5][0]= 'ucs_hover'
        a[6][0]= 'a_star'
    elif algorithm =='a*':
        a_file.a_star(input,output)
        a[3][0]= 'bfs'
        a[4][0]= 'dfs'
        a[5][0]= 'ucs'
        a[6][0]= 'a_hover'
    algorithm_running = False
    

#Hàm thay đổi trạng thái nút pause
def state_button_pause(a):
    if a[0][16] =='c':
        a[0][16] = 'p'
    else:
        a[0][16] = 'c' 

#Hàm kiểm tra file output có rỗng hay không
def check_empty():
    if os.path.exists('output.txt') and os.stat('output.txt').st_size == 0:
        return True
    else:
        False
        
def test(font,DISPLAYSURF,WINDOWWIDTH,WINDOWHEIGHT,path):
    while algorithm_running:
        if path == None:
            print('thuat toan dang chay')
            draw_noti('THUAT TOAN DANG TIM DUONG DI',font,DISPLAYSURF,WINDOWWIDTH,WINDOWHEIGHT)
            pygame.display.update()
        time.sleep(0.5)
#Hàm vẽ thông báo ra màn hình
def draw_noti(text,font,DISPLAYSURF,WINDOWWIDTH,WINDOWHEIGHT):
    text = font.render(text, True, (255, 0, 0))  # Màu đỏ
    text_rect = text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))  # Đặt ở giữa màn hình
    DISPLAYSURF.blit(text, text_rect)  # Vẽ thông báo tạm dừng
#Hàm GUI cho đồ án
def GUI():
    global algorithm
    global total_weight_gui
    global input
    global output
    global state_pause
    global highlight_input
    global algorithm_running
    global speed
    pygame.init()
    font = pygame.font.SysFont("Arial", 30)
    font_step = pygame.font.SysFont("Arial", 20)
    WINDOWWIDTH, WINDOWHEIGHT = 1200, 850
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    TILESIZE = 60  # Kích thước ô vuông
    pygame.display.update()
#==============================================================================
    arr_input=['in1_hover','in2_hover','in3_hover','in4_hover','in5_hover','in6_hover','in7_hover','in8_hover','in9_hover','in10_hover']
    staring = True
    while staring:
        a = default_map(input,highlight_input,arr_input)
        print_array(a)
        draw_map(a,DISPLAYSURF,TILESIZE)
        pygame.display.update()
              
        path = None

        # Khởi tạo thread cho `test` và `get_algorithm`
        thread1 = threading.Thread(target=test, args=(font, DISPLAYSURF, WINDOWWIDTH, WINDOWHEIGHT,path))
        thread2 = threading.Thread(target=get_algorithm, args=(algorithm, a))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        # Đổi tên file theo tên file của bạn
        path = extract_path_from_file(output)
        
        #Khai báo map cho GUI
        arr_switch = find_position_switch(a)
       #Mảng lưu cân nặng của các viên đá theo thứ tự i
        arr_weight_stone = get_weight_from(input)
        #Mảng lưu vị trí đá trong mảng
        arr_stones = arr_stone_pos(a)

        # Tọa độ nút pause (cột 1)
        pause_button_x = 16 * TILESIZE  
        pause_button_y = 0 * TILESIZE
        # Tọa độ nút reset (có thể thay đổi)
        reset_button_x = 18 * TILESIZE  
        reset_button_y = 0 * TILESIZE
        # Tọa độ nút input  
        input1_button_x = 3 * TILESIZE
        input1_button_y = 0 * TILESIZE
        input2_button_x = 4 * TILESIZE
        input2_button_y = 0 * TILESIZE
        input3_button_x = 5 * TILESIZE
        input3_button_y = 0 * TILESIZE
        input4_button_x = 6 * TILESIZE
        input4_button_y = 0 * TILESIZE
        input5_button_x = 7 * TILESIZE
        input5_button_y = 0 * TILESIZE
        input6_button_x = 8 * TILESIZE
        input6_button_y = 0 * TILESIZE
        input7_button_x = 9 * TILESIZE
        input7_button_y = 0 * TILESIZE
        input8_button_x = 10 * TILESIZE
        input8_button_y = 0 * TILESIZE
        input9_button_x = 11 * TILESIZE
        input9_button_y = 0 * TILESIZE
        input10_button_x = 12 * TILESIZE
        input10_button_y = 0 * TILESIZE
        # Tọa độ nút thuật toán
        bfs_button_x = 0*TILESIZE
        bfs_button_y = 3*TILESIZE
        dfs_button_x = 0*TILESIZE
        dfs_button_y = 4*TILESIZE
        ucs_button_x = 0*TILESIZE
        ucs_button_y = 5*TILESIZE
        a_button_x = 0*TILESIZE
        a_button_y = 6*TILESIZE
        
        x2_button_x = 14*TILESIZE
        x2_button_y = 0*TILESIZE

        # input của nhân vật lấy từ ouput của thuật toán
        input_sequence = path

        # Khởi tạo đồng hồ để điều khiển tốc độ khung hình
        import time
        clock = pygame.time.Clock()
        start_time = None  # Thời gian bắt đầu di chuyển
        elapsed_time = 0  # Thời gian đã trôi qua
        # Vòng lặp game
        running = True
        total_weight_gui = 0
        step = 0
        speed = 1000
        paused = False  # Biến trạng thái để theo dõi việc dừng game
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    staring = False
                
              
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Nếu nhấn vào nút input-01 -02 ...
                    if input1_button_x <= mouse_x <= input1_button_x + TILESIZE and \
                    input1_button_y <= mouse_y <= input1_button_y + TILESIZE:
                        get_input_file(1)
                        algorithm_running=True
                        running = False
                    if input2_button_x <= mouse_x <= input2_button_x + TILESIZE and \
                    input2_button_y <= mouse_y <= input2_button_y + TILESIZE:
                        get_input_file(2)
                        algorithm_running=True
                        running = False
                    if input3_button_x <= mouse_x <= input3_button_x + TILESIZE and \
                    input3_button_y <= mouse_y <= input3_button_y + TILESIZE:
                        get_input_file(3)
                        algorithm_running=True
                        running = False
                    if input4_button_x <= mouse_x <= input4_button_x + TILESIZE and \
                    input4_button_y <= mouse_y <= input4_button_y + TILESIZE:
                        get_input_file(4)
                        algorithm_running=True
                        running = False
                    if input5_button_x <= mouse_x <= input5_button_x + TILESIZE and \
                    input5_button_y <= mouse_y <= input5_button_y + TILESIZE:
                        get_input_file(5)
                        algorithm_running=True
                        running = False
                    if input6_button_x <= mouse_x <= input6_button_x + TILESIZE and \
                    input6_button_y <= mouse_y <= input6_button_y + TILESIZE:
                        get_input_file(6)
                        algorithm_running=True
                        running = False
                    if input7_button_x <= mouse_x <= input7_button_x + TILESIZE and \
                    input7_button_y <= mouse_y <= input7_button_y + TILESIZE:
                        get_input_file(7)
                        algorithm_running=True
                        running = False
                    if input8_button_x <= mouse_x <= input8_button_x + TILESIZE and \
                    input8_button_y <= mouse_y <= input8_button_y + TILESIZE:
                        get_input_file(8)
                        algorithm_running=True
                        running = False
                    if input9_button_x <= mouse_x <= input9_button_x + TILESIZE and \
                    input9_button_y <= mouse_y <= input9_button_y + TILESIZE:
                        get_input_file(9)
                        algorithm_running=True
                        running = False
                    if input10_button_x <= mouse_x <= input10_button_x + TILESIZE and \
                    input10_button_y <= mouse_y <= input10_button_y + TILESIZE:
                        get_input_file(10)
                        algorithm_running=True
                        running = False
                    #Nếu nhấn vào nút x2
                    if x2_button_x <= mouse_x <= x2_button_x + TILESIZE and \
                    x2_button_y <= mouse_y <= x2_button_y + TILESIZE:
                        if speed > 100 :
                            speed /= 2
                            speed = int(speed)
                            print(speed)
                    # ================================Kiểm tra nếu chuột nhấn vào nút pause=============================================
                    if pause_button_x <= mouse_x <= pause_button_x + TILESIZE and \
                    pause_button_y <= mouse_y <= pause_button_y + TILESIZE:
                        paused = not paused  # Đổi trạng thái paused
                        state_button_pause(a)
                        algorithm_running=True
                    # Kiểm tra nếu chuột nhấn vào nút reset
                    if reset_button_x <= mouse_x <= reset_button_x + TILESIZE and \
                    reset_button_y <= mouse_y <= reset_button_y + TILESIZE:
                        paused = False
                        # Khôi phục lại trạng thái ban đầu
                        a = default_map(input,highlight_input,arr_input)  
                        draw_map(a,DISPLAYSURF, TILESIZE)  # Vẽ bản đồ
                        pygame.display.update()
                        pygame.time.delay(speed)
                        input_sequence = extract_path_from_file(output)
                        arr_stones = arr_stone_pos(a)
                        total_weight_gui =0
                        step = 0
                        speed = 1000
                        start_time = time.time()
                        seen_algorithm(algorithm,a)
                       
                        
                    #Kiểm tra nếu chuột nhấn vào nút lựa chọn thuật toán
                    if bfs_button_x <= mouse_x <= bfs_button_x + TILESIZE and \
                        bfs_button_y <= mouse_y <= bfs_button_y + TILESIZE:
                            algorithm = 'bfs'
                            algorithm_running=True
                            running = False
                    if dfs_button_x <= mouse_x <= dfs_button_x + TILESIZE and \
                        dfs_button_y <= mouse_y <= dfs_button_y + TILESIZE:
                            algorithm ='dfs'
                            algorithm_running=True
                            running = False
                    if ucs_button_x <= mouse_x <= ucs_button_x + TILESIZE and \
                        ucs_button_y <= mouse_y <= ucs_button_y + TILESIZE:
                            algorithm ='ucs'
                            algorithm_running=True
                            running = False
                    if a_button_x <= mouse_x <= a_button_x + TILESIZE and \
                        a_button_y <= mouse_y <= a_button_y + TILESIZE:
                            algorithm = 'a*'
                            algorithm_running=True
                            running = False
                 
            if not paused and input_sequence:
                if start_time is None:
                    start_time = time.time()  # Ghi nhận thời gian bắt đầu
                move_player(input_sequence[0],a,arr_stones,arr_weight_stone,arr_switch)
                input_sequence = input_sequence[1:]
                step = step + 1
                # Tính thời gian đã trôi qua
                elapsed_time = time.time() - start_time
            draw_map(a,DISPLAYSURF,TILESIZE)
            display_step(DISPLAYSURF, step, elapsed_time,font_step)  # Hiển thị bước và thời gian
            pygame.display.update()  # Cập nhật màn hình  
            if paused:  # Nếu paused, hiển thị thông báo
                draw_noti('PAUSE',font,DISPLAYSURF,WINDOWWIDTH,WINDOWHEIGHT)
            clock.tick(99999999)  # Giới hạn tốc độ khung hình
            pygame.display.update()  # Cập nhật màn hình
            pygame.time.delay(speed)  # Thời gian delay để người chơi có thể thấy thông báo


GUI()