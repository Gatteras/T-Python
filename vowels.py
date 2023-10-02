
# vowels = ['a', 'e', 'i', 'o', 'u', 'y']
vowels2 = set('aeiouy')
vowels3 = ('a', 'e', 'i', 'o', 'u', 'y')
vowels_dict = {}
found = []
word = input("Provide a word to search for vowels: ")

found2 = sorted(list(vowels2.intersection(set(word))))
for letter in word:
    if letter in vowels3:
        vowels_dict.setdefault(letter, 0)
        vowels_dict[letter] += 1
        if letter not in found:
            found.append(letter)
print(sorted(found), found2)
for k, v in sorted(vowels_dict.items()):
    print(k, v, sep=':')
