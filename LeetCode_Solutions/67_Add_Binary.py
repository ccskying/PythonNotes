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
    '''
    previous two solution's time complexity is O(N + M)
    '''
    def addBinary_bit_by_bit(self, a, b) -> str:
        n = max(len(a), len(b))
        a, b = a.zfill(n), b.zfill(n)
        
        carry = 0
        answer = []
        for i in range(n - 1, -1, -1):
            if a[i] == '1':
                carry += 1
            if b[i] == '1':
                carry += 1
                
            if carry % 2 == 1:
                answer.append('1')
            else:
                answer.append('0')
            
            carry //= 2
        
        if carry == 1:
            answer.append('1')
        answer.reverse()
        
        return ''.join(answer)