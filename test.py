# 本来自带换行，加了\就去掉换行
# '''
# print("""\
# A
# B
# C
# \\
# """)
# '''


# s = "#".join("1" + "2" + "3")
# s = '#'.join(['a', 'b', "c"])
# s = "1'23'4"
# s = '1"2"34'
# s = "1''2"
# for s in range(6, 0, -1):
#     # s=sum(range(1,101))
#
#     print(s)
#
# s = [1, 2, 3]
# print(s[:])
#
# # largest 64 bit integer
# x = 2 ** 63 - 1
# # can we increase x?
# y = x + 1
# print(y > x)
# s='-5\\\3'
# print(s)
# print(len(s))
# yuanzu=(1,'a')
# liebiao=[1,'a']
# zidian={1:'a'}
# print(yuanzu)

# print(list(map(lambda x: 2 + (0 if x==1 else 8),range(4))))

# The Sieve of Eratosthenes
# for finding prime numbers in [2,n]
# def prime_sieve(n):
#     multiples = set()
#     primes = set()
#     for i in range(2, n + 1):
#         if i not in multiples:
#             primes.add(i)
#         for j in range(i * i, n + 1, i):
#             multiples.add(j)
#     return sorted(primes)
# print(prime_sieve(100))


# import re
# text = ''' Tell not me; when the butt is out, we will drink water;
# not a drop before: therefore bear up, and board 'em.
# Servant-monster, drink to me memnottt. '''
# matches = re.findall('not|me', text)
# print(len(matches))


# 求两个单词最短编辑距离，还没看懂 Todo
# def levenshtein(a, b):
#     if not a: return len(b)
#     if not b: return len(a)
#     #递归
#     num= levenshtein(a, b[1:])+1
#     return num
#     # return min(levenshtein(a[1:], b[1:])+(a[0] != b[0]), levenshtein(a[1:], b)+1, levenshtein(a, b[1:])+1)
# print(levenshtein("xkcd","cool"))

def a(string):
    if len(string) == 0:
        return "empty"
    return a(string[1:])


stringa = 'cd'
print(a(stringa))

# def jiecheng(n):
#     if n<2:
#         return 1
#     return jiecheng(n-1)*n
# for i in range(10):
#     print("i="+str(i)+"时的阶乘结果："+str(jiecheng(i)))


