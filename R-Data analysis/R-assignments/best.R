
best<-function(state,outcome){
  data<-read.csv("outcome-of-care-measures.csv")
  data[,7]<-as.character(data[,7])
  data1<-subset(data,State==state)
  if(nrow(data1)==0){stop("invalid state",call.=TRUE)}
  if (outcome=="heart attack")suppressWarnings({
  data1[,11]<-as.numeric(as.character(data1[,11]))
  data2<-subset(data1,data1[,11]== min(data1[,11],na.rm=TRUE))
  data3<-data2[order(data2$Hospital.Name,na.last=NA,decreasing=FALSE),]
  s<-data3$Hospital.Name
  print(as.character(s[1]))
  })
  else if (outcome=="heart failure")suppressWarnings({
  data1[,17]<-as.numeric(as.character(data1[,17]))
  data2<-subset(data1,data1[,17]==min(data1[,17],na.rm=TRUE))
  data3<-data2[order(data2$Hospital.Name,na.last=NA,decreasing=FALSE),]
  s<-data3$Hospital.Name
  print(as.character(s[1]))
  })
  else if (outcome=="pneumonia")suppressWarnings({
  data1[,23]<-as.numeric(as.character(data1[,23]))
  data2<-subset(data1,data1[,23]==min(data1[,23],na.rm=TRUE))
  data3<-data2[order(data2$Hospital.Name,na.last=NA,decreasing=FALSE),]
  s<-data3$Hospital.Name
  print(as.character(s[1]))
  })
  else {(stop("invalid outcome",call.=TRUE))}
  }
  


    
    