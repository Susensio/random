from tictactoe import *
from players import *


# run_game(human_player, human_player)
run_game(progressive_deepening_player, ab_iterative_player)


# print(human_player(TicTacToeBoard()))

# run_game(human_player, human_player)

# board = TicTacToeBoard(((1, 0, 0), (2, 0, 0), (0, 0, 0)))
# board = board.do_move(1, 1).do_move(2, 1).do_move(2, 2)
# print(board)
# print(board.longest_chain(1))
# print(board.is_win())

# TEST_BOARD = TicTacToeBoard(board_array=((1, 1, 2),
#                                          (1, 2, 1),
#                                          (1, 1, 1)))
# print(TEST_BOARD.is_tie())
