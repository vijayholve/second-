slide_bar_1=document.querySelector(".slide-bar-1")
main_bar=document.querySelector(".main-bar")
slide_bar_2=document.querySelector(".slide-bar-2")

slide_bar_1.addEventListener("click",()=>{
    if ( main_bar.style.display == "none" || main_bar.style.display == "") {
        main_bar.style.display = "flex";
        slide_bar_1.style.display="none";
    
    } else {
        main_bar.style.display = "none";
       
    }
});
slide_bar_2.addEventListener("click",()=>{
    
        slide_bar_1.style.display = "block";
        main_bar.style.display="none";

   
});