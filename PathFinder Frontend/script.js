function loginUser(event) {
    event.preventDefault();
    window.location.href = "home.html";
}
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
