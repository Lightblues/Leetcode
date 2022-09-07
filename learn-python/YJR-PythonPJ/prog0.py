import re

def f(txt):
    sols = []
    lines = txt.splitlines()

    for lineno, line in zip(range(len(lines)), lines):
        normalized_line = re.sub(r'[\s,-]', '', line)
        if not normalized_line.isdigit():
            continue
# '12345'
        total = 0
        for i in range(0, len(normalized_line), 2):
            if i < len(normalized_line)-1:
                total += int(normalized_line[i]) ** int(normalized_line[i+1])
            else:
                total += int(normalized_line[i])

        total = sum(int(i) for i in str(total))

        if total % 2:
            sols.append((lineno + 1, total, normalized_line))

    for item in sols:
        print('[{:^3d}] {:3d} {}'.format(*item))

if __name__ == '__main__':
    txt = """456-556-778
    456, 556, 790
    ab 456
    45655679
    1234
    0
    """
    f(txt)