from typing import List
import copy

class Cell:
    # 每个宫的行列索引范围
    range_box = [
        (0, 3, 0, 3), (0, 3, 3, 6), (0, 3, 6, 9),
        (3, 6, 0, 3), (3, 6, 3, 6), (3, 6, 6, 9),
        (6, 9, 0, 3), (6, 9, 3, 6), (6, 9, 6, 9)
    ]

    def __init__(self):
        self.box = 0
        self.possibilities = [1] * 9
        self.value = 0

    def check_certainty(self) -> int:
        """检查方块值的确定性。若确定，则返回方块的值"""
        value = 0
        for v in range(9):
            if self.possibilities[v]:
                if value:
                    return 0
                else:
                    value = v + 1
        return value


    def clear(self) -> None:
        """重置方块的取值"""
        self.possibilities = [1] * 9
        self.value = 0

class Solver:
    def __init__(self):
        # 初始化棋盘
        board = [[Cell() for _ in range(9)] for _ in range(9)]
        for b in range(9):
            row_min, row_max, col_min, col_max = Cell.range_box[b]
            for r in range(row_min, row_max):
                for c in range(col_min, col_max):
                    board[r][c].box = b
        self.board = board

    def set_value(self, row, col, value) -> None:
        """设置特定位置方块的值"""
        if value:
            # 对同行同列的格进行约束
            for c in range(9):
                self.board[row][c].possibilities[value - 1] = 0
            for r in range(9):
                self.board[r][col].possibilities[value - 1] = 0
            # 对同宫的格进行约束
            row_min, row_max, col_min, col_max = Cell.range_box[self.board[row][col].box]
            for r in range(row_min, row_max):
                for c in range(col_min, col_max):
                    self.board[r][c].possibilities[value -1] = 0
            # 确定该格的值
            self.board[row][col].value = value
            self.board[row][col].possibilities = [0] * 9

    def load_state(self, state) -> None:
        """加载棋盘状态"""
        self.clear_state()
        for r in range(9):
            for c in range(9):
                value = state[r][c]
                self.set_value(r, c, value)

    def clear_state(self) -> None:
        """重置棋盘状态"""
        for r in range(9):
            for c in range(9):
                self.board[r][c].clear()

    @property
    def state(self) -> List[List[int]]:
        """获取当前状态"""
        state = [[] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                state[r].append(self.board[r][c].value)
        return state

    def print_state(self) -> None:
        """格式化打印当前状态"""
        for r in range(9):
            for c in range(9):
                print(self.board[r][c].value if self.board[r][c].value else ".", end=" ")
            print("")

    def find_best_cell(self) -> tuple:
        """找到可能性最少的一个格子"""
        min_choice = 10
        best_cell = None
        for r in range(9):
            for c in range(9):
                if self.board[r][c].value:
                    continue
                num_choice = sum(self.board[r][c].possibilities)
                if num_choice < min_choice:
                    min_choice = num_choice
                    best_cell = r, c
        return best_cell


    def check_victory(self) -> bool:
        """检查关卡是否完成"""
        for r in range(9):
            for c in range(9):
                if not self.board[r][c].value:
                    return False
        return True

    def update_state(self) -> None:
        """更新约束状态"""
        flag_change = True
        while flag_change:
            flag_change = False
            # 根据该格的唯一可能进行取值
            for r in range(9):
                for c in range(9):
                    if self.board[r][c].value:
                        continue
                    value = self.board[r][c].check_certainty()
                    if value:
                        self.set_value(r, c, value)
                        flag_change = True
            # 根据每个行、列、宫中数字的唯一性进行取值
            p_r = [[[] for _ in range(9)] for _ in range(9)]
            p_c = [[[] for _ in range(9)] for _ in range(9)]
            p_z = [[[] for _ in range(9)] for _ in range(9)]
            for r in range(9):
                for c in range(9):
                    for v in range(9):
                        if self.board[r][c].possibilities[v]:
                            p_r[r][v].append((r,c))
                            p_c[c][v].append((r,c))
                            p_z[self.board[r][c].box][v].append((r,c))
            for i in range(9):
                for v in range(9):
                    if len(p_r[i][v]) == 1:
                        self.set_value(p_r[i][v][0][0], p_r[i][v][0][1], v + 1)
                        flag_change = True
                    if len(p_c[i][v]) == 1:
                        self.set_value(p_c[i][v][0][0], p_c[i][v][0][1], v + 1)
                        flag_change = True
                    if len(p_z[i][v]) == 1:
                        self.set_value(p_z[i][v][0][0], p_z[i][v][0][1], v + 1)
                        flag_change = True

    def check_conflict(self) -> bool:
        """检查是否存在冲突"""
        for r in range(9):
            for c in range(9):
                if self.board[r][c].value:
                    continue
                if sum(self.board[r][c].possibilities) == 0:
                    return True
        return False

    def solve(self) -> bool:
        """进行求解"""
        self.update_state()
        if self.check_victory():
            return True
        if self.check_conflict():
            return False
        r, c = self.find_best_cell()
        for v in range(9):
            if self.board[r][c].possibilities[v]:
                saved_board = copy.deepcopy(self.state)
                self.set_value(r, c, v + 1)
                if self.solve():
                    return True
                self.load_state(saved_board)
        return False