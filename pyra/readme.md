## Pyra
Pyra is the backend for IR-Stats V2. Written in Python and using the new iRacing endpoints and a PostgreSQL Database. It currently handles logging into the iRacing endpoints and retrieving race data, user data and storing it in SQL tables.
Pyra is currently stored in Vercel as a serverless function.

#### Why the change?
Previous iterations of IR-Stats used NodeJS and a MongoDB Atlas instance. Data access had become an issue with larger sets, which is the reason behind the change of paradigm for data storage.
Also, the current endpoints which the previous version uses are deprecated and will stop working #soon.

Writing it in Python will also allow us to use PyTorch in the future for some planned features.

#### Installation
1. Locally run `py -m pip install -r requirements.txt` to install dependencies.
2. Create an `.env` file including the following environment variables:
	```
	POSTGRES_URL=""
	POSTGRES_USER=""
	POSTGRES_HOST=""
	POSTGRES_PASSWORD=""
	POSTGRES_DATABASE=""
	POSTGRES_PORT=""
	```
3. If it's the first time running the application and tables don't exist, run `py db.py`
4. To locally test, use the `local_test.py` script, ensuring to change username and password in the code.