import random
#groups users based on the amount k of the same rated movies
def group_by_rated_movies(rating_count, ratings, agg):
    print "<-- Aggregating-->"
    matrix = []
    movie_id_count = ratings.groupby(key_columns='movieId',operations={'count':agg.COUNT()}).sort('count',ascending=False)
    #movie_rated_times = movie_id_count['count'].filter(lambda x: x>rating_count)

    # while len(matrix) < k:
    #     movie_id = random.choice(ratings['movieId'].unique())
    #     frame = ratings.filter_by(movie_id,'movieId')
    #     if frame.num_rows()>=5
    #         matrix.append(test)

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


matrix = [
        [1,2,3],
        [2,3,4],
        [4,5,6,7]
    ]
test_strategies(matrix , 3.0)