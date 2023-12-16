def create_contact(first_name, last_name, phone_number):
    return {"first_name": first_name, "last_name": last_name, "phone_number": phone_number}

def get_contact_string(contact):
    return f"{contact['first_name']} {contact['last_name']}: {contact['phone_number']}"
