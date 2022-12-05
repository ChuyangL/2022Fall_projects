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

    def is_winning(self, player: int) -> bool:
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

    def isWin(self,player:int) -> bool:
        # using bitboard to detect whether_win
        if player == 1:
            bitboard = self.bit_columns[0]
        else:
            bitboard = self.bit_columns[1]
        if bitboard & (bitboard >> 4) & (bitboard >> 8) & (bitboard >> 12) != 0:
            return True # diagonal \
        if bitboard & (bitboard >> 6) & (bitboard >> 12) & (bitboard >> 18) != 0:
            return True # diagonal /
        if bitboard & (bitboard >> 5) & (bitboard >> 10) & (bitboard >> 15) != 0:
            return True; # horizontal
        if bitboard & (bitboard >> 1) & (bitboard >> 2) & (bitboard >> 3) != 0:
            return True # vertical
        return False



    def find_optimized_solution(self, player: int) -> List[int]:
        # TODO: Chuyang
        """
        Find out the optimized solution for the input player to make move.

        :param player: 1 for first player and 2 for second player.

        :return: place to make move [row, column].
        """

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

