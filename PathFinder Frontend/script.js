console.log("JS LOADED");

// ==================== LOGIN ====================

async function loginUser(event) {
    event.preventDefault();

    const name = document.querySelector('input[name="name"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;

    try {
        const res = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        const data = await res.json();

        if (data.status === "success") {
            localStorage.setItem("user_id", data.user_id);
            localStorage.setItem("username", name);
            window.location.href = "main.html";
        } else {
            alert(data.message);
        }
    } catch (err) {
        console.error("Login error:", err);
        alert("Something went wrong. Please try again.");
    }
}


// ==================== POST ====================

function addPost() {
    const input = document.getElementById("postInput");
    const feed = document.getElementById("feedArea");
    const username = localStorage.getItem("username");

    if (!input || input.value.trim() === "") return;

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


// ==================== LOGOUT ====================

function logout() {
    localStorage.removeItem("username");
    localStorage.removeItem("user_id");
    window.location.href = "login.html";
}


// ==================== SIDEBAR ====================

function setActive(element) {
    document.querySelectorAll(".sidebar li").forEach(li => {
        li.classList.remove("active");
    });
    element.classList.add("active");
}


// ==================== CAREER DROPDOWN ====================

function toggleDropdown() {
    const dropdown = document.getElementById("careerDropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}

function showDetails(career) {
    const details = document.getElementById("careerDetails");
    if (!details) return;

    const careerMap = {
        marketing: "<h3>Marketing</h3><p>Required Degree: BBA / Marketing</p><p>Skills: Communication, Creativity</p><p>Jobs: Digital Marketer, Brand Manager</p>",
        hr: "<h3>Human Resource</h3><p>Required Degree: BBA / HRM</p><p>Skills: Leadership, Communication</p><p>Jobs: HR Manager, Recruiter</p>",
        teaching: "<h3>Teaching</h3><p>Required Degree: Education / Subject Degree</p><p>Skills: Patience, Presentation</p><p>Jobs: Teacher, Lecturer</p>",
        journalism: "<h3>Journalism</h3><p>Required Degree: Journalism / Media</p><p>Skills: Writing, Research</p><p>Jobs: Reporter, News Editor</p>"
    };

    details.innerHTML = careerMap[career] || "<p>No details available.</p>";
}


// ==================== CAREER SUGGEST ====================

function suggestCareer() {
    const input = document.getElementById("interestInput");
    const result = document.getElementById("result");
    if (!input || !result) return;

    const interest = input.value.toLowerCase();

    if (interest.includes("marketing")) {
        result.innerHTML = "Suggested Career: Marketing Specialist";
    } else if (interest.includes("people") || interest.includes("management")) {
        result.innerHTML = "Suggested Career: Human Resource Manager";
    } else if (interest.includes("teaching") || interest.includes("education")) {
        result.innerHTML = "Suggested Career: Teacher";
    } else if (interest.includes("writing") || interest.includes("news")) {
        result.innerHTML = "Suggested Career: Journalist";
    } else {
        result.innerHTML = "No suggestion found. Try another interest.";
    }
}


// ==================== OTP VERIFY ====================

async function verifyOTP(event) {
    event.preventDefault();

    const inputs = document.querySelectorAll(".otp");
    let otp = "";
    inputs.forEach(input => { otp += input.value; });

    if (otp.length !== 4) {
        alert("Enter 4 digit OTP");
        return;
    }

    const email = new URLSearchParams(window.location.search).get("email");

    try {
        const res = await fetch("http://127.0.0.1:5000/verify", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, otp })
        });

        const data = await res.json();

        if (data.status === "success") {
            alert("OTP Verified ✅");
            window.location.href = "./new-password.html?email=" + email;
        } else {
            alert("Wrong OTP ❌");
        }
    } catch (err) {
        console.error("OTP verify error:", err);
        alert("Something went wrong. Please try again.");
    }
}


// ==================== FORGOT PASSWORD / SEND OTP ====================

async function sendResetEmail(event) {
    event.preventDefault();

    const emailInput = document.querySelector('input[name="email"]');
    if (!emailInput) return;

    const email = emailInput.value.trim();
    if (!email) {
        alert("Please enter your email.");
        return;
    }

    console.log("EMAIL:", email);

    try {
        const res = await fetch("http://127.0.0.1:5000/send-otp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await res.json(); // ✅ Fixed: was res.text() before

        console.log("RESPONSE:", data);

        if (data.status === "success") {
            window.location.href = "reset-sent.html?email=" + email;
        } else {
            alert(data.message || "Failed to send OTP ❌");
        }
    } catch (err) {
        console.error("Send OTP error:", err);
        alert("Something went wrong. Please try again.");
    }
}


// ==================== MESSAGE FUNCTIONS ====================

// Send message to a user
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
    .catch(err => console.error('Send message error:', err));
}

// Load inbox messages
function loadInbox() {
    const userId = localStorage.getItem('user_id');
    if (!userId) return;

    fetch(`http://127.0.0.1:5000/api/messages/inbox/${userId}`)
    .then(res => res.json())
    .then(data => {
        const messages = data.messages;
        const container = document.getElementById('inbox-container');
        if (!container) return;

        if (messages.length === 0) {
            container.innerHTML = '<p>কোনো message নেই।</p>';
        } else {
            container.innerHTML = messages.map(msg => `
                <div style="border:1px solid #ddd; padding:10px; margin:5px 0; border-radius:8px;">
                    <strong>${msg.sender_name}</strong>
                    <span style="font-size:12px; color:gray;">${msg.created_at}</span>
                    <p>${msg.content}</p>
                </div>
            `).join('');
        }
    })
    .catch(err => console.error('Load inbox error:', err));
}

// Unread message badge count
function loadUnreadCount() {
    const userId = localStorage.getItem('user_id');
    if (!userId) return; // ✅ Not logged in, skip

    const badge = document.getElementById('msg-badge');
    if (!badge) return; // ✅ Badge element doesn't exist on this page, skip

    fetch(`http://127.0.0.1:5000/api/messages/unread-count/${userId}`)
    .then(res => res.json())
    .then(data => {
        badge.innerText = data.count;
    })
    .catch(err => console.error('Unread count error:', err));
}


// ✅ Only runs loadUnreadCount if badge element exists on this page
window.addEventListener('load', () => {
    if (document.getElementById('msg-badge')) {
        loadUnreadCount();
    }
});