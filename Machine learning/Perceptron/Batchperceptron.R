batchperceptron<-function(S,y)
{
  n=dim(S)[1]
  d=dim(S)[2]
  repeated=matrix(t(matrix(y,n,1*d)),n,d,byrow=T)
  # getting S1 after multiplying y's and x's 
  S1=S*repeated
  a_history=c()
  #initialize
  a = c(0,rep(1,d-1))
  a_history=c(a)
  theta = 1e-5
  # training
  k=1
  y1=classify(S,a)
  k1=y*y1
  # Get the derivative function
  E = S1[which(k1<0),]
  # Get the cost function
  r1=abs(S%*%a)
  cost = sum(r1[which(k1<0),])
  while (cost>theta){
    a = a + sum(E)/k
    a_history=c(a_history,a)
    y1=classify(S,a)
    
    k1=y*y1
    
    E = S1[which(k1<0),]
    r1=abs(S%*%a)
    cost = sum(r1[which(k1<0),])

    k=k+1
  }
    a_history=matrix(a_history,nrow=(length(a_history)/d),ncol=d,byrow=T)
    print (a_history)
}