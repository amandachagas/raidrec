import graphlab as gl
import groups as g
import json
import random
import evaluate as evaluate
from sklearn.metrics import precision_score, average_precision_score

# gl.canvas.set_target("ipynb")

## Run the following lines once to parse the data in SFrame format
items = gl.SFrame.read_csv('data/movies.csv')
items.save('data/items_data_saved.csv', format='csv')
ratings = gl.SFrame.read_csv('data/ratings.csv')
# ratings.save('data/ratings_data')

print "===== ITENS_INITIAL ====="
print items
print "----- RATINGS -----"
print ratings

items['year'] = items['title'].apply(lambda x: x[-5:-1])
items['title'] = items['title'].apply(lambda x: x[:-7])
items['genres'] = items['genres'].apply(lambda x: x.split('|'))

items.remove_column('year')

print ">>>>>>>>>>>>>>>> NEW ITEEEEEEEMS"
print items
# items.save('data/items_data')

print "===== ITENS_CLEANNED ====="
print items

print "@ @ @ @ @ @"
print ratings['movieId'].unique().size()

# ratings.show()





# print " = = = = = = = = = = = = = = = = = = = = = = "
# print "          - MODEL BASED ON ITEM_SIMILARITY -         "
# print " = = = = = = = = = = = = = = = = = = = = = = "
# training_data, validation_data = gl.recommender.util.random_split_by_user(ratings, 'userId', 'movieId')
# model = gl.recommender.create(training_data, 'userId', 'movieId')

# print " = = = = = = = EVALUATING ITEM_SIMILARITY MODEL = = = = = = = ="
# evalPrecisionRecall = model.evaluate_precision_recall(validation_data)
# evalRMSE = model.evaluate_rmse(validation_data, target='rating')
# eval = model.evaluate(validation_data)
# print(eval)

# # print model

# # print "U U U U U U U U U U U u"
# # print items[items['movieId'] == 12]

# print "There can be more Itens than Rated Itens..."
# print ratings['movieId'].unique().size()
# print items['movieId'].unique().size()

# # print "/ / / / / / / / /"
# # print model.get_similar_items([12], k=5)

# # print "\ \ \ \ \ \ \ \ \\"
# # print model.get_similar_items([12]).join(items, on={'similar': 'movieId'}).sort('rank')


# # You can now make recommendations for all the users you've just trained on
# # results = model.recommend(users=[2])
# # print "@-@-@-@-@-@"
# # print results

# # print " - - - - Big Merge - - - -"
# # print ratings[ratings['userId'] == 2].join(items, on='movieId')

# # print "= = = = Recommendations to userId 2 merging item and rating tables = = = ="
# # print model.recommend(users=[2], k=20).join(items, on='movieId').sort('rank')

# recent_data = gl.SFrame()
# recent_data['movieId'] = [595, 597, 12]   # Indiana Jones and the Last Crusade
# recent_data['rating'] = [3.0, 4.0, 4.5]
# recent_data['userId'] = 99999

# print " = = = = = RECS For userId 99999 - BASED ON ITEM_SIMILARITY = = = = = = "
# print model.recommend(users=[99999], new_observation_data=recent_data).join(items, on='movieId').sort('rank')






print " = = = = = = = = = = = = = = = = = = = = = = "
print "          - MODEL BASED ON CONTENT -         "
print " = = = = = = = = = = = = = = = = = = = = = = "
# print items[items['movieId'] == 595]
# print items[items['movieId'] == 597]
# print items[items['movieId'] == 12]

# model_content = gl.recommender.item_content_recommender.get_default_options()
train_content, test_content = gl.recommender.util.random_split_by_user(ratings, 'userId', 'movieId')
model_content = gl.recommender.item_content_recommender.create(items, 'movieId', ratings, 'userId', 'rating',similarity_metrics='pearson')
print " = = = = = RECS For userId 99999 - BASED ON ITEM CONTENT = = = = = = "
# print model_content.recommend(users=[99999], new_observation_data=recent_data).join(items, on='movieId').sort('rank')

