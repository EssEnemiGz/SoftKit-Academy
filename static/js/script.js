if (document.getElementById("year") !== null){
	document.getElementById("year").innerHTML = new Date().getFullYear();
}

// BOTTON TO VIEW THE TOP PAGE

setTimeout(function(){
	const dropicon = document.querySelector(".dropicon-block");
	const exiticon = document.querySelector(".exit-icon");
	const links = document.querySelector(".droplinks");
	const menu = document.querySelector(".dropdown");
	
	dropicon.onclick = function() {
		event.stopPropagation();
		menu.classList.toggle('open');
	};
	
	exiticon.onclick = function() {
		event.stopPropagation();
		menu.classList.toggle('open');
	};
	
	links.onclick = function() {
		event.stopPropagation();
		menu.classList.toggle('open');
	}
}, 1000)