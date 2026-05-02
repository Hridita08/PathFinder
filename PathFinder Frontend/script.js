// // 1. Password Toggle Logic
function togglePassword() {
    const pass = document.getElementById("password");
    const icon = document.querySelector(".toggle-pass");

    if (pass.type === "password") {
        pass.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        pass.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}

// 2. Login Page Animation
window.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".pf-login-container");
    if (container) {
        setTimeout(() => {
            container.classList.add("show");
        }, 100);
    }
});

// 3. Non-Technical Page Logic
function setActive(element) {
    document.querySelectorAll(".sidebar li").forEach(li => {
        li.classList.remove("active");
    });
    element.classList.add("active");
}

function toggleDropdown() {
    const dropdown = document.getElementById("careerDropdown");
    if (dropdown) {
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    }
}

function showDetails(career) {
    const detailsContainer = document.getElementById("careerDetails");
    const careers = {
        marketing: "<h3>Marketing</h3><p>Required Degree: BBA / Marketing</p><p>Skills: Communication, Creativity</p><p>Jobs: Digital Marketer, Brand Manager</p>",
        hr: "<h3>Human Resource</h3><p>Required Degree: BBA / HRM</p><p>Skills: Leadership, Communication</p><p>Jobs: HR Manager, Recruiter</p>",
        teaching: "<h3>Teaching</h3><p>Required Degree: Education / Subject Degree</p><p>Skills: Patience, Presentation</p><p>Jobs: Teacher, Lecturer</p>",
        journalism: "<h3>Journalism</h3><p>Required Degree: Journalism / Media</p><p>Skills: Writing, Research</p><p>Jobs: Reporter, News Editor</p>"
    };

    if (detailsContainer) {
        detailsContainer.innerHTML = careers[career] || "Select a career to see details.";
    }
}

function suggestCareer() {
    let interest = document.getElementById("interestInput").value.toLowerCase();
    let result = document.getElementById("result");

    if (!result) return;

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