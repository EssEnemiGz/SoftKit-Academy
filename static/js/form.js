'use strict';

// Global const

const REGISTER_OPTION = 'register';
const LOGIN_OPTION = 'login';
const register_url = `${location.protocol}//${document.domain}/api/register/verify`;
const login_url = `${location.protocol}//${document.domain}:5000/api/login/verify`;

async function send(data, option){
	let response, url, result;

	if (option === REGISTER_OPTION){
		url = register_url;
	}else{
		url = login_url;
	};

	data = JSON.stringify(data);
	response = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json", "Accept":"application/json", mode:"cors", credentials:"same-origin"} , body:data });

	if (response.ok){
		result = await response.json();
		window.location.href = result['redirect'];
		return 200;
	} else {
		if (response.status === 401){
			alert("¡El usuario no existe o hay información incorrecta!")
		}
		else{
			alert("Error del servidor o está registrando un usuario ya existente, intente de nuevo.")
		}
	};
};

function register(){
	let username, password, email, confirmation, code;
	username = document.querySelector(".register .username").value 
	password = document.querySelector(".register .password").value 
	email = document.querySelector(".register .email").value
 
	let json = {
		'username':username,
		'password':password,
		'email':email
	}

	send(json, REGISTER_OPTION, username);
	return 0;
}

function login(){
	let username, password, email;
	username = document.querySelector(".login #username").value 
	password = document.querySelector(".login #password").value 
	email = document.querySelector(".login #email").value
 
	let json ={
		'username':username,
		'password':password,
		'email':email,
	}

	send(json, LOGIN_OPTION, username);
	return 0;
}

