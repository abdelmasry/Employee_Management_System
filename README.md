<h1 style="color: #93C572" align=center>Employee Management System</h1>
 


# <p style="color: #00FFFF">Overview:</p>


* In this task, you are required to develop an Employee Management System that encompasses various features for
managing companies, departments, and employees. The system will allow users to create, read, update, and delete
(CRUD) records for each of these entities. 

* Additionally, there will be a workflow for handling the onboarding process
of new employees and implementing role-based access control to ensure secure data handling. The system should adhere to the requirements specified below to ensure all features are implemented correctly.

* While there are mandatory requirements that must be completed, there are also bonus requirements. The bonus
requirements are optional and should only be implemented if you have extra time and it does not compromise the quality of the mandatory requirements. Achieving the bonus requirements is not essential but will be considered a plus.

* This task is designed to evaluate your technical skills, problem-solving abilities, and attention to detail. It also assesses your capability to work under stress and tight schedules, reflecting real-world scenarios where meeting deadlines is
crucial.
***


# <p style="color: #00FFFF "> Comprehensive Documentation and Approach:</p>

(Implementation details and any considerations made during the development process.)

<p style="color: #55A78B"> The Backend has been implemented using Django framework. Following the MVT architecure. Serializers were used to make the datbase models utilized as JSON objects for the API Endpoints. Signals(event-triggers) were used to handle edge cases of models relationships. Sqlite Database was used to facilitate the development process.</p>

***



# <p style="color: #00FFFF ">Prerequisites, installation steps, and additional information required for a smooth evaluation:<p>
* 1- git clone https://github.com/abdelmasry/Employee_Management_System
* 2- Make sure that you have Python: 3.10.0
* 3- cd Employee_Management_System
* 4- source /path/to/your/virtual/env/bin/activate
* 5- pip install -r requirements.txt
* 6- python manage.py runserver or gunicorn Employee_Management_System.wsgi:application 
* 7- start using the API Endpoints


***
# <p style="color: #00FFFF ">Check List:</p>
- [x] Backend
    - [x] Models
    - [x] Validations & Business Logic
    - [ ] Workflow (Bonus)
    - [x] Security & Permissions
    - [x] APIs
    - [ ] Testing(Bonus)
    - [ ] Logging(Bonus)

- [ ] Frontend

- [ ] API Integration
***
# <p style="color: #00FFFF ">The security measures implemented, especially concerning role-based access control and data protection:</p>
* Create SuperUser/ADMIN: python manage.py createsuperuser
* THIS IS ALREADY CREATED:
    * SuperUser_Username: BrainWise
    * SuperUser_Email: brainwise@mail.com
    * SuperUser_Password: Brainwise162023
    * Token: ccc50594f0b5656baaeb1bccd10256db51bbbd0f
* Shortcut for generating tokens: python manage.py drf_create_token <Username>
* Admins:
    * Create, View, Edit, Delete:  Users, Companies, Departments, Employees
* Managers: 
    * Create, View, Edit, Delete:  Companies, Departments, Employees
* Employee:
    View: Employees

#### <p style="color: yellow">Scenario:</p>

<p style="color: #55A78B">User with role=ADMIN with a generated token (can be otained through making a POST request with username and password in json body to the endpoint: localhost:port/main/token) creates a user through making a POST request with a JSON {new_username, new_email, role, new_password}  to the enpoint: localhost:port/main/user/ then the user sends a POST reques the token endpoint to get a token and then start to utilize the enpoints by providing the token in the Headers of the request as the Authorization: Token <token>.</p>




***
# <p style="color: #00FFFF ">API Documentation:</p>


## Endpoints

### User Accounts

#### Retrieve a Single User or List All Users

- **URL**: `/user/` or `/user/<int:id>/`
- **Method**: GET
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Retrieves a single user account if `id` is provided, otherwise retrieves a list of all user accounts.
- **Parameters**:
  - `id` (optional): The ID of the user to retrieve.
- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 404 Not Found

#### Create a New User Account

- **URL**: `/user/`
- **Method**: POST
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Creates a new user account.
- **Parameters**:
  - `username` (str): The username of the new user.
  - `password` (str): The password of the new user.
  - `email` (str): The email of the new user.
- **Response**:
  - **Success**: HTTP 201 Created
  - **Failure**: HTTP 400 Bad Request

#### Delete a User Account

- **URL**: `/user/<int:id>/`
- **Method**: DELETE
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Deletes the specified user account.
- **Parameters**:
  - `id` (int): The ID of the user to delete.
- **Response**:
  - **Success**: HTTP 204 No Content
  - **Failure**: HTTP 404 Not Found

### Company

#### Retrieve a Single Company or List All Companies

- **URL**: `/company/` or `/company/<int:pk>/`
- **Method**: GET
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Retrieves a single company if `pk` is provided, otherwise retrieves a list of all companies.
- **Parameters**:
  - `pk` (optional): The primary key of the company to retrieve.
- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 404 Not Found

#### Create a New Company

- **URL**: `/company/`
- **Method**: POST
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Creates a new company.
- **Parameters**:
  - `name` (str): The name of the company.
  - `address` (str): The address of the company.
- **Response**:
  - **Success**: HTTP 201 Created
  - **Failure**: HTTP 400 Bad Request

#### Update a Company

- **URL**: `/company/<int:pk>/`
- **Method**: PUT
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Updates the specified company.
- **Parameters**:
  - `pk` (int): The primary key of the company to update.
  - `name` (str): The new name of the company.
  - `address` (str): The new address of the company.
- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 400 Bad Request

#### Delete a Company

- **URL**: `/company/<int:pk>/`
- **Method**: DELETE
- **Permissions**: `IsAuthenticated`, `IsAdminUser`
- **Description**: Deletes the specified company.
- **Parameters**:
  - `pk` (int): The primary key of the company to delete.
- **Response**:
  - **Success**: HTTP 204 No Content
  - **Failure**: HTTP 404 Not Found

### Department

#### Retrieve a Single Department or List All Departments

- **URL**: `/department/` or `/department/<int:pk>/`
- **Method**: GET
- **Permissions**: `IsManagerUser` or `IsAdminUser`
- **Description**: Retrieves a single department if `pk` is provided, otherwise retrieves a list of all departments.
- **Parameters**:
  - `pk` (optional): The primary key of the department to retrieve.
- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 404 Not Found

#### Create a New Department

- **URL**: `/department/`
- **Method**: POST
- **Permissions**: `IsManagerUser` or `IsAdminUser`
- **Description**: Creates a new department.
- **Parameters**:
  - `name` (str): The name of the department.
  - `company` (int): The ID of the company to which the department belongs.
- **Response**:
  - **Success**: HTTP 201 Created
  - **Failure**: HTTP 400 Bad Request

#### Update a Department

- **URL**: `/department/<int:pk>/`
- **Method**: PUT
- **Permissions**: `IsManagerUser` or `IsAdminUser`
- **Description**: Updates the specified department.
- **Parameters**:
  - `pk` (int): The primary key of the department to update.
  - `name` (str): The new name of the department.
  - `company` (int): The new ID of the company to which the department belongs.
- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 400 Bad Request

#### Delete a Department

- **URL**: `/department/<int:pk>/`
- **Method**: DELETE
- **Permissions**: `IsManagerUser` or `IsAdminUser`
- **Description**: Deletes the specified department.
- **Parameters**:
  - `pk` (int): The primary key of the department to delete.
- **Response**:
  - **Success**: HTTP 204 No Content
  - **Failure**: HTTP 404 Not Found

### Employee

#### Retrieve a Single Employee or List All Employees

- **URL**: `/employee/` or `/employee/<int:pk>/`
- **Method**: GET
- **Permissions**: `IsAuthenticated`, `IsEmployeeUser` (for viewing), `IsAdminUser` or `IsManagerUser` (for other methods)
- **Description**: Retrieves a single employee if `pk` is provided, otherwise retrieves a list of all employees.
- **Parameters**:
  - `pk` (optional): The primary key of the employee to retrieve.
- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 404 Not Found

#### Create a New Employee

- **URL**: `/employee/`
- **Method**: POST
- **Permissions**: `IsAuthenticated`, `IsAdminUser` or `IsManagerUser`
- **Description**: Creates a new employee.
- **Parameters**:
  - `name` (str): The name of the employee.
  - `department` (int): The ID of the department to which the employee belongs.
  - `designation` (str): The position of the employee.
- **Response**:
  - **Success**: HTTP 201 Created
  - **Failure**: HTTP 400 Bad Request

#### Update an Employee

- **URL**: `/employee/<int:pk>/`
- **Method**: PUT
- **Permissions**: `IsAuthenticated`, `IsAdminUser` or `IsManagerUser`
- **Description**: Updates the specified employee.
- **Parameters**:
  - `pk` (int): The primary key of the employee to update.
  - `name` (str): The new name of the employee.
  - `department` (int): The new ID of the department to which the employee belongs.
  - `designation` (str): The new position of the employee.

- **Response**:
  - **Success**: HTTP 200 OK
  - **Failure**: HTTP 400 Bad Request

#### Delete an Employee

- **URL**: `/employee/<int:pk>/`
- **Method**: DELETE
- **Permissions**: `IsAuthenticated`, `IsAdminUser` or `IsManagerUser`
- **Description**: Deletes the specified employee.
- **Parameters**:
  - `pk` (int): The primary key of the employee to delete.
- **Response**:
  - **Success**: HTTP 204 No Content
  - **Failure**: HTTP 404 Not Found


