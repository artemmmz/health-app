## Account microservice
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)

### Tests

Microservice uses integration tests, unit-tests, mock tests

#### Run tests
`pytest`

### How work with the microservice

- Copy and rename file .env.example to .env or use environment vairables
- Run `docker-compose` in directory `infrastructure`

### URLs
Docs: `/docs`

Accounts:
- GET `/api/accounts/` - Get all accounts (only for role ADMIN)
- POST `/api/accounts/` - Create a new account (only for role ADMIN)
- GET `/api/accounts/me` - Get current account
- POST `/api/accounts/update` - Update current account
- PUT `/api/accounts/{user_id}` - Update account using `user_id` (only for role ADMIN)
- DELETE `/api/accounts/{user_id}` - Deactivate account using `user_id` (only for role ADMIN)

Authorization:
- POST `/api/authentication/access` - Get access token
- POST `/api/authentication/refresh` - Get new tokens pair
- POST `/api/authentication/signin` - Authorize
- POST `/api/authentication/signout` - Log out
- POST `/api/authentication/signup` - Registration
- POST `/api/authentication/validate` - Interseption access token

Doctors:
- GET `/api/doctors/` - Get all doctors
- GET `/api/doctors/{user_id}` - Get doctor using `user_id`


### Environment variables

##### App settings
- `MODE`: `development`, `production`, `testing` - by default `development`

##### Database config
- `POSTGRES_PROTOCOL` - string, by default `postgresql+asyncpg`
- `POSTGRES_HOST` - string
- `POSTGRES_PORT` - integer, by default `5432`
- `POSTGRES_USER` - string
- `POSTGRES_PASSWORD` - string
- `POSTGRES_DB` - string
- `POSTGRES_ARGUMENTS` - dict, optional

##### Kafka config
- `KAFKA_PROTOCOL` - string, by default `kafka`
- `KAFKA_HOST` - string
- `KAFKA_PORT` - integer, by default `9092`

##### Redis config
- `REDIS_PROTOCOL` - string, by default `redis`
- `REDIS_HOST` - string
- `REDIS_PORT` - integer, by default `6379`
- `REDIS_USER` - string
- `REDIS_PASSWORD` - string
- `REDIS_DB` - integer, by default `0`

##### Security config
- `JWT_ALGORITHM` - string, by default `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` - integer, by default `15`
- `REFRESH_TOKEN_EXPIRE_DAYS` - integer, by default `180`
- `SECRET_KEY` - string, by default random 32-bit string
- `BACKEND_CORS_ORIGINS` - list of urls, by default `['*']`


### TODO:

- [X] Make Authentication
- [X] Make Accounts
- [X] Make Roles
- [X] Make custom exceptions
- [ ] Make Kafka connections
- [X] Make Tests
