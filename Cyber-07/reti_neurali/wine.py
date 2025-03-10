import matplotlib.pyplot as plt
from sklearn.datasets import load_wine
import pandas as pd

# Load the wine dataset
wine = load_wine()
print(wine.DESCR)
data = wine.data
target = wine.target


#Scatter plot
fig, ax = plt.subplots()

x_index = 2
y_index = 9

colors = ['blue', 'red', 'green']

for label, color in zip(range(len(wine.target_names)), colors):
    ax.scatter(wine.data[wine.target==label, x_index], 
                wine.data[wine.target==label, y_index],
                label=wine.target_names[label],
                c=color)

ax.set_xlabel(wine.feature_names[x_index])
ax.set_ylabel(wine.feature_names[y_index])
ax.legend(loc='upper left')
plt.show()

# con pandas!!!!!
wine_df = pd.DataFrame(wine.data, columns=wine.feature_names)
pd.plotting.scatter_matrix(wine_df, 
                           c=wine.target
                          )
plt.show()

