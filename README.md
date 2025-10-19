# ToDoListAPI
---
## Description
REST API to allow users manage their To-Dos built with Flask. Project was inspired by [Todo List API](https://roadmap.sh/projects/todo-list-api) by roadmap.sh.

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
## Testing

To test all functions of ToDoListAPI, including registration, login and CRUD, run the following command:
```
> python -m pytest
```

---
## Author

Artur Belotserkovskiy
- Github: https://github.com/ArturBel
