#groups users based on the amount k of the same rated movies
def group_by_rated_movies(k, ratings):
    matrix = []
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