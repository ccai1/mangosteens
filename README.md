# Smapify

## Team mangosteens - Cathy Cai, Tabassum Fabiha, Angela Tom, Stefan Tan

## Overview:
Smapify is a web-based application that allows users to input their current location and the address of their destination to generate a playlist based on the duration of the trip and their current mood, favorite genre and other optional filters alongside with a set of directions for the trip. Through the accounts that users make, they are able to save a favorite playlist along with the route that it is associated with it. With Smapify, users are **guaranteed** to know how to get to their destination while also jamming to music they enjoy!         

## Instructions to Run:
1. Open a terminal session.
2. Create your own environment by typing (name is a placeholder for the name of the virtual environment of your choosing):
```
$ python3 -m venv name
```
3. Activate the virtual environment by typing ```$ . name/bin/activate``` in the terminal and make sure it is running python3 by typing ```(venv)$ python --version``` in the terminal.
4. Clone this repository. To clone this repo, open a terminal session and navigate to the directory you want for this repository to located in. Then clone using SSH by typing ```(venv)$ git clone git@github.com:ccai1/mangosteens.git``` or clone using HTTPS by typing ```(venv)$ git clone https://github.com/ccai1/mangosteens.git``` in the terminal.
5. Navigate to the Smapify repository by typing ```$ cd mangosteens/``` in the terminal.
6. Make sure you have all the dependencies installed in your virtual environment. If not, look at the [Dependencies section](https://github.com/ccai1/mangosteens#dependencies) below.
7. Procure [API keys](https://github.com/ccai1/mangosteens#apis)...
8. Run the python file by typing ```(venv)$ python app.py``` in the terminal.
9. This should appear in the terminal after running the python file.   
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 248-748-502
```

10. Open a web browser and navigate to the link http://127.0.0.1:5000/.
11. Follow the prompts of our application and enjoy!

## Dependencies:
* Flask==1.0.2

   Used as the framework for the app.
* Jinja2==2.10

   Template engine for Python.
* passlib==1.7.1

   Hashes password to increase security of app.
1. Install the dependencies listed above by typing ```(venv)$pip install -r <path-to-file>requirements.txt``` in your terminal.

## APIs:
* Spotify

   Used to retrieve songs that matches the user's inputs. It does not use API keys but instead uses OAuth2. To learn more about the Spotify API go [here](https://developer.spotify.com/web-api/).
* MapQuest (Directions API)

   Used to retrieve directions, routes, and maps from the user's current location to their destination. To sign up and obtain an API key go [here](https://developer.mapquest.com/documentation/).  
* Public Transit

   Used to retrieve routes using public transits. To learn more about this API go [here](https://developer.here.com/documentation/transit/topics/what-is.html).

For our purposes, mangosteen's keys are stored as keys.json in the data directory.
