import sys
import numpy as np
import math
import random
import pygame
from typing import List

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Board:
    def __init__(self):
        self.board = np.array([['0'] * 5] * 5)      # 2-dimensional array represents the board
        self.tops = np.array([4] * 5)               # available row of the column, if not available (-1)
        self.player_1 = np.array([[0] * 5] * 5)     # cells occupied by player 1
        self.player_2 = np.array([[0] * 5] * 5)     # cells occupied by player 2
        self.encode_board = []                      # encode form of the board
        self.bit_columns = np.array([[0] * 5] * 2)  # bitmask of the board

        for i in range(5):
            self.encode_board.append([])
            for j in range(5):
                self.encode_board[i].append((4 - i) + (5 * j))

        self.encode_board = np.array(self.encode_board)

    def print_bit_columns(self):
        """
        Contributor: Chuyang Li
        Function to print out the bitmask of the board.

        :return: (None)
        """
        print('bit')
        for row in self.bit_columns:
            for column in row:
                print(f'{bin(column)[2:]:0>5}', end='  ')
            print('\n', end='')
        print('\n', end='')

    def get_bit_value(self, player, board=None) -> str:
        """
        Contributor: Chuyang Li
        Convert bitmask to value.

        :return: String of the bitmask.
        """
        result = '0b'
        if board:
            for c in range(5):
                for r in range(4, -1, -1):
                    if board[r][c] == str(player):
                        result += '1'
                    else:
                        result += '0'

        else:
            for row in self.bit_columns[player - 1]:
                result += f'{bin(row)[2:]:0>5}'

        return result

    def print_board(self, target: str):
        """
        Contributor: Chuyang Li
        Helper to print out board status.

        :param target: String represents the status to be printed.
        :return: (None)
        """
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
        """
        Contributor: Chuyang Li
        Print all status.

        :return: (None)
        """
        targets = ['board', 'player_1', 'player_2', 'encoding', 'bit', 'top']

        for target in targets:
            self.print_board(target)

    def change_bit_columns(self, player: int, row: int, column):
        """
        Contributor: Chuyang Li
        Update bit columns.

        :param player: Integer represents player.
        :param row: Row to be updated.
        :param column: Column to be updated.

        :return: (None)
        """
        self.bit_columns[player - 1][4 - column] ^= 1 << (4 - row)
        self.print_board('bit')

    def find_position(self, column: int):
        """
        Contributor: Chuyang Li
        Return open position for the column.

        :param column: Target column (start from 0).
        :return: Row or raise value error.
        """
        if self.tops[column] < 4:
            return self.tops[column] + 1
        else:
            raise ValueError('Column Full. Invalid move!')

    def is_winning(self, player: int, bitboard: int = None) -> bool:
        """
        Contributor: Maggie Zhang
        Find out if the input player has connect 3 pieces on board.

        :param bitboard: Current status of the board of the player.
        :param player: 1 for first player and 2 for second player.

        :return: if this player has connect 3.
        """
        if bitboard is None:
            bitboard = eval(self.get_bit_value(player))

        # Winning diagonal \
        if bitboard & (bitboard >> 4) & (bitboard >> 8) != 0:
            return True
        # Winning diagonal /
        if bitboard & (bitboard >> 6) & (bitboard >> 12) != 0:
            return True
        # Winning vertical
        if bitboard & (bitboard >> 5) & (bitboard >> 10) != 0:
            return True
        # Winning horizontal
        if bitboard & (bitboard >> 1) & (bitboard >> 2) != 0:
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

    def minimax(self, board, player, tops, depth, alpha, beta, maximizingPlayer) -> tuple:
        """
        Contributor: Chuyang Li
        Reference:
        https://github.com/KeithGalli/Connect4-Python/blob/503c0b4807001e7ea43a039cb234a4e55c4b226c/connect4_with_ai.py#L226
        Searching result using minimax with Alpha-Beta pruning.

        :param board: Status to be searched.
        :param player: Current player.
        :param tops: Availble spots.
        :param depth: Remaining search depth.
        :param alpha: Current alpha value.
        :param beta: Current beta value.
        :param maximizingPlayer: If this player is a maximizing player.
        :return: Best column and its score.
        """
        # When search reach an end (depth = 0 or game winning)
        if depth == 0 or self.is_winning(player, board) or self.is_winning(3 - player, board):
            if self.is_winning(player, board) or self.is_winning(3 - player, board):
                if self.is_winning(player, board):
                    return (None, 100000000000000)
                elif self.is_winning(3 - player, board):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, player))

        # For maximizing player
        if maximizingPlayer:
            value = -math.inf
            column = random.choice([i for i in range(5)])
            for col, row in enumerate(tops):
                if row >= 0:
                    # Get new status (if this move is made)
                    new_board = board.copy()
                    new_board[row][col] = str(player)
                    new_tops = tops.copy()
                    new_tops[col] = row - 1
                    # Search the next stage
                    new_score = self.minimax(new_board, 3 - player, new_tops,
                                             depth - 1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)

                    # Alpha break
                    if alpha >= beta:
                        break
            return column, value

        # For minimizing player
        else:
            value = math.inf
            column = random.choice([i for i in range(5)])
            for col, row in enumerate(tops):
                if row >= 0:
                    new_board = board.copy()
                    new_board[row][col] = str(player)

                    new_tops = tops.copy()
                    new_tops[col] = row - 1
                    # Search the next stage
                    new_score = self.minimax(new_board, 3 - player, new_tops,
                                             depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    # Beta break
                    if alpha >= beta:
                        break
            return column, value

    def evaluate_window(self, window: List[str], player: int) -> int:
        """
        Contributor: Chuyang Li
        Evaluate score for this window.

        :param window: list of value in board.
        :param player: 1 for player 1 and 2 for player 2.
        :return: score of the window.
        """
        score = 0
        opponent = 3 - player

        if window.count(player) == 3:
            score += 100
        elif window.count(player) == 2 and window.count(0) == 1:
            score += 5
        elif window.count(player) == 1 and window.count(0) == 2:
            score += 2
        elif window.count(str(opponent)) == 2 and window.count(0) == 1:
            score -= 5

        return score

    def score_position(self, board, player) -> int:
        """
        Contributor: Chuyang Li
        Calculate score for the board.

        :param board: Board to be evaluate.
        :param player: 1 for player 1 and 2 for player 2.
        :return: Score for the board.
        """
        score = 0

        # Increase score for column in center
        center_array = [int(i) for i in list(board[:, 2])]
        # print(center_array)
        center_count = center_array.count(player)
        score += center_count * 3

        # Calculate score for horizontal windows
        for r in range(5):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(3):
                window = row_array[c:c + 3]
                # print(window)
                score += self.evaluate_window(window, player)

        # Calculate score for vertical windows
        for c in range(5):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(3):
                window = col_array[r:r + 3]
                score += self.evaluate_window(window, player)

        # Calculate score for diagonal / windows
        for r in range(3):
            for c in range(3):
                window = [board[r + i][c + i] for i in range(3)]
                score += self.evaluate_window(window, player)

        # Calculate score for diagonal \ windows
        for r in range(3):
            for c in range(3):
                window = [board[r + 2 - i][c + i] for i in range(3)]
                # print(window)
                score += self.evaluate_window(window, player)

        return score

    """def find_optimized_solution(self, player: int) -> List[int]:
        # TODO: Chuyang

        Find out the optimized solution for the input player to make move.

        :param player: 1 for first player and 2 for second player.

        :return: place to make move [row, column].

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
        return result"""

    def make_move(self, player: int, row: int, column: int):
        """
        Contributor: Maggie Zhang
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

"""
    def play_game(self):
        
        Contributor: Chuyang Li

        :return: (None)
        
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
"""


class ConnectFour:
    def __init__(self):
        self.game = Board()
        self.game_over = False
        self.round = 1

        pygame.init()
        # define our screen size
        self.square_size = 100

        # define width and height of board
        self.width = 500
        self.height = 600

        self.size = (self.width, self.height)

        self.radius = int(self.square_size / 2 - 5)

        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont("monospace", 50)

    def display_board(self):
        """
        Contributor: Chuyang Li
        Display updated view of the board. Red for player 1 and yellow for player 2.

        :return: (None)
        """
        for c in range(5):
            for r in range(5):
                pygame.draw.rect(self.screen, BLUE, (c * self.square_size,
                                                     r * self.square_size + self.square_size,
                                                     self.square_size, self.square_size))
                pygame.draw.circle(self.screen, BLACK, (
                    int(c * self.square_size + self.square_size / 2),
                    int(r * self.square_size + self.square_size + self.square_size / 2)), self.radius)

        for c in range(5):
            for r in range(5):
                if self.game.board[r][c] == '1':
                    pygame.draw.circle(self.screen, RED, (
                        int(c * self.square_size + self.square_size / 2),
                        int((r + 1) * self.square_size + self.square_size / 2)), self.radius)
                elif self.game.board[r][c] == '2':
                    pygame.draw.circle(self.screen, YELLOW, (
                        int(c * self.square_size + self.square_size / 2),
                        int((r + 1) * self.square_size + self.square_size / 2)), self.radius)

    def human_round(self, player):
        """
        Contributor: Chuyang Li
        Human drop piece using mouse.

        :param player: 1 for player 1 and 2 for player 2.
        :return: (None)
        """
        color = YELLOW
        if player == 1:
            color = RED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                posx = event.pos[0]
                pygame.draw.circle(self.screen, color, (posx, int(self.square_size / 2)), self.radius)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                posx = event.pos[0]
                col = int(math.floor(posx / self.square_size))

                if self.game.tops[col] >= 0:
                    row = self.game.tops[col]
                    self.game.make_move(player, row, col)

                    if self.game.is_winning(player):
                        label = self.font.render(f"Player {player} wins!!", True, RED)
                        self.screen.blit(label, (40, 10))
                        self.game_over = True

    def AI_round(self, player):
        """
        Contributor: Chuyang Li
        Generate move using minimax.

        :param player: 1 for player 1 and 2 for player 2.
        :return: (None)
        """
        col, minimax_score = self.game.minimax(player, self.game.board, 4, -math.inf, math.inf, True)

        if self.game.tops[col] >= 0:
            row = self.game.tops[col]
            self.game.make_move(player, row, col)

        if self.game.is_winning(player):
            label = self.font.render(f"Player {player} wins!!", True, RED)
            self.screen.blit(label, (40, 10))
            self.game_over = True

    def play_connect_three_game(self):
        self.display_board()
        pygame.display.update()

        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                    posx = event.pos[0]
                    if self.round % 2 == 1:
                        pygame.draw.circle(self.screen, RED, (posx, int(self.square_size / 2)), self.radius)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                    # print(event.pos)
                    # Ask for Player 1 Input
                    if self.round % 2 == 1:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.square_size))

                        if self.game.tops[col] >= 0:
                            row = self.game.tops[col]
                            player = 2 - (self.round % 2)
                            self.game.make_move(player, row, col)

                            if self.game.is_winning(player):
                                label = self.font.render("Player 1 wins!!", False, RED)
                                self.screen.blit(label, (40, 10))
                                self.game_over = True

                            self.round += 1
                            self.display_board()
                            pygame.display.update()

            # # Ask for Player 2 Input
            if self.round % 2 == 0 and not self.game_over:

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                player = 2 - (self.round % 2)
                col, minimax_score = self.game.minimax(player, self.game.board, 4, -math.inf, math.inf, True)

                if self.game.tops[col] >= 0:
                    # pygame.time.wait(500)
                    row = self.game.tops[col]
                    self.game.make_move(player, row, col)

                    if self.game.is_winning(player):
                        label = self.font.render("Player 2 wins!!", False, YELLOW)
                        self.screen.blit(label, (40, 10))
                        self.game_over = True

                    self.round += 1
                    self.display_board()
                    pygame.display.update()

            if self.game_over:
                pygame.time.wait(3000)


if __name__ == "__main__":
    a = Board()
    a.make_move(1, 4, 2)
    print(a.score_position(a.board, 1))

