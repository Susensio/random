# Lesson 04: Matrices
# Implement vector arithmetic operations such as addition, division, subtraction, and the vector dot product.

# Lesson 05: Matrix Types and Operations
# Implement other matrix operations such as the determinand, trace and rank.

from lesson3 import Array


class Matrix():

    def __init__(self, matrix):
        assert all(len(matrix[0]) == len(row) for row in matrix), "Matrix not well formed"

        self.matrix = [Array([c for c in row]) for row in matrix]

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, [e.vector for e in self.matrix])

    def __iter__(self):
        yield from self.matrix

    def __len__(self):
        return len(self.matrix)

    @property
    def shape(self):
        """
        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> A.shape
        (2, 3)
        """
        return len(self.matrix), len(self.matrix[0])

    def __getitem__(self, pos):
        try:
            row, col = pos
            return self.matrix[row][col]
        except TypeError:
            row = pos
            return self.matrix[row]

    def __setitem__(self, pos, item):
        try:
            row, col = pos
            self.matrix[row][col] = item
        except TypeError:
            row = pos
            self.matrix[row] = item

    @property
    def T(self):
        """Traspose.

        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> A.T
        Matrix([[1, 4], [2, 5], [3, 6]])
        """
        return Matrix([[self[r, c] for r, _ in enumerate(self)]
                       for c, _ in enumerate(self.matrix[0])])

    def __add__(self, other):
        """Elemnt-wise addition.

        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> B = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> A + B
        Matrix([[2, 4, 6], [8, 10, 12]])
        """
        assert self.shape == other.shape, "Matrices not the same shape"

        addition = [[a + b for a, b in zip(Ai, Bi)] for Ai, Bi in zip(self, other)]
        return Matrix(addition)

    def __neg__(self):
        """Negation.

        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> - A
        Matrix([[-1, -2, -3], [-4, -5, -6]])
        """
        return Matrix([[-e for e in row] for row in self])

    def __sub__(self, other):
        """Elemnt-wise subtraction.

        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> B = Matrix([[1, 2, 3], [6, 5, 4]])
        >>> A - B
        Matrix([[0, 0, 0], [-2, 0, 2]])
        """
        return self + (- other)

    def __matmul__(self, other):
        """Dot product.

        >>> A = Matrix([[1, 2], [3, 4], [5, 6]])
        >>> B = Matrix([[1, 2], [3, 4]])
        >>> A @ B
        Matrix([[7, 10], [15, 22], [23, 34]])

        >>> C = Matrix([[1, -1, 2], [0, -3, 1]])
        >>> D = Matrix([[2, 1, 0]])
        >>> C @ D.T
        Matrix([[1], [-3]])
        """
        assert self.shape[1] == other.shape[0], "Matrices not multiplicable"
        product = [[sum([a * b for a, b in zip(Ai, Bj)])  # Vector dot products A_row · B_col
                    for Bj in other.T.matrix] for Ai in self]
        return Matrix(product)

    @property
    def inverse(self):
        """Inverse.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A.inverse
        Matrix([[-2.0, 1.0], [1.5, -0.5]])
        """
        assert self.is_square
        return self.adjugate / self.det

    @property
    def is_square(self):
        """Square matrix.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A.is_square
        True
        >>> B = Matrix([[1, 2], [3, 4], [5, 6]])
        >>> B.is_square
        False
        """
        rows, cols = self.shape
        return rows == cols

    def __truediv__(self, divisor):
        """Element-wise division.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A / 2
        Matrix([[0.5, 1.0], [1.5, 2.0]])
        """
        return Matrix([[e / divisor for e in row] for row in self])

    def __rmul__(self, factor):
        """Element-wise multiplication.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> 2 * A
        Matrix([[2, 4], [6, 8]])
        """
        return Matrix([[factor * e for e in row] for row in self])

    @property
    def adjugate(self):
        """Traspose of cofactor matrix.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A.adjugate
        Matrix([[4, -2], [-3, 1]])
        """
        assert self.is_square
        cofactor = Matrix([[(-1)**(r + c) * self.minor(r, c).det for c, _ in enumerate(row_values)]
                           for r, row_values in enumerate(self)])
        return cofactor.T

    @property
    def det(self):
        """Recursive calculation.

        >>> A = Matrix([[4]])
        >>> A.det
        4
        >>> B = Matrix([[1, 2], [3, 4]])
        >>> B.det
        -2
        """
        assert self.is_square
        if len(self) == 1:
            return self[0, 0]

        return sum([((-1)**col * e) * self.minor(0, col).det
                    for col, e in enumerate(self.matrix[0])])

    def minor(self, row, col):
        """
        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A.minor(0, 0)
        Matrix([[4]])
        """
        assert self.is_square
        M = Matrix([[e for c, e in enumerate(row_values) if c != col]
                    for r, row_values in enumerate(self) if r != row])
        return M

    def __mul__(self, other):
        """Elemnt-wise multiplication.

        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> B = Matrix([[1, 2, 3], [4, 5, 6]])
        >>> A * B
        Matrix([[1, 4, 9], [16, 25, 36]])
        """
        assert self.shape == other.shape, "Matrices not the same shape"
        product = [[a * b for a, b in zip(Ai, Bi)] for Ai, Bi in zip(self, other)]
        return Matrix(product)

    def is_symmetric(self, other):
        """
        >>> A = Matrix([[1, 2], [3, 4]])
        >>> B = Matrix([[1, 3], [2, 4]])
        >>> A.is_symmetric(B)
        True
        """
        return self.T == other

    def __eq__(self, other):
        return all([[a == b for a, b in zip(Ai, Bi)] for Ai, Bi in zip(self, other)])

    @property
    def trace(self):
        """Sum of the elements on the main diagonal.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A.trace
        5
        """
        assert self.is_square
        return sum(self.diagonal)

    @property
    def diagonal(self):
        """Main diagonal.

        >>> A = Matrix([[1, 2], [3, 4]])
        >>> A.diagonal
        [1, 4]
        """
        assert self.is_square
        return [self[i, i] for i, _ in enumerate(self)]

    @property
    def rank(self):
        """ Recursive

        >>> A = Matrix([[1, 0, 1], [-2, -3, 1], [3, 3, 0]])
        >>> A.rank
        2
        >>> B = Matrix([[1, 1]])
        >>> B.rank
        1
        >>> C = Matrix([[1, 1, 0, 2], [-1, -1, 0, -2]])
        >>> C.rank
        1
        """
        if self.is_square:  # If square matrix, return max of minors' determinant
            side = len(self)
            det = self.det
            if self.det:
                return side
            elif side == 1:
                return 0
            else:
                for i in range(side):
                    for j in range(side):
                        minor = self.minor(i, j)
                        if minor.det:
                            return side - 1
                        else:
                            return minor.rank
        else:   # If rectangular, make it more square removing one row or column
            rows, cols = self.shape
            if rows < cols:
                ranks = []
                for c in range(cols):
                    rank = Matrix([[col for j, col in enumerate(row) if j != c] for row in self]).rank
                    if rank == rows:
                        return rows
                    else:
                        ranks.append(rank)
                return max(ranks)
            else:
                for r in range(rows):
                    rank = Matrix([row for i, row in enumerate(self) if i != r]).rank
                    if rank == cols:
                        return cols
                    else:
                        ranks.append(rank)
                return max(ranks)

    @property
    def is_triangular(self):
        assert self.is_square, "Not a square matrix"
        return self.is_upper_triangular or self.is_lower_triangular

    @property
    def is_upper_triangular(self):
        """
        >>> A = Matrix([[1, 2, 3], [0, 5, 6], [0, 0, 9]])
        >>> A.is_upper_triangular
        True
        >>> B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> B.is_upper_triangular
        False
        """
