classify<-function(s,z){
  label=c()
  d=length(z)
  s=s[,1:d-1]
  c=tail(z,1)
  v=head(z,d-1)
  vh=matrix(v,ncol=d-1,byrow=F)
  y=s%*%t(vh)-c
  y=data.frame(t(y))
  
  for (i in 1:length(y))
  {
    if (y[1,i]>0){
      label=c(label,1)  
    }
    else {
      label=c(label,-1)  
    }
    
  }
  return (label)
  
  
}