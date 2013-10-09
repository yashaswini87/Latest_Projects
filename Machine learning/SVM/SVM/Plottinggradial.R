#Randomly selecting linear
path="C:/Users/yashu/Desktop/Fall 2013/Machine learning/uspsdata.txt"
mydata=read.table(path)
Type=read.table("C:/Users/yashu/Desktop/Fall 2013/Machine learning/uspscl.txt")
index =1:nrow(mydata)
set.seed(123)
trainindex =sample(index, trunc(0.8*length(index)))
testset= mydata[-trainindex,]
y_test=Type[-trainindex,]
trainset =mydata[trainindex, ]
y_train <- Type[trainindex, ]
index_training=1:nrow(trainset)
set.seed(123)
trainindex1 =sample(index_training, trunc(0.5*length(index_training)))
train1= mydata[-trainindex1,]
y_train1=Type[-trainindex1,]
train2 =mydata[trainindex1, ]
y_train2 <- Type[trainindex1, ]
misclassification_rate1=c()
misclassification_rate2=c()
gamma=c(0.0001,0.001,0.01,0.1,1)
sigma=c()
for (i in gamma){sigma=c(sigma,sqrt(1/(2*i)))}
for ( i in gamma){
  svm.model = svm(y_train1 ~ ., data = train1, kernel="radial",gamma=i)
  svm.pred = predict(svm.model, train2)
  misclassification_rate1=c(misclassification_rate1,crossprod(svm.pred-y_train2)/length(y_train2))
}
for ( i in gamma){
  svm.model = svm(y_train2 ~ ., data = train2, kernel="radial",gamma=i)
  svm.pred = predict(svm.model, train1)
  misclassification_rate2=c(misclassification_rate2,crossprod(svm.pred-y_train1)/length(y_train1))
}

finalmisclassification=(misclassification_rate1+misclassification_rate2)/2
plot (gamma,finalmisclassification,type="l")
plot (sigma,finalmisclassification,type="l")
print (finalmisclassification)
