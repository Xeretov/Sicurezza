# sudo apt install python3-scikit-learn
# sudo apt install python3-sklearn

import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


from sklearn.datasets import load_iris
iris = load_iris()

print(iris["target_names"])
print(iris.target_names)

n_samples, n_features = iris.data.shape
print('Number of samples:', n_samples)
print('Number of features:', n_features)
# the sepal length, sepal width, petal length and petal width of the first sample (first flower)
print(iris.data[0])

## Istogramma
# fig, ax = plt.subplots()
# x_index = 3
# colors = ['blue', 'red', 'green']

# for label, color in zip(range(len(iris.target_names)), colors):
#     ax.hist(iris.data[iris.target==label, x_index], label=iris.target_names[label], color=color)

# ax.set_xlabel(iris.feature_names[x_index])
# ax.legend(loc='upper right')
# plt.show()


# #Scatter plot
# fig, ax = plt.subplots()

# x_index = 3
# y_index = 0

# colors = ['blue', 'red', 'green']

# for label, color in zip(range(len(iris.target_names)), colors):
#     ax.scatter(iris.data[iris.target==label, x_index], 
#                 iris.data[iris.target==label, y_index],
#                 label=iris.target_names[label],
#                 c=color)

# ax.set_xlabel(iris.feature_names[x_index])
# ax.set_ylabel(iris.feature_names[y_index])
# ax.legend(loc='upper left')
# plt.show()

# n = len(iris.feature_names)
# fig, ax = plt.subplots(n, n, figsize=(16, 16))

# colors = ['blue', 'red', 'green']

# for x in range(n):
#     for y in range(n):
#         xname = iris.feature_names[x]
#         yname = iris.feature_names[y]
#         for color_ind in range(len(iris.target_names)):
#             ax[x, y].scatter(iris.data[iris.target==color_ind, x], 
#                              iris.data[iris.target==color_ind, y],
#                              label=iris.target_names[color_ind],
#                              c=colors[color_ind])

#         ax[x, y].set_xlabel(xname)
#         ax[x, y].set_ylabel(yname)
#         ax[x, y].legend(loc='upper left')

# plt.show()

# Pandas
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
pd.plotting.scatter_matrix(iris_df, 
                           c=iris.target, 
                           figsize=(8, 8)
                          );
plt.show()

