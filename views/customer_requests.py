import sqlite3
import json
from models import Customer

CUSTOMERS = [
    {
        "id": 1,
        "name": "Dave",
    },
    {
        "id": 2,
        "name": "Marcella",
    },
]


def create_customer(customer):
    """_summary_

    Args:
        customer (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Get the id value of the last customer in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the customer dictionary
    customer["id"] = new_id

    # Add the customer dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer


def delete_customer(id):
    """_summary_

    Args:
        id (_type_): _description_
    """
    # Initial -1 value for customer index, in case one isn't found
    customer_index = -1

    # Iterate the CUSTOMERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Store the current index.
            customer_index = index

    # If the customer was found, use pop(int) to remove it from list
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)


def get_all_customers():
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
            a.id,
            a.name,
            a.address
        FROM customer a
        """
        )

        # Initialize an empty list to hold all customer representations
        customers = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an customer instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Customer class above.
            customer = Customer(row["id"], row["name"], row["address"])

            customers.append(customer.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(customers)


# Function with a single parameter
def get_single_customer(id):
    """_summary_

    Args:
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Variable to hold the found customer, if it exists
    requested_customer = None

    # Iterate the CUSTOMERS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for customer in CUSTOMERS:
        # Dictionaries in Python use [] notation to find a key
        # instead of the dot notation that JavaScript used.
        if customer["id"] == id:
            requested_customer = customer

    return requested_customer


def update_customer(id, new_customer):
    """_summary_

    Args:
        id (_type_): _description_
        new_customer (_type_): _description_
    """
    # Iterate the customerS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Update the value.
            CUSTOMERS[index] = new_customer
            break


def get_customers_by_email(email):
    """
    not sure about this one completely
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
            c.email,
            c.password,
            c.location_id
        from Customer c
        WHERE c.email = ?
        """,
            (email,),
        )

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(
                row["id"], row["name"], row["address"], row["email"], row["password"]
            )
            customers.append(customer.__dict__)

    return json.dumps(customers)
