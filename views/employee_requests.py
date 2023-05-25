import sqlite3
import json
from models import Employee, Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Susan",
    },
    {
        "id": 2,
        "name": "Bob",
    },
]


def create_employee(employee):
    """_summary_

    Args:
        employee (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee


def delete_employee(id):
    """_summary_

    Args:
        id (_type_): _description_
    """
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)


def get_all_employees():
    """
    whats happening here?
    """
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.location_id,
            e.address,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id

        """
        )

        # Initialize an empty list to hold all employees representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employees instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # employees class above.
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"]
            )

            location = Location(row['id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


# Function with a single parameter
def get_single_employee(id):
    """_summary_

    Args:
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Variable to hold the found employee, if it exists
    requested_employee = None

    # Iterate the EMPLOYEES list above. Very similar to the
    # for..of loops you used in JavaScript.
    for employee in EMPLOYEES:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if employee["id"] == id:
            requested_employee = employee

    return requested_employee


def update_employee(id, new_employee):
    """_summary_

    Args:
        id (_type_): _description_
        new_employee (_type_): _description_
    """
    # Iterate the employeeS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break


def get_employees_by_location(location):
    """
    whats happening here?
    """

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        select
            c.id,
            c.name,
            c.address,
            c.location_id
        from Employee c
        WHERE c.location_id = ?
        """,
            (location,),
        )

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"]
            )
            employees.append(employee.__dict__)

    return json.dumps(employees)
