fetch("https://softkitacademy-ess123456s-projects.vercel.app/dashboard/califications", 
{headers:{"Content-Type":"application/json", "Accept":"application/json", mode:"cors", credentials:"same-origin"}})
.then(response => response.json()).then(data => {
    console.log(data)
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
        column.id = "column-"+week;
        return column
    }

    createRow = (week) => {
        const row = document.createElement('div')
        row.classList.add('--product-list')
        row.id = "row-"+week;
        return row
    }

    let actual_week;
    const temp = [];
    for (let j = 1; j < data.length; j++){
        const actual = data[j];
        const row = createRow(actual.week);
        if (actual_week === undefined || actual_week !== actual.week){
            actual_week = actual.week;
            const column = createColumn(actual.week);
            if (actual.week !== 1) column.style.display = 'none'; 
            table.appendChild(column)
            temp.push([]);
        }

        if (actual_week !== actual.week){ 
            table.appendChild(row)
        }

        console.log(document.getElementById('column-1'))
        const column = document.getElementById('column-'+actual.week);
        column_text = createDefault('h3', actual.task);
        column.appendChild(column_text)

        const point = document.createElement('p');
        point.innerText = actual.point
        row.appendChild(point)

        temp[actual_week-1].push(actual.point)
        table.appendChild(row)
    }
})