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

// ========non-technical page=========
function setActive(element){
    document.querySelectorAll(".sidebar li").forEach(li=>{
        li.classList.remove("active");
    });
    element.classList.add("active");
}
function toggleDropdown(){
    const dropdown=document.getElementById("careerDropdown");
    dropdown.style.display = dropdown.style.display==="block" ? "none" : "block";
}
function showDetails(career){

let details=document.getElementById("careerDetails");

if(career==="marketing"){
details.innerHTML=
"<h3>Marketing</h3><p>Required Degree: BBA / Marketing</p><p>Skills: Communication, Creativity</p><p>Jobs: Digital Marketer, Brand Manager</p>";
}

else if(career==="hr"){
details.innerHTML=
"<h3>Human Resource</h3><p>Required Degree: BBA / HRM</p><p>Skills: Leadership, Communication</p><p>Jobs: HR Manager, Recruiter</p>";
}

else if(career==="teaching"){
details.innerHTML=
"<h3>Teaching</h3><p>Required Degree: Education / Subject Degree</p><p>Skills: Patience, Presentation</p><p>Jobs: Teacher, Lecturer</p>";
}

else if(career==="journalism"){
details.innerHTML=
"<h3>Journalism</h3><p>Required Degree: Journalism / Media</p><p>Skills: Writing, Research</p><p>Jobs: Reporter, News Editor</p>";
}
function showDetails(career) {
    const details = {
        marketing: "Marketing involves promoting products, digital marketing, branding, and sales strategies.",
        hr: "Human Resource deals with recruitment, employee management, and workplace development.",
        teaching: "Teaching involves educating students, lesson planning, and guiding future generations.",
        journalism: "Journalism focuses on news reporting, media writing, and communication."
    };

    document.getElementById("careerDetails").innerText = details[career];
}

function suggestCareer() {
    let interest = document.getElementById("interestInput").value.toLowerCase();
    let result = document.getElementById("result");

    if (interest.includes("marketing")) {
        result.innerHTML = "Suggested Career: Marketing Specialist";
    } 
    else if (interest.includes("people") || interest.includes("management")) {
        result.innerHTML = "Suggested Career: Human Resource Manager";
    } 
    else if (interest.includes("teaching") || interest.includes("education")) {
        result.innerHTML = "Suggested Career: Teacher";
    } 
    else if (interest.includes("writing") || interest.includes("news")) {
        result.innerHTML = "Suggested Career: Journalist";
    } 
    else {
        result.innerHTML = "No suggestion found. Try another interest.";
    }
}

}
