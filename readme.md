# FastAPI Blog Repository

Welcome to my FastAPI blog repository! In this series, we will dive deep into FastAPI, a modern, fast (high-performance), web framework for building APIs with Python. This blog will guide you through various projects to master FastAPI and its numerous features.

## What is FastAPI?

FastAPI is a Python framework that simplifies the creation of APIs. With the increasing importance of APIs in the tech industry, big companies like OpenAI, Google, and Meta offer their services through APIs. This approach allows them to provide access to their services without exposing their internal code or systems. Everyone can use these services via APIs.

### API Management Market Growth

![alt text](<001_Images/Fast apiii.jpeg>)

According to recent reports, the API management market has been growing since 2022. As of 2024, it is valued at approximately 9 billion USD and is projected to reach 94 billion USD. This trend underscores the importance of learning API development, as it is a skill that will be highly beneficial in the near future. The rise of AI and the increasing popularity of APIs mean you can create your own APIs and even sell them in marketplaces.

## Blog Structure

In this blog, we will start with a brief overview of Python essentials necessary for FastAPI. Then, we'll proceed through several projects that will progressively teach you more advanced concepts.

### Project 1: Basic CRUD Operations

In our first project, we will learn how to:

- **GET**: Retrieve data
- **POST**: Create new data
- **PUT**: Update existing data
- **DELETE**: Remove data

### Project 2: Advanced Features

In the second project, we will cover:

- Classes
- Error Handling

### Project 3: Databases and Authentication

Our third project will focus on:

- Database integration
- ORM (Object-Relational Mapping)
- JWT (JSON Web Token) Authentication
- Routing

### Project 3.5: Database Migration

A smaller project where you will learn:

- Database migration techniques
- Data management strategies

### Project 4: Testing

The fourth project will teach:

- Unit Testing
- Integration Testing

### Project 5: Full Stack Development

In our final project, we will:

- Build a full-stack application
- Learn about Git and GitHub
- Deploy our application

## Next Steps

Excited? You should be! In the next step, we will cover the Python fundamentals necessary for working with FastAPI.


## Installing Python

Python is a crucial prerequisite for learning Fast API. To check if Python is already installed on your system, open a terminal and run the following command:

\`\`\`
python --version
\`\`\`

If Python is installed, this command will print the version number. If not, you'll need to install Python first. 

Follow this well-written guide from Real Python to install Python on your operating system (Windows, macOS, or Linux): [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/)

## Setting up an IDE

While Python files can be written in a simple text editor, an IDE (Integrated Development Environment) provides many useful features like code completion, debugging tools, and more. We recommend using VS Code, but you can use any IDE of your choice, such as PyCharm or Atom.

To install VS Code on Windows 11, follow this step-by-step guide: [How to Download VS Code in Windows 11](https://www.supportyourtech.com/tech/how-to-download-vs-code-in-windows-11-a-step-by-step-guide/)

For other operating systems or IDEs, refer to their official documentation.

## Running Python in the IDE

Once you have Python and an IDE installed, you can start writing and running Python code. In VS Code, you can create a new Python file by clicking on File > New File, and then saving the file with a `.py` extension (e.g., `hello.py`).

To run the Python file, you can use the built-in terminal in VS Code (Terminal > New Terminal) and navigate to the directory where your Python file is located. Then, run the following command:

\`\`\`
python hello.py
\`\`\`

This will execute your Python script.


# Python Variables

In Python, a variable is a named container that holds a value. Variables are used to store data that can be manipulated and referenced throughout a program. They are an essential concept in programming, as they allow you to store and manipulate data dynamically.

## Declaring Variables

In Python, you don't need to explicitly declare variables or specify their data types. You can simply assign a value to a variable using the assignment operator (`=`). Python automatically determines the data type based on the value assigned.

Here's an example:

```python
x = 5       # Integer
y = 3.14    # Float
name = "Alice"   # String
is_student = True  # Boolean


# Valid variable names
name = "John"
age = 25
_temp_variable = 10

# Invalid variable names
# 1var = 10  (starts with a digit)
# my-variable = 20  (contains a hyphen)
# my variable = 30  (contains a space)


x = 10
name = "Alice"
is_student = True


x = y = z = 0

name = "Bob"
print(name)  # Output: Bob

name = "Alice"
print(name)  # Output: Alice

"""
Variables
"""

first_name = "Muzzamil"
print(first_name)  # Output: Muzzamil

first_name = "Khalid"
print(first_name)  # Output: Khalid

# Arithmetic operations with variables
x = 10
y = 3
result = x + y
print(result)  # Output: 13

# Concatenating strings
greeting = "Hello"
name = "Alice"
message = greeting + ", " + name
print(message)  # Output: Hello, Alice
```

# Python Comments

This documentation provides an overview of different types of comments in Python and examples of how to use them effectively.

## Single-line Comments

Single-line comments in Python start with the `#` symbol. Everything following the `#` on that line is ignored by the Python interpreter.

Example:
```python
# This is a single-line comment explaining the next line of code
print("Hi Eric")
```
In the example above, the comment explains that the next line of code prints "Hi Eric" to the console.

# Multi-line Comments

## Consecutive Single-line Comments
When you need to write comments that span multiple lines, you can use consecutive single-line comments.
```python
# This is going over
# Multiple
# Lines
```
In the example above, each line of the comment starts with a # symbol.

# Multi-line Strings
Another way to add multi-line comments is to use multi-line strings. These are not technically comments but can be used as such. Multi-line strings are created using triple quotes (""" or '''). When not assigned to a variable, they are ignored by the interpreter.

```python
"""
This is going over
multiple 
lines
"""

'''
This is going over
multiple 
lines
'''
```

Both examples above demonstrate how to create multi-line comments using triple quotes. They are interchangeable, so you can use either double or single quotes.

# Usage Summary
- Single-line comments: Use # to start a comment. Ideal for short, one-line comments.
- Consecutive single-line comments: Use multiple # symbols at the beginning of each line for longer comments.
- Multi-line strings as comments: Use triple quotes (""" or ''') to create comments that span multiple lines. These are useful for longer explanations and documentation.

# Example Code with Comments
Here's a full example demonstrating the use of comments in Python code:
```python
# This script prints a greeting message to the console

# Define the greeting message
message = "Hi Eric"

# Print the greeting message
print(message)

# This is a comment spanning multiple lines
# explaining the next section of code. Each line
# starts with a hash symbol.

"""
The following block of code is currently commented out
and will not be executed. It prints 'Hello World'.
To enable it, remove the triple quotes.
"""
# print("Hello World")
```
This example shows a combination of single-line comments, multi-line comments using consecutive # symbols, and a multi-line string used as a comment block.