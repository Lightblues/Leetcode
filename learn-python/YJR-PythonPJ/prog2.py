

def construct_movies_by_director(datalist):
    directors = {}
    for data in datalist:
        year, name, pf, director = data
        if director not in directors:
            directors[director] = [(year, name, pf)]
        else:
            _data = (year, name, pf)
            if _data in directors[director]:
                raise Exception('重复数据')
            directors[director].append(_data)
    return directors

def top_directors(movielist):
    pfs = []
    for director, moives in movielist.items():
        total_pf = sum([movie[2] for movie in moives])
        pfs.append((director, total_pf))
    pfs.sort(key=lambda i: i[1], reverse=True)
    return pfs

if __name__ == '__main__':
    data_list = [(2013, 'Rush', 26.9, 'Ron Howard'),
                 (2001, 'A Beautiful Mind', 171, 'Ron Howard'),
                 # (2001, 'A Beautiful Mind', 171, 'Ron Howard'),
                 (2008, 'Hunger', 154, 'Steve McQueen')]
    try:
        movie_dict = construct_movies_by_director(data_list)
        sorted_list = top_directors(movie_dict)
        # print(movie_dict)
        print(sorted_list)
    except Exception as e:
        print(e)

