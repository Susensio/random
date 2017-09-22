# coding=UTF-8


class InvalidMoveException(Exception):
    """ Exception raised if someone tries to make an invalid move """
    pass


class ChessBoard(object):
    """ Store a Chess board

    A chess board is a matrix, laid out as follows:

        8 BR BN BB BQ BK BB BN BR
        7 Bp Bp Bp Bp Bp Bp Bp Bp 
        6 
        5 
        4 
        3 
        2 Wp Wp Wp Wp Wp Wp Wp Wp
        1 WR WN WB WQ WK WB WN WR
          a  b  c  d  e  f  g  h

    """

    _players = {0: ' ',
                1: 'W',
                2: 'B'}

    _pieces = {'K': 1000,
               'Q': 9,
               'R': 5,
               'B': 3,
               'N': 3,
               'p': 1,
               ' ': 0
               }

    def __init__(self, board_array=None, castling=None, en_passant=None, current_player=1):

        if board_array == None:
            self.board_array = (tuple((1, piece) for piece in 'RNBQKBNR'),
                                tuple(((1, 'p'),) * 8),
                                (((0, ' '),) * 8),
                                (((0, ' '),) * 8),
                                (((0, ' '),) * 8),
                                (((0, ' '),) * 8),
                                tuple(((2, 'p'),) * 8),
                                tuple((2, piece) for piece in 'RNBQKBNR'))

        else:
            # Make sure we're storing tuples, so that they're immutable
            self.board_array = tuple(map(tuple, (map(tuple, row) for row in board_array)))

        if castling == None:
            # White long, white short, black long and black short
            self.castling = {k: True for k in ('WL', 'WS', 'BL', 'BS')}
        else:
            self.castling = dict(castling)

        self.en_passant = en_passant
        self.current_player = current_player

    @property
    def other_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1

    def get_cell(self, row, col):
        return self.board_array[row][col]

    def get_pretty(piece):
        ''' Get a prettier string representation 'WR' of a piece tuple (1,R)'''
        return players[piece[0]] + piece[1]

    def get_cell_index(cell):
        ''' Translates a cell name 'b3' into indexes (1,2)'''
        return (int(cell[1]) - 1, ord(cell[0].lower()) - 97)

#     def is_win(self):
#         """
#         Return the id# of the player who has won this game.
#         Return 0 if it has not yet been won.
#         """
#         for i in range(self._board_height):
#             for j in range(self._board_width):
#                 cell_player = self.get_cell(i, j)
#                 if cell_player != 0:
#                     win = self._is_win_from_cell(i, j)
#                     if win:
#                         return cell_player

#         return 0

#     def do_move(self, row, col):
#         new_board = list(self.board_array)
#         target_row = list(new_board[row])
#         if target_row[col] == 0:
#             target_row[col] = self.current_player
#         else:
#             raise InvalidMoveException
#         new_board[row] = target_row
#         return TicTacToeBoard(new_board, current_player=self.other_player)

#     def get_all_next_moves(self):
#         """ Return a generator of all moves that the current player could take from this position """
#         for i in range(self._board_height):
#             for j in range(self._board_width):
#                 try:
#                     yield ((i, j), self.do_move(i, j))
#                 except InvalidMoveException:
#                     pass

#     def num_tokens_on_board(self):
#         tokens = 0

#         for row in self.board_array:
#             for col in row:
#                 if col != 0:
#                     tokens += 1

#         return tokens

    def clone(self):
        return ChessBoard(self.board_array, self.castling, self.en_passant, self.current_player)

    def __str__(self):
        retVal = []
        horizontal_line = "  " + " ――――" * 8

        retVal = [horizontal_line]
        for i in range(8):
            retVal += [str(8 - i) + ' | ' + ' | '.join([get_pretty(x) for x in board_array[-1 - i]]) + ' |']
            retVal += [horizontal_line]
        retVal += ["    " + '    '.join([str(x) for x in 'abcdefgh'])]
        return '\n' + '\n'.join(retVal) + '\n'


# class TicTacToeRunner(object):
#     """ Runs a game of Tic-Tac-Toe.

#     The game runner is implemented via callbacks:  The two players specify callbacks to be
#     called when it's their turn.  The callback is passed two arguments, self and self.get_board().
#     The callback functions must return tuples of integers corresponding to the (row, column) they want
#     to put a token on.
#     """

#     def __init__(self, player1_callback, player2_callback, board=TicTacToeBoard()):
#         self.board = board
#         self.player1_callback = player1_callback
#         self.player2_callback = player2_callback

#     def run_game(self, verbose=True):
#         """ Run the test defined by this test runner.  Print and return the id of the winning player. """
#         player1 = (self.player1_callback, 1, self.board.board_symbol_mapping[1])
#         player2 = (self.player2_callback, 2, self.board.board_symbol_mapping[2])

#         win_for_player = []

#         while not win_for_player and not self.board.is_tie():
#             for callback, id, symbol in (player1, player2):
#                 if verbose:
#                     print(self.board)

#                 has_moved = False

#                 while not has_moved:
#                     try:
#                         target = callback(self.board.clone())
#                         print("Player {} ({}) puts a token in (row,col) = {}".format(id, symbol, target))
#                         self.board = self.board.do_move(*target)
#                         has_moved = True
#                     except InvalidMoveException as e:
#                         print(e)
#                         print("Illegal move attempted. Please try again.")
#                         continue

#                 if self.board.is_game_over():
#                     win_for_player = self.board.is_win()
#                     break

#         win_for_player = self.board.is_win()

#         if win_for_player == 0 and self.board.is_tie():
#             print("It's a tie!  No winner is declared.")
#             print(self.board)
#             return 0
#         else:
#             print("Win for {}!".format(self.board.board_symbol_mapping[win_for_player]))
#             print(self.board)
#             return win_for_player


# def human_player(board):
#     """
#     A callback that asks the user what to do
#     """
#     row = None
#     col = None

#     while type(row) != int:
#         row = input("Pick a row #: -----> ")
#         try:
#             row = int(row)
#         except ValueError:
#             print("Please specify an integer row number")

#     while type(col) != int:
#         col = input("Pick a column #: --> ")
#         try:
#             col = int(col)
#         except ValueError:
#             print("Please specify an integer col number")

#     return (row, col)


# def run_game(player1, player2):
#     """ Run a game of Connect Four, with the two specified players """
#     game = TicTacToeRunner(player1, player2)
#     return game.run_game()


print(ChessBoard().get_cell(1, 1))
