from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
# fit a k-nearest neighbor model to the data
X = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]]) #X为4个标签的坐标
y = ['A','A','B','B']                          #y为4个标签坐标的类别，这里只有2个类别，A和B
model = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
           metric_params=None, n_neighbors=2, p=2, weights='uniform')
#注意n_neighbors=2，这个是标签坐标数量，其他参数不用管

model.fit(X, y) #建立模型
print(model)

# make predictions
expected = ['B'] 
predicted = model.predict([[0,0]])#可以修改[]内的坐标，这是test set
# summarize the fit of the model
print(metrics.classification_report(expected, predicted))
print(metrics.confusion_matrix(expected, predicted))