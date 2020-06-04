#Jason Hughes
#Lab 4

import math

class vector:
    def __init__(self, dim, f):
        self.n = dim
        self.f = {key:float(val) for (key,val) in f.items() if val != 0.0}
    
    def dot (self, other):
        "' This function takes the dot product of two vectors that are given in dictionary form. We take the non-zero values at each key and multiply it by the corresping value at the smae key in the other vector. '"
        commonKeys = [key for key in self.f if key in other.f]
        return sum(self.f[key] * other.f[key] for key in commonKeys)

    def __mul__(self, other):
        "' This function allows us to mupltiply with vectors using exception handling. It ill first see if the dot product works for what is passed (that is we are multiplying by another vector). If that does not work we assume it it is scalar multiplication and in that case we multiply each value by the scalar. '"
        try:
           return( self.dot(other))
        except AttributeError:
        # In here if other is a scalar because dot() would throw if thats the case
            return vector(self.n, {key:other*val for (key,val)in self.f.items()})
        else:
            raise Exception('Multiplication of the vector with non-int, non-float, and non-vector types unsupported')
    
    def __rmul__(self, other):
        "' This function reverse multiplies, that is it detects if a scalar is passed first instead of the dictionary and will prperly preform scalar multiplication. '"
        return self * other

    def __str__(self):
        "' THis function outputs the vector which is dictionary form and outputs it with the postion on top of the value that is in that position if it non zero '"
        keys = self.f.keys()
        w = ''
        for x in keys: w +='   '+ str(x)
        q = ''
        for x in keys: q += '-------'
        s = ''
        for x in keys: s +=' '+ str(round(self.f[x],2))
        d = str(self.n)
        return w + '\n' + q + '\n'+ s + '\n' + 'dimension = ' + d

    def __add__(self, other):
        "' This function takes corresponding values in the two dictionaries and puts them in temp. '"
        temp = {}
        for (key,val) in other.f.items():
            temp[key] = 0
        for (key,val) in self.f.items():
            temp[key] = val
        for (key,val) in other.f.items():
            temp[key]+= val
        return (vector(self.n,temp))

    def __neg__(self):
        "' This function negates each value in the dictionary for the non zero entries. '"
        negation = {}
        for (key, val) in self.f.items():
            negation[key] = -val
        return vector(self.n, negation)

    def __sub__(self, other):
        "' This function subtractes corresponding values from each other  '"
        out = {} 
        for (key, val) in other.f.items():
            out[key] = 0

        for (key, val) in self.f.items():
            out[key] = val

        for (key, val) in other.f.items():
            out[key] = out[key] - val
        return (vector(self.n, out))


    def __truediv__(self, other):
        "' This function divides each value of the dictionary by some number that is passed in. If the number is zero the function will return the origonal vector and do no calculation to it.  '"
        divd = {}
        try:
            for (key, val) in self.f.items():
                divd[key] = val / other
            return vector(self.n, divd)
        except ZeroDivisionError:
            # if there is a divison by zero we simply output the orginal vector
            return vector(self.n, self.f)

    def norm(self):
        "' This Function returns the length of the vector by calculating the square root of the sum of the non zero entries squared. '"
        length = 0
        normal = {}
        for (key,val) in self.f.items():
            normal[key] = val**2
        for (key,val) in normal.items():
            length += val
        return (math.sqrt(length))

    def proj(self, other):
        "' This function calculates the projection of self onto other. In this function we use the dot func. and the __mul__ func. instead of doing all the calculations in here. '"
        projection = {}
        q = self.dot(other)
        w = (other.norm())**2
        
        for (key, val) in other.f.items():
            projection[key] = (q/w) * val
        return (vector(self.n, projection))
