# -*- coding: utf-8 -*-
"""Clustering Question 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FZkTMz_7haD1cp89sAQ17KfN9gAF631T
"""

#importing the libraries
import numpy as np
import pandas as pd 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
from plotly import tools
from plotly.subplots import make_subplots
import plotly.offline as py


#importing the dataset
data = pd.read_csv('clusterDataset2021.csv')
X = data.iloc[:, [0]].values
y = data.iloc[:, [1]].values
z = data.iloc[:, [2]].values

#Building the 3D scatter plot
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(projection='3d')
ax.scatter(X, y, z)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
plt.show()

#print min and max of each attribute to understand the ranges
print('min att1 is ', min(X))
print('max att1 is ', max(X))
print('min att2 is ', min(y))
print('max att2 is ', max(y))
print('min att3 is ', min(z))
print('max att3 is ', max(z))

# Use within cluster sum of squares to determine the optimum number of clusters to use in the clustering algorithm
from sklearn.cluster import KMeans
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 21)
    kmeans.fit(data)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Clusters')
plt.ylabel('Within Cluster Sum of Squares')
plt.show()

#Storing the data in a datframe for training the model
x = data[['att1','att2','att3']].values

import sys
np.set_printoptions(threshold=sys.maxsize)

#Training the kmeans model
kmeans = KMeans(n_clusters = 5, init = 'k-means++', random_state = 21)
y_kmeans = kmeans.fit_predict(x)
print(y_kmeans)

#creating the final visualisation fo the clusters with the centroid seeded by kmeans++
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure(figsize = (15,15))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x[y_kmeans == 0, 0], x[y_kmeans == 0, 1], x[y_kmeans == 0, 2], s = 40, c = 'blue', alpha = 0.3, marker='o', label = 'Cluster 1')
ax.scatter(x[y_kmeans == 1, 0], x[y_kmeans == 1, 1],x[y_kmeans == 1, 2], s = 40, c = 'orange', alpha = 0.3, marker='o',  label = 'Cluster 2')
ax.scatter(x[y_kmeans == 2, 0], x[y_kmeans == 2, 1], x[y_kmeans == 2, 2], s = 40, c = 'cyan', alpha = 0.3, marker='o',  label = 'Cluster 3')
ax.scatter(x[y_kmeans == 3, 0], x[y_kmeans == 3, 1], x[y_kmeans == 3, 2], s = 40, c = 'red', alpha = 0.3, marker='o',  label = 'Cluster 4')
ax.scatter(x[y_kmeans == 4, 0], x[y_kmeans == 4, 1], x[y_kmeans == 4, 2], s = 40, c = 'magenta', alpha = 0.3, marker='o',  label = 'Cluster 5')
ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],kmeans.cluster_centers_[:, 2], s = 500, c = 'black', label = 'Centroids')
plt.title('Clusters formed with kmeans++')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
ax.set_zlabel('Z-axis')
plt.legend()
plt.show()

# creating new vis to explore the cluster 2 and cluster 4 a bit better
# 3d scatterplot using plotly
Scene = dict(xaxis = dict(title  = 'X AXIS-->'),yaxis = dict(title  = 'Y AXIS --->'),zaxis = dict(title  = 'Z AXIS -->'))
labels = kmeans.labels_
trace = go.Scatter3d(x=x[:, 0], y=x[:, 1], z=x[:, 2], mode='markers',marker=dict(color = labels, size= 10, line=dict(color= 'black',width = 10)))
layout = go.Layout(margin=dict(l=0,r=0),scene = Scene,height = 800,width = 800)
data = [trace]
fig = go.Figure(data = data, layout = layout)
fig.show()

import scipy.cluster.hierarchy as sch

dendrogram = sch.dendrogram(sch.linkage(x, method = 'ward'))
plt.title('Dendrogam', fontsize = 30)
plt.xlabel('X AXIS')
plt.ylabel('Ecuclidean Distance')
plt.show()

