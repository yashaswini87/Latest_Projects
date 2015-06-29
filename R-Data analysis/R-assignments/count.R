count<-function(cause){
  homicides<-readLines("homicides.txt")
  if (cause=="asphyxiation"){s<-length(grep("[Cc]ause: [Aa]sphyxiation", homicides))}
  else if (cause=="blunt force"){s<-length(grep("[Cc]ause: [Bb]lunt [Ff]orce", homicides))}
  else if (cause=="other"){s<-length(grep("[Cc]ause: [Oo]ther",homicides))}
  else if (cause=="shooting"){s<-length(grep("[Cc]ause: [Ss]hooting",homicides))}
  else if (cause=="stabbing"){s<-length(grep("[Cc]ause: [Ss]tabbing",homicides))}
  else if (cause=="unknown"){s<-length(grep("[Cc]ause: [Uu]nknown",homicides))}
  else {stop("invalid cause",call.=TRUE)}
}