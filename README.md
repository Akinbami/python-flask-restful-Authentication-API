


## Local User API from (Mysql Database)

# Endpoints
* **http://127.0.0.1:5000/api/register** <br />
* **http://127.0.0.1:5000/api/login** <br />
* **http://127.0.0.1:5000/api/secret** <br />
* **http://127.0.0.1:5000/api/logout/access** <br />


# Register

Create user

* **URL** <br />
    `http://127.0.0.1:5000/api/register`
* **Method**
    `POST`
* **URL Params** <br />
    `name=[string]`  **Required:**
    `password=[string]`  **Required:**

* **Data Params** <br />
    `None`
* **Success Response:**
    * **Code:** 200 <br />
    * **Sample Body:** <br />
        ```json
            {
                "status": "Ok",
                "data": {
                    "id": 7,
                    "username": "samson3",
                    "date_registered": "2020-09-04T19:55:24"
                }
            }
                ```

# Login

Login User

* **URL** <br />
    `http://127.0.0.1:5000/api/login`
* **Method**
    `POST`
* **URL Params** <br />
    `name=[string]`  **Required:**
    `password=[string]`  **Required:**

* **Data Params** <br />
    `None`
* **Success Response:**
    * **Code:** 200 <br />
    * **Sample Body:** <br />
        ```json
            {
                "status": true,
                "message": "Logged in as samson3",
                "access_token": "eyJ0eXAiOOiJhY2Nlc3MifQ.tJdURzaLiCuVHrwtIupvm8PwbbTG9SJdeUvV0zoX4U4...",
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbBKw81m8gfhgjhkjhjghfgdrtryt6567898tyghjjghf..."
            }
        ```

# Secret

Access secret endpoint

* **URL** <br />
    `http://127.0.0.1:5000/api/secret`
* **Method**
    `GET`
* **URL Params** <br />
    `None`
* **Data Params** <br />
    `None`
* **Authorization** <br />
    `Bearer Token`
* **Success Response:**
    * **Code:** 200 <br />
    * **Sample Body:** <br />
    ```json
        {
            "valid": true
        }
    ```

# Logout
Logout User

* **URL** <br />
    `http://127.0.0.1:5000/api/logout/access`
* **Method**
    `DELETE`
* **URL Params** <br />
    `None`

* **Data Params** <br />
    `None`

* **Authorization** <br />
    `Bearer Token`

* **Success Response:**
    * **Code:** 200 <br />
    * **Content:** <br />
    ```json
        {
            "message": "Access token has been revoked"
        }
    ```


## Database Model
- **User**
- **RevokedTokenModel**


## Tools Used

- **python3 7.3(https://www.php.net/downloads)**
- **Flask 1.1.1(https://flask.palletsprojects.com/en/1.1.x/)**
- **Mysql 8.0(https://www.mysql.com/downloads/)**

## Development Libraries

- **Flask-Migrate 1.1.1(https://flask-migrate.readthedocs.io/en/latest/)**
- **Flask-SQLAlchemy 1.1.1(https://flask-sqlalchemy.palletsprojects.com/en/2.x/)**
- **Flask-JWT-Extended 1.1.1(https://flask-jwt-extended.readthedocs.io/en/stable/)**

## application terminal commands
create database with the name flask_auth in mysql server and run the following commands to start the application
- **git clone git@github.com:Akinbami/python-flask-restful-Authentication-API.git**<br>
`clone repository to system`
- **pip install -r requirements.txt**<br>
`install dependencies`
- **flask db init**<br>
`create database migration files`
- **flask db migrate**<br>
`detect and sync database changes`
- **flask db upgrade**<br>
`apply database migrations`
- **flask run**<br>
`start application`

## NOTE
- **No testing is implemented**<br>
- **Basic Exceptions are not handled**<br>