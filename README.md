Django REST API for Message Handling


This Django project provides a RESTful API for handling messages between users. Users can send messages to each other, view their messages, mark messages as read, and delete messages. The API also includes user authentication and authorization mechanisms.

Features
Write Message: Users can send messages to other users.
Get All Messages: Users can retrieve all messages sent to them.
Get Unread Messages: Users can retrieve only their unread messages.
Read Message: Users can view a specific message and mark it as read.
Delete Message: Users can delete messages they sent or received.
User Authentication: API endpoints are protected with JWT authentication.
Admin User Creation: Admin users can create new users.

Installation

Clone the Repository and enter the project --> cd message_api_project

Install dependencies: 
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Access the API at http://localhost:8000/.

Usage
Authentication: To access protected endpoints, include an Authorization header with a valid JWT token.
Endpoints: Refer to the API documentation or Postman collection for available endpoints and their usage.
