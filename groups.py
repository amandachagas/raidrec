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
        arr.append( float(reduce(lambda x,y: x*y, row))*5/3125 )
    return arr

def average_without_misery(matrix, threshold):
    arr = []
    for row in matrix:
        if min(row)<threshold:
            arr.append(min(row))
        else:
            arr.append( sum(row)/float(len(row)) )
        # wm = [n for n in row if n >= threshold]
        # if(wm):
        #     arr.append( sum(wm)/float(len(wm)) )
        # else:
        #     arr.append(1.0)
    return arr

def run_strategies(matrix, awm_threshold):
    strat = {}
    strat["average"] = average(matrix)
    strat["least_misery"] = least_misery(matrix)
    strat["most_pleasure"] = most_pleasure(matrix)
    strat["multiplicative"] = multiplicative(matrix)
    strat["average_without_misery"] = average_without_misery(matrix, awm_threshold)
    return strat
