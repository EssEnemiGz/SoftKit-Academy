fetch(`${location.protocol}//${document.domain}/render/students`, {
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'mode': 'no-cors'
    }
}).then(response => {
    if (!response.ok){
        alert("Error critico al registrar sus notas, revise los logs")
        throw new Error(response)
    }

    return response.json()
}).then(data => {
    const main = document.getElementById('students');

    for (let i=0; i<data.length;i++){
        const element = document.createElement('option')
        element.value = data[i]['id']
        element.innerText = data[i]['username']

        main.appendChild(element)
    }
})

function sendPoints() {
    const user_id = document.getElementById("students").value
    const server_code = document.querySelector(".server-code").value
    const califications = document.querySelector(".califications").value.split(",")
    const week = document.getElementById("week").value

    let json = {
        'user_id': user_id,
        'server_code': server_code,
        'califications': califications,
        "week": week
    }
    json = JSON.stringify(json)

    fetch(`${location.protocol}//${document.domain}/insert/califications`, { method:"POST", headers: {'Content-Type': 'application/json', 'Accept': 'application/json', mode: 'cors', credentials: 'same-origin' }, body: json }).then(response => {
        if (!response.ok) {
            throw new Error(`Ha ocurrido un error, intente de nuevo\n\n Error code: ${response.status}`)
        }

        alert("Calificaciones registradas sin errores reportados")
    })
    return 0;
}
