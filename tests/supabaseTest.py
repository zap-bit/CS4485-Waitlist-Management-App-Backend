import os
from supabase import create_client, Client
from dotenv import load_dotenv
import hashlib
import time

# Load environment variables from .env file
load_dotenv()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase URL or API Key in environment variables.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user_account(name, email, pswd, phone):
    hashed_password = hash_password(pswd)
    data = {
        "name": name,
        "account_type": "USER",
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "business_name": None  # USER accounts do not have a business name
    }
    response = supabase.table("account").insert(data).execute()
    return response

def create_bus_account(name, email, pswd, b_name, phone):
    hashed_password = hash_password(pswd)
    data = {
        "name": name,
        "account_type": "BUSINESS",
        "email": email,
        "password": hashed_password,
        "phone": phone,
        "business_name": b_name  # BUSINESS accounts require a business name
    }
    response = supabase.table("account").insert(data).execute()
    return response

# KYLE TODO: EDIT THIS BASED ON THE CAP_TYPE BC WE NEED TO HAVE QUEUES CREATED WITH IT
def create_capacity_event(account_uuid, name, location, cap_type, queue_capacity, est_wait):
    """
    Creates a CAPACITY type event in the EVENTS table on Supabase.
    """
    data = {
        "account_uuid": account_uuid,
        "name": name,
        "event_type": "CAPACITY",
        "location": location,
        "cap_type": cap_type,
        "queue_capacity": queue_capacity,
        "est_wait": est_wait,
        "archived": False  # Default value for archived
    }
    response = supabase.table("events").insert(data).execute()
    return response

# KYLE TODO: EDIT THIS BASEAD ON NUM_TABLES SO THAT TABLES ARE CREATED WITH AVG_SIZE
def create_table(event_uuid, table_name, table_capacity):
    """
    Creates a table entry in the Supabase database.

    Parameters:
        event_uuid (str): The UUID of the event the table belongs to.
        table_name (str): The name of the table.
        size (int): The size of the table.

    Returns:
        dict: The response from the Supabase database.
    """
    data = {
        "event_uuid": event_uuid,
        "name": table_name,
        "table_capacity": table_capacity
    }
    response = supabase.table("event_table").insert(data).execute()
    return response

def create_table_event(account_uuid, name, num_tables, avg_size, reservation_duration, no_show_policy):
    """
    Creates a TABLE type event in the EVENTS table on Supabase and generates table entries.

    Parameters:
        account_uuid (str): The UUID of the account.
        name (str): The name of the event.
        num_tables (int): The number of tables to create.
        avg_size (int): The average size of each table.
        reservation_duration (int): The duration of reservations for the tables.
        no_show_policy (str): The policy for no-shows.

    Returns:
        dict: The response from the Supabase database for the event creation.
    """
    data = {
        "account_uuid": account_uuid,
        "name": name,
        "event_type": "TABLE",
        "num_tables": num_tables,
        "avg_size": avg_size,
        "reservation_duration": reservation_duration,
        "no_show_policy": no_show_policy,
        "archived": False  # Default value for archived
    }
    event_response = supabase.table("events").insert(data).execute()

    # Ensure the response contains data
    if not event_response.data or not isinstance(event_response.data, list) or len(event_response.data) == 0:
        raise ValueError("Failed to create event or retrieve event UUID.")

    # Extract the event UUID
    event_uuid = event_response.data[0].get("uuid")
    if not event_uuid:
        raise ValueError("Event UUID not found in the response.")

    # Create table entries
    for i in range(1, num_tables + 1):
        create_table(event_uuid, f"Table{i}", avg_size)

    return event_response

