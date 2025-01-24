
## 🤖 Simple Feedback bot based on Aiogram-dialog. 


## .env variables 

- DB_TYPE - Possible values/databases: `POSTGRES`, `SQLITE3`
- DB_NAME - Name of database. Just filename in Sqlite3 case
- DB_USER - User of database
- DB_PASSWORD - Password of database
- DB_HOST - Host of database
- DB_PORT - Port of database

*USER\PASSWORD\HOST\PORT - Can be empty if you use SQLITE3*

- REDIS_DATABASE - Redis DB
- REDIS_HOST - Redis Host
- REDIS_PORT - Redis Port
- REDIS_PASSWORD - Redis pass
- REDIS_USERNAME - Redis user

- ADMINS - user_ids from telegram. If you want to enter multiple values, do it with commas, for example:
`ADMINS=123, 432, 123`

- BOT_TOKEN - Telegram bot token from @BotFather

- LOGGING_LEVEL - Logging level
## System dependencies:
- Redis
- Poetry
- Python => 3.12 < 3.13
## Setup:
1. Install dependencies
`poetry install --no-root`
2. Create and apply migrations:
`poetry run dotenv run alembic revision--m='prod' --autogenerate && poetry run dotenv run alembic upgrade head`
## Start

`poetry run dotenv run python3 -m src.bot`