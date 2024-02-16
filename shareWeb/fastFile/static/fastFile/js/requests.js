document.querySelectorAll('.lock').forEach(function(lock){
    lock.onclick = function(){
        const article = this.closest('article')
        
        const modal = document.querySelector('dialog')
        if(modal.open){
            modal.close()
            this.style.filter = 'brightness(100%)'
            return
             
        }
        else{  
            this.style.filter = 'brightness(50%)'
           modal.show()
        }
        modal.querySelector('form').addEventListener('submit',(event) => {
            event.preventDefault()
            let form = event.target
            let password = form.querySelector('input[type="password"]')
            if (password.value.trim() === ''){
                password.value = '*************'
                return
            }
            let passwordValue = password.value.trim()
            let csrfToken = document.querySelector('[name=csrf-token]').content
            const title = article.querySelector('h3').innerText.trim()
            document.body.style.cursor='progress'
            fetch('/requests', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrfToken  
                },
    
                body: JSON.stringify({
                    password : passwordValue,
                    name : title,
                    type : 'lock'
                })
              }).then(response =>response.json()).then(result =>{
                    if(result.respost == 'ok')
                    {
                        document.body.style.cursor='default'
                        window.location.href =`/file/${title}`
                    }else{
                        document.body.style.cursor='default'
                        alert_email(result.respost)
                    }
                    
                
              })

        })
    }
})
function alert_email(message){
    

    let alertBox = document.getElementById("alert-email")
    let span = alertBox.querySelector('span')
    span.innerText = message
    alertBox.show()
    setTimeout(function(){

        alertBox.close()
   
    },2000)
    
    

}
document.querySelectorAll('.request-button').forEach(function(request){
    request.onclick = function(){
        const article = this.closest('article')

        document.body.style.cursor='progress'

        let csrfToken = document.querySelector('[name=csrf-token]').content
        const title = article.querySelector('h3').innerText.trim()
        fetch('/requests', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken  
            },

            body: JSON.stringify({
                name : title,
                type : 'admin-permition'
            })
          }).then(response =>response.json()).then(result =>{
                if(result.respost == 'ok')
                {
                    document.body.style.cursor='default'
                    alert_email('made request')
                    this.style.display='none'

                }else{
                    document.body.style.cursor='default'    
                    alert_email(result.respost)
                    
                }
                
            
          })
        
    }
})

