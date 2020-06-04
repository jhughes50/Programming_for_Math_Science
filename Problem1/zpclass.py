######################
###  Jason Hughes  ###
# Programming Final  #
#### Problem One #####
######################

from math import pow


class Zp:

    def __init__ (self, n, p):
        "' Inititalizer function: p, a prime number stays as p. n is the remainder of integer
        integer divion.'"
        self.p = p
        self.n = n % self.p

    def __add__ (self, other):
        "' A funtion to add two numbers and take the remainder of the sum when
        integer-divided by p '"
        return Zp((self.n + other.n), self.p)

    def __neg__ (self):
        "' A function to negate n. '"
        return Zp(-self.n, self.p)

    def __sub__ (self, other):
        "' A function to subtract two numbers and take the remainder of the suntraction
        sum and divide that by p and give the remainder.'"
        return Zp((self.n - other.n), self.p)

    def __str__ (self):
        "' A function that outputs the answer of modulo division in the form
        n (mod p).'"
        return '%i (mod %i)'% (self.n, self.p)

    def __mul__ (self, other):
        "' A funtion that mutltiplies two numbers and takes the remainder when divided by p. '"
        return Zp((self.n * other.n),self.p)

    def __pow__ (self, p):
        "' A function that raises the n to the p power, we check its correctness with 
        fermat's little thrm. '"
        return Zp((self.n ** self.p),self.p)

    def __truediv__ (self, other):
        "' A function that divides two numbers and and returns the remainder when
        devided with p. We use a special thrm to do this.'"
        return Zp((self.n * (other.n ** self.p - 2)), self.p)

    def atab (self):
        "' A function to output the addition table of interger modulo p. '"
        print('+',end = ' ')
        for i in range(self.p):
            print(i,end = ' ')
        print('\n')

        for k in range(self.p):
            print(k, end = ' ')
            for j in range(self.p):
                w = (k + j) % self.p
                print(w, end = ' ')
            print('\n')

    def mtab (self):
        "' A function to output the multiplication table of integer modulo p. '"
        print('*',end = ' ')
        for i in range(self.p):
            print(i,end = ' ')
        print('\n')

        for k in range(self.p):
            print(k, end = ' ')
            for j in range(self.p):
                w = (k * j) % self.p
                print(w, end = ' ')
            print('\n')
    


a = Zp(3,5)
b = Zp(4,5)
print('a: ',a)
print('b: ',b)
print('+ ',a+b)
print('- ',a-b)
print('* ',a*b)
print('/ ',a/b)
print('** ',a**b)
a.atab()
print('\n')
a.mtab()
