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

// Technical page
function goHome(){
window.location.href="main.html";
}
function goTechnical(){
    window.location.href = "technical.html";
}
function showCareer(btn,type){

let card = btn.closest(".tech-card");
let box = card.querySelector(".career-details");

/* toggle */
if(box.style.display === "block"){
    box.style.display = "none";
    box.innerHTML = "";
    return;
}

let content = "";

switch(type){

case "software":
content = `
<p><b>Software Developer</b></p>
<p>Builds software and applications.</p>
<p>Skills: Java, Python, C++</p>`;
break;

case "web":
content = `
<p><b>Web Developer</b></p>
<p>Builds websites and web apps.</p>
<p>Skills: HTML, CSS, JavaScript</p>`;
break;

case "data":
content = `
<p><b>Data Scientist</b></p>
<p>Works with data and machine learning.</p>
<p>Skills: Python, ML, Statistics</p>`;
break;

case "cyber":
content = `
<p><b>Cyber Security Specialist</b></p>
<p>Protects systems from cyber attacks.</p>`;
break;

case "ai":
content = `
<p><b>AI / ML Engineer</b></p>
<p>Builds intelligent systems.</p>`;
break;

case "network":
content = `
<p><b>Network Engineer</b></p>
<p>Design and manage computer networks.</p>`;
break;

case "cloud":
content = `
<p><b>Cloud Engineer</b></p>
<p>Works with AWS & Azure cloud platforms.</p>`;
break;

case "mobile":
content = `
<p><b>Mobile App Developer</b></p>
<p>Builds Android & iOS apps.</p>`;
break;

}

box.innerHTML = content;
box.style.display = "block";
}
