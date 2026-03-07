import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase URL or API Key in environment variables.")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_user_account(email: str, pswd: str, name: str, business_name: str, role: str):
    """
    Inserts a user account into the Supabase database.

    :param email: Email of the user (non-nullable). 
    :param pswd: Password of the user (non-nullable).
    :param name: Name of the user (non-nullable).
    :param business_name: Business name (nullable).
    :param role: Role of the user ('USER' or 'BUSINESS').
    """
    data = {
        "email": email,
        "password": pswd,
        "name": name,
        "businessname": business_name,
        "role": role
    }

    response = supabase.table("account").insert(data).execute()

    if response.status_code == 201:
        print("User account inserted successfully.")
    else:
        print("Failed to insert user account:", response.data)

def create_business_account(email: str, pswd: str, name: str, business_name: str):
    """
    Inserts a business account into the Supabase database.

    :param email: Email of the business user (non-nullable).
    :param pswd: Password of the business user (non-nullable).
    :param name: Name of the business user (non-nullable).
    :param business_name: Business name (non-nullable for BUSINESS role).
    """
    data = {
        "email": email,
        "password": pswd,
        "name": name,
        "businessname": business_name,
        "role": "BUSINESS"
    }

    response = supabase.table("account").insert(data).execute()

    if response.status_code == 201:
        print("Business account inserted successfully.")
    else:
        print("Failed to insert business account:", response.data)


def create_table_event(name: str, number_of_tables: int, avg_table_size: int,
                       reservation_duration: int, no_show_policy: str):
    """
    Inserts a TABLE-type event into the Supabase database.
    businessUserUUID is a placeholder — will be sourced from the active user on the frontend.

    :param name: Name of the event (non-nullable).
    :param number_of_tables: Number of tables for the event.
    :param avg_table_size: Average table size.
    :param reservation_duration: Duration of each reservation (in minutes).
    :param no_show_policy: Policy text for no-shows.
    """
    # TODO: Replace with active user's UUID from frontend authentication
    business_user_uuid = "PLACEHOLDER_BUSINESS_USER_UUID"

    data = {
        "businessaccountuuid": business_user_uuid,
        "name": name,
        "eventtype": "TABLE",
        "numberoftables": number_of_tables,
        "avgtablesize": avg_table_size,
        "reservationduration": reservation_duration,
        "noshowpolicy": no_show_policy
    }

    response = supabase.table("event").insert(data).execute()

    if response.status_code == 201:
        print("Table event inserted successfully.")
    else:
        print("Failed to insert table event:", response.data)


def create_capacity_event(name: str, location: str, capacity: int, estimated_time_per_person: int):
    """
    Inserts a CAPACITY-type event into the Supabase database.
    businessUserUUID is a placeholder — will be sourced from the active user on the frontend.

    :param name: Name of the event (non-nullable).
    :param location: Location of the event.
    :param capacity: Maximum capacity of the event.
    :param estimated_time_per_person: Estimated time per person (in minutes).
    """
    # TODO: Replace with active user's UUID from frontend authentication
    business_user_uuid = "PLACEHOLDER_BUSINESS_USER_UUID"

    data = {
        "businessaccountuuid": business_user_uuid,
        "name": name,
        "eventtype": "CAPACITY",
        "location": location,
        "capacity": capacity,
        "estimatedtimeperperson": estimated_time_per_person
    }

    response = supabase.table("event").insert(data).execute()

    if response.status_code == 201:
        print("Capacity event inserted successfully.")
    else:
        print("Failed to insert capacity event:", response.data)


def create_event_table(capacity: int):
    """
    Inserts an event table into the Supabase database.
    eventUUID is a placeholder — will be sourced from the currently selected event on the frontend.
    partyLeaderUUID and partyUUID start as None and will be assigned later.

    :param capacity: Seating capacity of this table.
    """
    # TODO: Replace with the selected event's UUID from frontend
    event_uuid = "PLACEHOLDER_EVENT_UUID"

    data = {
        "eventuuid": event_uuid,
        "partyleaderuuid": None,
        "partyuuid": None,
        "capacity": capacity
    }

    response = supabase.table("eventtable").insert(data).execute()

    if response.status_code == 201:
        print("Event table inserted successfully.")
    else:
        print("Failed to insert event table:", response.data)


def create_party(party_size: int, special_requests: str):
    """
    Inserts a party into the Supabase database.
    partyLeaderUUID and eventUUID are placeholders — will be sourced from the frontend.

    :param party_size: Number of people in the party.
    :param special_requests: Any special requests for the party (text).
    """
    # TODO: Replace with the selected party leader's UserAccountUUID from frontend
    party_leader_uuid = "PLACEHOLDER_PARTY_LEADER_UUID"
    # TODO: Replace with the selected event's UUID from frontend
    event_uuid = "PLACEHOLDER_EVENT_UUID"

    data = {
        "partyleaderuuid": party_leader_uuid,
        "eventuuid": event_uuid,
        "partysize": party_size,
        "specialrequests": special_requests
    }

    response = supabase.table("party").insert(data).execute()

    if response.status_code == 201:
        print("Party inserted successfully.")
    else:
        print("Failed to insert party:", response.data)


# Example usage
if __name__ == "__main__":
    # Example testers for creating tables in Supabase
    print("gotta put smthn here so the test file runs, will replace with actual tests later -Kyle")
    # Create a business account
    # create_business_account(email="business@example.com", pswd="securepassword", name="Business Owner", business_name="Example Business")

    # # Create a table event
    # create_table_event(
    #     name="Table Event Example",
    #     number_of_tables=10,
    #     avg_table_size=4,
    #     reservation_duration=60,
    #     no_show_policy="No-shows will be charged a fee."
    # )

    # # Create a capacity event
    # create_capacity_event(
    #     name="Capacity Event Example",
    #     location="Main Hall",
    #     capacity=100,
    #     estimated_time_per_person=30
    # )

    # # Create an event table
    # create_event_table(capacity=6)

    # # Create a party
    # create_party(
    #     party_size=5,
    #     special_requests="Vegetarian meal options requested."
    # )