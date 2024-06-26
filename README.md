# Progression Pilot
Progression Pilot is a website built in Flask with Jinja html templating, used for easily creating chord progressions to use in music. It was made as part of the CS50x computer science course. [Here](https://www.youtube.com/watch?v=Hz-QCDL7C0g) is a video showing the features of the website.

## Running
To install all python dependencies use `pip install -r requirements.txt`

To launch the website in a development enviroment from the project directory run `flask run`.

## File breakdown
### app.py
This is the main part of the backend, handling databases (using CS50's own SQL library based on SQLite), sending data to the user and recieving data. It is written in Flask (a popular python backend tool) and usually returns HTML files. Based on the app.py from the CS50x project finance.

### schema.txt
This file contains the database schema for `progressions.db`. Useful during development to for modifying or adding to the database structure.

### progressions.db
The SQL database storing all user and progression data. This is only accessed by `app.py`.

### requirements.txt
The required python librarys for pip.

### <ins>templates</ins>

#### layout.html
This is the main template for all pages, containing the navbar (with a block for extra options), imports for tone.js (from static), bootstrap and the filesheet, a block for code, a block for the header, and a block for the main HTML.

#### index.html
The home page of the website. Shows your previously created progressions which are sent by `app.py` when loading the template.

#### login.html
The page to login to your account.

#### register.html
The page to register a new account.

#### new.html
The page to create a new progression, with some choices such as time signature and tempo.

#### edit.html
The main page of the website - where you create and edit progresssions. Contains svg for creating a circle of 5ths - I created the paths in an online svg editor and copied into the html file. I also used javascript to allow for the editing of progressions and playing back of them - using `tone.js`'s polysynth to play chords in real time. This allowed for an easy play and stop system where a chord is started playing at the beginning of a chord, and can be either stopped at the end of the chord or when the *stop* button is pressed, and allowing for beginning playing the progresssion from any point.

### <ins>static</ins>

#### styles.css
The stylesheet for the HTML pages.

#### tone
The `tone.js` library (probably not the best way, but I couldn't find a better one).

## Design choices
### languages
I desided to use Flask (with Jinja) because it was what I was most familar with after the rest of the course. I used javascript so I could run things on clientside, and so I could easily use sound playing librarys.

### svg
I desided to use svg for the chord adding interface, as it let me make an interface that will already be familiar to many composers, but also was easy to understand for beginners. I also decided to use svg because it was something that I wanted to learn anyway. The svg paths took me a long time to set up as whenever I needed to make a change, I had to replace all the svg paths. It was also difficult to remember which path was which, as th epaths themselves give little indication as to what they will look like in the end - so i had to spend a while making sure the paths were matched with the correct anchor tags.