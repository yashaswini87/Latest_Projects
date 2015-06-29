rankall<-function(outcome,num){
data<-read.csv("outcome-of-care-measures.csv")
s<-vector('list',0)
s<-unique(data[,7],incomparable=FALSE)
s<-sort(s)
n<-length(s)
k<-vector('list',0)
p<-vector('list',0)
hospital<-vector('list',0)
state<-vector('list',0)
  for (i in 1:n){
    t<-paste0("",s[i],"")
    data1<-subset(data,State==t)
    ##print(nrow(data1))
    ##if(nrow(data1)==0){stop("invalid state",call.=TRUE)}
      if (outcome=="heart attack")suppressWarnings({
      data1[,11]<-as.numeric(as.character(data1[,11]))
      ##data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
      data2<-data1[order(data1[,11],data1[,2],na.last=NA,decreasing=FALSE),]
      k<-data2[,2]
      p<-data2[,7]
      if(!missing(num)){
        if(num=="best"){hospital[i]<-as.character(head(k,1))
                        state[i]<-as.character(head(p,1))}                    
        else if(num=="worst"){hospital[i]<-as.character(tail(k,1))
                              state[i]<-as.character(tail(p,1))}
        else {hospital[i]<-as.character(k[num])
              state[i]<-as.character(s[i])}}
       else{ hospital[i]<-head(as.character(k,1))
      state[i]<-head(as.character(p,1))}})

else if (outcome=="heart failure")suppressWarnings({
  data1[,17]<-as.numeric(as.character(data1[,17]))
  ##data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
  data2<-data1[order(data1[,17],data1[,2],na.last=NA,decreasing=FALSE),]
  k<-data2[,2]
  p<-data2[,7]
  
  if(!missing(num)){if(num=="best"){hospital[i]<-as.characterhead(head(k,1))
                  state[i]<-as.character(head(p,1))}                    
  else if(num=="worst"){hospital[i]<-as.character(tail(k,1))
                        state[i]<-as.character(tail(p,1))}
  else {hospital[i]<-as.character(k[num])
        state[i]<-as.character(s[i])}}
  else{ hospital[i]<-head(as.character(k,1))
        state[i]<-head(as.character(p,1))}}
  )
    else if (outcome=="pneumonia")suppressWarnings({
      data1[,23]<-as.numeric(as.character(data1[,23]))
      ##data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
      data2<-data1[order(data1[,23],data1[,2],na.last=NA,decreasing=FALSE),]
      k<-data2[,2]
      p<-data2[,7]
      
      if(!missing(num)){if(num=="best"){hospital[i]<-as.character(head(k,1))
                                        state[i]<-as.character(head(p,1))}                    
                        else if(num=="worst"){hospital[i]<-as.character(tail(k,1))
                                              
                                              state[i]<-as.character(tail(p,1))}
                        else {hospital[i]<-as.character(k[num])
                              state[i]<-as.character(s[i])}}
      else{ hospital[i]<-as.character(head(k,1))
            state[i]<-as.character(head(p,1))}})
  }
final<-data.frame(cbind(hospital,state))
rownames(final)<-final$state
final<-final }

    