def func(a, b=4, *args, **kwargs):
    print(a, b, args, kwargs)

if __name__ == '__main__':
    func(1)
    func(1, 2,)
    func(1,2,3,4,5,)
    func(1,2,3,4,c=3, d=4)

    # l = [3,4,5]
    # func(1,2,*l)
    l = range(0, 6)
    func(*l)

    kws = {'c':3, 'd':4}
    func(*l, **kws)