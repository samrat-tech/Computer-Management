
# Computer Management



## Distinctiveness and Complexity
This project is called Computer Management, it's a website made using Django on the back-end and Javascript on the front-end.
This projects satisfies all the distinctiveness and complexity requirements, because it's a totally different idea from the 
other projects in this course.

The idea behind Computer Management, is to be a management website where the users can add
available computers on their store, manage sales & purchases, and also finances.

The distinctiveness of this project from the others is very clear, since it doesn't appear to be a social network, an e-commerce or an e-mail, 
and it's not based on the old CS50W Pizza project. It's completely different from the other projects in the course too, 
that even used Javascript in the front-end.

It's possible to check the project complexity in relation to the other ones, once it has much more functions compared to the others.
It also included some models and it's completely mobile-responsive.
## Project Files

There's not many additional files that's created beyond the Django framework standards.
Inside the static directory there's my own custom CSS, SCSS, and Javascript files and 
there's some SVG images that I used in the project too. And inside the templates directory 
in the inventory app there's all the HTML files used in the website.

#### Contents in each file:
- views.py contains all of the project's views
- models.py contains all of the project's models, which are "User", "Part", "ComputerItem", and "Sale"
- admin.py registers all of the various models for the Django admin interface
- base.html is the base template for the app, includes project's navigational items and import stylesheets
- app.html contains the app's center, front views
- contact.html contains the contact details and map location
- login.html contains the login template for the app
- register.html contains the register template for the app
- main.scss contains the main scss design file for the app
- _variables.scss contains all of the variables used by main.scss
- _responsive.scss contains the mobile responsiveness stylesheet
- _placeholders.scss contains placeholders used by main.scss
- _mixins.scss contains mixins used by main.scss
- main.css is the compiled version of main.scss
- main.js contains all the API requests and dynamic features of the web app
- bottom_graphics.svg is the "wave" design on the bottom of the page
- requirements.txt contains all of the necessary Python packages in order to run the web application

## How to run the application

#### Windows

```bash
  pip install -r requirements.txt
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
```

#### Linux

```bash
  pip install -r requirements.txt
  python3 manage.py makemigrations
  python3 manage.py migrate
  python3 manage.py runserver
```
    