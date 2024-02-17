const lis = document.querySelectorAll(".li-settings");
lis.forEach(function(li){
    li.addEventListener('mouseover',function(){
        li.classList.add("li-settings-before");
    })

    li.addEventListener('mouseout',function(){
        li.classList.remove("li-settings-before");
    })
    //show modals
    li.onclick = function(){
        
        let s = `#dialog-${li.dataset.edit}`
        
        let modal = document.querySelector(s)
        lis.forEach(function(li2){
            let modal2 = document.querySelector(`#dialog-${li2.dataset.edit}`)

             if(modal2.open && modal2 != modal ){
                modal2.close() 
             }
        })

        if(modal.open){
            modal.close()
            return
             
        }
        else{  
            
           modal.show()
        }      

    }
})
