const temp = [];
let best_score = -1;
let min_score = 11;
const promedio_list = []
const minimo_list = []

fetch("https://softkitacademy-ess123456s-projects.vercel.app/dashboard/califications",
    { headers: { "Content-Type": "application/json", "Accept": "application/json", mode: "cors", credentials: "same-origin" } })
    .then(response => response.json()).then(data => {
        document.getElementById('username').innerText = data[0];

        const table = document.getElementById('table');

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

        const minCalc = (numeros) => {
            const numerosValidos = numeros.filter(num => typeof num === 'number' && !isNaN(num));

            if (numerosValidos.length === 0) {
                console.log("No hay números válidos en el array.");
                return NaN; 
            }

            return Math.min(...numerosValidos);
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

            const column = document.getElementById('column-'+actual.week);
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
        const minimo = minCalc(minimo_list);
        document.getElementById('best-score').innerText = best_score;
        document.getElementById('minimo').innerText = minimo.toFixed(2);
        document.getElementById('promedio').innerText = promedio.toFixed(2);

        table.appendChild(row);
    })

const trending = (action, element) => {
    element.classList.toggle('--invisible');
    if (action === "down"){
        document.getElementById('best-score').innerText = min_score;
        document.getElementById('best-score-desc').innerText = "Tu peor puntaje en una tarea";
        return 0;
    }

    document.getElementById('best-score').innerText = best_score;
    document.getElementById('best-score-desc').innerText = "Tu mejor puntaje en una tarea";
}