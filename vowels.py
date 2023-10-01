
vowels = ['a', 'e', 'i', 'o', 'u', 'y']
word = input("Provide a word to search for vowels: ")

vowels_dict = {}
found = []
word_consonant = []

for letter in word:
    if letter in vowels:
        vowels_dict.setdefault(letter, 0)
        vowels_dict[letter] += 1
        if letter not in found:
            found.append(letter)

print(sorted(found))
for k, v in sorted(vowels_dict.items()):
    print(k, v, sep=':')
