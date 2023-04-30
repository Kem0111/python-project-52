### Hexlet tests and linter status:
[![Actions Status](https://github.com/Kem0111/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/Kem0111/python-project-52/actions) <a href="https://codeclimate.com/github/Kem0111/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/99ac7c5906b10c988c28/maintainability" /></a> [![Python Django CI/CD](https://github.com/Kem0111/python-project-52/actions/workflows/task_manager.yml/badge.svg)](https://github.com/Kem0111/python-project-52/actions/workflows/task_manager.yml) <a href="https://codeclimate.com/github/Kem0111/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/99ac7c5906b10c988c28/test_coverage" /></a>

# Task Manager

This is a task manager that allows users to create, assign, and track tasks. The main entities involved in this project are Status, Labels, Tasks, and Users.

## Entity Relationship Diagram (Text Representation)
```
User      (Many-to-One)                      
  ├─► Author ──────┐        ┌──────┐
  │                |        │Status│
  │                |        └──────┘
  │                |           ▲
  │                ▼           |  (Many-to-One)
  │            ┌───────┐ ──────┘     
  │            │ Task  │
  │            └───────┘ ──────┐ 
  │                ▲           |  (Many-to-Many)
  │                |           ▼ 
  └─► Executor ────┘        ┌──────┐
    (Many-to-One)           │Labels|
                            └──────┘
```      
Each task can have only 1 author (User), 1 assignee (User), and 1 status. The relationship between tasks and labels is many-to-many. This means that a task can have multiple labels, and a label can be associated with multiple tasks.  

## Libraries and Tools Used in the Project

| Library / Tool         | Description                                     |
|------------------------|-------------------------------------------------|
| python                 | The core programming language for the project   |
| django                 | Web framework for building web applications     |
| python-dotenv          | Loads environment variables from .env file      |
| gunicorn               | WSGI HTTP server for serving the application    |
| django-bootstrap4      | Integrates Bootstrap 4 with Django projects     |
| django-widget-tweaks   | Customizes Django form rendering                |
| coverage               | Measures code coverage of test suite            |
| flake8                 | Python code linting tool                        |
| psycopg2-binary        | PostgreSQL database adapter for Python          |
| rollbar                | Error tracking and logging for application      |
| Docker                 | A platform for developing,shipping, and running applications|               
| PostgreSQL             | A powerful, open-source object-relational database system|
| Render.com             | A cloud platform for deploying, scaling, and monitoring apps|

# Installation
To install and run the project using Docker, you need to have Docker and Docker Compose installed on your system. Once you have them installed, you can follow these steps:
To set up the project, follow these steps:

1. Clone the repository

``` git clone https://github.com/Kem0111/python-project-52.git ```

2. To set up the environment for the project, you need to define environment variables in a .env file:

    ```SECRET_KEY=
    DEBUG=False
    DJANGO_ENV="local" or "production"
    ```  

    If you are using the production environment, you need to configure the database settings:  
    ```
    POSTGRES_PASSWORD=
    POSTGRES_USER=
    POSTGRES_DB=
    POSTGRES_HOST=
    POSTGRES_PORT=
    ```

    Additionally, set the Rollbar access token:
    ```
    ROLLBAR_ACCESS_TOKEN=(variable)
    ```
    These environment variables will be used to configure your Task Manager project's settings.

3. Run the following command in your terminal or command prompt to start the project:
    ```
    docker-compose up -d  
    docker-compose exec app make migrations
    ```

