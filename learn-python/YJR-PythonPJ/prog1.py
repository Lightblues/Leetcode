import random


def dispatch(amount, n):
    out = []
    amount *= 100
    # while True:
    #     if n == 1:
    #         out.append(amount)
    #         break
    #     elif n > 1:
    #         r = random.randint(1, amount-(n-1))
    #         n -= 1
    #         out.append(r)
    #         amount -= r
    for i in range(n, 1, -1):
        r = random.randint(1, amount-(i-1))
        out.append(r)
        amount -= r
    out.append(amount)
    return [i/100 for i in out]


if __name__ == '__main__':
    amount = float(input('Input total amount: '))
    n = int(input('Input n: '))
    answer = dispatch(amount, n)
    for x in answer:
        print('%.2f' % x, end=' ')
    print()
    print('The sum: ', sum(answer))