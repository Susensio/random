# Lesson 06: Matrix Factorization
# Implement small examples of other simple methods for matrix factorization, such as the PLU and QR decomposition,
# the Cholesky decomposition, and the eigendecomposition.

# Lesson 07: Singular-Value Decomposition
# Implement SVD and find 5 applications of this method.

from lesson3 import Array
from lesson45 import Matrix


def echelon_form(matrix):
    """Gaussian elimination.

    >>> A = Matrix([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    >>> echelon_form(A)
    Matrix([[2, 1, -1, 8], [0.0, 0.5, 0.5, 1.0], [0.0, 0.0, -1.0, 1.0]])

    >>> B = Matrix([[1, 3, 1, 9], [1, 1, -1, 1], [3, 11, 5, 35]])
    >>> echelon_form(B)
    Matrix([[1, 3, 1, 9], [0.0, -2.0, -2.0, -8.0], [0.0, 0.0, 0.0, 0.0]])

    >>> C = Matrix([[0, 2, 1, -1], [0, 2, 4, 0], [0, 0, 0, 0]])
    >>> echelon_form(C)
    Matrix([[0, 2, 1, -1], [0.0, 0.0, 3.0, 1.0], [0.0, 0.0, 0.0, 0.0]])

    >>> D = Matrix([[0]])
    >>> echelon_form(D)
    Matrix([[0]])
    """
    M = Matrix(matrix)
    i = 0
    j = 0
    while i < M.shape[0] and j < M.shape[1]:
        if M[i, j] == 0:
            column = [bool(M[row, j]) for row in range(len(M)) if row > i]
            try:
                swap_row = column.index(True) + i + 1
                M[i], M[swap_row] = M[swap_row], M[i]
            except ValueError:
                j = j + 1
        else:
            for row in range(i + 1, len(M)):
                factor = - M[row, j] / M[i, j]
                M[row] = M[row] + factor * M[i]
            i = i + 1
            j = j + 1
    return M


def reduced_echelon_form(matrix):
    """Full Gauss-Jordan elimination.

    >>> A = Matrix([[1, 3], [1, 4]])
    >>> reduced_echelon_form(A)
    Matrix([[1.0, 0.0], [0.0, 1.0]])

    >>> B = Matrix([[1, 3, 1], [1, 1, -1], [3, 11, 5]])
    >>> reduced_echelon_form(B)
    Matrix([[1.0, 0.0, -2.0], [-0.0, 1.0, 1.0], [0.0, 0.0, 0.0]])

    >>> C = Matrix([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
    >>> reduced_echelon_form(C)
    Matrix([[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 3.0], [-0.0, -0.0, 1.0, -1.0]])
    """
    M = echelon_form(Matrix(matrix))
    i = M.shape[0] - 1
    while i >= 0:
        row_bool = [bool(e) for e in M[i]]
        if any(row_bool):  # If not an empty row
            j = row_bool.index(True)  # First nonzero element
            M[i] = M[i] / M[i, j]
            for row in range(i):
                factor = - M[row, j]
                M[row] = M[row] + factor * M[i]
        i = i - 1
    return M


def lu(matrix):
    """LU decomposition.

    >>> A = Matrix([[-5, 3, 4], [10, -8, -9], [15, 1, 2]])
    >>> L, U = lu(A)
    >>> L
    Matrix([[1, 0, 0], [-2.0, 1, 0], [-3.0, -5.0, 1]])
    >>> U
    Matrix([[-5, 3, 4], [0.0, -2.0, -1.0], [0.0, 0.0, 9.0]])
    >>> L @ U == A
    True
    """
    assert matrix.is_square

    order = matrix.shape[0]
    P = Matrix.identity(order)
    L = Matrix.identity(order)
    U = Matrix(matrix)
    i = 0
    while i < order:
        if U[i, i] == 0:
            return
        for row in range(i + 1, order):
            factor = U[row, i] / U[i, i]
            U[row] = U[row] - factor * U[i]
            L[row, i] = factor

        i = i + 1

    return L, U


