import graphlab as gl
import groups as g
import json

# gl.canvas.set_target("ipynb")

## Run the following lines once to parse the data in SFrame format
items = gl.SFrame.read_csv('data/movies.csv')
items.save('data/items_data_saved.csv', format='csv')
ratings = gl.SFrame.read_csv('data/ratings.csv')
# ratings.save('data/ratings_data')

print "===== ITENS ====="
print items
print "----- RATINGS -----"
print ratings

items['year'] = items['title'].apply(lambda x: x[-5:-1])
items['title'] = items['title'].apply(lambda x: x[:-7])
items['genres'] = items['genres'].apply(lambda x: x.split('|'))

# items.save('data/items_data')

print "[][[][][][]"
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

print "VAI FILHA A A A A A A A A AO"
print model.recommend(users=[99999], new_observation_data=recent_data).join(items, on='movieId').sort('rank')

print " = = = = = = = = = = = = = = = = = = = = = = "
print "          - MODEL BASED ON CONTENT -         "
print " = = = = = = = = = = = = = = = = = = = = = = "
print items[items['movieId'] == 595]
print items[items['movieId'] == 597]
print items[items['movieId'] == 12]

# # model_content = gl.recommender.item_content_recommender.get_default_options()
# model_content = gl.recommender.item_content_recommender.create(items, 'movieId', ratings, 'userId')
# print "   #&@!# @&# @#* @ #*@#( *@( #@( #(# (@"
# print model_content.recommend(users=[99999], new_observation_data=recent_data).join(items, on='movieId').sort('rank')

# print model_content.recommend_from_interactions([0])

#>>>use this to export SFrame into json
#ratings.export_json('data/ratings.json', orient='records')
print " = = = = = Initializing Group = = = = = "
matrix = g.group_by_rated_movies(5, ratings,gl.aggregate)
print matrix

print " = = Avaliacoes filmes = = "
av_titanic = ratings[ratings['movieId'] == 1721]
print "Tamanho Titanic:"
print len(av_titanic)
print av_titanic.print_rows(num_rows=164)
print av_titanic[av_titanic['userId'] == 125]
av_braveheart = ratings[ratings['movieId'] == 110]
print "Tamanho Braveheart:"
print len(av_braveheart)
av_jurassic_park = ratings[ratings['movieId'] == 480]
print "Tamanho Jurassic Park:"
print len(av_jurassic_park)
av_lion_king = ratings[ratings['movieId'] == 364]
print "Tamanho Lion King:"
print len(av_lion_king)
av_star_wars_4 = ratings[ratings['movieId'] == 260]
print "Tamanho Star Wars 4:"
print len(av_star_wars_4)
# print av_titanic

count_2 = 0
count_3 = 0
count_4 = 0
count_5 =0
users_rated_5_movies = []

for titanic_obj in av_titanic:
	aux_dict = dict()
	for braveheart_obj in av_braveheart:
		if titanic_obj['userId'] == braveheart_obj['userId']:
			count_2+=1
			for jurassic_park_obj in av_jurassic_park:
				if titanic_obj['userId'] == jurassic_park_obj['userId']:
					count_3+=1
					for lion_king_obj in av_lion_king:
						if titanic_obj['userId'] == lion_king_obj['userId']:
							count_4+=1
							for star_wars_4_obj in av_star_wars_4:
								if titanic_obj['userId'] == star_wars_4_obj['userId']:
									count_5+=1
									aux_dict['userId'] = star_wars_4_obj['userId']
									users_rated_5_movies.append(aux_dict)
print count_2
print count_3
print count_4
print count_5
print users_rated_5_movies
# users_rated_5_movies.export_json('data/users_rated_5_movies.json', orient='records')
with open('users_rated_5_movies.json', 'w') as outfile:  
    json.dump(users_rated_5_movies, outfile)


### Use the following lines to fast load your data in SFrame format
# same_items_data = gl.load_sframe('data/items_data')
# same_ratings_data = gl.load_sframe('data/ratings_data')

# same_items_data
# same_ratings_data