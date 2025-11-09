# ToDoListAPI

## Description
REST API to allow users manage their To-Dos built with Flask. Project was inspired by [Todo List API](https://roadmap.sh/projects/todo-list-api) by roadmap.sh.

---
## Project structure
```
ToDoListAPI/
├── app/
│   ├── __init__.py      # def to initialize app instance
│   ├── config.py        # default and test configurations
|   ├── errors.py        # def to register errors for app instance
│   ├── extensions.py    # db, migration, jwt and redis 
│   ├── models.py        # user and todo model
│   ├── schemas.py       # schemas for user and todo
│   ├── api/
│   │   ├── __init__.py  # def to register blueprints for app instance
│   │   ├── auth.py      # register and login endpoints
│   │   └── todos.py     # crud operations
├── migrations/          # alembic output (used for db migration and upgrade)
├── tests/
│   ├── conftest.py      # config for test
│   ├── test_auth.py     # script to test login and registration
│   └── test_todos.py    # script to test crud
├── requirements.txt
├── manage.py            # app instance is run here
├── .env                 # secrets are stored here
├── .env.example         # example of how .env should look like
└── README.md
```

---
## Main features
- Multiple users registration
- Authorization via JWT tokens
- Refresh tokens for JWT renewal
- Token revocation via Redis
- CRUD operations for To-Dos
- Test scripts and testing configuration
---
## Installation
1) Clone the repository:
```
> git clone https://github.com/ArturBel/ToDoListAPI.git
> cd ToDoListAPI
```

2) Create and activate virtual environment:
```
> python -m venv venv
> source venv/bin/activate
> pip install -r requirements.txt
```

3) Create database in Postgres for storage (and/or testing) and apply migration.
```
psql> CREATE DATABASE todolistapi OWNER postgres;       # main db
psql> CREATE DATABASE todolistapi_test OWNER postgres;  # testing db
> flask db upgrade                              # migration is already created
```

4) Create .env file to store secrets, paste there example file and add real values:
```
.env   # your .env might look like this

DATABASE_URL=postgresql://postgres:password@localhost:5432/todolistapi
TEST_DATABASE_URL=postgresql://postgres:password4@localhost:5432/todolistapi_test
SECRET_KEY=change-this
JWT_SECRET_KEY=change-this-as-well
ACCESS_EXPIRY_MINUTES=15
REFRESH_EXPIRY_DAYS=1
REDIS_HOST=localhost
REDIS_PORT=6379
```

4) Run Flask app:
```
> python manage.py
# or manually run manage.py script
```

---
## Usage

### Authorization
Register using the 'POST' method:
```
POST /api/auth/register
{
	"email": "user@email.com",
	"username": "Username",
	"password": "password"
}
```

The endpoint should validate the request body and return a `201 Created` status code with newly created user:
```
{
	"access_token": "access",
	"email": "user@email.com",
	"id": 1,
	"message": "user registered successully",
	"refresh_token": "refresh",
	"username": "User"
}
```


After that, login using the 'POST' method:
```
POST /api/auth/login
{
	"email": "user@email.com",
	"password": "password"
}
```

The following response with `200 OK` status is expected:
```
{
	"access_token": "access",
	"msg": "login successful",
	"refresh_token": "refresh"
}
```


In order to refresh access token, refresh endpoint with refresh token in bearer header is used:
```
POST /api/auth/refresh
```

This returns `200 OK` status and creates new refresh and access tokens:
```
{
	"new_access_token": "new_access"
}
```

In order to log out and revoke your current token, logout endpoint must be accessed via 'POST':
```
POST /api/auth/logout
```

Upon successful logout, current access token should be revoked and stored in Redis until natural invalidation and this message should be displayed:
```
{
	"msg": "token revoked successfully"
}
```

### CRUD operations

**For all CRUD operations with ToDo instances bearer token is required.**
#### Create a ToDo
To create a new ToDo, 'POST' method is used:
```
POST /api/todos/
{
	"title": "Finish documentation",
	"description": "Finish Flask's ToDoListAPI documentation"
}
```

The following response with `201 Created` is expected:
```
{
	"completed": false,
	"created_at": "2025-11-09T16:41:37.192366",
	"description": "Finish Flask's ToDoListAPI documentation",
	"id": 1,
	"owner": {
		"created_at": "2025-10-12T18:27:42.574736",
		"email": "user@mail.com",
		"id": 1,
		"username": "User"
	},
	"owner_id": 1,
	"title": "Finish documentation",
	"updated_at": "2025-11-09T16:41:37.192371"
}
```

#### Read ToDo or ToDos
To get a single ToDo, use 'GET' method and primary key of the ToDo. Alternatively, to get all ToDos, use 'GET' method alone:
```
GET /api/todos/{int: pk}
```

The endpoint should return a `200 OK` status code with the blog post(s):
```
[
	{
		"completed": false,
		"created_at": "2025-11-09T16:41:37.192366",
		"description": "Finish Flask's ToDoListAPI documentation",
		"id": 1,
		"owner": {
		"created_at": "2025-10-12T18:27:42.574736",
		"email": "user@mail.com",
		"id": 1,
		"username": "User"
		},
		"owner_id": 1,
		"title": "Finish documentation",
		"updated_at": "2025-11-09T16:41:37.192371"
	}
	# if you created multiple todos, more will be displayed here
]
```

#### Update a ToDo
To edit a ToDo, 'PUT' method is used with a primary key:
```
PUT /api/todos/{int: pk}
{
	"completed": true
}
```

It should return `200 OK` status and display following result:
```
{
	"completed": true,
	"created_at": "2025-11-09T16:41:37.192366",
	"description": "Finish Flask's ToDoListAPI documentation",
	"id": 1,
	"owner": {
		"created_at": "2025-10-12T18:27:42.574736",
		"email": "user@mail.com",
		"id": 1,
		"username": "User"
	},
	"owner_id": 1,
	"title": "Finish documentation",
	"updated_at": "2025-11-09T16:41:37.192371"
}
```

#### Delete a Post
To delete a ToDo, `DELETE` method should be used, as well as primary key of a ToDo:
```
DELETE /posts/{int: pk}
```

It should return `204 NO CONTENT` status and delete a ToDo from database.

---
## Testing

To test all functions of ToDoListAPI, including registration, login and CRUD, run the following command:
```
> python -m pytest
```

---
## Author

Artur Belotserkovskiy
- Github: https://github.com/ArturBel
