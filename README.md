# Smapify

## Team mangosteens - Cathy Cai, Tabassum Fabiha, Angela Tom, Stefan Tan

## Overview:
⋅⋅⋅Smapify is a web-based application that allows users to input their current location and the address of their destination to generate a playlist based on the duration of the trip and their current mood, favorite genre and other optional filters alongside with a set of directions for the trip. Through the accounts that users make, they are able to save a favorite playlist along with the route that it is associated with it. With Smapify, users are **guaranteed** to know how to get to their destination while also jamming to music they enjoy!         

## Instructions to Run:
1. Open a terminal session.
2. Make sure you have sudo access to your local computer and install virtualenv if you don't want the processes interfere with your system by typing ```$ sudo pip install virtualenv``` if you don't have one already. Skip to step 5 if you already have a virtual environment and had already activated it. 
3. Create your own environment by typing (myproject and venv are placeholders for names of your choosing):
```
$ mkdir myproject
$ cd myproject
$ virtualenv venv
```
4. Activate the virtual environment by typing ```$ . venv/bin/activate``` in the terminal and make sure it is running python3 by typing ```(venv)$ python --version``` in the terminal. 
5. Clone this repository. To clone this repo, open a terminal session and navigate to the directory you want for this repository to located in. Then clone using SSH by typing ```(venv)$ git clone git@github.com:ccai1/mangosteens.git``` or clone using HTTPS by typing ```(venv)$ git clone https://github.com/ccai1/mangosteens.git``` in the terminal.
6. Navigate to the Smapify repository by typing ```$ cd mangosteens/``` in the terminal. 
7. Make sure you have all the dependencies installed in your virtual environment. If not, look at the **Dependencies section** below.
8. Procure API keys... **(ADDING HOW TO PROCURE LATER)**
9. Run the python file by typing ```(venv)$ python app.py``` in the terminal. 
10. This should appear in the terminal after running the python file.   
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 248-748-502
```

11. Open a web broswer and navigate to the link http://127.0.0.1:5000/.
12. Follow the prompts of our application and enjoy!

## Dependencies: **(ADDING FUNCTION AND PURPOSE OF IT LATER)**
⋅⋅* click==6.7
⋅⋅* Flask==1.0.2
⋅⋅* itsdangerous==0.24
⋅⋅* Jinja2==2.10
⋅⋅* MarkupSafe==1.0
⋅⋅* passlib==1.7.1
⋅⋅* pkg-resources==0.0.0
⋅⋅* Werkzeug==0.14.1
1. Install the dependencies listed above by typing ```(venv)$pip install -r <path-to-file>requirements.txt``` in your terminal. 
