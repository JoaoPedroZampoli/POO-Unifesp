tupla = 2, 3, 4
print(len(tupla))

basket = {'apple', 'orange', 'apple', 'kiwi'}
print(basket)

a = set('abracadabra')

print(a)

b = set('alacazam')

print(b)

print(a - b)

tel = {'jack': 4098, 'sape': 4139}

print(tel)

tel['guido'] = 4127

print(tel)

del tel['sape']

print(tel)

names = list(tel)
names.sort()

print(names)

print('guido' in tel)

print(dict([('sape', 3912), ('otavio', 1234)]))
