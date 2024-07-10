# AnderBaher-Coding-Challenge
Book List Web Application
This Book List web application can be adapted to design other applications by changing the entities and data fields. It serves as a base for creating full-stack web applications, showcasing CRUD operations, web frameworks, and database integration.





Project Overview
This project is a fully functioning full-stack web application that manages a list of books. The application fetches data from a third-party API, stores it in an SQLite database, and provides a web interface for users to view, create, update, and delete book entries.





Key Features
CRUD Operations: Create, Read, Update, and Delete book entries.
Database Integration: Uses SQLite for storing book data.
Web Framework: Built with FastAPI for handling backend and API requests.
Hosting: Deployed on Heroku for live access.
HTML Templates: Uses HTML, CSS, and JavaScript for the frontend.





Technologies Used
FastAPI: Chosen for its performance, ease of use, and modern design. FastAPI supports asynchronous programming and automatic generation of OpenAPI and JSON Schema documentation.
SQLite: Selected for its simplicity and serverless nature, making it easy to set up and manage without needing a separate database server.
HTML, CSS, JavaScript: Used for building the frontend due to their simplicity and wide support. React was not used to avoid additional complexity.
Heroku: Used for deploying the application, providing easy integration with GitHub and automatic deployment on commit.



Project Structure



project/
│
├── app/
│   ├── __init__.py
│   ├── fast_api.py
│   ├── 
│
├── templates/
│   ├── index.html
│   ├── create.html
│   ├── detail.html
│   └── update.html
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── scripts.js
│
├── main.py
├── requirements.txt
├── Procfile
└── README.md




Setting Up the Project:


Prerequisites
Ensure you have the following installed:
Python 3.8+
Git
Heroku CLI
