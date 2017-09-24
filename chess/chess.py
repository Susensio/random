# coding=UTF-8
# import sys
# sys.path.append("../")
# from timer_decorator import timeit


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

    _pieces = {1: {'symbol': 'K', 'value': 1000},
               2: {'symbol': 'Q', 'value': 9},
               3: {'symbol': 'R', 'value': 5},
               4: {'symbol': 'B', 'value': 3},
               5: {'symbol': 'N', 'value': 3},
               6: {'symbol': 'p', 'value': 1},
               0: {'symbol': ' ', 'value': 0}
               }

    def __init__(self, board_array=None, castling=None, en_passant=None, current_player=1):

        if board_array is None:
            self.board_array = (tuple((1, int(piece)) for piece in '35421453'),
                                tuple(((1, 6),) * 8),
                                (((0, 0),) * 8),
                                (((0, 0),) * 8),
                                (((0, 0),) * 8),
                                (((0, 0),) * 8),
                                tuple(((2, 6),) * 8),
                                tuple((2, int(piece)) for piece in '35421453'))

        else:
            # Make sure we're storing tuples, so that they're immutable
            self.board_array = tuple(map(tuple, (map(tuple, row) for row in board_array)))

        if castling is None:
            # White long, white short, black long and black short
            self.castling = {k: True for k in ((0, 0), (0, 7), (7, 0), (7, 7))}
        else:
            self.castling = dict(castling)

        if en_passant is None:
            # White long, white short, black long and black short
            self.en_passant = ()
        else:
            self.en_passant = tuple(en_passant)
        self.current_player = current_player

    @property
    def other_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1

    def get_square(self, row, col):
        return self.board_array[row][col]

    def is_empty(self, row, col):
        return self.get_square(row, col)[0] == 0

    @staticmethod
    def pretty_piece(piece):
        """ Get a prettier string representation 'WR' of a piece tuple (1,R) """
        return ChessBoard._players[piece[0]] + ChessBoard._pieces[piece[1]]['symbol']

    @staticmethod
    def pretty_square(square):
        """ Get a prettier string representation 'a3' of a square tuple (2,0) """
        return chr(97 + square[1]) + str(square[0] + 1)

    @staticmethod
    def pretty_move(move):
        """ Get a prettier string representation 'a3' of a square tuple (2,0) """
        return ' '.join([ChessBoard.pretty_square(square) for square in move])

    @staticmethod
    def get_square_index(square):
        """ Translates a square name 'b3' into indexes (1,2)"""
        assert(len(square)==2)
        square_index = (int(square[1]) - 1, ord(square[0].lower()) - 97)
        assert(0<=square_index[0]<8 and 0<=square_index[1]<8)
        return square_index

    @staticmethod
    def get_square_score(square):
        if square[0] in (3, 4) and square[1] in (3, 4):
            return 4
        elif 2 <= square[0] <= 5 and 2 <= square[1] <= 5:
            return 3
        elif 1 <= square[0] <= 6 and 1 <= square[1] <= 6:
            return 2
        else:
            return 1

    def get_pieces_score(self):
        score = sum([sum([self._pieces[piece[1]]['value'] for piece in row if piece[0] == self.current_player]) for row in self.board_array])
        score -= sum([sum([self._pieces[piece[1]]['value'] for piece in row if piece[0] == self.current_player]) for row in self.board_array])
        return score

    def get_space_score(self):
        score = sum([ChessBoard.get_square_score(move[1]) for move in self.get_all_next_moves()])
        score -= sum([ChessBoard.get_square_score(move[1]) for move in self.get_all_next_moves(self.other_player)])
        return score

    def is_check(self):
        return (self.current_player,1) in [self.get_square(*move[1]) for move in self.get_all_next_moves(self.other_player)]

    def is_win(self):
        """
        Return the id# of the player who has won this game.
        Return 0 if it has not yet been won.
        Count King pieces in board
        """
        kings = [piece for row in self.board_array for piece in row if piece[1] == 1]

        if len(kings) == 1:
            return kings[0][0]
        else:
            return 0

    def do_move(self, move):
        new_board = list(self.board_array)
        en_passant = None

        if len(move) == 2:
            # normal move
            (start, end) = move

            # Disable castling
            if self.castling.get(start):
                # Rock moved
                self.castling[start] = False
            if self.get_square(*start) == 1:
                # King moved
                self.castling[(start[0], 0)] = False
                self.castling[(start[0], 7)] = False

            if start[0] == end[0]:
                # Same row
                row = list(new_board[start[0]])
                row[end[1]] = self.get_square(*start)
                row[start[1]] = (0, 0)
                new_board[start[0]] = row
            else:
                # Different rows
                if self.get_square(*start) == 6 and start[1] - end[1] in (-2, 2):
                    # Pawn possible enpassant
                    en_passant = end

                row_start = list(new_board[start[0]])
                row_end = list(new_board[end[0]])
                row_end[end[1]] = self.get_square(*start)
                row_start[start[1]] = (0, 0)
                new_board[start[0]] = row_start
                new_board[end[0]] = row_end
        else:
            # Castling move
            if self.current_player == 1:
                self.castling[(0, 0)] = False
                self.castling[(0, 7)] = False
            else:
                self.castling[(7, 0)] = False
                self.castling[(7, 0)] = False

            (start_rock, end_rock, start_king, end_king) = move
            row = list(new_board[start_rock[0]])
            row[end_rock[1]] = self.get_square(*start_rock)
            row[end_king[1]] = self.get_square(*start_king)
            row[start_rock[1]] = (0, 0)
            row[start_king[1]] = (0, 0)
            new_board[start_rock[0]] = row

        return ChessBoard(new_board, current_player=self.other_player, castling=self.castling, en_passant=en_passant)

    def get_horizontals_from_square(self, row, col):
        squares = []
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        player = self.get_square(row, col)[0]
        for direction in directions:
            r = row + direction[0]
            c = col + direction[1]
            while True:
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                if self.is_empty(r, c):
                    squares.append((r, c))
                    r += direction[0]
                    c += direction[1]
                elif self.get_square(r, c)[0] != player:
                    squares.append((r, c))
                    break
                else:
                    break
        return squares

    def get_diagonals_from_square(self, row, col):
        squares = []
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        player = self.get_square(row, col)[0]
        for direction in directions:
            r = row + direction[0]
            c = col + direction[1]
            while True:
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                if self.is_empty(r, c):
                    squares.append((r, c))
                    r += direction[0]
                    c += direction[1]
                elif self.get_square(r, c)[0] != player:
                    squares.append((r, c))
                    break
                else:
                    break
        return squares

    def get_valid_moves(self, row, col):
        piece = self.get_square(row, col)
        moves = []
        if piece[1] == 1:
            # KING
            moves += [((row, col), (row + i, col + j)) for i in range(-1, 2) for j in range(-1, 2)
                      if (i or j)
                      and (0 <= row + i < 8 and 0 <= col + j < 8)
                      and self.get_square(row + i, col + j)[0] != piece[0]]
            # Castling
            if row in (0,7):
                if self.castling[(row,0)]:
                    # Long castling
                    if self.is_empty(row,1) and self.is_empty(row,2) and self.is_empty(row,3):
                        # if not self.is_check():
                            moves += ((row,0),(row,3),(row,4),(row,2))

                if self.castling[(row,7)]:
                    # Short castling
                    if self.is_empty(row,6) and self.is_empty(row,5):
                        # if not self.is_check():
                            moves += ((row,7),(row,5),(row,4),(row,6))



        elif piece[1] == 2:
            # QUEEN
            moves += [((row, col), move) for move in self.get_horizontals_from_square(row, col)]
            moves += [((row, col), move) for move in self.get_diagonals_from_square(row, col)]

        elif piece[1] == 3:
            # ROCK
            moves += [((row, col), move) for move in self.get_horizontals_from_square(row, col)]

        elif piece[1] == 4:
            # BISHOP
            moves += [((row, col), move) for move in self.get_diagonals_from_square(row, col)]

        elif piece[1] == 5:
            # KNIGHT
            moves += [((row, col), (row + i, col + j)) for i in range(-2, 3) for j in range(-2, 3)
                      if (abs(i) + abs(j)) == 3
                      and (0 <= row + i < 8 and 0 <= col + j < 8)
                      and self.get_square(row + i, col + j)[0] != piece[0]]

        elif piece[1] == 6:
            # PAWN
            direction = 1 if piece[0] == 1 else -1
            if self.get_square(row + direction, col)[0] == 0:
                moves += [((row, col), (row + direction, col))]
            moves += [((row, col), (row + direction, col + j)) for j in (-1, 1)
                      if (0 <= row + direction < 8 and 0 <= col + j < 8)
                      and self.get_square(row + direction, col + j)[0] not in (0, piece[0])]
            if ((row == 1 and direction == 1) or (row == 6 and direction == -1)
                and self.get_square(row + direction, col)[0] == 0 and self.get_square(row + direction * 2, col)[0] == 0):
                moves += [((row, col), (row + direction * 2, col))]
            moves += [((row, col), (row + direction, col + j)) for j in (-1, 1)
                      if (row, col + j) in self.en_passant]

        return moves

    def get_all_next_moves(self, player=None):
        """ Return a generator of all moves that the current player could take from this position """
        if player is None:
            player = self.current_player
        for i in range(8):
            for j in range(8):
                if self.get_square(i, j)[0] == player:
                    moves = self.get_valid_moves(i, j)
                    for move in moves:
                        yield move

    def get_all_next_moves_done(self):
        for move in self.get_all_next_moves():
            yield (move, self.do_move(move))

    def clone(self):
        return ChessBoard(self.board_array, self.castling, self.en_passant, self.current_player)

    def __str__(self):
        retVal = ['Turn for {}'.format('whites' if self.current_player == 1 else 'blacks')]
        horizontal_line = "  " + " ――――" * 8

        retVal += [horizontal_line]
        for i in range(8):
            retVal += [str(8 - i) + ' | ' + ' | '.join([self.pretty_piece(x) for x in self.board_array[-1 - i]]) + ' |']
            retVal += [horizontal_line]
        retVal += ["    " + '    '.join([str(x) for x in 'abcdefgh'])]
        return '\n' + '\n'.join(retVal) + '\n'