from sklearn.cluster import AgglomerativeClustering
fig = plt.figure()
ax = plt.subplot(111)
hc = AgglomerativeClustering(n_clusters = 5, affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(x)

plt.scatter(x[y_hc == 0, 0], x[y_hc == 0, 1], s = 100, c = 'blue', label = 'cluster 1')
plt.scatter(x[y_hc == 1, 0], x[y_hc == 1, 1], s = 100, c = 'orange', label = 'cluster 2')
plt.scatter(x[y_hc == 2, 0], x[y_hc == 2, 1], s = 100, c = 'cyan', label = 'cluster 3')
plt.scatter(x[y_hc == 3, 0], x[y_hc == 3, 1], s = 100, c = 'red', label = 'cluster 4')
plt.scatter(x[y_hc == 4, 0], x[y_hc == 4, 1], s = 100, c = 'magenta', label = 'cluster 5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:, 1], s = 50, c = 'black' , label = 'centeroid')
plt.title('Hierarchial Clustering, affinity = euclidean, linkage = ward', fontsize = 20)
#moving the legend outside of the plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel(' X ')
plt.ylabel(' Y ')
#plt.grid()
plt.show()

import scipy.cluster.hierarchy as sch

dendrogram = sch.dendrogram(sch.linkage(x, method = 'ward'))
plt.title('Dendrogam', fontsize = 30)
plt.xlabel('X AXIS')
plt.ylabel('Ecuclidean Distance')
plt.show()

#default
from sklearn.cluster import AgglomerativeClustering
fig = plt.figure()
ax = plt.subplot(111)
hc = AgglomerativeClustering(affinity = 'euclidean', linkage = 'ward')
y_hc = hc.fit_predict(x)

plt.scatter(x[y_hc == 0, 0], x[y_hc == 0, 1], s = 100, c = 'blue', label = 'cluster 1')
plt.scatter(x[y_hc == 1, 0], x[y_hc == 1, 1], s = 100, c = 'orange', label = 'cluster 2')
plt.scatter(x[y_hc == 2, 0], x[y_hc == 2, 1], s = 100, c = 'cyan', label = 'cluster 3')
plt.scatter(x[y_hc == 3, 0], x[y_hc == 3, 1], s = 100, c = 'red', label = 'cluster 4')
plt.scatter(x[y_hc == 4, 0], x[y_hc == 4, 1], s = 100, c = 'magenta', label = 'cluster 5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:, 1], s = 50, c = 'black' , label = 'centeroid')
plt.title('Hierarchial Clustering default clusters', fontsize = 20)
#moving the legend outside of the plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel(' X ')
plt.ylabel(' Y ')
#plt.grid()
plt.show()

fig = plt.figure()
ax = plt.subplot(111)
hc = AgglomerativeClustering(n_clusters = 5, affinity = 'cosine', linkage = 'complete')
y_hc = hc.fit_predict(x)

plt.scatter(x[y_hc == 0, 0], x[y_hc == 0, 1], s = 100, c = 'blue', label = 'cluster 1')
plt.scatter(x[y_hc == 1, 0], x[y_hc == 1, 1], s = 100, c = 'orange', label = 'cluster 2')
plt.scatter(x[y_hc == 2, 0], x[y_hc == 2, 1], s = 100, c = 'cyan', label = 'cluster 3')
plt.scatter(x[y_hc == 3, 0], x[y_hc == 3, 1], s = 100, c = 'red', label = 'cluster 4')
plt.scatter(x[y_hc == 4, 0], x[y_hc == 4, 1], s = 100, c = 'magenta', label = 'cluster 5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:, 1], s = 50, c = 'black' , label = 'centeroid')
plt.title('Hierarchial Clustering, Afinity = cosine, Linkage = complete', fontsize = 20)
#moving the legend outside of the plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel(' X ')
plt.ylabel(' Y ')
#plt.grid()
plt.show()

fig = plt.figure()
ax = plt.subplot(111)
hc = AgglomerativeClustering(n_clusters = 5, affinity = 'cosine', linkage = 'average')
y_hc = hc.fit_predict(x)

plt.scatter(x[y_hc == 0, 0], x[y_hc == 0, 1], s = 100, c = 'blue', label = 'cluster 1')
plt.scatter(x[y_hc == 1, 0], x[y_hc == 1, 1], s = 100, c = 'orange', label = 'cluster 2')
plt.scatter(x[y_hc == 2, 0], x[y_hc == 2, 1], s = 100, c = 'cyan', label = 'cluster 3')
plt.scatter(x[y_hc == 3, 0], x[y_hc == 3, 1], s = 100, c = 'red', label = 'cluster 4')
plt.scatter(x[y_hc == 4, 0], x[y_hc == 4, 1], s = 100, c = 'magenta', label = 'cluster 5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:, 1], s = 50, c = 'black' , label = 'centeroid')
plt.title('Hierarchial Clustering, Afinity = cosine, Linkage = average', fontsize = 20)
#moving the legend outside of the plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel(' X ')
plt.ylabel(' Y ')
#plt.grid()
plt.show()

fig = plt.figure()
ax = plt.subplot(111)
hc = AgglomerativeClustering(n_clusters = 5, affinity = 'cosine', linkage = 'single')
y_hc = hc.fit_predict(x)

plt.scatter(x[y_hc == 0, 0], x[y_hc == 0, 1], s = 100, c = 'blue', label = 'cluster 1')
plt.scatter(x[y_hc == 1, 0], x[y_hc == 1, 1], s = 100, c = 'orange', label = 'cluster 2')
plt.scatter(x[y_hc == 2, 0], x[y_hc == 2, 1], s = 100, c = 'cyan', label = 'cluster 3')
plt.scatter(x[y_hc == 3, 0], x[y_hc == 3, 1], s = 100, c = 'red', label = 'cluster 4')
plt.scatter(x[y_hc == 4, 0], x[y_hc == 4, 1], s = 100, c = 'magenta', label = 'cluster 5')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:, 1], s = 50, c = 'black' , label = 'centeroid')
plt.title('Hierarchial Clustering, Afinity = cosine, Linkage = single', fontsize = 20)
#moving the legend outside of the plot area
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel(' X ')
plt.ylabel(' Y ')
#plt.grid()
plt.show()