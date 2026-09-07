
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