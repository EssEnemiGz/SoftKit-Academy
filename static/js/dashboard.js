const temp = [];
let best_score = -1;
let min_score = 11;
const promedio_list = []
const minimo_list = []

fetch(`${location.protocol}//${document.domain}:5000/dashboard/califications`,
    { headers: { "Content-Type": "application/json", "Accept": "application/json", mode: "no-cors", credentials: "same-origin" } })
    .then(response => response.json()).then(data => {
        document.getElementById('username').innerText = data[0];
        const table = document.getElementById('table');

        if (data.length === 1){
            document.getElementById('best-score').innerText = "--"
            document.getElementById('promedio').innerText = "--";
            table.classList.add('no-data');
            return 0;
        }

        createDefault = (element, content) => {
            const result = document.createElement(element)
            result.innerText = content;
            return result
        }

        createColumn = (week) => {
            const column = document.createElement("div")
            column.classList.add('--columns-list')
            column.id = "column-" + week;
            return column
        }

        createRow = (week) => {
            const row = document.createElement('div')
            row.classList.add('--product-list')
            row.id = "row-" + week;
            return row
        }

        const promedioCalc = (numeros) => {
            if (numeros.length === 0) return 0;

            const suma = numeros.reduce((acumulador, valorActual) => acumulador + valorActual, 0);
            return suma / numeros.length;
        }

        let actual_week, row;
        for (let i = 1; i < data.length; i++) {
            const actual = data[i];
            if (actual_week === undefined || actual_week !== actual.week) {
                actual_week = actual.week;
                const column = createColumn(actual.week);
                column.appendChild(createDefault('h3', 'Semana'))
                row = createRow(actual.week);
                row.appendChild(createDefault('p', actual.week))
                table.appendChild(column)
                temp.push([]);
            }

            if (actual_week !== actual.week) {
                table.appendChild(row)
                row = createRow(actual.week);
                table.appendChild(row)
            }

            const column = document.getElementById('column-' + actual.week);
            column_text = createDefault('h3', actual.task);
            column.appendChild(column_text)

            const point = data[i].point;
            const info = createDefault('p', point);
            row.appendChild(info)
            temp[actual_week - 1].push(actual.point)
            table.appendChild(row)

            if (best_score < point) best_score = point;
            if (min_score > point) min_score = point;
            minimo_list.push(point);
            promedio_list.push(point);
        }

        const promedio = promedioCalc(promedio_list);
        document.getElementById('best-score').innerText = best_score;
        document.getElementById('promedio').innerText = promedio.toFixed(2);

        table.appendChild(row);
    })

fetch(`${location.protocol}//${document.domain}:5000/meet/info`,
    { headers: { "Content-Type": "application/json", "Accept": "application/json", mode: "no-cors", credentials: "same-origin" } }
).then(response => {
    if (!response.ok) {
        alert("Hubo un error cargando sus reuniones proximas. Recargue la pagina o contacte con su maestro");
        throw new Error(response)
    }

    return response.json()
}).then(data => {
    if (!data.length) {
        document.getElementById('google-meet-link').remove()
        document.getElementById('meet-date').innerText = "Sin reuniones activas";
        document.getElementById("meeting-icon").innerText = "group_off";
        document.getElementById("reuniones").innerText = "Sin reuniones"
        return 0;
    }

    const link = data[0].link;
    const date = data[0].date+" "+data[0].hour;

    const dateObject = new Date(date);
    const options = { weekday: 'long', month: 'long', day: 'numeric' };
    const largeDate = dateObject.toLocaleDateString('es-US', options);
    const largeTime = dateObject.toLocaleTimeString('es-ES', { hour:'2-digit', minute:'2-digit'});

    document.getElementById('google-meet-link').href = link;
    document.getElementById('meet-date').innerText = largeDate.charAt(0).toUpperCase() + largeDate.slice(1).toLowerCase() + " " + largeTime;
})

const trending = (action, element) => {
    element.classList.toggle('--invisible');
    if (action === "down") {
        if (min_score !== 11) document.getElementById('best-score').innerText = min_score;
        document.getElementById('best-score-desc').innerText = "Tu peor puntaje en una tarea";
        return 0;
    }

    if (best_score !== -1) document.getElementById('best-score').innerText = best_score;
    document.getElementById('best-score-desc').innerText = "Tu mejor puntaje en una tarea";
}