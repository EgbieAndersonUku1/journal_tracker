# About the project

JobJournalTracker is a web based job journal application that I built from the ground up, 
an application that can be used by anyone whether they are a freelancers, jobseeker, contractor, etc to track, add, modify,
view or delete their job entries. This website consolidation all job applications, interviews, employer responses into one 
easy to view place. 

The primary reason for building this application was to eliminate the hassle of tracking the 
different jobs applied from different sites.

A great way to think about it would be be having multiple passwords for a bunch of different websites or 
application and using some kind of password managers or application to keep track of all your passwords and what
sites each password belongs too. This is exactly the same but instead of passwords you track jobs
 
### Usage

1. Create an account by registering
2. Verify your email address
3. Login and begin adding jobs to the application. 
    1. Title
    1. Description
    1. Job URL (for easy reference)
    1. State of your application e.g applied, awaiting interview (You can always edit)   
    1. Where your found the job e.g Indeed, Linkedln, etc
    1. Salary
    1. Country
    1. Any additional information you want to add
    1. Hit save when done

4. You can edit, modify, search, view or delete any job entry you have added
5. Easily change your password, email or de-activate your account with a simple button
6. View all your account activity, etc         


## Prerequisites
1. Install python 3.8 or higher than Python 3.7. This application uses a lot of the latest python modules like dataclasses. etc
1. To be able to send emails from this application you need a Gmail account. I decided to use Gmail instead of API keys
    1. You need to set less-secure-app inside your gmail settings to on. This allows gmail
    to be able to send emails using application like python

## what are dataclasses?
Dataclasses was introduced in Python 3.7 but it is backported to python 3.6 and is now part of the standard Python library. Datatclassess have many functionality but one of the biggest functionality is the elimination of writing __init__, __repr__, __eq__, etc. 

Take these two classes

    1. Car(object):
          def __init__(self, colour, make, type, car_name="Ford Raptor"):
              self.colour = colour
              self.make = make
              self.type = type
              self.car_name = car_name
          
          def __repr__(self):
              return f"Car name <{self.car_}> with make {self.make}"
    
    Now with dataclassess
    
    from dataclasses import dataclass, field
    
    @dataclass
    Car(object):
        colour: str
        make: str
        type: str
        car_name: str = field(default="Ford Raptor")
          
    
  

## Installing and running this on your local system
To run this application on your computer create a virtual environment. The virtual environment is optional but it
is always a good idea to create a new environment so that you do not break any previous programs that you have written

1. Create a folder you can name whatever you want
1. Type the command git clone https://github.com/EgbieAndersonUku1/journal_tracker.git . (The . tells github not to create a folder but instead 
   download it to your current folder instead
1.  run the requirements.txt file by entering the command inside your root directory

    1. pip install -r requirements.txt
    
    This will download everything needed to run the application
    
1. Next create .env file in your root folder and adding the following things to it inside the quotation. This email and address must be gmail


    1. EMAIL_ADDRESS = ""
    1. EMAIL_CONFIRMATION_SALT = ""
    1. EMAIL_PASSWORD = ""
    1. SECRET_KEY = ""
    1. ADMIN_EMAIL = ""
  
If you are using sqlite which is already install then skip this step, but if you have mysql installed on your system 
and you would rather use that database then enter the following command

    1. DB_USERNAME = ""
    1. DB_PASSWORD = ""
    1. DB_HOST = ""
    1. MYSQL_ROOT_PASSWORD = ''
    1. Then comment out line 55 and uncomment line 39 in the settings.py file


Now open a terminal in the root directory and enter the following command

    1. python run.py db init
    1. python run.py db migrate
    1. python run.py db upgrade
    1. python run.py shell => This will open up shell window
    
    Inside the shell window you opened using the command python run.py shell enter the following command
    
    1. from app import db
    1. from models.users.user import *
    1. from models.jobs.job import *
    1. db.create_all()
    
    1. Close the shell window. Open a terminal window in the root folder and enter the following command
    
    1. Running the application use the following command: python run.py runserver
    1. Viewing the application use the following command in any browser: http://127.0.0.1:5000 


 
# Technologies used 

1. Python 3.8
1. Flask - Micro framework written in python
1. Bootstrap v4.5.3
1. Javascript
1. HTML
1. css



## About the author

 My name is Egbie for short and I am a mathematician, a test analyst, a freelancer and a python developer. I have been
using Python and Flask <em>(This site was built entirely using Python 3.8, the flask framework along with
CSS, Bootstrap and Javascript) </em> for a long time in order to solve problems. 
From small tasks to building websites, web scrappers, website automation testing which includes
using different types of frameworks e.g Selenium, Robot, etc.

         
As a test analyst I have the skills and in depth knowledge of testing which is
a complete different skill set to developing. While the goal of developer is to develop, the goal of tester analyst is to
destroy so to speak by finding bugs in any given application by coming up with interesting
ways that program can be used, ways never intended by the developer which will result in either a crash, errors or worse the
program or application does not crash but behaviours differently then the developer intended.

My knowledge of testing includes but not limited to manual testing, black box testing, white box testing, regression testing, etc

I enjoy solving solving problems and mapping that problem into code, taking on new challenges, understanding and learning
new techniques, technologies and new testing methods, finding interesting ways to test a given application, 
building things to solve a given problem, it is one of the primary reason I built this site to solve a particular problem.

        
If you have any queries about this site or like to talk about a freelance project please contact me using the contact
email <a href="#">egbieuku@hotmail.com</a>



## Website
To use the website visit the link https://www.jobjournaltracker.com
