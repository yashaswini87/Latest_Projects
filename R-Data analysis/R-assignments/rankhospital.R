rankhospital<-function(state,outcome,rank){
  data<-read.csv("outcome-of-care-measures.csv")
  data[,7]<-as.character(data[,7])
  data1<-subset(data,State==state)
  if(nrow(data1)==0){stop("invalid state",call.=TRUE)}
  if (outcome=="heart attack")suppressWarnings({
    data1[,11]<-as.numeric(as.character(data1[,11]))
    ##data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
    data2<-data1[order(data1[,11],data1[,2],na.last=NA,decreasing=FALSE),]
    s<-data2$Hospital.Name
    if(rank=="best"){print(as.character(head(s,1)))}
    else if(rank=="worst"){print(as.character(tail(s,1)))}
    else {print(as.character(s[rank]))}
  })
  else if (outcome=="heart failure")suppressWarnings({
    data1[,17]<-as.numeric(as.character(data1[,17]))
    ##data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
    data2<-data1[order(data1[,17],data1[,2],na.last=NA,decreasing=FALSE),]
    s<-data2$Hospital.Name
    if(rank=="best"){print(as.character(head(s,1)))}
    else if(rank=="worst"){print(as.character(tail(s,1)))}
    else {print(as.character(s[rank]))}
  })
  else if (outcome=="pneumonia")suppressWarnings({
    data1[,23]<-as.numeric(as.character(data1[,23]))
    ##data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
    data2<-data1[order(data1[,23],data1[,2],na.last=NA,decreasing=FALSE),]
    s<-data2$Hospital.Name
    if(rank=="best"){print(as.character(head(s,1)))}
    else if(rank=="worst"){print(as.character(tail(s,1)))}
    else {print(as.character(s[rank]))}
  })
  else {(stop("invalid outcome",call.=TRUE))}
}