def create_party(account_uuid, event_uuid, party_size, special_req=None):
    """
    Creates a party entry in the Supabase database and generates attendance entries for the party.

    Parameters:
        account_uuid (str): The UUID of the account.
        event_uuid (str): The UUID of the event.
        party_size (int): The size of the party.
        special_req (str, optional): Any special requests for the party.

    Returns:
        dict: The response from the Supabase database for the party creation.
    """
    # Fetch the name associated with the account_uuid
    account_response = supabase.table("account").select("name").eq("uuid", account_uuid).execute()
    if not account_response.data or len(account_response.data) == 0:
        raise ValueError("Account not found for the given UUID.")

    party_leader_name = account_response.data[0]["name"]

    data = {
        "account_uuid": account_uuid,
        "event_uuid": event_uuid,
        "party_size": party_size,
        "special_req": special_req
    }
    party_response = supabase.table("party").insert(data).execute()

    # Create attendance entries
    create_attendance(True, account_uuid, event_uuid, party_leader_name, False)  # Use the fetched name for the party leader
    for i in range(1, party_size):
        create_attendance(False, account_uuid, event_uuid, f"Guest{i}", False)

    return party_response

def create_attendance(party_leader, account_uuid, event_uuid, name, present=False):
    """
    Creates an attendance entry in the Supabase database.
    """
    data = {
        "party_leader": party_leader,
        "account_uuid": account_uuid,
        "event_uuid": event_uuid,
        "name": name,
        "present": present
    }
    response = supabase.table("attendance").insert(data).execute()
    return response

def assign_user_to_table(table_uuid, account_uuid):
    """
    Assigns a user to a table by updating the table entry in the Supabase database.

    Parameters:
        table_uuid (str): The UUID of the table to assign the user to.
        user_uuid (str): The UUID of the user to assign to the table.

    Returns:
        dict: The response from the Supabase database.
    """
    data = {
        "account_uuid": account_uuid
    }
    response = supabase.table("event_table").update(data).eq("uuid", table_uuid).execute()
    return response

# Example usage
if __name__ == "__main__":
    
    print("testing backend/databse connection -Kyle")

    """
    for testing purposes:
    USER_UUID = dbe6ea8a-3ac5-454b-ad2d-baf4c971f68e (Bob)
    BUSS_UUID = eb30833a-45e7-4fa8-9f82-24aa2a292f49 (Joe)

    TABL_UUID = 3f1ec332-d5ac-4cfb-b7a6-cc75abe889f4 (chow down)
    CAPY_UUID = ff445652-ed9f-4e32-8230-6a0b35e405cc (buffet)
    """

    # if commented out, that means it was already tested and added to the supabase DB

    """CREATING ACCOUNTS"""
    # create_user_account("Bob", "bob@gmail.com", "password123", 1112223333)
    # create_bus_account("Joe", "joesfood@company.com", "joeshack", "joes food", 1234567890)
    # create_user_account("Sir. Toby III", "Toby3@gmail.com", "royalToby", 2136547098)
    # create_bus_account("Jimmy", "hotdogJim@work.com", "jimdog", "JimmyDogs", 9087673554)

    """CREATING EVENTS"""
    # create_capacity_event("eb30833a-45e7-4fa8-9f82-24aa2a292f49", "buffet", "plaza", "SINGLE", 10, 30)
    # create_table_event("eb30833a-45e7-4fa8-9f82-24aa2a292f49", "chow down", 5, 4, 30, 20)
    # create_table_event("eb30833a-45e7-4fa8-9f82-24aa2a292f49", "nom nom time", 6, 5, 30, 20)

    """CREATING PARTY"""
    create_party("dbe6ea8a-3ac5-454b-ad2d-baf4c971f68e", "ff445652-ed9f-4e32-8230-6a0b35e405cc", 4)
    create_party("dbe6ea8a-3ac5-454b-ad2d-baf4c971f68e", "3f1ec332-d5ac-4cfb-b7a6-cc75abe889f4", 2, "Vegan")

    """ASSIGNING USER TO TABLE"""
    # assign_user_to_table("a1a15974-93b0-4714-8894-35edca7df2a9", "dbe6ea8a-3ac5-454b-ad2d-baf4c971f68e")
