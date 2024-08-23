# Qur'an Academy Backend

This repository contains the backend code for the Qur'an Academy Phase 1 project, designed to facilitate online Quranic education. It offers functionalities for user management, content organization, assessment creation and management, and role-based access control.

## Setup Instructions

Follow these steps to set up the project on your local machine:

## Usage

1. **Prerequisites:** Ensure you have Python 3 and a virtual environment manager like `venv` installed on your system.

2. **Run Setup File:**

   Execute the setup file by running the following command:

   ```bash
   ./setup
   ```

3. **Activate QAvenv:**

   Activate the QAvenv virtual environment by running the appropriate command based on your operating system:

   - Linux/macOS:

     ```bash
     source QAvenv/bin/activate
     ```

   - Windows:

     ```bash
     QAvenv\Scripts\activate.bat
     ```

   After activating the virtual environment, you can proceed with using the Qur'an Academy Phase 1 Backend.

4. **Database Setup (MySQL):**

      The MySQL database connection details are configured in the `config.py` file. These details typically include the host, port, username, password, and database name. Make sure you have MySQL installed and running on your system.

      ```python
      # config.py

      MYSQL_HOST = 'localhost'
      MYSQL_PORT = 3306
      MYSQL_USER = 'your_username'
      MYSQL_PASSWORD = 'your_password'
      MYSQL_DATABASE = 'your_database_name'
      ```

      Update the values in the `config.py` file with your MySQL database connection details.

5. **Create Database Schema (if necessary):**

   ```bash
   python3 run.py create-db
   ```

6. **Run the Server:**

   ```bash
   python3 run.py
   ```

   The backend server will typically start on `http://localhost:5000` by default. You can access the API using REST client tools like Postman or curl.

## Usage Guidelines

The Qur'an Academy API provides functionalities for managing users, content, assessments, and administrative tasks. Different parts of the API require authentication, while some public endpoints might be accessible without authorization.

**Authentication:**

To authenticate and access protected endpoints, follow these steps:

1. **Register a User:** Use the `/api/v1/auth/register` endpoint with a POST request containing user details like firstName, lastName, age, country, username, email, password, and role (if role not set it will be student by default). Refer to the API documentation for detailed request and response structures.

2. **Login:** Use the `/api/v1/auth/login` endpoint with a POST request containing username or email and password. A successful login will return a JWT token that needs to be included in subsequent authorized API requests. Include the token in the `Authorization` header using the Bearer token format (`Authorization: Bearer <your_token>`).

## API Endpoints

For a comprehensive list of endpoints, their functionalities, expected request and response formats, and authentication requirements, refer to the separate [API documentation](https://documenter.getpostman.com/view/37271893/2sAXjDdac5).

### API Documentation

The API documentation provides detailed information on all available endpoints, including:

- **User Management Endpoints:** Register, login, and manage users.
- **Content Management Endpoints:** Create, update, and organize Quranic content.
- **Assessment Endpoints:** Create, administer, and analyze assessments.
- **Role-Based Access Control:** Details on the access control mechanisms used to secure the API.

Each endpoint is documented with:

- **Endpoint URL:** The specific URL for the API request.
- **Method:** The HTTP method to be used (GET, POST, PUT, DELETE).
- **Headers:** Any necessary headers, including authentication tokens.
- **Request Body:** Structure of the data that needs to be sent with the request.
- **Response Body:** Example responses, including success and error cases.
- **Authentication Requirements:** Details on which endpoints require authentication and the type of token needed.

Explore the full API documentation [here](https://documenter.getpostman.com/view/37271893/2sAXjDdac5) to understand how to interact with the Qur'an Academy Backend effectively.

## Project Architecture Overview

The Qur'an Academy backend follows a modular MVC (Model-View-Controller) design pattern, with clear separation of concerns:

- **Models (`backend/app/models`)**: Define database entities representing user, content, assessment, and related data.
- **Services (`backend/app/services`)**: Handle business logic and data manipulation for users, content, and assessments.
- **API Routes (`backend/app/api/v1`)**: Define endpoints for user interaction with the API, delegating logic to services. Employ route-based authentication using decorators/middleware to protect sensitive resources.
- **Middleware (`backend/app/middleware`)**: Implement authentication and role-based access control (RBAC) to restrict access based on user roles.
- **Error Handling (`backend/app/error_handler`)**: Handle and respond to API errors gracefully, providing informative error messages.
- **Tests (`backend/tests`)**: Unit and integration tests ensure code quality and functionality.

**Role-Based Access Control (RBAC):**

RBAC restricts API access based on user roles. Users can be assigned roles (e.g., student, teacher, admin) with different access levels. Authorized users are granted access to specific resources, while unauthorized requests result in appropriate error responses. This ensures data integrity and enforces a secure, consistent user experience.

## Demonstration

To explore the API functionalities, consider using tools like Postman or curl. You can experiment with API requests and responses, test authentication, manage users and content, and create assessments.

## Development Process

The project was developed using Python 3 (3.x recommended), leveraging Flask for web framework functionality. Unit and integration tests were written to ensure code quality and API behavior. The use of a virtual environment helps manage dependencies and isolate project-specific packages.

The project follows a modular design pattern, separating concerns into models, services, routes, middleware, and error handling components. This structure enhances code readability, maintainability, and scalability. The API documentation provides detailed information on endpoints, request/response formats, and authentication requirements.

## Key Achievements

- **Robust User Management:** Users can register, login, and have roles assigned.
- **Secure Authentication:** JWT tokens are used for authentication, ensuring data security.
- **Flexible Content Management:** Easily create, update, and organize Quranic content.
- **Comprehensive Assessment System:** Create, administer, and analyze assessments to track student progress.
- **Role-Based Access Control:** Enforce granular access control based on user roles.
- **Scalability:** Designed to handle a growing user base and increasing demands.
- **API-Driven Architecture:** Provides a flexible and extensible API for integration with other applications.

**Additional Notes:**

- For more detailed information on API endpoints and usage, refer to the separate API documentation.
- Consider including a section on future plans or enhancements for the project.
- If applicable, provide instructions for deploying the application to a production environment.
