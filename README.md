# django-social-network-api

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Notes](#notes)
  - [Optimizations Applied to ORM Queries](#optimizations-applied-to-orm-queries)
  - [Challenges Faced](#challenges-faced)

## Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:bonillagabo/django-social-network-api.git

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

2. Apply Django migrations:
    ```bash
    py manage.py migrate

3. Start the application:
    ```bash
    py manage.py runserver

4. Run unit tests:
    ```bash
    py manage.py test

5. Postman Collection: 
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

## Notes

### Optimizations Applied to ORM Queries

1. **Pagination**: Implementing pagination improves performance by limiting the number of results returned in a single query. This prevents the application from loading large volumes of data at once, which could lead to excessive memory usage and slower response times. Pagination also enhances user experience by displaying data in manageable chunks.

2. **`select_related()` and `prefetch_related()`**: These methods were used to optimize database access and reduce the number of queries.
   - **`select_related()`**: This method is used for single-valued relationships (such as ForeignKey or OneToOne) and performs a SQL join to retrieve related objects in a single query, minimizing the need for additional database hits.
   - **`prefetch_related()`**: This method is used for multi-valued relationships (such as ManyToMany or reverse ForeignKey) and performs separate queries for related data, combining the results in Python. This approach helps avoid the "N+1 query problem," where multiple queries are issued for related objects.

3. **`get_object_or_404()`**: This method simplifies error handling by returning a 404 response if the object is not found, rather than causing an unhandled exception. This approach contributes to cleaner and more reliable error management in views.

### Challenges Faced

Applying `select_related()` and `prefetch_related()` effectively required careful consideration of data relationships. Incorrect usage could lead to inefficient queries or excessive data retrieval. Balancing the trade-offs between query complexity and performance was crucial.
