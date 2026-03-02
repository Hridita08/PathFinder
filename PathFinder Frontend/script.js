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