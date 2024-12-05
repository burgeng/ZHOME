# Zillow Real Estate Data Dashboard (CIS550 Project)
In our project, we will explore housing market data from [Zillow](https://www.zillow.com/research/data/). This data will be hosted on an AWS RDS instance running [Postgresql](https://www.postgresql.org/). \
[Flask](https://flask.palletsprojects.com/en/stable/) is used as the API backend serving the data, and [React.js](https://react.dev/) is used to render the frontend (with [yarn](https://yarnpkg.com/) as its package manager). [ChartJS](https://www.chartjs.org/docs/latest/) is used to render the plots.

**Database Connection**: To connect to the postgreSQL database, you will need to create a file named `.env` inside the `react-flask-app/api` directory. Populate this file with the following keys:
```
DATABASE_ENDPOINT=
DATABASE_PORT=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
```
Please talk to one of the group members to get the values for these keys. They are not provided here for security reasons.

### Running the app locally
To run the app locally, follow these steps *after cloning the repository to your local machine and entering the directory*:
1. Ensure that you have all required **Python packages** installed - `pip install -r requirements.txt`
2. Navigate to the app directory - `cd react-flask-app`
3. Start the backend (Flask) - `yarn start-api` \
a. Check the connection to the database by visiting `localhost:5000/checkdbconnection`
4. Start the frontend (ReactJS) - `yarn start`
5. Navigate to app in browser at `localhost:3000/`
