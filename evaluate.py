from sklearn.metrics import precision_score


def get_database_mean(recs,ratings,at):
	count = 0
	acc = 0
	result_mean = []
	recs = recs[:at]

	for recs_item in recs:
		for rating_item in ratings:
			if( recs_item ==  rating_item['movieId']):
				count += 1
				acc += rating_item['rating']
		result_mean.append(round(acc/count, 2))
	return result_mean


def binary_precision(result_mean, cutoff):
	binary_mean = []
	returned_movies = []
	for item in result_mean:
		if item >= cutoff:
			binary_mean.append(1)
		else:
			binary_mean.append(0)

		returned_movies.append(1)

	return precision_score(binary_mean, returned_movies)


def run_precision_at(recs, ratings, at, cutoff):
	print at
	print cutoff
	my_result_mean = get_database_mean(recs,ratings,at)
	my_precision = binary_precision(my_result_mean, cutoff)
	return my_precision