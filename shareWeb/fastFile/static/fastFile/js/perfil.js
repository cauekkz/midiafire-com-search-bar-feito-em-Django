
document.querySelector('#inbox-icon').onclick = function(){
        
        
        const modal = document.querySelector('#inbox')
        if(modal.open){
            modal.close()
            this.style.filter = 'brightness(100%)'
            const csrfToken = document.querySelector('[name=csrf-token]').content
            fetch('/deleteMessages', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrfToken  
                },
        
              }).then(response =>response.json()).then(result =>{
                if (result == 'deleted'){
                    document.getElementsByClassName('messagesArticle').forEach(
                        function(article){
                            article.style.display='none'
                        }
                    )
                }
            })
            
             
        }
        else{  
            this.style.filter = 'brightness(50%)'
            
            modal.show()
        }

} 
document.querySelectorAll('.btn-decision').forEach(function(btn){
    btn.onclick = function(){
        const article = this.closest('article')
        const id = article.dataset.id
        const allow = this.dataset.decision
        const csrfToken = document.querySelector('[name=csrf-token]').content
        const requestUser = String(article.dataset.user)

        
        fetch('/allowUser', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken  
            },

            body: JSON.stringify({
                id : id,
                decision: allow,
                caller: requestUser
            })
          }).then(response =>response.json()).then(result =>{
                
                if(result.respost === 'made')
                {
                    article.style.display = 'none'

                }else{
                    
                    alert_email(result.respost)
                    
                }
                
            
          })
          
    }
    
})