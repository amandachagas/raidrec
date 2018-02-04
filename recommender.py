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

# items.save('data/items_data')

print "===== ITENS_CLEANNED ====="
print items

print "@ @ @ @ @ @"
print ratings['movieId'].unique().size()

# ratings.show()

training_data, validation_data = gl.recommender.util.random_split_by_user(ratings, 'userId', 'movieId')
model = gl.recommender.create(training_data, 'userId', 'movieId')

# print model

print "U U U U U U U U U U U u"
print items[items['movieId'] == 12]

print "There can be more Itens than Rated Itens..."
print ratings['movieId'].unique().size()
print items['movieId'].unique().size()

print "/ / / / / / / / /"
print model.get_similar_items([12], k=5)

print "\ \ \ \ \ \ \ \ \\"
print model.get_similar_items([12]).join(items, on={'similar': 'movieId'}).sort('rank')


# You can now make recommendations for all the users you've just trained on
results = model.recommend(users=[2])

print "@-@-@-@-@-@"
print results

print " - - - - Big Merge - - - -"
print ratings[ratings['userId'] == 2].join(items, on='movieId')

print "= = = = Recommendations to userId 2 merging item and rating tables = = = ="
print model.recommend(users=[2], k=20).join(items, on='movieId').sort('rank')

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
model_content = gl.recommender.item_content_recommender.create(items, 'movieId', ratings, 'userId')
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
data = ratings.filter_by(user_list,'userId')
print data


#fixed group
fixed_group = user_list[:5]
print fixed_group
fixed_rates_m = []

#random group
random_group = random.sample(user_list,5)
print random_group
random_rates_m = []

movie_list = [1721, 110, 480, 364, 260]
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

print fixed_rates_m
print random_rates_m

fixed_strat = g.run_strategies(fixed_rates_m, 2)
print fixed_strat
random_strat = g.run_strategies(random_rates_m, 2)
print random_strat

movie_group = gl.SFrame()
movie_group['movieId'] = movie_list
movie_group['userId'] = 98765

for key, value in fixed_strat.iteritems():
	print '<---------------------------------------------------------------------------->'
	print '<---- Recommending based on the "%s" with the fixed groups ---->'% key
	print '<---------------------------------------------------------------------------->'
	movie_group['rating'] = value
	print movie_group['rating']
	print model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

for key, value in random_strat.iteritems():
	print '<---------------------------------------------------------------------------->'
	print '<---- Recommending based on the "%s" with the random groups ---->'% key
	print '<---------------------------------------------------------------------------->'
	movie_group['rating'] = value
	print movie_group['rating']
	print model_content.recommend(users=[98765], new_observation_data=movie_group).join(items, on='movieId').sort('rank')

### Use the following lines to fast load your data in SFrame format
# same_items_data = gl.load_sframe('data/items_data')
# same_ratings_data = gl.load_sframe('data/ratings_data')

# same_items_data
# same_ratings_data