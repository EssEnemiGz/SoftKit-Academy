switcher = (more_icon) => {
    const menu = more_icon.nextElementSibling;

    menu.classList.toggle("--invisible");
}

switchParent = (reference, collapse) =>{
    document.querySelector(reference).classList.toggle('--invisible')
    document.querySelector('body').classList.toggle('--pseudo-invisible')

    if (collapse) collapse.parentElement.classList.toggle('--invisible')
}