document.querySelector('#inbox-icon').onclick = function(){
        
        
        const modal = document.querySelector('#inbox')
        if(modal.open){
            modal.close()
            this.style.filter = 'brightness(100%)'
            return
             
        }
        else{  
            this.style.filter = 'brightness(50%)'
           modal.show()
        }

} 
document.querySelectorAll('.btn-decision').forEach(function(btn){
    btn.onclick = function(){
        const id = this.closest('article').dataset.id
        const allow = Boolean(this.dataset.decision)
        const csrfToken = document.querySelector('[name=csrf-token]').content
        fetch('/allowUser', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken  
            },

            body: JSON.stringify({
                id : id,
                decision: allow
            })
          }).then(response =>response.json()).then(result =>{
                if(result.respost === 'made' || result.respost === 'He already has permission')
                {
                    article.style.display = 'none'

                }else{
                    
                    alert_email(result.respost)
                    
                }
                
            
          })
    }
})