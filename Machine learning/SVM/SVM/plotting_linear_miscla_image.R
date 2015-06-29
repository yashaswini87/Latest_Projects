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
for (i in gamma){
  svm.model = svm(y_train1 ~ ., data = train1, kernel="linear",gamma=i)
  svm.pred = predict(svm.model, train2)
  misclassification_rate1=c(misclassification_rate1,crossprod(svm.pred-y_train2)/length(y_train2))
}
for (i in gamma){
  svm.model = svm(y_train2 ~ ., data = train2, kernel="linear",gamma=i)
  svm.pred = predict(svm.model, train1)
  misclassification_rate2=c(misclassification_rate2,crossprod(svm.pred-y_train1)/length(y_train1))
}

finalmisclassification=(misclassification_rate1+misclassification_rate2)/2
j=which.min(finalmisclassification)
best_estimate=gamma[j]
svm.model = svm(y_train ~ ., data = trainset, kernel="linear",gamma=best_estimate)
svm.pred = predict(svm.model, testset)
check_sign=svm.pred*y_test
for (i in (which(check_sign<0)))
  { 
    m=matrix(unlist(testset[i,]),16,16)
    print(image(m,axes=FALSE))
}

