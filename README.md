# django-social-network-api

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/bonillagabo/django-social-network-api.git

2. Navigate to the cloned repository:
    ```bash
    cd django-social-network-api

3. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4. Install the project dependencies:

    ```bash
    pip install -r requirements.txt

5. Create the .env file from .env.example and add your Django secret key:

    ```bash
    cp .env.example .env

    Then, edit the .env file to add a secret key (required by Django):
    SECRET_KEY=your_secret_key_here

## Usage

1. Navigate to the root directory of the project:
    ```bash
    cd social_network

2. Start the application:
    ```bash
    py manage.py runserver

3. Run unit tests:
    ```bash
    py manage.py test

4. Postman Collection: 
In the root directory of the project, you can find a Postman collection file. This collection includes all the endpoints of the application along with some example responses. You can import this collection into Postman to explore and test the API. The Postman collection file is named djando_social_network.postman_collection.json. To import it:
    - Open Postman.
    - Click on the "Import" button.
    - Choose the file djando_social_network.postman_collection.json from the root directory.

## Authentication

All endpoints require a Bearer token for authentication in the header. You can obtain this token by using the `api/token/` endpoint. Send a POST request with the following body:

    {
        "username": "user",
        "password": "pass"
    }

Replace "user" and "pass" with the credentials of a registered user. You can register a new user using the `api/users/` endpoint, which does not require a token in the header. This endpoint is used only to facilitate obtaining a valid token.

## API Endpoints

- [Obtain Token](#obtain-token)
- [Create User](#create-user)
- [Get All Users](#get-all-users)
- [Get One User by ID](#get-one-user-by-id)
- [Follow a User](#follow-a-user)
- [Create a Post](#create-a-post)
- [Get All Posts](#get-all-posts)
- [Get One Post by ID](#get-one-post-by-id)
- [Create a Post Comment](#create-a-post-comment)
- [Get All Post Comments](#get-all-post-comments)

### Obtain Token
- **Endpoint:** `api/token/`
- **Method:** POST
- **Description:** Obtains a Bearer token for authentication.
- **Request Body:**
    ```json
    {
        "username": "user",
        "password": "pass"
    }

### Create User
- **Endpoint:** `api/users/`
- **Method:** POST
- **Description:** : Create a new user.
- **Request Body:** 
    ```json
    {
        "username": "user",
        "email": "user@gmail.com",
        "name": "User",
        "lastname": "Example",
        "password": "password123"
    }

### Get All Users
- **Endpoint:** `api/users/`
- **Method:** GET
- **Description:** Retrieve a list of all users.
- **Query Parameters:**
  - `page_number` (optional): The page number to retrieve.
  - `page_size` (optional): The number of users per page.
- **Request Header:** `Authorization: Bearer your_token_here`

### Get One User by ID
- **Endpoint:** `api/users/{id}/`
- **Method:** GET
- **Description:** : Retrieve details of a specific user. Including number of total posts, number of total comments, followers and following.
- **Path Parameter:**
  - `id` (required): The unique identifier of the user to retrieve.
- **Request Header:** `Authorization: Bearer your_token_here`

### Follow a User
- **Endpoint:** `api/users/{follower_id}/follow/{followee_id}/`
- **Method:** POST
- **Description:** Sets the user with `follower_id` as a follower of the user with `followee_id`.
- **Path Parameters:**
  - `follower_id` (required): The ID of the user who is following another user.
  - `followee_id` (required): The ID of the user being followed.
- **Request Header:** `Authorization: Bearer your_token_here`

### Create a Post
- **Endpoint:** `api/posts/`
- **Method:** POST
- **Description:** Create a new post.
- **Request Body:** 
    ```json
    {
        "author": 1,
        "content": "Text"
    }
- **Request Header:** `Authorization: Bearer your_token_here`

### Get All Posts
- **Endpoint:** `api/posts/`
- **Method:** GET
- **Description:** Retrieve a list of all posts ordered from newest to oldest from all users,
with pagination and filters.
- **Query Parameters:**
  - `page_number` (optional): The page number to retrieve.
  - `page_size` (optional): The number of posts per page.
  - `author_id` (optional): Filter posts by a specific author's ID.
  - `from_date` (optional): Filter posts created from this date onwards (format: YYYY-MM-DD).
  - `to_date` (optional): Filter posts created up to this date (format: YYYY-MM-DD).
- **Request Header:** `Authorization: Bearer your_token_here`

### Get One Post by ID
- **Endpoint:** `api/posts/{id}/`
- **Method:** GET
- **Description:**  Retrieve details of a specific post with it's last three comments
included and the information of it's creator.
- **Path Parameter:**
  - `id` (required): The ID of the post to retrieve.
- **Request Header:** `Authorization: Bearer your_token_here`

### Create a Post Comment
- **Endpoint:** `api/posts/{id}/comments/`
- **Method:** POST
- **Description:** Add a new comment to a post.
- **Path Parameter:**
  - `id` (required): The ID of the post to comment on.
- **Request Body:** 
    ```json
    {
        "author": 1,
        "content": "comentario"
    }
- **Request Header:** `Authorization: Bearer your_token_here`

### Get All Post Comments
- **Endpoint:** `api/posts/{id}/comments/`
- **Method:** GET
- **Description:** Retrieve all comments for a specific post.
- **Path Parameter:**
  - `id` (required): The ID of the post for which to retrieve comments.
- **Request Header:** `Authorization: Bearer your_token_here`