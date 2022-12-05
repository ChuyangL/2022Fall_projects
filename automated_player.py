import numpy as np
import math
import random
from typing import List


class Board:
    def __init__(self):
        self.board = np.array([['.'] * 5] * 5)
        self.tops = np.array([4] * 5)
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
                print(f'{bin(column)[2:]:0>5}', end='  ')
            print('\n', end='')
        print('\n', end='')

    def get_bit_value(self) -> List[int]:
        result = []

        for row in self.bit_columns:
            tmp = []
            for column in row:
                tmp.append(eval(f'0b{bin(column)[2:]:0>5}'))
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
        elif target == 'top':
            print(target)
            print(self.tops)
            return
        elif target == 'bit':
            self.print_bit_columns()
            return

        print(target)
        for row in b:
            print(row)
        print('\n')

    def print_all(self):
        targets = ['board', 'player_1', 'player_2', 'encoding', 'bit', 'top']

        for target in targets:
            self.print_board(target)

    def change_bit_columns(self, player: int, row: int, column):
        self.bit_columns[player - 1][4 - column] ^= 1 << (4 - row)
        self.print_board('bit')

    def find_position(self, column: int):
        if self.tops[column] < 4:
            return self.tops[column] + 1
        else:
            raise ValueError('Column Full. Invalid move!')

    def is_winning(self, player: int, board: np.array = None) -> bool:
        # TODO: Maggie
        """
        Find out if the input player has connect 3 pieces on board.

        :param board:
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

    def minimax(self, player, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0:
            return None, self.score_position(board, player)
        if maximizingPlayer:
            value = -math.inf
        else:  # Minimizing player
            value = math.inf
        column = random.choice(self.tops)
        for row, col in self.tops:
            if row < 0:
                continue
            else:
                new_board = board.copy()
                new_board[row][col] = str(player)
                new_score = self.minimax(3 - player, new_board, depth - 1, alpha, beta, not maximizingPlayer)[1]
                if new_score > value:
                    value = new_score
                    column = col
                if maximizingPlayer:
                    alpha = max(alpha, value)
                else:
                    beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value

    def evaluate_window(self, window, player):
        score = 0
        opponent = 3 - player

        if window.count(player) == 3:
            score += 100
        elif window.count(player) == 2 and window.count('.') == 1:
            score += 5
        elif window.count(player) == 1 and window.count('.') == 2:
            score += 2

        if window.count(opponent) == 2 and window.count('.') == 1:
            score -= 4

        return score

    def score_position(self, board, player):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, 5//2])]
        center_count = center_array.count(str(player))
        score += center_count * 3

        ## Score Horizontal
        for r in range(5):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(5 - 2):
                window = row_array[c:c + 3]
                score += self.evaluate_window(window, player)

        ## Score Vertical
        for c in range(5):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(5 - 2):
                window = col_array[r:r + 3]
                score += self.evaluate_window(window, player)

        ## Score posiive sloped diagonal
        for r in range(5 - 2):
            for c in range(5 - 2):
                window = [board[r + i][c + i] for i in range(3)]
                score += self.evaluate_window(window, player)

        for r in range(5 - 3):
            for c in range(5 - 3):
                window = [board[r + 3 - i][c + i] for i in range(3)]
                score += self.evaluate_window(window, player)

        return score

    def find_optimized_solution(self, player: int) -> List[int]:
        # TODO: Chuyang
        """
        Find out the optimized solution for the input player to make move.

        :param player: 1 for first player and 2 for second player.

        :return: place to make move [row, column].
        """
        # If the board is empty, put the first piece in the middle
        if list(self.tops) == [4, 4, 4, 4, 4]:
            return [4, 2]
        else:
            # Iterate all 5 (or less than 5) positions to find the best place to put the piece
            result = [self.tops[2], 2]
            max_height = np.max(self.bit_columns)
            try:
                max_position = list(self.bit_columns[0]).index(max_height)
            except ValueError:
                max_position = list(self.bit_columns[1]).index(max_height)
            # print(max_height)
            # print(max_position)
            dist = 5
            opponent_winning = False
            for i in range(len(self.tops)):
                # If the column is full, skip to the next column
                position = self.tops[i]
                if position < 0:
                    continue
                else:
                    r, c = position, i
                    # print(r)
                    # print(c)
                    # A temporary board to see the result
                    new_board_1 = self.player_1.copy()
                    new_board_2 = self.player_2.copy()
                    new_board_1[r][c] = 1
                    new_board_2[r][c] = 1
                    player_1_winning = self.is_winning(player, new_board_1)
                    player_2_winning = self.is_winning(player, new_board_2)
                    # If this move cause immediate winning, return this position
                    if (player_1_winning and player == 1) or (player_2_winning and player == 2):
                        return [r, c]
                    # if this position does not cause immediate winning,
                    # but blocks opponent from winning
                    # record the position and iterate next position to see if there are better solution
                    elif (player_1_winning and player == 2) or (player_2_winning and player == 1):
                        result = [r, c]
                        opponent_winning = True
                    # If none of these happen
                    else:
                        print([r, c])
                        if not opponent_winning:
                            tmp_top = [r - 1, c]
                            if tmp_top[0] < 0:
                                continue
                            else:
                                # See if this move will cause opponent winning in the next round
                                # If not, find the position with maximum freedom (chance of winning)
                                if not self.cause_opponent_winning(player, tmp_top):
                                    height = self.bit_columns[player - 1][c]
                                    if height != 0:
                                        height = int(math.log(height, 2) + 1)
                                        print(height)
                                    if r != 4 - height:
                                        continue
                                    else:
                                        if c == max_position:
                                            result = [r, c]
                                            dist = 0
                                        elif height < max_height:
                                            if not result or abs(c - max_position) < dist:
                                                result = [r, c]
                                                dist = abs(c - max_position)
        # print(result)
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
        self.change_bit_columns(player, row, column)
        # print(self.bit_columns)
        self.tops[column] = row - 1
        self.print_board('board')


    def play_game(self):
        """
        Contributor: Chuyang Li

        :return: (None)
        """
        player_1 = input('For player 1, please choose from automated/manual: ')
        player_2 = input('For player 2, please choose from automated/manual: ')

        round = 0
        while True:
            round += 1
            player = 2 - (round % 2)
            if eval(f'player_{player}').lower() == 'automated':
                row, column = self.find_optimized_solution(player)
            elif eval(f'player_{player}').lower() == 'manual':
                column = int(input('Please make your move (input column only, starts from 0): '))
                row = self.tops[column]
            self.make_move(player, row, column)
            if self.is_winning(player):
                print(f'Player {player} won the game.')
                break


if __name__ == "__main__":
    a = Board()
    a.play_game()

