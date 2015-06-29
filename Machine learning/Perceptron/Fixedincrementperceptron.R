fixedperceptron<-function(S,y)
{
  n=dim(S)[1]
  d=dim(S)[2]
  a = c(0,rep(1,d-1))
  r1=abs(S%*%a)
  theta = 1e-5
  a_history=c()
  a_history = c(a)
  y1=classify(S,a)
  k1=y*y1
  cost = sum(r1[which(k1<0),])
  k=0
  # training
  matrix_y=matrix(y)
  while (cost>theta & k<=20){
    a = a + t(matrix_y[1:k,])%*%S[1:k,]
    a_history = c(a_history,a)  
    matrix_a=matrix(a)  
    r1=abs(S%*%matrix_a)
    a1=c()
    a1=c(a)
    y1=classify(S,a1)
    k1=y*y1
    cost = sum(r1[which(k1<0),])
    k=k+1
  }
  a_history=matrix(a_history,nrow=(length(a_history)/d),ncol=d,byrow=T)
  return (a_history)
}