# Email Authentication with Flask

My attempt at building a email auth 

## Features

- **Sign Up**: Users can sign up with a username, email, and password. A confirmation email is sent upon registration.
- **Email Confirmation**: Users must confirm their email address via a link before accessing certain routes.
- **Login**: Authenticated users can log in if their email is confirmed.
- **Profile**: Users can view their profile information if logged in and email is confirmed.
- **Logout**: Users can log out to clear their session.

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Email Service**: Flask-Mail

## Installation

### Prerequisites

- Python 3.8+
- MongoDB

### Steps

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `app.config`:
   - Replace the placeholders with your credentials:
     ```python
     app.config['SECRET_KEY'] = 'your_secret_key'
     app.config['MONGO_URI'] = 'your_mongo_uri'
     app.config['MAIL_USERNAME'] = 'your_email@example.com'
     app.config['MAIL_PASSWORD'] = 'your_email_password'
     app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
     ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://127.0.0.1:5000/`.

## API Endpoints

### `POST /signup`
- **Description**: Registers a new user and sends a confirmation email.
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "status": "ok",
    "token": "confirmation_token"
  }
  ```

### `POST /login`
- **Description**: Logs in a user if the email is confirmed.
- **Request Body**:
  ```json
  {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "securepassword"
  }
  ```
- **Response**:
  ```json
  {
    "status": "logged in"
  }
  ```

### `GET /confirm/<token>`
- **Description**: Confirms the user's email address using the provided token.
- **Response**:
  ```json
  {
    "message": "You have confirmed your account. Thanks!"
  }
  ```

### `GET /profile`
- **Description**: Retrieves the user's profile if logged in and email is confirmed.
- **Response**:
  ```json
  {
    "username": "testuser",
    "email": "testuser@example.com",
    "is_confirmed": true
  }
  ```

### `GET /logout`
- **Description**: Logs out the user by clearing their session.
- **Response**:
  ```json
  {
    "message": "You have been logged out"
  }
  ```

## Notes

- Ensure that the `MAIL_USERNAME` and `MAIL_PASSWORD` are configured for a valid SMTP server.
- Use secure passwords and tokens for production environments.

## License

This project is open-source and available under the [MIT License](LICENSE).

