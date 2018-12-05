# Team Charizard NUber Project

For Mr. Diaz's CS 3398 Software Engineering class, we have created a RESTful API which will serve as the backend for our new, ingenius, never-before-thought-of business proposal...NUber

<hr>

### We implemented our backend with the Python3 programming language. This was our technology stack:
- The Flask Microframework
- Flask_RESTful
- Flask_SQLAlchemy
- Flask_Marshmallow
- Flask_Migrate
- Marshmallow_SQLAlchemy
- Google Maps API

<hr>

### How to run
1. Be sure to have Python3 and Pip installed on your computer
2. Install *virtualenv* with Pip <br>
```pip install virtualenv```
3. *cd* into the project folder and create a virtual environment <br>
```virtualenv -p python3 venv```
4. Activate virtual environment <br>
```source venv/bin/activate```
5. Install all dependencies listed in *requirements.txt* <br>
```pip install -r requirements.txt```
6. Create a binary executable of *create_database.sh* <br>
```chmod 755 create_database.sh```
7. Run *create_database.sh* to make a new instance of your database <br>
```./create_database.sh```
8. RUN DAT BOI:sunglasses:
```python main.py```

### When you spin up the server, you should see output like the following:
```
* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: Do not use the development server in a production environment.
  Use a production WSGI server instead.
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 295-600-791
```
<hr>

### How to Use Extra Features

- Groups :: Riders have an attribute field named 'groupHost', by setting 
            your 'groupHost' to another rider's 'name' you will be added to their group. When in 
            a group only the group host can select a driver.
- RideCost :: Riders have an attribute called 'outstandingBalance', this holds how much 
              money riders owe their driver, this cost is divided by the number of people in the group.
- Radius Search :: Drivers have attribute fields 'avaiable', 'lat', and 'long' which describe their availability and location. These                        fields allow for riders to search for potential drivers based on their availability and relative distance from the                      rider
- Charge Riders :: Drivers obviously wish to be paid. Once a Rider has reached their destination, calculations are performed based on                      how far the rider was transported from their original location, and a cost is assigned at a fixed rate per mile.
- Rating System :: Each Driver posseses a 'rating' attribute, which holds an aggregate average of their ratings, given to them by                          previous Riders. This Rating System is used to assess the overall perceived quality of the Driver.

<hr>

### Routes
Below are the available list of routes and their functionalities

#### Admin
- ```/admin```
  - GET: Returns a list of all admins in the database
    - Arguments: None
  - POST: Create a new admin
    - Body:
      - id: integer
      - name: string
  - PUT: Updates an admin
    - Arguments:
      - id: integer
    - Body:
      - name: string
  - DELETE: Deletes an admin from the database
    - Arguments:
      - id: integer
      
- ```/admin/driver```
  - GET: Returns a list of all drivers in the database
    - Arguments: None
  - POST: Creates a new driver
    - Body: 
      - id: integer
      - name: string
      - lat: float
      - long: float
      - available: boolean
      - amountMoney: float
      - selected_rider: integer
  - PUT: Updates a driver
    - Arguments:
      - id: integer
    - Body:
      - name: string
      - lat: float
      - long: float
      - available: boolean
      - amountMoney: float
      - selected_rider: integer
  - DELETE: Deletes a driver from the database
    - Arguments:
      - id: integer
      
- ```/admin/rider```
  - GET: Returns a list of all riders in the database
    - Arguments: None
  - POST: Creates a new rider
    - Body:
      - id: integer
      - name: string
      - lat: float
      - long: float
      - outstandingBalance: float
      - groupHost: string
  - PUT: Updates a rider
    - Arguments:
      - id: integer
    - Body:
      - id: integer
      - name: string
      - lat: float
      - long: float
      - outstandingBalance: float
      - groupHost: string
  - DELETE: Deletes a rider from the database
    - Arguments:
      - id: integer

#### Driver
- ```/driver/update_position```
  - PUT: Updates driver Position
    - Arguments:
      - id: integer
    - Body:
      - lat: float
      - long: float
  
- ```/driver/update_availability```
  - PUT: Updates driver availability
    - Arguments:
      - id: integer
    - Body:
      - available: boolean
  
- ```/driver/get_rider_destination```
  - GET: Returns rider's destination
    - Arguments:
      - driver_id: int

- ```/driver/get_rider_location```
  - GET: Returns rider's location
    - Arguments:
      - driver_id: int

- ```/driver/get_rider_charge```
  - GET: Returns rider's chare
    - Arguments:
      - driver_id: int

#### Rider
- ```/rider/set_destination```
  - PUT: Updates rider's destination
    - Arguments:
      - id: int
    - Body:
      - destination: string
  
- ```/rider/update_position```
  - PUT: Updates rider's position
    - Arguments:
      - id: integer
    - Body:
      - lat: float
      - long: float

- ```/rider/select_driver```
  - PUT: Selects an available driver for the rider. NOTE: If the rider is in a group and is not the host, they cannot do this
    - Body:
      - driver_id: int
      - rider_id: int

- ```/rider/get_drivers```
  - GET: Returns driver's in a given radius
    - Arguments:
      - id: int
      - radius: int 

- ```/rider/get_driver_location```
  - GET: Returns driver's location
    - Arguments:
      - rider_id: int

- ```/rider/get_driver_average```
  - GET: Returns driver's average rating
    - Arguments:
      - driver_id: int
      
- ```/rider/rate_driver```
  - POST: Adds a rating to the rider's driver
    - Body:
      - driver_id: int
      - rating: int
