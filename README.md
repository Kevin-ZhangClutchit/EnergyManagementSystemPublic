# EnergyManagementSystemPublic

Kaiwen Zhang 

## Disclaimer

This is the public version of my project of CS-GY 6083 FA 23 meant for code submission. Please do not copy and respect Academic Integrity of NYU.

As it's the public version, it contains no information about commit history and development route. If you would like to see it, you can email me for private version with commit history.

For reference of codes, they are either in project report or code comments within python files so I omit it here.

## Code structure

This is a energy management system website with jinja2 as front end, flask + mysql as backend. It introduces necessary mechanism to prevent sql-injection attack, xss attack and supports concurrent sessions.

The frontend templates are within the **template** folder with subfolder name correspondent to the .py file per blue print. As stated in the project report:

> Basically, we follow and use the structure of the [flask official tutorials](https://flask.palletsprojects.com/en/3.0.x/tutorial/). Especially, we use its css file as I have no time for writing front-end. We follow its blueprint pattern with  following 5 blueprints:
>
> * **db**: used to handle database interactions. We use mysql-connector following the [official guideline](https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html) provided by mysql and follow the pattern of flask tutorials.
> * **auth**: used to handle login, logout and register. We migrate it from original flask tutorials to flask-login based on [Flask-Login 0.7.0 documentation](https://flask-login.readthedocs.io/en/latest/).
> * **blog**: This is originally the main function of flask tutorials. I rewrite it to our main page used to demonstrate **5 energy views** and handle user profile edit.
> * **service**: This is where users see all their service locations. They can add, edit or remove service locations here.
> * **device**: This is where users the devices attached for a certain service location. They can add or delete devices there. They can also see the device activity and **energy summary view** there.