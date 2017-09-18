# coding=UTF-8


class InvalidMoveException(Exception):
    """ Exception raised if someone tries to make an invalid move """
    pass


class TicTacToeBoard(object):
    """ Store a Tic-Tac-Toe board

    A Tic-Tac-Toe board is a matrix, laid out as follows:

         0 1 2
       0 * * *
       1 * * *
       2 * * *

    """

    # The horizontal width of the board
    _board_width = 5
    # The vertical height of the board
    _board_height = 5

    _goal = 4

    board_symbol_mapping = {0: ' ',
                            1: 'X',
                            2: 'O'}

    def __init__(self, board_array=None, current_player=1):

        if board_array == None:
            self.board_array = ((0, ) * self._board_width, ) * self._board_height
        else:
            # Make sure we're storing tuples, so that they're immutable
            self.board_array = tuple(map(tuple, board_array))

        self.current_player = current_player

    @property
    def other_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1

    def get_cell(self, row, col):
        return self.board_array[row][col]

    def _contig_vector_length(self, row, col, direction):
        """
        Starting in the specified cell and going a step of direction = (row_step, col_step),
        count how many consecutive cells are owned by the same player as the starting cell.
        """
        count = 0
        playerid = self.get_cell(row, col)

        while (0 <= row < self._board_height
                and 0 <= col < self._board_width
                and playerid == self.get_cell(row, col)):
            row += direction[0]
            col += direction[1]
            count += 1

        return count - 1

    def _max_length_from_cell(self, row, col):
        """ Return the max-length chain containing this cell """
        return max(self._contig_vector_length(row, col, (1, 1)) + self._contig_vector_length(row, col, (-1, -1)) + 1,
                   self._contig_vector_length(row, col, (1, 0)) + self._contig_vector_length(row, col, (-1, 0)) + 1,
                   self._contig_vector_length(row, col, (0, 1)) + self._contig_vector_length(row, col, (0, -1)) + 1,
                   self._contig_vector_length(row, col, (-1, 1)) + self._contig_vector_length(row, col, (1, -1)) + 1)

    def longest_chain(self, playerid):
        """
        Returns the length of the longest chain of tokens controlled by this player,
        0 if the player has no tokens on the board
        """
        longest = 0
        for i in range(self._board_height):
            for j in range(self._board_width):
                if self.get_cell(i, j) == playerid:
                    longest = max(longest, self._max_length_from_cell(i, j))

        return longest

    def _is_win_from_cell(self, row, col):
        """ Determines if there is a winning set of four connected nodes containing the specified cell """
        return (self._max_length_from_cell(row, col) >= self._goal)

    def is_win(self):
        """
        Return the id# of the player who has won this game.
        Return 0 if it has not yet been won.
        """
        for i in range(self._board_height):
            for j in range(self._board_width):
                cell_player = self.get_cell(i, j)
                if cell_player != 0:
                    win = self._is_win_from_cell(i, j)
                    if win:
                        return cell_player

        return 0

    def is_game_over(self):
        """ Return True if the game has been won, False otherwise """
        return (self.is_win() != 0 or self.is_tie())

    def is_tie(self):
        """ Return true iff the game has reached a stalemate """

        return not any([0 in row for row in self.board_array])

    def do_move(self, row, col):
        new_board = list(self.board_array)
        target_row = list(new_board[row])
        if target_row[col] == 0:
            target_row[col] = self.current_player
        else:
            raise InvalidMoveException
        new_board[row] = target_row
        return TicTacToeBoard(new_board, current_player=self.other_player)

    def get_all_next_moves(self):
        """ Return a generator of all moves that the current player could take from this position """
        for i in range(self._board_height):
            for j in range(self._board_width):
                try:
                    yield ((i, j), self.do_move(i, j))
                except InvalidMoveException:
                    pass

    def num_tokens_on_board(self):
        tokens = 0

        for row in self.board_array:
            for col in row:
                if col != 0:
                    tokens += 1

        return tokens

    def clone(self):
        return TicTacToeBoard(self.board_array, self.current_player)

    def __str__(self):
        horizontal_line = "  " + " ―――" * self._board_width
        retVal = ["    " + '   '.join([str(x) for x in range(self._board_width)])]
        retVal += [horizontal_line]
        for i, row in enumerate(self.board_array):
            retVal += [str(i) + ' | ' + ' | '.join([self.board_symbol_mapping[x] for x in row]) + ' |']
            retVal += [horizontal_line]
        return '\n' + '\n'.join(retVal) + '\n'


class TicTacToeRunner(object):
    """ Runs a game of Tic-Tac-Toe.

    The game runner is implemented via callbacks:  The two players specify callbacks to be 
    called when it's their turn.  The callback is passed two arguments, self and self.get_board().
    The callback functions must return tuples of integers corresponding to the (row, column) they want
    to put a token on.
    """

    def __init__(self, player1_callback, player2_callback, board=TicTacToeBoard()):
        self.board = board
        self.player1_callback = player1_callback
        self.player2_callback = player2_callback

    def run_game(self, verbose=True):
        """ Run the test defined by this test runner.  Print and return the id of the winning player. """
        player1 = (self.player1_callback, 1, self.board.board_symbol_mapping[1])
        player2 = (self.player2_callback, 2, self.board.board_symbol_mapping[2])

        win_for_player = []

        while not win_for_player and not self.board.is_tie():
            for callback, id, symbol in (player1, player2):
                if verbose:
                    print(self.board)

                has_moved = False

                while not has_moved:
                    try:
                        target = callback(self.board.clone())
                        print("Player {} ({}) puts a token in (row,col) = {}".format(id, symbol, target))
                        self.board = self.board.do_move(*target)
                        has_moved = True
                    except InvalidMoveException as e:
                        print(e)
                        print("Illegal move attempted. Please try again.")
                        continue

                if self.board.is_game_over():
                    win_for_player = self.board.is_win()
                    break

        win_for_player = self.board.is_win()

        if win_for_player == 0 and self.board.is_tie():
            print("It's a tie!  No winner is declared.")
            print(self.board)
            return 0
        else:
            print("Win for {}!".format(self.board.board_symbol_mapping[win_for_player]))
            print(self.board)
            return win_for_player


def human_player(board):
    """
    A callback that asks the user what to do
    """
    row = None
    col = None

    while type(row) != int:
        row = input("Pick a row #: -----> ")
        try:
            row = int(row)
        except ValueError:
            print("Please specify an integer row number")

    while type(col) != int:
        col = input("Pick a column #: --> ")
        try:
            col = int(col)
        except ValueError:
            print("Please specify an integer col number")

    return (row, col)


def run_game(player1, player2):
    """ Run a game of Connect Four, with the two specified players """
    game = TicTacToeRunner(player1, player2)
    return game.run_game()
