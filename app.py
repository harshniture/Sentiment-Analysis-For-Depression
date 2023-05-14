from flask import Flask, request, jsonify
import tweepy
import re
import pickle

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the Tweepy API credentials
consumer_key = 'UqHRhFlJ7KXj5onzKFkdUI9uq'
consumer_secret = 'm7xO2XlzuyuQ7gQtvwKz4d7weZIl0Zs0KiRrakRjzCaQoUzkgK'
access_key = '1487411554215555072-6ou3xZf8SB3KIOYbzz4R1RjYiy73Z1'
access_secret = 'UibHIscgD3o8TRXJ8DfPUC3Yu02ENKkj5cSPKtbMXNOkc'

# Authenticate with Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the tweet from the request data
    tweet = request.get_json()['tweet']

    # Preprocess the tweet
    tweet = re.sub(r'http\S+', '', tweet) # Remove URLs
    tweet = re.sub('[^A-Za-z0-9]+', ' ', tweet) # Remove special characters
    tweet = tweet.lower() # Convert to lowercase

    # Predict the sentiment of the tweet
    sentiment = model.predict([tweet])[0]

    # Return the sentiment as a JSON response
    response = {'sentiment': sentiment}
    return jsonify(response)

@app.route('/search', methods=['POST'])
def search():
    # Get the search query from the request data
    query = request.get_json()['query']

    # Search for tweets that match the query
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en', tweet_mode='extended').items(100)

    # Preprocess the tweets and predict their sentiments
    predictions = []
    for tweet in tweets:
        text = tweet.full_text
        text = re.sub(r'http\S+', '', text) # Remove URLs
        text = re.sub('[^A-Za-z0-9]+', ' ', text) # Remove special characters
        text = text.lower() # Convert to lowercase
        sentiment = model.predict([text])[0]
        predictions.append({'text': text, 'sentiment': sentiment})

    # Return the predicted sentiments as a JSON response
    response = {'predictions': predictions}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
