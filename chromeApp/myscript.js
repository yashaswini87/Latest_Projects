// Checking page title
if (document.title.indexOf("Walmart.com") != -1) {
    //Creating Elements
    var btn = document.createElement("DIV");
    btn.style.border = "thick solid #0000FF";
    //btn.style.width = "150%";
    btn.style.height = "400px";
    var t = document.createTextNode("Hack Day");
    btn.appendChild(t);
    //Appending to DOM
    var adDiv = document.getElementById("sponsored-container-bottom-5"); 
    adDiv.appendChild(btn);
    
}
