import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

SEED = 17
np.random.seed(SEED)

class SimpleLinearRegression:
    def __init__(self, step = 0.01, tol = 1e-4, max_iter=1000, verbose=False, random_state=SEED):
        self.max_iter = max_iter # max iter count of gradient descent
        self.step = step # step of descent in the direction of antigradient
        self.tol = tol # we compare norm of gradient with that threshold
        self._w = None # w_1
        self._intercept = None # w_0
        self.random_state = random_state 
        self.verbose = verbose
        
    def predict(self, X):
        """
        estimate target variable "y" based on features X 
        """
        y_pred = self._w * X + self._intercept
        assert y_pred.shape[0] == X.shape[0]
        return y_pred
    
    def score(self, X, y):
        """
        MSE
        X - features
        y - true values of target variable
        """
        return np.mean((y - self.predict(X))**2)
    
    def _gradient(self, X, y):
        """
        Compute gradient of MSE subject to w_1, w_0
        X - features
        y - true values of target variable
        """
        N = len(X)
        grad_intercept = -2/N * sum((y[i] - self._w * X[i] - self._intercept) for i in range(0, N))
        grad_w = -2/N * sum(X[i]*(y[i] - self._w * X[i] - self._intercept) for i in range(0, N))
        return grad_w, grad_intercept
        
    def fit(self, X, y):
        """
        Train model with gradient descent
        X - features
        y - true values of target variable
        """
        # for reproducable results
        np.random.seed(self.random_state)
        
        # initialize weights
        self._w, self._intercept = np.random.randn(2)
        # perform gradient descent
        for iter in range(self.max_iter):
            # compute gradient at current W
            grad_w, grad_intercept = self._gradient(X, y)
            
            # make step, update W
            self._w = self._w - self.step * grad_w
            self._intercept = self._intercept - self.step * grad_intercept
            
            # compute gradient norm            
            grad_norm = np.sqrt(grad_intercept ** 2 + grad_w ** 2)
            
            # people like to watch how the error is reducing during iterations 
            if self.verbose:
                mse_score = self.score(X, y)
                print('iteration %d, MSE = %f, ||grad|| = %f' % (iter, mse_score, grad_norm))
                
            # compare gradient norm with threshold
            if grad_norm < self.tol:
                print('model converged')
                return self
        print('model did not converge')
        return self

def mse_score(y_true, y_pred):
    """
    y_true - true values of target variable
    y_pred - predicted values of target variable 
    """
    result = np.mean((y_true - y_pred)**2)
    return result

boston_data = datasets.load_boston()
print(boston_data.keys())

df = pd.DataFrame(boston_data['data'], columns=boston_data['feature_names'])
df['target'] = boston_data['target']
df.head()

print(boston_data['DESCR'])

# разбили датасет в соотношении 60:40
df_train, df_test = train_test_split(df, test_size=0.4, random_state=SEED, shuffle=True)

# обучите модель на df_train c verbose=True
# Обратите внимание на отладочный вывод, ваша ошибка MSE должна уменьшаться с каждой итерацией
# мы хотим научится предсказывать значение target по признаку CRIM

model = SimpleLinearRegression(verbose=True)

X_train = np.array(df_train['CRIM'])
y_train = np.array(df_train['target'])
model.fit(X_train, y_train)
y_train_pred = model.predict(X_train)
mse_train_score = mse_score(y_train, y_train_pred)

print('MSE on train:', mse_train_score)

# # посчитали качество обученной модели на df_test

X_test = np.array(df_test["CRIM"])
y_test = np.array(df_test["target"])
y_test_predict = model.predict(X_test)
mse_test_score = mse_score(y_test, y_test_predict)
print('MSE on test:', mse_test_score)
