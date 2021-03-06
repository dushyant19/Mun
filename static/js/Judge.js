let textbox = document.getElementById("textbox")


const SetMessages = ()=>{
    textbox.innerHTML = ""
    const chits = Messages()
    chits.forEach(message=>{
        const wrapper = document.createElement('div')
        const header = document.createElement('div')
        const content = document.createElement('div')
        const RatifyButton = document.createElement('button') 
        const RejectButton = document.createElement('button')

        content.textContent = message.chit
        header.textContent = "From: " + message.chit_from.name + " <" + message.chit_from._id + ">"
        
        if(message.reply_to_country)
        {
            const replyHeader = document.createElement('div')
            replyHeader.textContent = "Reply from " + message.chit_from.name + " to " + message.reply_to_country +"'s" + " message"
            wrapper.appendChild(replyHeader)
        }

        RatifyButton.textContent = "Ratify"
        RejectButton.textContent = "Reject"

        ApproveButton.addEventListener('click',()=>{
            fetch('/chits/judge',{
                method:'POST',
                body:JSON.stringify({
                    chit_id:message.id,
                }),
                headers:{
                    'Content-Type':'application/json'
                }
            })
            .then(response=>response.json())
            .then(data=>Success=data.message)
            .catch(error=>errorMessage=error.message)
        })

        RejectButton.addEventListener('click',()=>{
            fetch('/chits/judge/reject',{
                method:'POST',
                body:JSON.stringify({
                    chit_id:message.id,
                }),
                headers:{
                    'Content-Type':'application/json'
                }
            })
            .then(response=>response.json())
            .then(data=>Success=data.message)
            .catch(error=>errorMessage=error.message)
        })

        wrapper.appendChild(header)
        wrapper.appendChild(content)
        wrapper.appendChild(RatifyButton)
        wrapper.appendChild(RejectButton)
        textbox.appendChild(wrapper)
    })
}

setInterval(SetMessages, 60000)


