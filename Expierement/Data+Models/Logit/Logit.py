import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix

class LogReg():
    def __init__(self):
        self.thetas = None
        self.loss_history = []

    def fit(self, x, y, iter=20000, learning_rate=0.001):
        x, y = x.copy(), y.copy()

        self.add_ones(x)

        thetas, n = np.zeros(x.shape[1]), x.shape[0]

        loss_history = []

        for i in range(iter):
            y_pred = self.h(x, thetas)
            loss_history.append(self.objective(y, y_pred))
            grad = self.gradient(x, y, y_pred, n)
            thetas -= learning_rate * grad
            self.thetas = thetas
            self.loss_history = loss_history

    def predict(self, x):
        x = x.copy()
        self.add_ones(x)
        z = np.dot(x, self.thetas)
        probs = np.array([self.stable_sigmoid(value) for value in z])
        return np.where(probs >= 0.5, 1, 0), probs

    def add_ones(self, x):
        return x.insert(0, 'x0', np.ones(x.shape[0]))

    def h(self, x, thetas):
        z = np.dot(x, thetas)
        return np.array([self.stable_sigmoid(value) for value in z])

    def objective(self, y, y_pred):
        y_one_loss = y * np.log(y_pred + 1e-9)
        y_zero_loss = (1 - y) * np.log(1 - y_pred + 1e-9)
        return -np.mean(y_zero_loss + y_one_loss)

    def gradient(self, x, y, y_pred, n):
        return np.dot(x.T, (y_pred - y)) / n

    def stable_sigmoid(self, z):
        if z >= 0:  return 1 / (1 + np.exp(-z))
        else:   return np.exp(z) / (np.exp(z) + 1)

pd.set_option('display.expand_frame_repr', False)

df = pd.read_csv('_sorted_brisbane_2e4.csv')

print(df.describe())

X = df[['√x (sx) error ', 'Readout assignment error ', 'Prob meas1 prep0 ']]
#X = df[['Readout assignment error ', 'Prob meas1 prep0 ']]
#X = df[['√x (sx) error ', 'Readout assignment error ']]
#X = df[['√x (sx) error ']]
#X = df[['Readout assignment error ']]
#X = df[['Prob meas1 prep0 ']]
y = df['Quality']

X = (X - X.mean()) / X.std()

model = LogReg()

model.fit(X, y)

y_pred, probs = model.predict(X)

print(accuracy_score(y, y_pred))

dd = pd.DataFrame(confusion_matrix(y, y_pred),
             columns = ['Forecast 0', 'Forecast 1'],
             index = ['Actual 0', 'Actual 1'])

print(dd)
