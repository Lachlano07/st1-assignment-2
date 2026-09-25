A - revist approved UML

Before coding, the Stage 3 model (Patient, Practitioner, Appointment) was checked against this week's brief:

1. Patient: patient_id, name, contact_info, date_of_birth, get_appointment_history() - unchanged from Stage 3.

2. Practitioner: practitioner_id, name, get_schedule() - Stage 3 only had id and name, but this week's handout explicitly asks for a specialty field too. This is a small, justified extension to the approved model rather than a new AI suggestion, so it's added directly.

3. Appointment: id, date, time, status, patient, practitioner, cancel(), update_status(), conflicts_with(). unchanged from Stage 3, now with real behaviour instead of stubs.



b- Implment Patient 

Patient.py implements Patient exactly as specified in the approved Stage 3 UML: patient_id, name, contact_info and date_of_birth, plus the get_appointment_history() method that was left as a stub in Stage 3.

Basic validation was added in init. patient_id, name and contact_info must all be non-blank, reflecting the "mandatory fields" rule (BR-2) at the Patient level and date_of_birth must actually be a datetime.date object rather than a plain string, since NFR-01 requires dates to be held as structured values rather than free text.

get_appointment_history() needed something real to return, so one small addition was made beyond the Stage 3 skeleton. A private _appointments list plus a record_appointment() method that appends an Appointment to it. This satisfies FR-09 ("retain each patient's appointment history") without introducing a repository or service class. Stage 3 (Task F) had already decided against.

c- Implment Practitioner 

practitioner.py follows the same brief but for a different entity. practitioner_id name and specialty. Specialty wasn't part of the original Stage 3 skeleton (which only had id and name). it's added here because the Stage 4 handout explicitly calls for it under Task C, so it's treated as a confirmed, justified extension to the approved model rather than scope creep.

Validation is intentionally lighter than Patient's. practitioner_id, name and specialty must all be non-blank with no further type-checking, since the approved Practitioner UML never specified anything more elaborate. The handout also explicitly says "no database logic" for this class, so there is nothing here beyond plain attributes.

Like Patient, get_schedule() needed real data to return, so the same minimal pattern was used: a private _appointments list plus a record_appointment() method (FR-10). The two classes end up structurally similar for that reason - not because one was copied from the other, but because both Stage 3 stub methods needed the same small fix to make them return something real.

D - Appointment 
see Ai Appointment.py

E - Ai Review
Checked against the criteria in the handout:

1. Model consistency: matches the Stage 3 UML, same attributes, same three methods, status still starts BOOKED. Consistent.

