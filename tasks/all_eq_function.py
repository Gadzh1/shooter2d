def all_eq(lst):
    biggest = max(lst, key=lambda i: len(i))
    print(biggest)
    listt_2 = []
    for i in lst:
        listt_2.append((i + '_' * (len(biggest) - len(i))))
    return listt_2


listt = ['asd', 'asd', 'asdd']

print(all_eq(['крот', 'белка', 'выхухоль']))
print(all_eq(['a', 'aa', 'aaa', 'aaaa', 'aaaaa']))
print(all_eq(['qweasdqweas', 'q', 'rteww', 'ewqqqqq']))
