
HTTP Client Application for UtmShop

Description
This application implements an HTTP client that interacts with the UtmShop online store API.

Server Components
Install the .NET SDK and runtime:
    brew install --cask dotnet-sdk

Install the .NET 5.0 Runtime from the official Microsoft website.

Starting the Server
To start the API server, navigate to the project directory and run:
    dotnet clean  
    dotnet restore  
    dotnet build  
    dotnet run

Verify that the server is running by accessing the Swagger UI:
    https://localhost:5001/swagger/index.html

Client Configuration
1. Install the required Python libraries:
       pip install requests urllib3
2. Save the client_magazin.py file in your desired directory.

Implemented Features
The client implements all the requirements specified in the lab:

1. List Categories – Displays all available categories  
2. Category Details – Shows complete information about a specific category  
3. Create New Category – Adds a new category with a title and description  
4. Delete a Category – Removes an existing category from the system  
5. Edit Category Title – Updates the name of a category  
6. List Products in a Category – Shows all products under a specific category  
7. Add New Product – Creates a new product with name, description, price, and stock

Usage
Run the client application:
    python client_magazin.py

https://github.com/zaferakbiyik/pr