#        assert self.is_square, "Not a square matrix"
        return all(e == 0 for i, row in enumerate(self) for j, e in enumerate(row) if (i - j) > 0)

    @property
    def is_lower_triangular(self):
        """
        >>> A = Matrix([[1, 0, 0], [4, 5, 0], [7, 8, 9]])
        >>> A.is_lower_triangular
        True
        >>> B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> B.is_upper_triangular
        False
        """
#        assert self.is_square, "Not a square matrix"
        return all(e == 0 for i, row in enumerate(self) for j, e in enumerate(row) if (j - i) > 0)

    def echelon_form(self):
        """Gaussian elimination.

        >>> A = Matrix([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
        >>> A.echelon_form()
        Matrix([[2, 1, -1, 8], [0.0, 0.5, 0.5, 1.0], [0.0, 0.0, -1.0, 1.0]])

        >>> B = Matrix([[1, 3, 1, 9], [1, 1, -1, 1], [3, 11, 5, 35]])
        >>> B.echelon_form()
        Matrix([[1, 3, 1, 9], [0.0, -2.0, -2.0, -8.0], [0.0, 0.0, 0.0, 0.0]])

        >>> C = Matrix([[0, 2, 1, -1], [0, 2, 4, 0], [0, 0, 0, 0]])
        >>> C.echelon_form()
        Matrix([[0, 2, 1, -1], [0.0, 0.0, 3.0, 1.0], [0.0, 0.0, 0.0, 0.0]])

        >>> D = Matrix([[0]])
        >>> D.echelon_form()
        Matrix([[0]])
        """
        M = Matrix(self)
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

    def reduced_echelon_form(self):
        """Full Gauss-Jordan elimination.

        >>> A = Matrix([[1, 3], [1, 4]])
        >>> A.reduced_echelon_form()
        Matrix([[1.0, 0.0], [0.0, 1.0]])

        >>> B = Matrix([[1, 3, 1], [1, 1, -1], [3, 11, 5]])
        >>> B.reduced_echelon_form()
        Matrix([[1.0, 0.0, -2.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]])

        >>> C = Matrix([[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]])
        >>> C.reduced_echelon_form()
        Matrix([[1.0, 0.0, -2.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]])
        """
        M = Matrix(self).echelon_form()
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


#    def plu(self):
#        """Main diagonal.
#
#        >>> A = Matrix([[1, 2], [3, 4]])
#        >>> P, L, U = A.plu
#        >>> P
#        Matrix([[0.0, 1.0], [1.0, 0.0]])
#        >>> L
#        Matrix([[1.0, 0.0], [0.33333333, 1.0]])
#        >>> U
#        Matrix([[3.0, 4.0], [0.0, 0.66666667]])
#        """
#
#        return P, L, U
#


if __name__ == '__main__':
    import doctest
    doctest.testmod()
#    M = [[1,2,3],[10,15,20],[-7,8,-9]]
#    A = Matrix(M)
#    print(A.det)
#    M[0][0] = 100
#    print(A.det)
#    print(A-B)
#    print(A.T)
#    A=Matrix([[1, 1]])
#    print(A.rank)
#    A = Matrix([[0, 2, 1, -1], [0, 2, 4, 0], [0, 0, 0, 0]])
#    print(A)
#    print(A.echelon_form())
