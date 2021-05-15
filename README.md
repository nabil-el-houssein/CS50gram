# CS50gram
#### Video Demo: https://youtu.be/KmmS6Am5p34

## **Table of contents**
* [Introduction](#introduction)
* [Directories and Files](#directories-and-files)
* [Runnning the web app](#running-the-web-app)


## Introduction
  CS50gram is an instagram clone responsive web app. It tries to utilize as much django features as possible with 4 models and 4 sophisticated model-forms. Almost every database update happens without the require to reload the entire page using javascript `fetch` function. It also contains a real-time search feature.
  

## Directories and files
  The main directory consists of two directories (**capstone** & **cs50gram**) and two files (**manage.py** & **requirements.txt**).
  - ### **capstone**
    1. Edited `urls.py` to include `cs50gram` urls.
    2. Edited `settings.py` to include `django-crispy-forms` and allow the uploading of images.

  - ### **cs50gram**
    This is where the main work has been done and it consists of two directories (**static** & **templates**) and seven files (**admin.py, apps.py, forms.py, models.py, tests.py, urls.py** & **views.py**).
    
    - #### **static**
      Static is where all the static files are stored and it consists of the following:
      1. images
          1. `default_profile_pic.jpg` which is set to be the default profile picture for each and every created user until updated.
          2. All the uploaded posts and profile pictures will be stored here.

      2. `follow.js` which handles showing and updating the followings/followers in the database without the need to reload the entire page.
      3. `index.js` which handles showing and updating the likes/comments in the database, in addition to deleting posts, all without the need to reload the entire page.
      4. `preview_image.js` which shows an image preview before posting the image to the database.
      5. `search.js` which handles the real-time search feature for the users on the network.
      6. `profile.css` which defines the stylings for the profile page.
      7. `styles.css` which defines the stylings for the entire web app.

  - #### **templates**
    Templates is where all the `HTML` files are located and it constists of the following:
     1. `add_post.html` which displays a form to add a post to the network.
     2. `edit_profile` which displays a form to edit user's profile.
     3. `explore.html` which shows all the posts on the network except the logged in user's posts.
     4. `index.html` which shows all the posts of the users the logged in user follows. (Feed/Homepage)
     5. `layout.html` where the main layout of the web app is located.
     6. `login.html` which displays a form for a user to be able to login.
     7. `profile.html` which displays the profile of each user.
     8. `register.html` which displays a form for a user to be able to register.

  - #### **admin.py**
    Registers all the models in the admin site.
    
  - #### **apps.py**
    Default django file.
  
  - #### **forms.py**
    Constructs a form for each model with the help of `django-crispy-forms`.
    
  - #### **models.py**
    Consists of four models:
    1. `User` which saves the users accross the network.
    2. `Post` which tracks each post on the network.
    3. `Comment` which tracks each post's comment.
    4. `Profile` which tracks each user's profile.
    
  - #### **tests.py**
    Default django file.
    
  - #### **urls.py**
    Contains the url patterns for all the functions and the APIs.
    
  - #### **views.py**
    The core of the web app that contains all the functions that renders the templates, modifies the models and handles the API calls.

  - ### **manage.py**
    A command-line utility that lets you interact with this Django project.
    
  - ### **requirements.txt**
    Contains all the required python modules used by the web app.


## Running the web app
  To run the app after cloning the repo:
  1. In your `terminal`, cd into the `capstone` directory.
  2. Run `pip install -r requirements.txt` to install all the required modules.
  3. Run `python manage.py makemigrations` to make migrations for the web app.
  4. Run `python manage.py migrate` to apply migrations to your database.
  5. Run `python manage.py runserver` and copy the link to your browser to access the web app.


# This was CS50w
