if (document.getElementById("year") !== null){
	document.getElementById("year").innerHTML = new Date().getFullYear();
}

// SUNSCRIBE TO MAIL
const subscribe = () => {
	const user_email = document.getElementById("user-email").value
	fetch(`https://mail.softkitacademy.com/email/subscription/pending?email=${user_email}`,
		{
			headers:{"Accept":"application/json", "Content-Type":"application/json"},
			method:"POST"
		}
	)
	.then(response => {
		if (!response.ok){
			return response.text().then(error => {
                alert(`Error al comunicarse con el servidor, codigo de estado: ${response.status}. \n\nEl servidor dice: ${error}`)
                return;
            })
		}

		return response.text().then(done => {
			alert(done)
			return;
		})
	})
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