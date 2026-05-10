<div align="center">

<img src="PathFinder Frontend/logo.png" alt="PathFinder Logo" width="50px" />

#  PathFinder

### Intelligent Career Guidance System for BAUET

[![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

> **PathFinder** is a web-based Intelligent Career Guidance System designed to help **BAUET students** choose the right career path based on their skills, interests, and academic performance.

</div>

---

## 📌 Table of Contents

- [🎯 Project Objectives](#-project-objectives)
- [✨ Features](#-features)
- [🛠️ Technologies Used](#️-technologies-used)
- [🏗️ System Architecture](#️-system-architecture)
- [📂 Project Structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🔮 Future Improvements](#-future-improvements)
- [👥 Team](#-team)

---

## 🎯 Project Objectives

| # | Goal |
|---|------|
| 1 | 🎓 Help students discover the most suitable career paths |
| 2 | 🔍 Analyze student skills, interests & academic performance |
| 3 | 🧠 Provide intelligent, data-driven career recommendations |
| 4 | 💻 Deliver an easy-to-use web platform for career guidance |

---

## ✨ Features

- 🔐 **User Registration & Login** — Secure authentication for students and guides
- 👨‍🎓 **Student Dashboard** — Personalized overview of progress and recommendations
- 📊 **Skill & Interest Analysis** — Comprehensive assessment forms
- 🧠 **Career Recommendation Engine** — Smart suggestions based on student data
- 📱 **Responsive Web Design** — Works seamlessly across all screen sizes
- 💬 **Inbox & Notifications** — Stay updated with messages and alerts
- 🔒 **Password Recovery** — Secure forget/reset password flow
- 🔖 **Saved Posts** — Bookmark and revisit career resources

---

## 🛠️ Technologies Used

<table>
  <tr>
    <th>Layer</th>
    <th>Technology</th>
    <th>Purpose</th>
  </tr>
  <tr>
    <td>🌐 <strong>Frontend</strong></td>
    <td>HTML, CSS, JavaScript</td>
    <td>UI structure, styling, and interactivity</td>
  </tr>
  <tr>
    <td>⚙️ <strong>Backend</strong></td>
    <td>Python (Flask)</td>
    <td>Business logic & career recommendation processing</td>
  </tr>
  <tr>
    <td>🗄️ <strong>Database</strong></td>
    <td>MySQL</td>
    <td>Storing user and career data</td>
  </tr>
  <tr>
    <td>🧑‍💻 <strong>Dev Tools</strong></td>
    <td>VS Code, Git & GitHub</td>
    <td>Development, version control & collaboration</td>
  </tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────┐     ┌────────────────────────┐     ┌──────────────┐     ┌──────────────┐
│    User     │────▶│  Frontend              │────▶│   Backend    │────▶│   Database   │
│             │     │  (HTML, CSS, JS)       │     │   (Python)   │     │   (MySQL)    │
└─────────────┘     └────────────────────────┘     └──────────────┘     └──────────────┘
                         Collects user data         Processes data       Stores all data
                         through forms              & generates          persistently
                                                    career suggestions
```

---

## 📂 Project Structure

```
PathFinder/
│
├── 🌐 frontend/
│   ├── 📄 Pages
│   │   ├── index.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── role.html
│   │   ├── login.html
│   │   ├── register-student.html
│   │   ├── register-guide.html
│   │   ├── profile.html
│   │   ├── own_profile.html
│   │   ├── main.html
│   │   ├── technical.html
│   │   ├── non-technical.html
│   │   ├── search-result.html
│   │   ├── saved_posts.html
│   │   ├── inbox.html
│   │   ├── notification.html
│   │   ├── settings.html
│   │   ├── forget-password.html
│   │   ├── new-password.html
│   │   └── reset-sent.html
│   │
│   ├── 🎨 assets/
│   │   ├── images/
│   │   │   ├── logo.png
│   │   │   └── students.jpg
│   │   └── icons/
│   │       ├── assessment.png
│   │       ├── college.png
│   │       ├── mentor.png
│   │       ├── profile.png
│   │       ├── school.png
│   │       ├── technology.png
│   │       └── virtual.png
│   │
│   ├── 🎨 css/
│   │   └── style.css
│   │
│   └── ⚙️ js/
│       └── script.js
│
├── 🐍 backend/
│   └── app.py
│
├── 🗄️ database/
│   └── schema.sql
│
├── 📋 README.md

```



---

## 🧪 Testing

- ✅ User registration and login flow
- ✅ Database connection
- ✅ Responsive design across devices
- ✅ Bug fixing and UI/UX improvements

---

## 🔮 Future Improvements

- 🤖 AI-based career prediction model
- 🛡️ Admin panel for managing career data
- 📝 More detailed and dynamic skill assessments
- 📈 Integration with live job market data
- 🌐 Multi-language support

---

## 👥 Team

This project is developed by students of **BAUET** as part of a web development course project.

---

## 📜 License

This project is for **educational purposes only**.

---

<div align="center">

⭐ **If you find this project helpful, please give it a star on GitHub!** ⭐

*Built with ❤️ by BAUET students*

</div>