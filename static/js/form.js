'use strict';

// Global const

const REGISTER_OPTION = 'register';
const LOGIN_OPTION = 'login';
const register_url = `https://${document.domain}/register/verify`;
const login_url = `https://${document.domain}/login/verify`;

const queryString = window.location.search;
const params = new URLSearchParams(queryString);
const form = params.get('form');

// Displays

const registerForm = document.querySelector('.register');
const loginForm = document.querySelector('.login');

function change(){
	registerForm.classList.toggle('show');
	loginForm.classList.toggle('show');
};

// Visibility

if (form === REGISTER_OPTION){
	// Pass
} else if (form === LOGIN_OPTION){
	registerForm.classList.toggle('show');
	loginForm.classList.toggle('show');
};

async function send(data, option){
	let response, url, result;

	if (option === REGISTER_OPTION){
		url = register_url;
	}else{
		url = login_url;
	};

	data = JSON.stringify(data);
	response = await fetch(url, { method:"POST", headers:{"Content-Type":"application/json", "Accept":"application/json", mode:"cors", credentials:"same-origin"} , body:data });
	result = await response.json();

	if (response.ok){
		window.location.href = result['redirect'];
		return 200;
	} else {
		if (response.status === 401){
			alert("¡El usuario no existe o hay información incorrecta!")
		}
		else{
			alert("Error del servidor, intente de nuevo.")
		}
	};
};

function register(){
	let username, password, email, confirmation, id_centro;
	username = document.querySelector(".register .username").value 
	password = document.querySelector(".register .password").value 
	confirmation = document.querySelector(".register .confirm").value
	email = document.querySelector(".register .email").value
	code = document.querySelector(".register .code").value
 
	let json = {
		'username':username,
		'password':password,
		'confirm':confirmation,
		'email':email,	
		'code':code
	}

	if ( username.length < 1  &&  password.length < 1 ){ // CREATE A ERROR MENSAJE
		return "ERROR";
	} else if (password !== confirmation){
		return "ERROR";
	};

	send(json, REGISTER_OPTION, username);
	return 0;
}

function login(){
	let username, password, email, id_centro;
	username = document.querySelector(".login .username").value 
	password = document.querySelector(".login .password").value 
 
	let json ={
		'username':username,
		'password':password,
		'email':email,
	}

	send(json, LOGIN_OPTION, username);
	return 0;
}