# print model_content.recommend_from_interactions([0])

#>>>use this to export SFrame into json
#ratings.export_json('data/ratings.json', orient='records')
print " = = = = = Initializing Group = = = = = "
# matrix = g.group_by_rated_movies(5, ratings,gl.aggregate)
# print matrix
user_file = gl.SFrame.read_json('data/users_rated_5_movies.json')
user_list = list(user_file['userId'])

#fixed group


fixed_group = user_list[:5]

# GRUPO 02
fixed_group = [77,596,442,243,627]

# GRUPO 03
fixed_group = [355,130,213,30,111]

# GRUPO 04
fixed_group = [627,596,388,306,311]

# GRUPO 05
fixed_group = [292,430,509,294,577]

# GRUPO 06
fixed_group = [15,355,562,243,294]

# GRUPO 07
fixed_group = [306,328,353,311,159]

# GRUPO 08
fixed_group = [73,130,577,243,328]

# GRUPO 09
fixed_group = [509,311,77,345,213]

# # GRUPO 10
# fixed_group = [130,355,78,430,111]


print ""
print " = = = = FIXED GROUP = = = = "
print "User ids: %s" % fixed_group
fixed_rates_m = []

#random group
random_group = random.sample(user_list,5)
print ""
print " = = = = RANDOM GROUP = = = = "
print "User ids: %s" % random_group
random_rates_m = []

movie_list = [1721, 110, 480, 364]
# movie_list = [1721, 110, 480, 364, 260]
# movie_list = [1721, 110, 364, 260, 71379]
for m in movie_list:
	m_frame = ratings.filter_by(m,'movieId')
	fixed_rates = []
	for u in fixed_group:
		fixed_rates.append(m_frame.filter_by(u,'userId')['rating'][0])
	fixed_rates_m.append(fixed_rates)

	random_rates = []
	for u in random_group:
		random_rates.append(m_frame.filter_by(u,'userId')['rating'][0])
	random_rates_m.append(random_rates)

print "\n...Individual rates in the fixed group..."
i=0
print '|               Movie Name               |     Rate by users       |'
for aux in fixed_rates_m:
	txt = '|{message: <40}|'.format(message=items.filter_by(movie_list[i],'movieId')['title'][0])
	for item in aux:
		txt+= " %.1f " % item
	txt += "|"
	print txt
	i+=1

print "\n...Individual rates in the random group..."
i=0
print '|               Movie Name               |     Rate by users      |'
for aux in random_rates_m:
	txt = '|{message: <40}|'.format(message=items.filter_by(movie_list[i],'movieId')['title'][0])
	for item in aux:
		txt+= " %.1f " % item
	txt += "|"
	print txt
	i+=1

fixed_strat = g.run_strategies(fixed_rates_m, 2)
print "\n>>>>>Fixed Group Rates after strategies are applied<<<<<<"
print "|            Strategy            |               Rates               |"
for key,value in fixed_strat.iteritems():
	txt = "| {message: <30} |".format(message=key)
	for item in value:
		txt+= " %.3f " % item
	txt += "|"
	print txt

random_strat = g.run_strategies(random_rates_m, 2)
print "\n>>>>>Random Group Rates after strategies are applied<<<<<<"
print "|            Strategy            |               Rates               |"
for key,value in random_strat.iteritems():
	txt = "| {message: <30} |".format(message=key)
	for item in value:
		txt+= " %.3f " % item
	txt += "|"
	print txt

movie_group = gl.SFrame()
movie_group['movieId'] = movie_list
movie_group['userId'] = 98765
print ""
for key, value in fixed_strat.iteritems():
	print '<---------------------------------------------------------------------------->'
	print '<---- Recommending based on the "%s" with the fixed groups ---->'% key
	print '<---------------------------------------------------------------------------->'
	movie_group['rating'] = value
	print movie_group['rating']
	print model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

