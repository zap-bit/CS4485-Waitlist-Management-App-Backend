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
def create_table_event(account_uuid, name, num_tables, avg_size, reservation_duration, no_show_policy):
    """
    Creates a TABLE type event in the EVENTS table on Supabase.
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
    response = supabase.table("events").insert(data).execute()
    return response

# Example usage
if __name__ == "__main__":
    
    print("testing backend/databse connection -Kyle")

    """
    for testing purposes:
    USER_UUID = dbe6ea8a-3ac5-454b-ad2d-baf4c971f68e (Bob)
    BUSS_UUID = eb30833a-45e7-4fa8-9f82-24aa2a292f49 (Joe)
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
