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
// Forget password


function addPost(){
    const input=document.getElementById("postInput");
    const feed=document.getElementById("feedArea");
    const username=localStorage.getItem("username");

    if(input.value.trim()==="") return;

    const post=document.createElement("div");
    post.className="post";
    post.innerHTML=`
        <strong>${username}</strong>
        <p>${input.value}</p>
        <div style="margin-top:10px;color:#555">
            <i class="fa fa-comment"></i> Comment
            &nbsp;&nbsp;
            <i class="fa fa-share"></i> Share
        </div>
    `;
    feed.prepend(post);
    input.value="";
}

function logout(){
    localStorage.removeItem("username");
    window.location.href="login.html";
}

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