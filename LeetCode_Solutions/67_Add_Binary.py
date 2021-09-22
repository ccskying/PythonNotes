class Solution:
    def addBinary_format_to_int(self, a, b) -> str:
        return '{0:b}'.format(int(a, 2) + int(b, 2))

    def addBinary_binary_calculation(self, a, b) -> str:
        x, y = int(a, 2), int(b, 2)
        # if carry is not 0
        while y:
            # XOR get result without carry
            answer = x ^ y
            # AND get the carry
            carry = (x & y) << 1
            x, y = answer, carry
        # out put of bin() is a string like: "0bXXXX"
        # return the result without "0b"
        return bin(x)[2:]