# for key, value in random_strat.iteritems():
# 	print '<---------------------------------------------------------------------------->'
# 	print '<---- Recommending based on the "%s" with the random groups ---->'% key
# 	print '<---------------------------------------------------------------------------->'
# 	movie_group['rating'] = value
# 	print movie_group['rating']
# 	print model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')


print " - / - / - / - / - / - / - / - "

print fixed_rates_m

group_average = g.average(fixed_rates_m)
group_least_misery = g.least_misery(fixed_rates_m)
group_most_pleasure = g.most_pleasure(fixed_rates_m)
group_multiplicative = g.multiplicative(fixed_rates_m)
group_average_without_misery = g.average_without_misery(fixed_rates_m,2)


movie_group['rating'] = group_average
recs_average = model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

movie_group['rating'] = group_least_misery
recs_least_misery = model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

movie_group['rating'] = group_most_pleasure
recs_most_pleasure = model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

movie_group['rating'] = group_multiplicative
recs_multiplicative = model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

movie_group['rating'] = group_average_without_misery
recs_average_without_misery = model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')


precision_at = 10
cutoff = 3.0

print "oi"
print "User ids: %s" % fixed_group
print "oi"


print "General mean AVERAGE"
result_mean_average = evaluate.run_precision_at(recs_average['movieId'], ratings, precision_at, cutoff)
print result_mean_average
print ""

print "General mean LEAST MISERY"
result_mean_least_misery = evaluate.run_precision_at(recs_least_misery['movieId'], ratings, precision_at, cutoff)
print result_mean_least_misery
print ""

print "General mean MOST PLEASURE"
result_mean_most_pleasure = evaluate.run_precision_at(recs_most_pleasure['movieId'], ratings, precision_at, cutoff)
print result_mean_most_pleasure
print ""

print "General mean MULTIPLICATIVE"
result_mean_multiplicative = evaluate.run_precision_at(recs_multiplicative['movieId'], ratings, precision_at, cutoff)
print result_mean_multiplicative
print ""

print "General mean AVERAGE WITHOUT MISERY"
result_mean_average_without_misery = evaluate.run_precision_at(recs_average_without_misery['movieId'], ratings, precision_at, cutoff)
print result_mean_average_without_misery
print ""



# print "General mean AVERAGE"
# result_mean_average = evaluate.get_database_mean(recs_average['movieId'], ratings,3)
# print result_mean_average

# print "General mean LEAST MISERY"
# result_mean_least_misery = evaluate.get_database_mean(recs_least_misery['movieId'], ratings,4)
# print result_mean_least_misery

# print "General mean MOST PLEASURE"
# result_mean_most_pleasure = evaluate.get_database_mean(recs_most_pleasure['movieId'], ratings,5)
# print result_mean_most_pleasure

# print "General mean MULTIPLICATIVE"
# result_mean_multiplicative = evaluate.get_database_mean(recs_multiplicative['movieId'], ratings,6)
# print result_mean_multiplicative

# print "General mean AVERAGE WITHOUT MISERY"
# result_mean_average_without_misery = evaluate.get_database_mean(recs_average_without_misery['movieId'], ratings,10)
# print result_mean_average_without_misery


# print "> > precision AVE"
# print evaluate.binary_precision(result_mean_average, 3.9)

# print "> > precision LEAST"
# print evaluate.binary_precision(result_mean_least_misery, 3.9)

# print "> > precision MOST"
# print evaluate.binary_precision(result_mean_most_pleasure, 3.9)

# print "> > precision MULTIPLICATIVE"
# print evaluate.binary_precision(result_mean_multiplicative, 3.9)

# print "> > precision WITHOUT"
# print evaluate.binary_precision(result_mean_average_without_misery, 3.9)

