# packagaes and dependency import
import pandas as pd
import seaborn as sns # for Exploratory Data Analysis
import numpy as np
import matplotlib
from pandas import DataFrame

matplotlib.use('TkAgg')  # or 'QtAgg' if PyQt is installed {pip install PyQt6}
import matplotlib.pyplot as plt

#Data Import 
data: DataFrame = pd.read_csv("/home/tjselevani/PycharmProjects/PythonProject/data/last-3-months-transactions.csv")

data.head()
