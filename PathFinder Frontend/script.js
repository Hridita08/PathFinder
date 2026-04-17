function loginUser(event) {
    event.preventDefault();
    window.location.href = "home.html";
}

// login page
function loginUser(e){

e.preventDefault();

let name = document.getElementById("name").value.trim();
let email = document.getElementById("email").value.trim();
let password = document.getElementById("password").value.trim();
let error = document.getElementById("errorMsg");

error.innerHTML="";

if(name==="" || email==="" || password===""){
error.innerHTML="All fields are required!";
return;
}

let emailPattern=/^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

if(!email.match(emailPattern)){
error.innerHTML="Please enter a valid email!";
return;
}

if(password.length<6){
error.innerHTML="Password must be at least 6 characters!";
return;
}

localStorage.setItem("username",name);

window.location.href="main.html";

}
function togglePassword(){

const pass = document.getElementById("password");
const icon = document.querySelector(".toggle-pass");

if(pass.type === "password"){
pass.type = "text";
icon.classList.remove("fa-eye");
icon.classList.add("fa-eye-slash");
}
else{
pass.type = "password";
icon.classList.remove("fa-eye-slash");
icon.classList.add("fa-eye");
}

}
window.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".pf-login-container");
    setTimeout(() => {
        container.classList.add("show");
    }, 100); // small delay for smoother effect
});
function loginUser(event){

event.preventDefault(); // page reload stop

const name = document.querySelector('input[name="name"]').value;

const email = document.querySelector('input[name="email"]').value;

const password = document.getElementById("password").value;

if(name && email && password){

localStorage.setItem("username", name);

/* login success → main page */

window.location.href = "main.html";

}

else{

alert("Please fill all fields");

}

}
const username = localStorage.getItem("username");

if(username){
    const userEl = document.getElementById("userDisplay");
    if(userEl){
        userEl.innerText = username;
    }
}
document.getElementById("userDisplay").innerText=username;
// if already logged in → go to main page

window.addEventListener("DOMContentLoaded", () => {
    if(localStorage.getItem("username")){
        window.location.href="main.html";
    }
});

// ========profile page=========

