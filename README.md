# Progression Pilot
Progression Pilot is a website built in Flask with Jinja html templating, used for easily creating chord progressions to use in music. It was made as part of the CS50x computer science course. [Here](https://www.youtube.com/watch?v=Hz-QCDL7C0g) is a video showing the features of the website.

## Running
To launch the website in a development enviroment from the project directory run
`flask run`

## File breakdown
### app.py
This is the main part of the backend, handling databases (using CS50's own SQL library based on SQLite), sending data to the user and recieving data. It is written in Flask (a popular python backend tool) and usually returns HTML files.

### schema.txt
This file contains the database schema for `progressions.db`. For development use.

### progressions.db
The SQL database storing all user and progression data. This is only accessed by `app.py`.

### requirements.txt
The required python librarys.

### templates
#### layout.html
This is the main template for all pages, containing the navbar (with a block for extra options), imports for tone.js (from static) and bootstrap, a block for code, a block for the header, and a block for the main HTML.

#### index.html
The home page of the website - shows your previously created progressions.

#### login.html
The page to login to your account

#### register.html
The page to register a new account

#### new.html
The page to create a new progression, with some choices such as time signature and tempo

#### edit.html
The main page of the website - where you create and edit progresssions. Contains svg for creating a circle of 5ths, as well as javascript to allow for the editing of progressions and playing back of them (using tone.js)

###