class ChessRunner(object):
    """ Runs a game of Chess.

    The game runner is implemented via callbacks:  The two players specify callbacks to be
    called when it's their turn.  The callback is passed two arguments, self and self.get_board().
    The callback functions must return tuples of integers corresponding to the (row, column) they want
    to put a token on.
    """

    def __init__(self, player1_callback, player2_callback, board=ChessBoard()):
        self.board = board
        self.player1_callback = player1_callback
        self.player2_callback = player2_callback

    def run_game(self, verbose=True):
        """ Run the test defined by this test runner.  Print and return the id of the winning player. """
        player1 = (self.player1_callback, 1, "Whites")
        player2 = (self.player2_callback, 2, "Blacks")

        win_for_player = None

        # while not win_for_player and not self.board.is_checkmate():
        while not win_for_player:
            for callback, id, symbol in (player1, player2):
                if verbose:
                    print(self.board)

                has_moved = False

                while not has_moved:
                    try:
                        target = callback(self.board.clone())
                        print("Player {} ({}) plays {}".format(id, symbol, ChessBoard.pretty_move(target)))
                        self.board = self.board.do_move(target)
                        has_moved = True
                    except InvalidMoveException as e:
                        print(e)
                        print("Illegal move attempted. Please try again.")
                        continue

                # if self.board.is_game_over():
                #     win_for_player = self.board.is_win()
                #     break

                win_for_player = self.board.is_win()
                if win_for_player:
                    break

        # win_for_player = self.board.is_win()

        # if win_for_player == 0 and self.board.is_tie():
        #     print("It's a tie!  No winner is declared.")
        #     print(self.board)
        #     return 0
        # else:
        print("Win for {}!".format(self.board._players[win_for_player]))
        print(self.board)
        return win_for_player


