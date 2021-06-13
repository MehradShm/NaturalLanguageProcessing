import streamlit as st
from PIL import Image
import pickle
import numpy as np
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report,confusion_matrix, f1_score

model, vectorizer, df = None, None, None
with open('kSVC.pickle','rb') as f:
    model = pickle.load(f)
with open('kvectorizer.pickle','rb') as f:
    vectorizer = pickle.load(f)
with open('SVCChi2.pickle','rb') as f:
    selector = pickle.load(f)

with open('database.pickle','rb') as f:
    df = pickle.load(f)

def ClassifyAndRecommend(content):
    sample_size, list_of_items,sentences = 5, [],[]
    vectorized = vectorizer.transform([content])
    vectorized = selector.transform(vectorized)
    predicted_label = model.predict(vectorized)[0]
    tmp = df[df['category'] == predicted_label].sample(n=sample_size)
    for i in range(sample_size):
        list_of_items.append(dict(tmp.iloc[i]))
    
    sentences.append('category' + ' --------> '+ predicted_label+'\n'+"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+'\n')
    for item in list_of_items:
        for i,key in enumerate(item.keys()):
            if i!= 0 and i!= len(item.keys())-1:
                sentences.append(str(key) + ' --> '+ str(item[key])+'\n')
        sentences.append('url : ' + item['url'])
        sentences.append('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
    return '\n'.join(sentences)    




st.title("Classifier-Recommender")

logo_image = Image.open('digii.jpg')
st.image(logo_image,width=600)

Content = st.text_area(label="Write your Content:", value='')

if st.button(label='Submit'):
    if Content != '':
        output= ClassifyAndRecommend(Content)
        st.success(output)
    else:
        st.write("Enter Your Review First!")

