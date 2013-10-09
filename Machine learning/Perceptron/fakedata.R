fakedata <- function(w,n)
{
# Load MASS Library for Null functionality
library(MASS)
LABELS=c()
S = c()
S1 = c()
S2 = c()

d=length(w)-1
c=tail(w,1)
v=head(w,d)
e=Null(v)                                                  # e is d x d-1 matrix
a=rnorm(n*(d-1),0,1)
a = matrix(a,nrow=n,ncol=d-1,byrow=T)      # a is n x d-1 matrix 
x=(a)%*%t(e)                                            # x is n x d matrix
a1= x + (   c*  (v/sum(v*v))   )  
lamda=abs(rnorm(n,0,1))

for (i in 1:n) {
k=lamda[i]*v
t=a1[i,]+k
t = c(t,1)
LABELS=c(LABELS,1)
S = c(S,t) 
}

S1 = matrix(S,nrow=n,ncol=d+1,byrow=T)
C1   = matrix(LABELS,nrow=n,byrow=F)


S = c()

t = c()
LABELS = c()

a=rnorm(n*(d-1),0,1)
a = matrix(a,nrow=n,ncol=d-1,byrow=T)      # a is n x d-1 matrix 
x=(a)%*%t(e)                                            # x is n x d matrix
a1= x + (   c*  (v/sum(v*v))   )  
lamda=-abs(rnorm(n,0,1))

for (i in 1:n) {
k=lamda[i]*v
t=a1[i,]+k
t = c(t,1)
LABELS=c(LABELS,-1)
S = c(S,t) 
}

S2 = matrix(S,nrow=n,ncol=d+1,byrow=T)
C2   = matrix(LABELS,nrow=n,byrow=F)

S = rbind(S1,S2)
C = rbind(C1,C2)

return (cbind(S,C))

}

