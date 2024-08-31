// HTML CONTENT LOADER
document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/render/components?component=header.html",
        {
            headers: { "Content-Type": "text/html", "Accept": "text/html" }
        }
    ).then(response => response.text()).then(data => {
        document.querySelector(".header").innerHTML = data;
    });
});