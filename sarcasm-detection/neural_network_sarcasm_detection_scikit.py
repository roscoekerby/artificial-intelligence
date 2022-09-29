# -*- coding: utf-8 -*-
"""neural-network-sarcasm-detection-scikit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r-iX5oRb4u-flimzjetY4aU5RLFCpFOI

# Preamble
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import re
import nltk
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
import string
# %matplotlib inline

sarcasm = pd.read_json('/content/drive/MyDrive/Colab Notebooks/Sarcasm_Headlines_Dataset.json', lines=True)
sarcasm2 = pd.read_json('/content/drive/MyDrive/Colab Notebooks/Sarcasm_Headlines_Dataset_v2.json', lines=True)

from google.colab import drive
drive.mount('/content/drive')

sarcasm.head()

sarcasm2.head()

sarcasm.info()

"""# Data Normalisation"""

print(sarcasm.isnull().sum())
sarcasm2.isnull().sum()

sarcasm.drop('article_link', axis=1, inplace=True)
sarcasm2.drop('article_link', axis=1, inplace=True)

sarcasm.isnull().sum()

sarcasm.head()

sarcasm2.head()

label_quality = LabelEncoder()

sarcasm['is_sarcastic'] = label_quality.fit_transform(sarcasm['is_sarcastic'])
sarcasm2['is_sarcastic'] = label_quality.fit_transform(sarcasm2['is_sarcastic'])

sarcasm.head(10)

sarcasm2.head()

print(sarcasm['is_sarcastic'].value_counts())
sarcasm2['is_sarcastic'].value_counts()

sns.countplot(sarcasm['is_sarcastic'])
sns.countplot(sarcasm2['is_sarcastic'])

nltk.download('stopwords')
stopword=set(stopwords.words('english'))

def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text=" ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text=" ".join(text)
    return text
sarcasm["headline"] = sarcasm["headline"].apply(clean)
sarcasm2["headline"] = sarcasm2["headline"].apply(clean)
print(sarcasm.head())
sarcasm2.head()

# First dataset training
data = sarcasm[["headline", "is_sarcastic"]]
x = np.array(data["headline"])
y = np.array(data["is_sarcastic"])

cv = CountVectorizer()
X = cv.fit_transform(x) # Fit the Data
# print(X.shape)
# print(y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)


# Second dataset training
data2 = sarcasm2[["headline", "is_sarcastic"]]
x2 = np.array(data2["headline"])
y2 = np.array(data2["is_sarcastic"])

cv2 = CountVectorizer()
X2 = cv2.fit_transform(x2) # Fit the Data

# Dimensions need to match
X2 = X2[:26709, :18833]
y2 = y2[:26709]

X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.20, random_state=42)

"""# Neural Network"""

#Training on subset of dataset 1 and Testing on another mutually exlusive subset of dataset 1 
mlpc = MLPClassifier(hidden_layer_sizes=(11,11,11), max_iter=10000) #500 originally but did not converge
mlpc.fit(X_train, y_train)
pred_mlpc = mlpc.predict(X_test)

#Training on subset of dataset 2 and Testing on another mutually exlusive subset of dataset 2 
mlpc2 = MLPClassifier(hidden_layer_sizes=(11,11,11), max_iter=10000) #500 originally but did not converge
mlpc2.fit(X_train2, y_train2)
pred_mlpc2 = mlpc2.predict(X_test2)

#Training on dataset 1 and testing on dataset 2
model = MLPClassifier(hidden_layer_sizes=(11,11,11), max_iter=10000)
model.fit(X_train, y_train)
pred_model = model.predict(X_test)
#print(model.score(X_test, y_test))

#Training on dataset 2 and testing on dataset 1 
model2 = MLPClassifier(hidden_layer_sizes=(11,11,11), max_iter=10000)
model2.fit(X_train2, y_train2)
pred_model2 = model2.predict(X_test)
#print(model2.score(X_test, y_test))

print(classification_report(y_test, pred_mlpc))
print(confusion_matrix(y_test, pred_mlpc))

print(classification_report(y_test2, pred_mlpc2))
print(confusion_matrix(y_test2, pred_mlpc2))

print(classification_report(y_test2, pred_model))
print(confusion_matrix(y_test2, pred_model))

print(classification_report(y_test, pred_model2))
print(confusion_matrix(y_test, pred_model2))

"""# Accuracy Scores"""

cm = accuracy_score(y_test, pred_mlpc)
cm

cm = accuracy_score(y_test2, pred_mlpc2)
cm

"""# Single sentence predictors"""

user = input("Enter a Text: ")
data = cv.transform([user]).toarray()
output = mlpc.predict(data)
if output == 1:
    print('sarcastic')
else: 
    print ('genuine')