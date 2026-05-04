 console.log("JS LOADED");
 async function loginUser(event) {
    event.preventDefault();

    const name = document.querySelector('input[name="name"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;

    const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();

    if(data.status === "success"){
        localStorage.setItem("user_id", data.user_id);   // ← user_id save
        localStorage.setItem("username", name);           // ← username save
        window.location.href = "main.html";
    } else {
        alert(data.message);
    }
}
 
function addPost(){
    const input = document.getElementById("postInput");
    const feed = document.getElementById("feedArea");
    const username = localStorage.getItem("username");
    const userId = localStorage.getItem("user_id");

    if(input.value.trim() === "") return;

    const post = document.createElement("div");
    post.className = "post";
 post.innerHTML = `
    <strong>${username}</strong>
    <p>${input.value}</p>
    <div style="margin-top:10px; color:#555">
        <i class="fa fa-comment"></i> Comment
        &nbsp;&nbsp;
        <i class="fa fa-share"></i> Share
    </div>
`;
    feed.prepend(post);
    input.value = "";
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

// otp verify er code

async function verifyOTP(event) {
    event.preventDefault(); // form reload bondho

    const inputs = document.querySelectorAll(".otp");
    let otp = "";

    inputs.forEach(input => {
        otp += input.value;
    });

    if (otp.length !== 4) {
    alert("Enter 4 digit OTP");
    return;
}

    const email = new URLSearchParams(window.location.search).get("email");

    const res = await fetch("http://127.0.0.1:5000/verify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            otp: otp
        })
    });

    const data = await res.json();

    if (data.status === "success") {
        alert("OTP Verified ✅");
        console.log("redirecting...");
       window.location.href = "./new-password.html?email=" + email; // now redirect
    } else {
        alert("Wrong OTP ❌");
    }
}
async function sendResetEmail(event) {
    event.preventDefault();

    const email = document.querySelector('input[name="email"]').value;
    console.log("EMAIL:", email); 
    const res = await fetch("http://127.0.0.1:5000/send-otp", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email })
    });

    const data = await res.text();
console.log("RESPONSE:", data);

if (data.includes("OTP")) {
    window.location.href = "reset-sent.html?email=" + email;
} else {
    alert("Failed to send OTP ❌");
}
}
  
// ==================== MESSAGE FUNCTIONS ====================

//  Post Message button
function openMessageModal(receiverId, receiverName) {
    const content = prompt(`${receiverName} কে message লিখুন:`);
    if (!content) return;

    const senderId = localStorage.getItem('user_id');

    fetch('http://127.0.0.1:5000/api/messages/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            sender_id: senderId,
            receiver_id: receiverId,
            content: content
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message))
    .catch(err => console.error('Error:', err));
}

// Header inbox icon 
function loadInbox() {
    const userId = localStorage.getItem('user_id');

    fetch(`http://127.0.0.1:5000/api/messages/inbox/${userId}`)
    .then(res => res.json())
    .then(data => {
        const messages = data.messages;
        let html = '';

        if (messages.length === 0) {
            html = '<p>কোনো message নেই।</p>';
        } else {
            messages.forEach(msg => {
                html += `
                    <div style="border:1px solid #ddd; padding:10px; margin:5px 0; border-radius:8px;">
                        <strong>${msg.sender_name}</strong>
                        <span style="font-size:12px; color:gray;">${msg.created_at}</span>
                        <p>${msg.content}</p>
                    </div>
                `;
            });
        }

        document.getElementById('inbox-container').innerHTML = html;
    })
    .catch(err => console.error('Error:', err));
}

// Unread badge count
function loadUnreadCount() {
    const userId = localStorage.getItem('user_id');
    if (!userId) return;

    fetch(`http://127.0.0.1:5000/api/messages/unread-count/${userId}`)
    .then(res => res.json())
    .then(data => {
        const badge = document.getElementById('msg-badge');
        if (badge) badge.innerText = data.count;
    })
    .catch(err => console.error('Error:', err));
}


window.addEventListener('load', loadUnreadCount);






