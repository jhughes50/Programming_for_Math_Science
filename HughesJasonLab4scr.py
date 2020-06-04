from HughesJasonLab4mod import *

X = vector(3, {0:3, 2:3})
Y = vector(3, {1:2, 2:4})

print('Attributes of my Vector class: \n')
for attr in vector.__dict__:
    print(attr)

print('\nAttributes of my vector instance\n')
for attr in X.__dict__:
    print (attr, X.__dict__[attr])

print('And we access the data members: \n')
print(X.n)
print(X.f)

print('\nLets multiply:')

print(X * Y)
    
print('\nAdditon:')
print(X+Y)

print('\nSubraction:')
print(Y-X)

print('\nDivision:')
print(X / 2)

print('\nLength:')
print(X.norm())

print('\nProjection:')
print(X.proj(Y))
