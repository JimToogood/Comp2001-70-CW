# Trail Application Micro-Service by Jim (James) Toogood. (Comp2001 70% Coursework)

This application is a python based Trail Comments micro-service build using Python, Flask, SQL and Docker, documented with Swagger (via Flasgger)

---

Usage Instructions:  
  
1) Download repo from link or use git clone  
2) Open terminal/cmd and cd into the root of the project  
  
*To build the docker image (recommended):*  
  
3) Run:  docker build -t jimtoogood/trail_app .  
   Or if not on windows  
   Run:  docker build --platform linux/amd64 -t jimtoogood/trail_app .  
4) Run:  docker run -p 8000:8000 jimtoogood/trail_app  
5) Open http://127.0.0.1:8000/apidocs in any web browser  
  
*Or to use the prebuilt docker image provided (built using --platform linux/amd64, tested on MacOS, but should still run on Windows machines):*  
  
3) Download prebuilt image from here (too big for GitHub): https://drive.google.com/file/d/1kpAmCNnJorlQNhNWm7e40HBorMmDTI8m/view?usp=sharing  
4) Run:  docker load -i trail-microservice.tar  
5) Run:  docker run -p 8000:8000 jimtoogood/trail_app  
6) Open http://127.0.0.1:8000/apidocs in any web browser  

---

Swagger documentation .ymls can be found in trail_app/flask_routes/docs  
  
Python code contains Get, Post, Delete, Put/Patch commands for all tables Comments, Locations, Trails, Users  
  
SQL code contains Create, Delete, Get, Insert, Update for all tables and Last edited trigger  

---

Requirements:  
  
Python 3.9  
Flask 2.2.2  
Werkzeug 2.3.8  
pyodbc 5.2.0  
flasgger 0.9.7.1  
requests 2.30.0
