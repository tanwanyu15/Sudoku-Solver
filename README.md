***

# 数独求解器 (Sudoku Solver)

一个使用Python实现的的数独求解器，采用**回溯算法**与**约束传播**技术。


## 项目结构

```
sudoku-solver/
├── solver.py      # 核心求解器模块，包含Cell和Solver类
├── test.py        # 使用示例和测试代码
└── README.md
```

## 核心算法

求解器 (`Solver` 类) 的核心是递归回溯算法，并辅以两层约束传播以大幅减少搜索空间：

1.  **约束传播 (`update_state`方法)**:
    *   **唯一候选数**：当某个格子只剩下一种可能的数字时，直接确定其值。
    *   **唯一位置**：在行、列或宫中，如果某个数字只能放入一个特定的格子，则在该格填入该数字。
    *   此过程会迭代进行，直到棋盘状态不再变化。

2.  **递归回溯 (`solve`方法)**:
    *   在经过约束传播后，如果问题未解决且无冲突，则选择一个**可能性最少的格子**进行尝试。
    *   依次尝试该格的所有可能数字，为每种选择创建一个新的求解分支（通过保存和加载棋盘状态实现）。
    *   在分支中递归调用求解过程。如果成功则返回；如果失败（产生冲突），则回溯到上一个选择点，尝试下一个数字。

## 快速开始

### 安装依赖
本项目无需额外依赖，仅需Python 3.x环境。

### 基本使用

1.  **克隆仓库**:
    ```bash
    git clone https://github.com/tanwanyu15/Sudoku-Solver
    cd Sudoku-Solver
    ```

2.  **运行示例**:
    直接运行 `test.py` 文件，它会加载一个预设的数独题目并求解。
    ```bash
    python test.py
    ```
    输出将显示“求解成功！”以及完整的解。

3.  **在自己的代码中使用**:
    ```python
    from solver import Solver

    # 1. 创建求解器实例
    solver = Solver()

    # 2. 定义题目 (0代表空格)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # 3. 加载题目
    solver.load_state(puzzle)

    # 4. 求解并输出结果
    if solver.solve():
        print("Solution found:")
        solver.print_state() # 控制台打印
        solution = solver.state # 获取为二维列表
    else:
        print("No solution exists.")
    ```

## API 参考

### `Solver` 类

*   `__init__(self)`：初始化一个空的9x9数独棋盘。
*   `load_state(state: List[List[int]]) -> None`：加载一个9x9的二维整数列表作为初始状态。列表中的0表示空格。
*   `set_value(row: int, col: int, value: int) -> None`：在指定位置(`row`, `col`)设置数字`value`，并更新相关的行、列、宫约束。
*   `solve() -> bool`：主求解函数。如果找到解则返回`True`，否则返回`False`。求解成功后，最终状态存储在`solver.board`中。
*   `property state -> List[List[int]]`：获取当前棋盘状态的二维列表。
*   `print_state() -> None`：将当前棋盘状态以友好格式打印到控制台（用`.`表示空格）。
*   `clear_state() -> None`：重置整个棋盘到空白状态。

## 核心类说明

- **`Cell` 类**: 表示数独棋盘上的一个格子。
    - `possibilities`: 一个长度为9的列表，用1/0表示数字1-9是否可能填入。
    - `value`: 格子的确定值，0表示未确定。
    - `box`: 格子所属的宫索引（0-8）。
- **`Solver` 类**: 封装了完整的求解逻辑和棋盘状态管理。
