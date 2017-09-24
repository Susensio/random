from util import memoize, run_search_function

# Define 'INFINITY' and 'NEG_INFINITY'
try:
    INFINITY = float("infinity")
    NEG_INFINITY = float("-infinity")
except ValueError:                 # Windows doesn't support 'float("infinity")'.
    INFINITY = float(1e3000)       # However, '1e3000' will overflow and return
    NEG_INFINITY = float(-1e3000)  # the magic float Infinity value anyway.


def basic_evaluate(board):

    pieces_score = board.get_pieces_score()
    space_score = board.get_space_score()

    return pieces_score * 6 + space_score


def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_win()


def minimax_find_board_value(board, depth, eval_fn):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal(depth, board):
        return eval_fn(board)

    best_val = None

    for move, new_board in board.get_all_next_moves_done():
        val = -1 * minimax_find_board_value(new_board, depth - 1, eval_fn)
        if best_val == None or val > best_val:
            best_val = val

    return best_val


def minimax(board, depth, eval_fn=basic_evaluate,
            verbose=False):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """

    best_val = None

    for move, new_board in board.get_all_next_moves_done():
        val = -1 * minimax_find_board_value(new_board, depth - 1, eval_fn)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

    if verbose:
        print("MINIMAX: Decided on (row,col) {} with rating {}".format(best_val[1], best_val[0]))

    return best_val[1]


def alpha_beta_search(board, depth,
                      eval_fn):

    best_val = None
    alpha = NEG_INFINITY
    beta = INFINITY

    for move, new_board in board.get_all_next_moves_done():
        val = -1 * alpha_beta_search_find_board_value(new_board, depth - 1, eval_fn,
                                                      -beta, -alpha)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

        alpha = max(alpha, val)

    return best_val[1]


def alpha_beta_search_find_board_value(board, depth, eval_fn,
                                       alpha, beta):
    """
    Minimax helper function: Return the minimax value of a particular board,
    given a particular depth to estimate to
    """
    if is_terminal(depth, board):
        return eval_fn(board)

    best_val = None

    for move, new_board in board.get_all_next_moves_done():
        val = -1 * alpha_beta_search_find_board_value(new_board, depth - 1, eval_fn,
                                                      -beta, -alpha)
        if best_val == None or val > best_val:
            best_val = val

        alpha = max(alpha, val)
        if alpha > beta:
            # Prune!
            # print "Pruned! \nboard=%s \talpha=%d \tbeta=%d \tval=%d" % (board, alpha, beta, val)
            return alpha

    return best_val


def basic_player(board): return minimax(board, depth=4, eval_fn=basic_evaluate)


def progressive_deepening_player(board): return run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate, timeout=10)


def alphabeta_player(board): return alpha_beta_search(board, depth=4, eval_fn=basic_evaluate)


def ab_iterative_player(board): return \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=basic_evaluate, timeout=10)
