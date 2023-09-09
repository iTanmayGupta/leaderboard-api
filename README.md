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

## Understanding Test Cases

The Leaderboard API includes a set of test cases to ensure that the application functions correctly and reliably. These test cases cover various aspects of the API's functionality and help identify any issues or regressions when making changes to the codebase.

Here's a brief explanation of each test case:

### `test_get_users`

This test case verifies the correctness of the `/users` endpoint, which returns a list of users sorted by their scores in descending order. It does the following:

- Clears the database to ensure a clean slate.
- Adds two test users with predefined names, ages, and addresses.
- Sends a GET request to the `/users` endpoint.
- Checks that the response status code is 200 (OK).
- Verifies that the response contains exactly two user entries.

### `test_get_user`

This test case checks the `/user/{id}` endpoint, which retrieves a user by their ID. It performs the following steps:

- Adds a test user to the database with a known name, age, and address.
- Sends a GET request to the `/user/{id}` endpoint, specifying the user's ID.
- Ensures that the response status code is 200 (OK).
- Verifies that the returned user data matches the predefined values.

### `test_add_user`

The purpose of this test case is to validate the `/user` endpoint for creating new users. It follows these steps:

- Constructs a JSON payload representing a new user with a name, age, and address.
- Sends a POST request to the `/user` endpoint with the JSON payload.
- Checks the response status code, which should be either 201 (Created) for a successful creation or 400 (Bad Request) for invalid input.
- For successful creations, it confirms that the returned data matches the provided input.

### `test_delete_user`

This test case focuses on the `/user/{id}` endpoint for deleting users. It performs the following actions:

- Adds a test user to the database.
- Sends a DELETE request to the `/user/{id}` endpoint, specifying the user's ID.
- Verifies that the response status code is 200 (OK).
- Ensures that the returned user data matches the deleted user's information.

### `test_increment_point`

The purpose of this test case is to test the `/user/{id}/increment` endpoint, which increments a user's score by one point. It follows these steps:

- Adds a test user to the database.
- Sends a PUT request to the `/user/{id}/increment` endpoint, specifying the user's ID.
- Validates that the response status code is 200 (OK).
- Checks that the returned user data reflects the incremented score.

### `test_decrement_point` and `test_decrement_point_zero`

These test cases cover the `/user/{id}/decrement` endpoint, which decreases a user's score by one point. They work as follows:

- For `test_decrement_point`, it adds a test user with a starting score greater than zero, decrements the score, and verifies the response.
- For `test_decrement_point_zero`, it adds a test user with a starting score of zero, attempts to decrement the score, and ensures a 400 (Bad Request) response is returned with an appropriate error message.

### `test_duplicate_user`

This test case verifies that attempting to create a user with the same name, address, and age as an existing user results in a 400 (Bad Request) response with an error message indicating the duplication.

### `test_invalid_inputs_when_creating_user`

This test case checks for invalid input scenarios when creating a new user. It includes cases such as an empty name, a negative age, and missing required fields, ensuring that the API returns a 400 (Bad Request) response with relevant error messages.

These test cases collectively validate the API's core functionality, including user creation, retrieval, deletion, score modification, error handling, and edge cases.

