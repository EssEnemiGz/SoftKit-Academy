// HTML CONTENT LOADER
const render_component = (component) => {
    document.addEventListener("DOMContentLoaded", function () {
        fetch(`/api/render/components?component=${component}`,
            {
                headers: { "Content-Type": "text/html", "Accept": "text/html" }
            }
        ).then(response => response.text()).then(data => {
            document.querySelector(".header").innerHTML = data;
        });
    });
}