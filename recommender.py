import graphlab as gl

## Run the following lines once to parse the data in SFrame format
items = gl.SFrame.read_csv('data/movies.csv')
items.save('data/items_data')
ratings = gl.SFrame.read_csv('data/ratings.csv')
ratings.save('data/ratings_data')

items
ratings

### Use the following lines to fast load your data in SFrame format
# same_items_data = gl.load_sframe('data/items_data')
# same_ratings_data = gl.load_sframe('data/ratings_data')

# same_items_data
# same_ratings_data