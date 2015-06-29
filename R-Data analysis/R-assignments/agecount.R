agecount<-function(age){
  if(missing(age)){stop("invalide state", call.=TRUE)}
  else { homicides<-readLines("homicides.txt")
         r<-regexpr("<dd>[Aa]ge")
  