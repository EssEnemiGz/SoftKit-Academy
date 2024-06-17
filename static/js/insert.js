function login() {
    const user_id = document.querySelector(".username").value
    const server_code = document.querySelector(".server-code").value
    const califications = document.querySelector(".califications").value.split(",")
    const week = document.querySelector(".week").value

    let json = {
        'username': user_id,
        'server_code': server_code,
        'califications': califications,
        "week": week
    }

    fetch(`${location.protocol}//${document.domain}/insert/califications`, { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json', mode: 'cors', credentials: 'same-origin' }, body: json }).then(response => {
        if (!response.ok){
            throw new Error(`Ha ocurrido un error, intente de nuevo\n\n Error code: ${response.status}`)
        }

        alert("Calificaiones registradas sin errores reportados")
    })
    return 0;
}