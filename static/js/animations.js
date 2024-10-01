const rotation_icon_container = document.getElementsByClassName("--rotation-animation-icon");
const courses_list = document.getElementsByName("rotator");

for (let k = 0; k < rotation_icon_container.length; k++) {
    rotation_icon_container[k].addEventListener("click", function () {
        rotation_icon_container[k].querySelector("img").classList.toggle("--rotated");

        for (let j = 0; j < courses_list.length; j++) {
            if (courses_list[j].getAttribute("value") == rotation_icon_container[k].id) {
                courses_list[j].classList.toggle("--hidden");
            }
        }
    })
}