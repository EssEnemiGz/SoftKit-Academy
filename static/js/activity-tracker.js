const readed = (content_id, url) => {
    fetch(`${location.protocol}//${document.domain}/api/tracker/readed?content_id=${content_id}`, {
        method:"PUT",
        headers:{
            "Content-Type":"application/json",
            "Accept":"application/json"
        }
    }).then(response => {
        if (!response.ok){
            alert("Recargue su pagina, ha ocurrido un error")
        }

        window.location.href = url;
        return response
    })
}

const visited = (content_id, url) => {
    fetch(`${location.protocol}//${document.domain}/api/tracker/visited?content_id=${content_id}`, {
        method:"PUT",
        headers:{
            "Content-Type":"application/json",
            "Accept":"application/json"
        }
    }).then(response => {
        if (!response.ok){
            alert("Recargue su pagina, ha ocurrido un error")
        }

        window.location.href = url;
        return response
    })
}

const completed = (content_id) => {
    fetch(`${location.protocol}//${document.domain}/api/tracker/completed?content_id=${content_id}`, {
        method:"PUT",
        headers:{
            "Content-Type":"application/json",
            "Accept":"application/json"
        }
    }).then(response => {
        if (!response.ok){
            alert("Recargue su pagina, ha ocurrido un error")
        }

        alert("Marcado como completado correctamente, su maestro ha recibido la notificación.")
        return response
    })
}