from sklearn.metrics import precision_score


def get_database_mean(recs,ratings):
	count = 0
	acc = 0
	result_mean = []

	for recs_item in recs:
		for rating_item in ratings:
			if( recs_item ==  rating_item['movieId']):
				count += 1
				acc += rating_item['rating']
		result_mean.append(round(acc/count, 2))
	return result_mean


def binary_precision(result_mean, cutoff):
	binary_mean = []
	for item in result_mean:
		if item >= cutoff:
			binary_mean.append(1)
		else:
			binary_mean.append(0)

	print "Binary Average: "
	print binary_mean

	returned_movies = [1,1,1,1,1,1,1,1,1,1]

	return precision_score(binary_mean, returned_movies)
