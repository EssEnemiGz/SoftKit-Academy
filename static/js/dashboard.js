fetch("https://softkitacademy-ess123456s-projects.vercel.app/dashboard/califications", 
{headers:{"Content-Type":"application/json", "Accept":"application/json", mode:"cors", credentials:"same-origin"}})
.then(response => response.json()).then(data => {
    console.log(data)
    document.getElementById('username').innerText = data[0];

    const main_table = document.getElementById('table');
    const column = document.getElementById('columns');
    let actual_week;
    for (let j = 1; j < data.length; j++){
        const actual = data[j];
        console.log(j, actual)
        if (actual_week !== actual.week){ 
            actual_week = actual.week;
            console.log("Cambio de semana")
        }

        if (actual_week === undefined){
            actual_week = actual.week;
        }

        const extra_column = document.createElement('h3')
        extra_column.innerText = actual.task;
        column.appendChild(extra_column)

        const notes = document.createElement('div');
        notes.classList.add('--products-list');

        const point = document.createElement('p');
        point.innerText = actual.point
        notes.appendChild(point)

        main_table.appendChild(notes)
    }
})