# Blog-app-with-Flask
### Create a full-stack Blog web app using HTML, CSS, Python-Flask, SQLite

### QUICK START

(Assuming you have Flask and SQLite intalled)

- Create a directory flask-blog and cd into it

```
mkdir flask-blog
```
```
cd flask-blog
```

- Clone the repository

```
git clone https://github.com/Amruth-S05/Blog-app-with-Flask.git
```
- cd into Bolg-app-with-Flask
```
cd Blog-app-with-Flask
```
- Initialize the database required to store user and post data

```
flask --app flaskr init-db
```
The database will be initialized in the new **instance** folder. Running this command again will erase all the data and reinitialize a new database.
- Run the application in development server

```
flask --app flaskr --debug run
```
- Visit 127.0.0.1:5000/ or localhost:5000/ from your browser
- To stop the development server use ^C in the terminal

### To use it as a package (Run app from anywhere)
(Assuming you are in Flask-app-blog)

- Install the package through pip
```
pip install -e .
```
- Now you can start the app even from the outside of project directory.
