import numpy as np
from typing import List


class Board:
    def __init__(self):
        self.board = np.array([['.'] * 5] * 5)
        self.tops = np.array([0] * 5)
        self.player_1 = np.array([[0] * 5] * 5)
        self.player_2 = np.array([[0] * 5] * 5)
        self.encode_board = []

        for i in range(5):
            self.encode_board.append([])
            for j in range(5):
                self.encode_board[i].append((4 - i) + (5 * j))

        self.encode_board = np.array(self.encode_board)

        self.bit_columns = np.array([[0] * 5] * 2)

    def print_bit_columns(self):
        print('bit')
        for row in self.bit_columns:
            for column in row:
                print(f'{bin(column)[2:]:0>6}', end='  ')
            print('\n', end='')
        print('\n', end='')

    def get_bit_value(self) -> List[int]:
        result = []

        for row in self.bit_columns:
            tmp = []
            for column in row:
                tmp.append(eval(f'0b{bin(column)[2:]:0>6}'))
            result.append(tmp)
        return result

    def print_board(self, target: str):
        if target == 'board':
            b = self.board
        elif target == 'player_1':
            b = self.player_1
        elif target == 'player_2':
            b = self.player_2
        elif target == 'encoding':
            b = self.encode_board
        elif target == 'bit':
            self.print_bit_columns()
            return

        for row in b:
            print(target)
            print(row)
            print('\n')

    def print_all(self):
        targets = ['board', 'player_1', 'player_2', 'encoding', 'bit']

        for target in targets:
            self.print_board(target)

    def change_bit_columns(self, player: int, row: int, column):
        self.bit_columns[player - 1][5 - column] ^= 1 << row
        self.print_board('bit')

    def find_position(self, column: int):
        if self.tops[column] < 4:
            return self.tops[column] + 1
        else:
            raise ValueError('Column Full. Invalid move!')

    def is_winning(self, player: int, board=None) -> bool:
        # TODO: Maggie
        """
        Find out if the input player has connect 3 pieces on board.

        :param player: 1 for first player and 2 for second player.

        :return: if this player has connect 3.
        """
        if board is None:
            board = self.player_1 if player == 1 else self.player_2

        def win_vertical(board):
            for row in range(3):
                for col in range(5):
                    if board[row][col] == 1 and board[row + 1][col] == 1 and board[row + 2][col] == 1:
                        return True
            return False

        def win_horizontal(board):
            for row in range(5):
                for col in range(3):
                    if board[row][col] == 1 and board[row][col + 1] == 1 and board[row][col + 2] == 1:
                        return True
            return False

        def win_left_diag(board):
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 1 and board[row + 1][col + 1] == 1 and board[row + 2][col + 2] == 1:
                        return True
            return False

        def win_right_diag(board):
            for row in range(3):
                for col in range(2, 5):
                    if board[row][col] == 1 and board[row + 1][col - 1] == 1 and board[row + 2][col - 2] == 1:
                        return True
            return False

        if win_horizontal(board) or win_vertical(board) or win_left_diag(board) or win_right_diag(board):
            return True

        return False

    def cause_opponent_winning(self, player: int, position: List[int]) -> bool:
        r, c = position[0], position[1]
        if player == 1:
            rival_board = self.player_2.copy()
        elif player == 2:
            rival_board = self.player_1.copy()
        rival_board[r][c] = 1

        return self.is_winning(3 - player, rival_board)

    def calculate_freedom(self, player: int, position: List[int]) -> int:
        freedom = 0
        player_max_height = self.bit_columns[player - 1]


    def find_optimized_solution(self, player: int) -> List[int]:
        # TODO: Chuyang
        """
        Find out the optimized solution for the input player to make move.

        :param player: 1 for first player and 2 for second player.

        :return: place to make move [row, column].
        """
        # If the board is empty, put the first piece in the middle
        if self.tops == np.array([0] * 5):
            return [4, 2]
        else:
            # Iterate all 5 (or less than 5) positions to find the best place to put the piece
            result = None
            result_freedom = 0
            opponent_winning = False
            for position in self.tops:
                # If the column is full, skip to the next column
                if position[0] < 0:
                    continue
                else:
                    r, c = position[0], position[1]
                    # A temporary board to see the result
                    new_board_1 = self.player_1.copy()
                    new_board_2 = self.player_2.copy()
                    new_board_1[r][c] = 1
                    new_board_2[r][c] = 1
                    player_1_winning = self.is_winning(player, new_board_1)
                    player_2_winning = self.is_winning(player, new_board_2)
                    # If this move cause immediate winning, return this position
                    if (player_1_winning and player == 1) or (player_2_winning and player == 2):
                        return position
                    # if this position does not cause immediate winning,
                    # but blocks opponent from winning
                    # record the position and iterate next position to see if there are better solution
                    elif (player_1_winning and player == 2) or (player_2_winning and player == 1):
                        result = position
                        opponent_winning = True
                    # If none of these happen
                    else:
                        if not opponent_winning:
                            tmp_top = [r - 1, c]
                            if tmp_top[0] < 0:
                                continue
                            else:
                                # See if this move will cause opponent winning in the next round
                                # If not, find the position with maximum freedom (chance of winning)
                                if not self.cause_opponent_winning(player, tmp_top):
                                    freedom = self.calculate_freedom(player, position)
                                    if not result or freedom > result_freedom:
                                        result = position
                                        result_freedom = freedom

        return result

    def make_move(self, player: int, row: int, column: int):
        # TODO: Maggie
        """
        Update board, bit_encoding according to the input player and position.
        :param player: 1 for first player and 2 for second player.
        :param row:
        :param column:
        :return:
        """

        # 1. first update the player board
        board = self.player_1 if player == 1 else self.player_2
        if row > -1 and row < 5 and column < 5 and column > -1:
            board[row][column] = 1
        if player == 1:
            self.player_1 = board
        else:
            self.player_2 = board

        # 2. update the game board
        # change the value on the position from "." to "1" or "2"
        self.board[row][column] = str(player)

        # 3. update bit_columns
        # for each player's bit_column, each element represents the bit value for the entire column

        if player == 1:
            self.bit_columns[0] = [''.join(str(row[i]) for row in self.player_1) for i in range(5)]
        else:
            self.bit_columns[1] = [''.join(str(row[i]) for row in self.player_2) for i in range(5)]

    def play_game(self):
        # TODO: Chuyang
        pass


if __name__ == "__main__":
    a = Board()
    a.change_bit_columns(1, 3, 2)
    a.change_bit_columns(0, 2, 2)
    print(a.get_bit_value())

