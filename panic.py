phrase = "Don't panic!"
plist = list(phrase)
print(phrase, plist)

new_phrase = ''.join(plist[::-1])
print(new_phrase)
plist = plist[1:8:]
# for i in range(4):
#    plist.pop()
# plist.pop(0)
plist.remove("'")
plist.insert(2, plist.pop(3))
plist.append(plist.pop(4))

new_phrase = ''.join(plist)
print(plist)
print(new_phrase)