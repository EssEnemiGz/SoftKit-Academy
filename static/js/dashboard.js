fetch("https://softkitacademy-ess123456s-projects.vercel.app/dashboard/califications", 
{headers:{"Content-Type":"application/json", "Accept":"application/json", mode:"cors", credentials:"same-origin"}})
.then(response => response.json()).then(data => {
    console.log(data)
    document.getElementById('username').innerText = data[0];

    const main_table = document.getElementById('table');
    const column = document.getElementById('columns');
    let actual_week, actual_row;
    actual_row = document.createElement('div');
    actual_row.classList.add('--products-list');
    for (let j = 1; j < data.length; j++){
        const actual = data[j];
        console.log(j, actual)

        if (actual_week === undefined){
            actual_week = actual.week;
        }

        if (actual_week !== actual.week){ 
            actual_week = actual.week;
            main_table.appendChild(notes)
            console.log("Cambio de semana")
        }

        const extra_column = document.createElement('h3')
        extra_column.innerText = actual.task;
        column.appendChild(extra_column)

        const point = document.createElement('p');
        point.innerText = actual.point
        actual_row.appendChild(point)
    }
    main_table.appendChild(notes)
})