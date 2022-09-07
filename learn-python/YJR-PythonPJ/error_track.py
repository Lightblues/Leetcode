def input_f():
    txt = input("Input int:a int:b float:c (a<b): ")
    txt = txt.strip().split()
    if len(txt) != 3:
        raise Exception("Length error, please input 3 numbers.")
    a, b, c = txt
    # test a b
    if not (a.isdigit() and b.isdigit()):
        raise ValueError('a and b should be int.')
    # text a< b
    if not int(a) < int(b):
        raise Exception('a should < b')
    # test c
    try:
        float(c)
    except Exception as e:
        # raise ValueError('c should be a float')
        raise e
    return [int(a), int(b), float(c)]


if __name__ == '__main__':
    while True:
        try:
            result = input_f()
            print(result)
            break
        except ValueError as e:
            print('ValurError', e)
        except Exception as e:
            print('Exception', e)





