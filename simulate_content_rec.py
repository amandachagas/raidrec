import graphlab as gl
import groups as g
import json
import random

## Run the following lines once to parse the data in SFrame format
items = gl.SFrame.read_csv('data/simulate_movies.csv')
items.save('data/items_data_saved.csv', format='csv')
ratings = gl.SFrame.read_csv('data/simulate_ratings.csv')
# ratings.save('data/ratings_data')

print "===== ITENS_INITIAL ====="
print items
print "----- RATINGS -----"
print ratings

items['year'] = items['title'].apply(lambda x: x[-5:-1])
items['title'] = items['title'].apply(lambda x: x[:-7])
items['genres'] = items['genres'].apply(lambda x: x.split('|'))

items.remove_column('year')

print "===== ITENS_CLEANNED ====="
print items

print " = = = = = = = = = = = = = = = = = = = = = = "
print "          - MODEL BASED ON CONTENT -         "
print " = = = = = = = = = = = = = = = = = = = = = = "

model_content = gl.recommender.item_content_recommender.create(items, 'movieId', ratings, 'userId', 'rating')
print " = = = = = RECS For userId 99999 - BASED ON ITEM CONTENT = = = = = = "
print model_content.recommend(users=[1]).join(items, on='movieId').sort('rank')