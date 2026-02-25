from solver import Solver

# 实例化求解器
solver = Solver()
# 初始棋盘状态
init_state = [
    [0,0,0,6,7,9,0,0,0],
    [0,9,0,1,0,0,4,0,0],
    [0,1,3,0,0,4,0,9,0],
    [8,0,9,0,0,5,2,0,0],
    [0,0,0,0,0,0,0,7,0],
    [0,7,6,4,0,0,0,0,1],
    [9,2,0,8,3,0,0,6,0],
    [0,0,1,0,0,0,8,0,2],
    [0,0,0,2,5,0,0,0,0]
]
# 加载棋盘状态
solver.load_state(init_state)
# 进行求解
if solver.solve():
    print("求解成功！")
    solver.print_state()
else:
    print("求解失败！")