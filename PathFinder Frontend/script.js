function loginUser(event) {
    event.preventDefault();
    window.location.href = "home.html";
}

function addPost(){
    const input = document.getElementById("postInput");
    const feed = document.getElementById("feedArea");
    const username = localStorage.getItem("username") || "User";
    if(input.value.trim() === "") return;
    const post = document.createElement("div");
    post.className = "post";
    post.innerHTML = `<strong>${username}</strong><p>${input.value}</p>`;
    feed.prepend(post);
    input.value = "";
}

function logout(){
    if(confirm("Are you sure?")) {
        localStorage.removeItem("username");
        window.location.href = "login.html";
    }
}

function setActive(element){
    document.querySelectorAll(".sidebar li").forEach(li => li.classList.remove("active"));
    element.classList.add("active");
}

function toggleDropdown(){
    const dropdown = document.getElementById("careerDropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function updatePassword() {
    const p1 = document.getElementById("newPass").value;
    const p2 = document.getElementById("confirmPass").value;
    const status = document.getElementById("statusMsg");
    if(!status) return;
    if(p1.length < 6) {
        status.style.color = "#dc2626";
        status.innerText = "Too short!";
        return;
    }
    if(p1 !== p2) {
        status.style.color = "#dc2626";
        status.innerText = "No match!";
        return;
    }
    localStorage.setItem("userPassword", p1);
    status.style.color = "#16a34a";
    status.innerText = "Success!";
}

// থিম ফাংশন
function applyTheme(theme) {
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.classList.add('dark-mode');
    } else {
        document.documentElement.removeAttribute('data-theme');
        document.body.classList.remove('dark-mode');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const themeSelect = document.getElementById('themeSelect');
    const savedTheme = localStorage.getItem('preferredTheme') || 'light';
    
    applyTheme(savedTheme);
    if(themeSelect) themeSelect.value = savedTheme;

    if(themeSelect) {
        themeSelect.addEventListener('change', function() {
            applyTheme(this.value);
            localStorage.setItem('preferredTheme', this.value);
        });
    }
});