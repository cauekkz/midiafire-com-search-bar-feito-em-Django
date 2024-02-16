const li = document.querySelectorAll(".li-settings");
li.forEach(function(li){
    li.addEventListener('mouseover',function(){
        li.classList.add("li-settings-before");
    })

    li.addEventListener('mouseout',function(){
        li.classList.remove("li-settings-before");
    })
})
