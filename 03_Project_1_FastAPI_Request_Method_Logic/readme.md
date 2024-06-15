# CRUD Operations with FastAPI: A Detailed Guide
This guide provides a detailed walkthrough for implementing CRUD (Create, Read, Update, Delete) operations using FastAPI. CRUD operations are fundamental in API development, enabling basic data manipulation. In this project, you will read each of these operations in detail.

# Introduction
In this project, we will use FastAPI to implement CRUD operations. CRUD stands for Create, Read, Update, and Delete, which correspond to the HTTP methods POST, GET, PUT, and DELETE, respectively. These operations will be applied to a collection of books, serving as our dummy data for demonstration purposes. Let's start by importing the necessary libraries.

# Import Libraries
First, we need to import the FastAPI and Body classes from the fastapi library. The Body class will be used to define request bodies for our POST and PUT methods.

```from fastapi import Body, FastAPI```

# Initialize the FastAPI Application
Next, we initialize the FastAPI application. This creates an instance of the FastAPI class, which we will use to define our API routes.

```app = FastAPI()```
# Dummy Data
For this example, we'll create a list of dictionaries to represent our book collection. Each dictionary contains information about a book, such as its title, author, and category.

```
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]
```

# The read_all_books Endpoint
The read_all_books endpoint is designed to return the entire list of books in our collection. It is defined as an asynchronous function to leverage FastAPI's ability to handle asynchronous I/O operations, which can improve performance in applications with high concurrency.

```
@app.get("/books")
async def read_all_books():
    return BOOKS
```

- HTTP Method: GET
- Path: /books
- Description: This endpoint retrieves all the books in the BOOKS list.
- Response: It returns the entire BOOKS list in JSON format.
# Advantages of Asynchronous Endpoints
Using the async keyword in FastAPI endpoints allows for better handling of concurrent requests. This is particularly useful when dealing with I/O-bound operations, such as database queries or API calls, making the application more efficient under heavy load.
# Testing the Endpoint with Swagger UI
FastAPI includes an interactive API documentation interface powered by Swagger UI, which makes it easy to test and interact with the API endpoints.

# Accessing Swagger UI
Start the FastAPI Application:
Run your FastAPI application. By default, FastAPI will serve the application at http://127.0.0.1:8000.
```
uvicorn book:app --reload
```

# Open Swagger UI:

Navigate to http://127.0.0.1:8000/docs in your web browser. This URL opens the Swagger UI, where you can see all the available endpoints and interact with them.
![img_1.png](img_1.png)
# Using Swagger UI to Test the read_all_books Endpoint
- **Locate the GET /books Endpoint**:
In the Swagger UI, find the section for the GET /books endpoint. It should be listed among other endpoints defined in your FastAPI application.
![img.png](img.png)
- **Expand the Endpoint**:
Click on the GET /books endpoint to expand it. You will see a "Try it out" button and a description of the endpoint.

- **Test the Endpoint**:
Click the "Try it out" button. Then, click the "Execute" button. Swagger UI will send a request to the GET /books endpoint and display the response.

- **View the Response**:
After executing the request, you will see the response data. This includes the status code and the JSON response containing the list of books.
![img_2.png](img_2.png)

