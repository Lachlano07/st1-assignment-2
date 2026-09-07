```python

appointments = []


def book_appointment(patient_name, practitioner_name, appointment_time):
    """Add a new appointment to the list."""
    if not patient_name:
        raise ValueError("Patient name cannot be empty")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    appointments.append(appointment)
    print(f"Booked: {patient_name} with {practitioner_name} at {appointment_time}.")


def display_appointments():
    """Print all booked appointments."""
    if not appointments:
        print("No appointments recorded.")
        return
    print("\n--- Current Appointments ---")
    for appointment in appointments:
        print(f"Patient: {appointment['patient']} | "
              f"Practitioner: {appointment['practitioner']} | "
              f"Time: {appointment['time']}")
    print("-----------------------------\n")


def main():
    print("Welcome to SmartCare: Community Clinic Appointment Booking System!")

    # A couple of example appointments already on the books
    book_appointment('Alice Smith', 'Dr. John Doe', '2024-07-20 10:00 AM')
    book_appointment('Bob Johnson', 'Dr. Jane Roe', '2024-07-20 11:30 AM')

    display_appointments()

    # Let the user book a new appointment themselves
    print("Let's book a new appointment:")
    patient_name = input("Enter patient's name: ")
    practitioner_name = input("Enter practitioner's name: ")
    appointment_time = input("Enter appointment time (e.g. 2024-07-21 09:00 AM): ")

    book_appointment(patient_name, practitioner_name, appointment_time)

    display_appointments()


if __name__ == "__main__":
    main()
```


```markdown
Act as a Python tutor. I am learning introductory software technology. Here is a small appointment-booking function. 1. Explain what the code does. 2. Identify three limitations. 3. Suggest improvements. 4. Do not rewrite the whole application. 5. Ask me two questions to test my understanding. here is the code i have made 
```
```

## What the code does

This is a simple command-line appointment booking system for a clinic. It has three parts:

1. **`book_appointment()`** — takes a patient name, practitioner name, and time, validates that the patient name isn't empty, builds a dictionary from those three fields, and appends it to a global `appointments` list. It prints a confirmation message.

2. **`display_appointments()`** — loops through the `appointments` list and prints each one in a readable format, or says "No appointments recorded" if the list is empty.

3. **`main()`** — the entry point. It pre-books two example appointments, displays them, then prompts the user to type in a new patient name, practitioner, and time, books that appointment too, and displays the updated list.

The data lives in memory only (the global `appointments` list) — nothing is saved to a file or database, so it all disappears when the program ends.

## Three limitations

1. **No validation on `practitioner_name` or `appointment_time`.** You check that `patient_name` isn't empty, but a blank practitioner or a nonsense string like `"banana"` for the time would be accepted without complaint.

2. **No duplicate or conflict checking.** Nothing stops you from booking two different patients with the same practitioner at the same time — there's no logic comparing new appointments against existing ones.

3. **`appointment_time` is a free-text string, not a real date/time object.** Because it's just whatever the user types, you can't reliably sort appointments chronologically, check if a time has already passed, or catch malformed input like `"2024-13-45"`.

## Suggested improvements (not a rewrite)

- Add a basic check in `book_appointment()` for empty/whitespace `practitioner_name` and `appointment_time`, similar to the existing `patient_name` check.
- Use Python's `datetime.strptime()` to parse `appointment_time` into a real `datetime` object — this immediately gives you validation (it raises an error on bad input) and lets you sort or compare appointments later.
- Before appending a new appointment, loop through the existing list and check whether the same practitioner already has an appointment at that same time, and warn or reject if so.

These are small, targeted additions you could try inserting into the existing functions without touching the overall structure.

## Two questions for you

1. In `book_appointment()`, the check is `if not patient_name:`. What would happen if someone entered `"   "` (just spaces) as the patient name — would this check catch it? Why or why not?

2. If you wanted to prevent double-booking a practitioner at the same time, what would you need to compare, and at what point in `book_appointment()` would that comparison need to happen (before or after building the `appointment` dictionary)? Why does the order matter?



Part d 
Write a simple, beginner-friendly Python function for a GP clinic that stores appointment information. Each appointment should record three pieces of information: the patient's name, the practitioner's name, and the appointment time.

Keep the code short, readable, and easy to follow.

It stores each appointment as a dictionary with `patient`, `practitioner`, and `time` keys, all kept in a list called `appointments`. `add_appointment()` appends a new one, and `view_appointments()` loops through and prints them numbered and readable. Running the file adds two sample appointments and prints them out.
# gp_appointments.py
#
# A simple, beginner-friendly program for a GP clinic to store appointments
# in memory (while the program is running). No databases, no GUI — just
# plain Python using a list of dictionaries.

# This list will hold all of our appointments.
# Each appointment is stored as a dictionary with three pieces of information:
# the patient's name, the practitioner's name, and the appointment time.
appointments = []


def add_appointment(patient_name, practitioner_name, appointment_time):
    """
    Add a new appointment to the appointments list.

    Parameters:
        patient_name (str): The name of the patient.
        practitioner_name (str): The name of the doctor/nurse/etc.
        appointment_time (str): The date and/or time of the appointment.
    """
    # Create a dictionary to represent this single appointment.
    new_appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }

    # Add the new appointment dictionary to our list of appointments.
    appointments.append(new_appointment)

    # Let the user know it worked.
    print(f"Appointment added: {patient_name} with {practitioner_name} at {appointment_time}")


def view_appointments():
    """
    Print out all stored appointments in a clear, readable format.
    """
    # If there are no appointments yet, say so and stop here.
    if len(appointments) == 0:
        print("There are no appointments booked yet.")
        return

    print("\n--- Current Appointments ---")

    # Go through each appointment in the list one at a time.
    # enumerate() lets us also get a number (starting at 1) for each one.
    for number, appointment in enumerate(appointments, start=1):
        print(f"{number}. Patient: {appointment['patient']}")
        print(f"   Practitioner: {appointment['practitioner']}")
        print(f"   Time: {appointment['time']}")
        print()  # blank line between appointments for readability


# ---------------------------------------------------------------
# Example usage: this only runs when the file is run directly
# (not if it's imported into another script).
# ---------------------------------------------------------------
if __name__ == "__main__":
    # Add a couple of sample appointments.
    add_appointment("John Smith", "Dr. Patel", "Monday 9:00 AM")
    add_appointment("Amy Nguyen", "Dr. Osei", "Monday 10:30 AM")

    # Print out all the appointments we've stored so far.
    view_appointments()