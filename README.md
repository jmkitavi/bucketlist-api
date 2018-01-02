[![CircleCI](https://circleci.com/gh/sirjmkitavi/cp2-bucketlist/tree/develop.svg?style=svg)](https://circleci.com/gh/sirjmkitavi/cp2-bucketlist/tree/develop)
[![Coverage Status](https://coveralls.io/repos/github/sirjmkitavi/cp2-bucketlist/badge.svg?branch=develop&update=1)](https://coveralls.io/github/sirjmkitavi/cp2-bucketlist?branch=develop)
[![Issue Count](https://codeclimate.com/github/sirjmkitavi/cp2-bucketlist/badges/issue_count.svg)](https://codeclimate.com/github/sirjmkitavi/cp2-bucketlist)

#BucketList Application API

## Introduction

> This application is a Flask API for a bucket list service that allows users to create, update and delete bucket lists. It also provides programmatic access to the items added to the items created. This API is a REST API and the return format for all endpoints is JSON.

## Endpoints

1. `POST /auth/login`
2. `POST /auth/register`
3. `GET /bucketlists/`: returns all bucket listing of all buckets list
4. `GET /bucketlists/<bucketlist_id>`: returns the bucket list with the specified ID
5. `PUT /bucketlist/<bucketlist_id>`: updates the bucket list with the specified with the provided data
6. `DELETE /bucketlist/<bucketlist_id>`: deletes the bucket list with the specified ID
7. `POST /bucketlists/<bucketlist_id>/items/`: adds a new item to the bucket list with the specified ID
8. `PUT /bucketlists/<bucketlist_id>/items/<item_id>`: updates the item with the given item ID from the bucket list with the provided ID
9. `DELETE /bucketlists/<bucketlist_id>/items/<item_id>`: deletes the item with the specified item ID from the bucket list with the provided ID

## Installation & Setup
1. Download & Install Python
 	* Head over to the [Python Downloads](https://www.python.org/downloads/) Site and download a version compatible with your operating system
 	* To confirm that you have successfully installed Python:
		* Open the Command Prompt on Windows or Terminal on Mac/Linux
		* Type python
		* If the Python installation was successfull you the Python version will be printed on your screen and the python REPL will start
2. Clone the repository to your personal computer to any folder
 	* On GitHub, go to the main page of the repository [BucketList API](git@github.com:pythonGeek/bucketlist_api.git)
 	* On your right, click the green button 'Clone or download'
 	* Copy the URL
 	* Enter the terminal on Mac/Linux or Git Bash on Windows
 	* Type `git clone ` and paste the URL you copied from GitHub
 	* Press *Enter* to complete the cloning process
3. Virtual Environment Installation and Setup [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
4. Enter the project directory by running `cd cp2-bucketlist`
5. Once inside the directory install the required modules
 	* Run `pip install -r requirements.txt`
 * On the terminal type `python manage.py runserver` to start the application

 ## Perform migrations
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade


## Testing
To run the tests for the app, and see the coverage, run
```
nosetests --with-coverage
```

Damn It This READMe needs some work.