# About the Project

I wanted to create a web app that provided a solution to disorganization and excess. I have accumulated a lifetime’s worth of possessions over the years and I wanted to create an app that would give me more order in my life. An advantage to knowing what you have is knowing what you do not need. So, I decided to create an inventory web app that keeps track of your household’s belongings. The ideal user for this app is someone who desires to keep track of the many possessions that they have acquired in their life.

This project is distinct from the past projects (CS50 Web) in that users can be joined together as a “household”. A django model stores the data for “household requests”. Once a user accepts a request, both users will be added to the household field in the User model. A user who has someone in their household will be able to view that user’s inventory, locations, and storage that the other user created.

This project is specifically distinct from the social network and commerce website because this web app’s core purpose is to showcase inventory among users of the same household rather than interacting between users. The app’s main purpose is to be able to view where items are located in locations within a household. The django models keep track of which users create “Locations” and “Storage Types” and these are shown to users of the same household to store items in.

# Built With

- Django
- Python
- Javascript
- Bootstrap
- HTML

# Getting Started

1. Access project directory from command line
2. Run django migrations to set up models:
   ⋅⋅⋅python manage.py makemigrations
   ⋅⋅⋅python manage.py migrate
3. Create a superuser
   ⋅⋅⋅python manage.py createsuperuser
4. Start local web server
   ⋅⋅⋅python manage.py runserver
5. Access at http://127.0.0.1:8000/

# Files

- Inventory folder - contains the inventory app for the final project (auto generated using ‘python manage.py startapp inventory’ command)
- Static files - contain inventory javascript file and inventory css file
- Templates - contain html files of the inventory app
- Admin.py - registers models with admin site
- Forms.py - contains forms for New Items, New Storage, New Storage Locations, and Searching users
- Urls.py - contains the url paths and api routes for app
- Views.py - contains inventory web responses
