# Mcq-Web-App
A Python Django web application for taking MCQ (Multiple choice questions) tests.

### About
This application is developed in Python Django (a web framework for rapid development).
A user can sign in with any of the one roles "Moderator" or "Contestant". for more info see roles below.
This Web Application presents a set of random questions from database to user and calculates user score accordingly.

### Types of User-Roles (Roles)
 **Moderator:** A user who wants to take tests.
 **Contestant:** A user who gives tests.

### Features
1. **Contestant Exam State Tracking.**
2. **Contestant Login and SignUp.**
3. **Admin Panel.**
4. **Score Calculation Rules.**
5. **Moderator can take multiple tests.**
6. **Moderator can assign any number of test that he has designed to any number of some students.**

### Setup in production environment:
This application is currently in development phase and hence its not suitable to use it in production environment till then you can try this application on your local machine see intructions "**Run on local machine**"
Once its release of first version it can be used in production.

### Run on local machine - instructions
1. pip3 install virtualenv
2. export PATH=$PATH:~/.local/bin
3. virtualenv -p python3 my_virtual_env
4. cd my_virtual_env
5. source bin/activate
6. (my_virtual_env) $ git clone https://github.com/ankity10/Mcq-Web-App.git
7. (my_virtual_env) $ cd Mcq-Web-App
8. (my_virtual_env) $ pip install -r requirements.txt
9. (my_virtual_env) $python manage.py runserver 8080
10. Open this link -> localhost:8080 and try this application.

### Todo
1. Import questions from excel sheet.
2. Ability to select questions for each test.
3. Ability to select students for each test
4. Ability to set marking scheme for each test.

### Contributing
1. You can setup this project locally by following intructions given above.
2. Then after fixing any issue yo can do a pull request.
3. In case of any issues please contact me => ankitwrk at gmail
