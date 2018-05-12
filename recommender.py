import graphlab as gl
import groups as g
import json
import random

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
print " = = = = = = = = = = = = = = = = = = = = = = "
print "          - MODEL BASED ON ITEM_SIMILARITY -         "
print " = = = = = = = = = = = = = = = = = = = = = = "
training_data, validation_data = gl.recommender.util.random_split_by_user(ratings, 'userId', 'movieId')
model = gl.recommender.create(training_data, 'userId', 'movieId')

print " = = = = = = = EVALUATING ITEM_SIMILARITY MODEL = = = = = = = ="
evalPrecisionRecall = model.evaluate_precision_recall(validation_data)
evalRMSE = model.evaluate_rmse(validation_data, target='rating')
eval = model.evaluate(validation_data)
print(eval)

# print model

# print "U U U U U U U U U U U u"
# print items[items['movieId'] == 12]

print "There can be more Itens than Rated Itens..."
print ratings['movieId'].unique().size()
print items['movieId'].unique().size()

# print "/ / / / / / / / /"
# print model.get_similar_items([12], k=5)

# print "\ \ \ \ \ \ \ \ \\"
# print model.get_similar_items([12]).join(items, on={'similar': 'movieId'}).sort('rank')


# You can now make recommendations for all the users you've just trained on
# results = model.recommend(users=[2])
# print "@-@-@-@-@-@"
# print results

# print " - - - - Big Merge - - - -"
# print ratings[ratings['userId'] == 2].join(items, on='movieId')

# print "= = = = Recommendations to userId 2 merging item and rating tables = = = ="
# print model.recommend(users=[2], k=20).join(items, on='movieId').sort('rank')

recent_data = gl.SFrame()
recent_data['movieId'] = [595, 597, 12]   # Indiana Jones and the Last Crusade
recent_data['rating'] = [3.0, 4.0, 4.5]
recent_data['userId'] = 99999

print " = = = = = RECS For userId 99999 - BASED ON ITEM_SIMILARITY = = = = = = "
print model.recommend(users=[99999], new_observation_data=recent_data).join(items, on='movieId').sort('rank')

print " = = = = = = = = = = = = = = = = = = = = = = "
print "          - MODEL BASED ON CONTENT -         "
print " = = = = = = = = = = = = = = = = = = = = = = "
# print items[items['movieId'] == 595]
# print items[items['movieId'] == 597]
# print items[items['movieId'] == 12]

# model_content = gl.recommender.item_content_recommender.get_default_options()
train_content, test_content = gl.recommender.util.random_split_by_user(ratings, 'userId', 'movieId')
model_content = gl.recommender.item_content_recommender.create(items, 'movieId', ratings, 'userId', 'rating')
print " = = = = = RECS For userId 99999 - BASED ON ITEM CONTENT = = = = = = "
print model_content.recommend(users=[99999], new_observation_data=recent_data).join(items, on='movieId').sort('rank')

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

movie_list = [1721, 110, 364, 260, 71379]
for m in movie_list:
	m_frame = ratings.filter_by(m,'movieId')
	fixed_rates = []
	for u in fixed_group:
		fixed_rates.append(m_frame.filter_by(u,'userId')['rating'][0])
	fixed_rates_m.append(fixed_rates)

	# random_rates = []
	# for u in random_group:
	# 	random_rates.append(m_frame.filter_by(u,'userId')['rating'][0])
	# random_rates_m.append(random_rates)

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

# print "\n...Individual rates in the random group..."
# i=0
# print '|               Movie Name               |     Rate by users      |'
# for aux in random_rates_m:
# 	txt = '|{message: <40}|'.format(message=items.filter_by(movie_list[i],'movieId')['title'][0])
# 	for item in aux:
# 		txt+= " %.1f " % item
# 	txt += "|"
# 	print txt
# 	i+=1

fixed_strat = g.run_strategies(fixed_rates_m, 2)
print "\n>>>>>Fixed Group Rates after strategies are applied<<<<<<"
print "|            Strategy            |               Rates               |"
for key,value in fixed_strat.iteritems():
	txt = "| {message: <30} |".format(message=key)
	for item in value:
		txt+= " %.3f " % item
	txt += "|"
	print txt

# random_strat = g.run_strategies(random_rates_m, 2)
# print "\n>>>>>Random Group Rates after strategies are applied<<<<<<"
# print "|            Strategy            |               Rates               |"
# for key,value in random_strat.iteritems():
# 	txt = "| {message: <30} |".format(message=key)
# 	for item in value:
# 		txt+= " %.3f " % item
# 	txt += "|"
# 	print txt

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


print " - / - / - / - / - / - / - / - "

newItems=items.copy()

contentTrain = gl.item_content_recommender.create(newItems, 'movieId', train_content, 'userId', target='rating')
evalPrecisionRecall = contentTrain.evaluate_precision_recall(test_content)
evalRMSE = contentTrain.evaluate_rmse(test_content, target='rating')
eval = contentTrain.evaluate(test_content)
print(eval)


# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

# print newItems['year'].sketch_summary()
# print newItems['genres'].sketch_summary()
# print newItems['title'].sketch_summary()


# for key, value in random_strat.iteritems():
# 	print '<---------------------------------------------------------------------------->'
# 	print '<---- Recommending based on the "%s" with the random groups ---->'% key
# 	print '<---------------------------------------------------------------------------->'
# 	movie_group['rating'] = value
# 	print movie_group['rating']
# 	print model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

# ## Use the following lines to fast load your data in SFrame format
# same_items_data = gl.load_sframe('data/items_data')
# same_ratings_data = gl.load_sframe('data/ratings_data')

# same_items_data
# same_ratings_data