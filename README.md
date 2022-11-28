# About

Test gallery api

# What's done

:white_check_mark: Docker deploy

:white_check_mark: Env variables

:white_check_mark: JWT authorization

:white_check_mark: Unit and integration tests


# How deploy

Create an .env file with the following structure in the root folder

```
POSTGRES_USER=postges
POSTGRES_PASSWORD=postges
POSTGRES_NAME=postges
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
Run the following command:

```
docker-compose up --build
```
 
# How use 

1. Navigate to the swagger url:

* /swagger

2. Register a user, create a token and insert it in 'Authorization' like this: 'Bearer Token'

3. Or, if you need to get an admin user, create and paste a token for an already created admin with username and password 'test_admin'