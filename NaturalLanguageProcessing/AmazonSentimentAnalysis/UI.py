import streamlit as st
from PIL import Image
from SA import *

sentiment_analyzer = Sentiment_Analyzer()

st.title("Amazon Sentiment Analyzer")

logo_image = Image.open('amazon.jpg')
st.image(logo_image,width=600)

SentimentReview = st.text_area(label="Write your Review to get it's Sentiment:", value='Here...')

if st.button(label='Find Sentiment'):
    if SentimentReview != 'Here...':
        sentiment, score = sentiment_analyzer.find_sentiment_Score([SentimentReview])
        st.success("Your Review's Sentiment is: {}, and it's approximate score is: {}".format(sentiment, np.round(score, 2)))
    else:
        st.write("Enter Your Review First!")

TopicReview = st.text_area(label="Write your Review to get it's Topic:", value='Here...')

if st.button(label='Find Topic'):
    if TopicReview != 'Here...':
        review_topic = sentiment_analyzer.find_topic([TopicReview])
        st.success('Your Review is Probably in Topic: {}'.format(review_topic))
    else:
        st.write("Enter Your Review First!")