def plu(matrix):
    """PLU decomposition.

    >>> A = Matrix([[1, 2], [3, 4]])
    >>> P, L, U = plu(A)
    >>> P @ L @ U == A
    True

    >>> B = Matrix([[0, 1, 0], [-8, 8, 1], [2, -2, 0]])
    >>> P, L, U = plu(B)
    >>> P
    Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    >>> L
    Matrix([[1, 0, 0], [-0.0, 1, 0], [-0.25, 0.0, 1]])
    >>> U
    Matrix([[-8, 8, 1], [0.0, 1.0, 0.0], [0.0, 0.0, 0.25]])

    >>> P @ L @ U == B
    True
    """
    assert matrix.is_square, "Not an square matrix"

    order = matrix.shape[0]
    P = Matrix.identity(order)
    L = Matrix.identity(order)
    U = Matrix(matrix)
    i = 0
    while i < order:
        column = [abs(U[row, i]) for row in range(order) if row >= i]
        swap_row = column.index(max(column)) + i
        if swap_row != i:
            U[i], U[swap_row] = U[swap_row], U[i]
            P[i], P[swap_row] = P[swap_row], P[i]
        if U[i, i] == 0:
            return
        for row in range(i + 1, order):
            factor = U[row, i] / U[i, i]
            U[row] = U[row] - factor * U[i]
            L[row, i] = factor

        i = i + 1

    return P, L, U


def qr(matrix):
    """Gram-Schmidt process.

    >>> A = Matrix([[1, 2], [3, 4]])
    >>> Q, R = qr(A)
    >>> Q.is_orthogonal
    True
    >>> R.is_upper_triangular
    True
    >>> Q @ R == A
    True

    >>> B = Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    >>> Q, R = qr(B)
    >>> Q.is_orthogonal
    True
    >>> R.is_upper_triangular
    True
    >>> Q @ R == B
    True
    """
    assert matrix.is_square, "Not an square matrix"
    order = matrix.shape[0]
    Q_cols = Matrix.empty(order)
    R_cols = Matrix.empty(order)
    matrix_cols = matrix.T
    for i, col in enumerate(matrix_cols):
        u = col - sum([(col @ Q_cols[k]) * Q_cols[k] for k in range(i)])
        e = u / u.norm
        Q_cols[i] = e
        for j in range(i + 1):
            R_cols[i, j] = col @ Q_cols[j]

    return Q_cols.T, R_cols.T


def cholesky(matrix):
    """Cholesky–Banachiewicz algorithm.

    >>> A = Matrix([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
    >>> L = cholesky(A)
    >>> L.is_lower_triangular
    True
    >>> L @ L.T == A
    True
    >>> L
    Matrix([[2.0, 0, 0], [6.0, 1.0, 0], [-8.0, 5.0, 3.0]])
    """
    assert matrix.is_square, "Not an square matrix"
    order = matrix.shape[0]
    L = Matrix.empty(order)
#    diag = L.diagonal
    for i in range(order):
        for j in range(i + 1):
            if i == j:
                L[i, j] = (matrix[i, j] - sum([L[i, k]**2 for k in range(i)]))**0.5
            else:
                L[i, j] = (matrix[i, j] - sum([L[i, k] * L[j, k] for k in range(i)])) / L[j, j]
    return L


def eigen(matrix):
    """QR algorithm.

    >>> A = Matrix([[2, 1], [1, 2]])
    >>> eigenvalues = eigen(A)
    >>> eigenvalues == Array([3, 1])
    True

    >>> B = Matrix([[2, 0, 0], [0, 3, 4], [0, 4, 9]])
    >>> eigenvalues = eigen(B)
    >>> eigenvalues == Array([2, 11, 1])
    True
    """
    Q, R = qr(matrix)
    while True:
        M = R @ Q
        _Q, _R = qr(M)
        if Q == _Q and R == _R:
            break
        Q, R = _Q, _R

    order = matrix.shape[0]
    eigenvalues = M.diagonal
    for eigenvalue in eigenvalues:
        A = matrix - eigenvalue * Matrix.identity(order)
        A = reduced_echelon_form(A)

    return eigenvalues


if __name__ == '__main__':
    import doctest
    doctest.testmod()