def human_player(board):
    """
    A callback that asks the user what to do
    """
    start = None
    end = None

    while True:
        start = input("Select a piece: --> ")
        try:
            start = ChessBoard.get_square_index(start)
            break
        except Exception:
            print("Please specify a correct square")

    while True:
        end = input("Move to square: --> ")
        try:
            end = ChessBoard.get_square_index(end)
            break
        except Exception:
            print("Please specify a correct square")

    move = (start, end)

    if start in ((0,4),(7,4)) and board.get_square(*start)[1] == 1:
        # King 
        if start[1]-end[1] == 2:
            # Long castling
            move = ((start[0],0),(start[0],3),start,end)
        elif start[1]-end[1] == -2:
            # Short castling
            move = ((start[0],7),(start[0],5),start,end)
    
    if move not in board.get_all_next_moves():
        raise InvalidMoveException

    return move


def run_game(player1, player2):
    """ Run a game of Connect Four, with the two specified players """
    game = ChessRunner(player1, player2)
    return game.run_game()


# from time import time
# ts = time()
# [print(ChessBoard.pretty_move(move)) for move in ChessBoard().get_all_next_moves(2)]
# board = ChessBoard()
# print([list(board.get_all_next_moves(board.other_player)) for _ in range(1)])
# te = time()
# print(te - ts)
# print(ChessBoard().get_valid_moves(0, 0))
# print(ChessBoard().get_pieces_score())
# print(ChessBoard().get_space_score())

# print(ChessBoard().do_move(((1, 4), (3, 4))).do_move(((6, 3), (4, 3))).do_move(((0,0),(0,3),(0,4),(0,2))))


# run_game(human_player, human_player)