# Lesson 03: Vectors
# Implement vector arithmetic operations such as addition, division, subtraction, and the vector dot product.

class Array():
    
    def __init__(self, vector):
        self.vector = [e for e in vector]
    
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.vector)
    
    def __iter__(self):
        yield from self.vector
        
    def __len__(self):
        return len(self.vector)

    def __getitem__(self, index):
        return self.vector[index]
        
    def __setitem__(self, index, item):
        self.vector[index] = item
        
    def __add__(self, other):
        """Elemnt-wise addition.
        a + b = (a1+b1, a2+b2, a3+b3)

        >>> Array([1, 2, 3]) + Array([4, 5, 6])
        Array([5, 7, 9])
        """

        addition = [e1 + e2 for e1, e2 in zip(self, other)]
        return Array(addition)
        
    def __sub__(self, other):
        """Elemnt-wise subtraction.
        a - b = (a1-b1, a2-b2, a3-b3)

        >>> Array([1, 2, 3]) - Array([4, 5, 6])
        Array([-3, -3, -3])
        """

        addition = [e1 - e2 for e1, e2 in zip(self, other)]
        return Array(addition)
    


    def __mul__(self, other):
        """Element-wise multiplication.
        a * b = (a1*b1, a2*b2, a3*b3)

        >>> Array([1, 2, 3]) * Array([4, 5, 6])
        Array([4, 10, 18])
        """

        product = [e1 * e2 for e1, e2 in zip(self, other)]
        return Array(product)
        
    def __rmul__(self, number):
        """Element-wise multiplication by number
        n * a = (n*a1, n*a2, n*a3)

        >>> 5 * Array([4, 5, 6])
        Array([20, 25, 30])
        """

        product = [number * e for e in self]
        return Array(product)


    def __truediv__(self, other):
        """Elemnt-wise division.
        a / b = (a1/b1, a2/b2, a3/b3)

        >>> Array([1, 2, 3]) / Array([4, 5, 6])
        Array([0.25, 0.4, 0.5])
        
        >>> Array([1, 2, 3]) / 2
        Array([0.5, 1.0, 1.5])
        """
        try:
            division = [e1 / e2 for e1, e2 in zip(self, other)]
        except TypeError:
            division = [e / other for e in self]
        return Array(division)     


    def __matmul__(self, other):
        """Vector dot product.
        a · b = a1*b1 + a2*b2 + a3*b3

        >>> Array([1, 2, 3]) @ (Array([4, 5, 6]))
        32
        """

        dot_product = sum(self * other)
        return dot_product


if __name__ == '__main__':
    import doctest
    doctest.testmod()
