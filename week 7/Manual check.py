import datetime
 
from Patient import Patient
from Practitioner import Practitioner
from Appointment import Appointment, InvalidStatusTransitionError
 
 
def check_valid_objects():
    print("1. Creating valid objects")
    patient = Patient("P1", "Alice Smith", "0400 000 000", datetime.date(1990, 5, 1))
    practitioner = Practitioner("D1", "Dr. Jane Roe", "General Practice")
    appt = Appointment("A1", datetime.date(2026, 10, 1), datetime.time(9, 0), patient, practitioner)
 
    # Link the appointment into each side's history/schedule (FR-09, FR-10)
    patient.record_appointment(appt)
    practitioner.record_appointment(appt)
 
    print(f"   Created {appt.appointment_id}, status = {appt.status.name}")
    print(f"   Patient history: {[a.appointment_id for a in patient.get_appointment_history()]}")
    print(f"   Practitioner schedule: {[a.appointment_id for a in practitioner.get_schedule()]}")
    return patient, practitioner, appt
 
 
def check_invalid_input():
    print("\n2. Testing invalid input")
    try:
        Patient("", "No Id Patient", "0400 000 000", datetime.date(1990, 1, 1))
    except ValueError as e:
        print(f"   Blank patient_id correctly rejected: {e}")
 
    try:
        Practitioner("D2", "", "Cardiology")
    except ValueError as e:
        print(f"   Blank practitioner name correctly rejected: {e}")
 
    try:
        Appointment(
            "",
            datetime.date(2026, 10, 1),
            datetime.time(9, 0),
            Patient("P2", "Bob Johnson", "0400 111 222", datetime.date(1980, 1, 1)),
            Practitioner("D3", "Dr. Lee", "General Practice"),
        )
    except ValueError as e:
        print(f"   Blank appointment_id correctly rejected: {e}")
 
 
def check_cancel(appt):
    print("\n3. Cancelling a scheduled appointment")
    appt.cancel()
    print(f"   {appt.appointment_id} status is now: {appt.status.name}")
 
 
def check_illegal_transition(appt):
    print("\n4. Attempting an illegal repeated transition (cancelling again)")
    try:
        appt.cancel()
    except InvalidStatusTransitionError as e:
        print(f"   Correctly rejected: {e}")
 
 
def check_conflict():
    print("\n5. Bonus check: double-booking conflict (BR-1, FR-04)")
    patient_a = Patient("P3", "Carol White", "0400 333 444", datetime.date(1985, 2, 2))
    patient_b = Patient("P4", "Dan Brown", "0400 555 666", datetime.date(1978, 3, 3))
    practitioner = Practitioner("D4", "Dr. Kim", "Paediatrics")
    slot = (datetime.date(2026, 10, 2), datetime.time(14, 0))
 
    appt_1 = Appointment("A2", slot[0], slot[1], patient_a, practitioner)
    appt_2 = Appointment("A3", slot[0], slot[1], patient_b, practitioner)
    print(f"   Same-slot appointments conflict: {appt_1.conflicts_with(appt_2)}")
 
    appt_1.cancel()
    print(f"   After cancelling A2, conflict is now: {appt_1.conflicts_with(appt_2)}")
 
 
if __name__ == "__main__":
    _, _, appt = check_valid_objects()
    check_invalid_input()
    check_cancel(appt)
    check_illegal_transition(appt)
    check_conflict()
 