2. Unsupported/extra features: the AI turned every attribute into a full property (date, time, patient, practitioner), not just status. The approved skeleton only ever needed status to be protected (that's the one field with business rules attached to it). The rest don't need controlled mutation. This is the AI adding more structure than the design called for.

3. Public state mutation: status itself was correctly protected (read-only property, changed only through update_status()/cancel()).This is the one place mutation genuinely needed guarding.

4. Unnecessary inheritance: none introduced. Fine.

5. Invented dependencies: none, no repository, service or persistence classes were added, which respects the Stage 3 decision (Task F, AI suggestion 5 - rejected) to keep entities plain for now.

6. Error handling: reasonable, but isinstance() checks were added for every argument, including ones nothing in the requirements asks to validate at this stage (e.g. checking patient/practitioner are the right type). That's defensive coding beyond what BR-2 actually requires (which is just that the fields are provided, not empty).



F- manual behaviour checks
see Manual check.py

out put 
1. Creating valid objects
   Created A1, status = BOOKED
   Patient history: ['A1']
   Practitioner schedule: ['A1']

2. Testing invalid input
   Blank patient_id correctly rejected: patient_id is required.
   Blank practitioner name correctly rejected: name is required.
   Blank appointment_id correctly rejected: appointment_id is required.

3. Cancelling a scheduled appointment
   A1 status is now: CANCELLED

4. Attempting an illegal repeated transition (cancelling again)
   Correctly rejected: Cannot move appointment from CANCELLED to CANCELLED.

5. Bonus check: double-booking conflict (BR-1, FR-04)
   Same-slot appointments conflict: True
   After cancelling A2, conflict is now: False
PS 

This covers all four required checks from them handout. Valid object creation, invalid input, cancelling a booked appointment and an illegal repeated transition, for example cancelling an already cancelled appointment. a fith check for the double bookings (BR-1) was added sinceconflics_with() is one of Appointments three methods 

G- Refactor 

To keep the implementation simple and consistent with the approved design (and not over-built), the following was removed/changed from the AI's version:

1. Properties on date, time, patient and practitioner were reverted to plain public attributes, matching the Stage 3 skeleton. Only status kept its property + private backing field, since that's the only attribute with a protected lifecycle.

2. The isinstance() type-checks on patient/practitioner/date/time were dropped. The only validation kept is that appointment_id is non-blank. a sensible identifier check. Type hints still document the expected types without enforcing them at runtime.

3. Long docstrings were trimmed to short comments tied to FR/BR numbers, so the traceability is kept without the verbosity.

Net result: same public behaviour (cancel, update_status, conflicts_with, the enum, the exception), noticeably less code.


H- AI Engieneering Log

Promt used and input given to AI- see AI usage.md

What AI generated: 
1. An AppointmentStatus enum with four members - BOOKED, COMPLETED, CANCELLED, NO_SHOW - matching the four statuses in BR-6.

2. An InvalidStatusTransitionError exception that stores the current and requested status and builds a message such as "Cannot transition appointment from X to Y."

3. An Appointment class whose constructor takes appointment_id, date, time, patient and practitioner, validates each one with an isinstance() check (including confirming patient/practitioner are genuine Patient/Practitioner objects, and date/time are real datetime.date/datetime.time values), and sets status to BOOKED by default.

4. Every attribute on that class - not just status, but date, time, patient and practitioner too - exposed only through a @property, each backed by a private underscore-prefixed field.

5. A class-level _ALLOWED_TRANSITIONS dictionary mapping each status to the set of statuses it can move to: BOOKED maps to {COMPLETED, CANCELLED, NO_SHOW}, and the other three map to an empty set.

6. cancel(), implemented as a one-line call to update_status(CANCELLED).

7. update_status(new_status), which checks new_status is actually an AppointmentStatus, looks up whether the move is allowed in _ALLOWED_TRANSITIONS, and raises InvalidStatusTransitionError if it isn't.

8. conflicts_with(other), which returns False immediately if either appointment is CANCELLED, and otherwise checks whether both appointments share the same practitioner, date and time.

Decisions: what the AI performed successfully. The enum aligns perfectly with BR-6's four statuses, and the transition table effectively reflects the "no transition from a final state" rule (BR-6, BR-15) without requiring additional support. The fundamental logic in cancel(), update_status(), and conflicts_with() required no modifications. What it did poorly was encapsulate every attribute in a property when only the status required protection, and it included isinstance() checks more extensive than necessary according to any business rule; both aspects were reduced. The typical approach the AI settled on for Appointment is to validate solely what a business rule clearly requires, employing an enum for a defined array of states.

Verification evidence: the Task F manual tests confirmed valid creation, invalid input, a successful cancellation, an unauthorized repeated transition, and a conflict check, with all five passing against the revised Appointment class.



reflection 

The part I changed the most was the encapsulation the AI wrapped every attribute in a property, but the approved design only ever protected status, so turning date/time/patient/practitioner back into plain attributes kept the class closer to the Stage 3 skeleton instead of quietly growing it. I also cut back the constructor's isinstance() checks to just the one rule the business rules actually ask for (appointment_id can't be blank), rather than keeping every check the AI added by default.

The approved design constrained the AI mainly by giving it a fixed method list and a fixed attribute list up front, so there was no room for it to add a service layer or extra classes, the prompt explicitly told it not to, and the earlier Stage 3 decision to reject that idea. meant I already knew to watch for it and refactor it out if it showed up.