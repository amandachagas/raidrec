import random
#groups users based on the amount k of the same rated movies
def group_by_rated_movies(rating_count, ratings, agg):
    print "<-- Aggregating-->"
    matrix = []
    movie_id_count = ratings.groupby(key_columns='movieId',operations={'count':agg.COUNT()}).sort('count',ascending=False)
    movie_rated_times = movie_id_count['count'].filter(lambda x: x>rating_count)

    k=5
    i=0
    # l1 = list(ratings.filter_by(movie_id_count[0]['movieId'],'movieId')['userId'])
    # l2 = list(ratings.filter_by(movie_id_count[1]['movieId'],'movieId')['userId'])
    # inter = list(set(l1).intersection(l2))
    # print inter
    # print len(inter)

    movie_id = movie_id_count[0]['movieId']
    frame = ratings.filter_by(movie_id,'movieId')
    l = list(frame['userId'])

    similar = []
    while i<len(movie_rated_times):        
        movie_id = movie_id_count[i]['movieId']
        frame = ratings.filter_by(movie_id,'movieId')
        if len(list(set(l).intersection(list(frame['userId']))))>k:
            similar.append(movie_id)
        i+=1
    print similar

    # while len(matrix) < k and i<len(movie_rated_times):
    #     movie_id = movie_id_count[i]['movieId']
    #     frame = ratings.filter_by(movie_id,'movieId')
    #     l = list(frame['userId'])

    #     print l
    #     matrix.append(frame)
    #     i+=1


    return matrix

def average(matrix):
    arr = []
    for row in matrix:
        arr.append( sum(row)/float(len(row)) )
    return arr

def least_misery(matrix):
    arr = []
    for row in matrix:
        arr.append( float(min(row)) )
    return arr

def most_pleasure(matrix):
    arr = []
    for row in matrix:
        arr.append( float(max(row)) )
    return arr

def multiplicative(matrix):
    arr = []
    for row in matrix:
        arr.append( float(reduce(lambda x,y: x*y, row)) )
    return arr

def average_without_misery(matrix, threshold):
    arr = []
    for row in matrix:
        wm = [n for n in row if n >= threshold]
        if(wm):
            arr.append( sum(wm)/float(len(wm)) )
        else:
            arr.append(0.0)
    return arr

def test_strategies(matrix, awm_threshold):
    print '<--Average-->'
    print average(matrix)
    print '<--Least Misery-->'
    print least_misery(matrix)
    print '<--Most Pleasure-->'
    print most_pleasure(matrix)
    print '<--Multiplicative-->'
    print multiplicative(matrix)
    print '<--Average Without Misery-->'
    print average_without_misery(matrix, awm_threshold)

def run_strategies(matrix, awm_threshold):
    strat = {}
    strat["average"] = average(matrix)
    strat["least_misery"] = least_misery(matrix)
    strat["most_pleasure"] = most_pleasure(matrix)
    strat["multiplicative"] = multiplicative(matrix)
    strat["average_without_misery"] = average_without_misery(matrix, awm_threshold)
    return strat

def test_file():
    matrix = [
            [1,2,3],
            [2,3,4],
            [4,5,6,7]
        ]
    test_strategies(matrix , 3.0)