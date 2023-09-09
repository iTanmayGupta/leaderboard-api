# Leaderboard API

The Leaderboard API is a RESTful web service built with Flask and SQLAlchemy that provides endpoints for managing user data and tracking user scores. Users can be added, retrieved, deleted, and their scores can be incremented or decremented. Additionally, there is a leaderboard feature to display users with the highest scores.

## Accessing the Deployed API

The Leaderboard API is currently deployed and accessible at the following URL:

[https://leaderboard-api-fqd4.onrender.com](https://leaderboard-api-fqd4.onrender.com)

You can also explore the API's Swagger documentation here:

[Swagger Documentation](https://leaderboard-api-fqd4.onrender.com/swagger/)

## Testing the API

You can test the API using the web application deployed at the following URL:

[Leaderboard Web App](https://leaderboard-ui-ashy.vercel.app)

This web app provides a user interface for interacting with the Leaderboard API. You can add users, view the leaderboard, and perform other actions to test the API's functionality.

## Local Development

Follow the instructions below to set up and run the Leaderboard API locally for development and testing purposes.

### Prerequisites

Before running the application, ensure you have the following software installed on your machine:

- Python 3.x
- PostgreSQL (or SQLite for testing)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/leaderboard-api.git
   ```

2. Navigate to the project directory:

    ```bash
    cd leaderboard-api
    ```

3. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

4. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Open the server.py file and locate the database configuration section:

    ```bash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
    ```

Replace username, password, and dbname with your PostgreSQL database credentials and the desired database name.

2. Optionally, you can configure the application to use SQLite for testing by modifying the testing configuration:

    ```bash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    ```

### Running the Server

To start the server, run the following command:

    python3 server.py

By default, the server runs on http://localhost:5000. You can access the API and Swagger documentation through this URL.

### Swagger Documentation

The Swagger documentation for the API is available at:

    http://localhost:5000/swagger/

You can use this documentation to explore and interact with the API endpoints.

### Running Tests

To run the test suite, execute the following command:

    pytest -s test_server.py
