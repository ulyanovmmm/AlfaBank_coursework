# -*- coding: utf-8 -*-
"""coursework_clustering.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YzhdQnsorJrg-Z7szwsmG9ZSa9gJdoZF

скачивание данных тут: https://github.com/ulyanovmmm/AlfaBank_coursework
"""

import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics

"""#Preprocessing"""

data = pd.read_csv('/content/output.csv', converters = {'keywords': literal_eval})
data = data[data['keywords'].map(lambda d: len(d))>1].reset_index().drop('index', axis = 1) # удаляем строки, где нет ключевых слов

data.head(3)

data.info()

data['keywords'] = data['keywords'].str.join(' ') # список в строку

data.head(3)

data.isna().sum() # нулевых значений нет

"""#Model"""

# Векторизация слов
count_vect = CountVectorizer()
bow = count_vect.fit_transform(data['keywords'].values)
bow.shape

bow

terms = count_vect.get_feature_names_out()
terms[20:30]

"""Наиболее простой, но в то же время достаточно неточный метод кластеризации в классической реализации. Он разбивает множество элементов векторного пространства на заранее известное число кластеров k. Действие алгоритма таково, что он стремится минимизировать среднеквадратичное отклонение на точках каждого кластера. Основная идея заключается в том, что на каждой итерации перевычисляется центр масс для каждого кластера, полученного на предыдущем шаге, затем векторы разбиваются на кластеры вновь в соответствии с тем, какой из новых центров оказался ближе по выбранной метрике. Алгоритм завершается, когда на какой-то итерации не происходит изменения кластеров."""

# модель KMeans
model = KMeans(n_clusters = 4,init='k-means++', n_init = 'auto')
model.fit(bow)

# номера кластеров
labels = model.labels_
labels

"""Коэффициент силуэта рассчитывается с использованием среднего внутрикластерного расстояния (a) и среднего расстояния между ближайшими кластерами (b) для каждого образца. Коэффициент силуэта для выборки равен (b - a) / max(a, b). Для пояснения, b - это расстояние между образцом и ближайшим кластером, в который он не входит."""

silhouette_score = metrics.silhouette_score(bow, labels, metric='euclidean')

# кластеры не очень далеки друг от друга
silhouette_score

# посомтрим, на сколько кластеров лучше всего разбивать
for i in range(4,11):
  model = KMeans(n_clusters = i,init='k-means++', n_init = 'auto')
  model.fit(bow)
  labels = model.labels_
  silhouette_score = metrics.silhouette_score(bow, labels, metric='euclidean')
  print(i, 'кластеров, коэффициент -', silhouette_score)

"""#Result"""

# присвоим каждой строке номер кластера, к которому он относится
data['Labels'] = labels

data.head(3)

# кол-во элементов в каждом кластере
data.groupby(['Labels'])['keywords'].count()

# самые популярные слова в кластерах
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = count_vect.get_feature_names_out()
for i in range(4):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
        print()

# генерация ключевых слов основываясь на кластерах
for i in range(4):
    print("A review of assigned to cluster ", i)
    print("-" * 70)
    print(data.iloc[data.groupby(['Labels']).groups[i][0]]['keywords'])
    print('\n')
    print("_" * 70)