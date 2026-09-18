Candidate Concepts

1. Patient
Class?: Yes
Reason: Distinct domain entity with its own identity, attributes (name, contact info, date of birth) and responsibilities (FR-01, FR-02, FR-09). referenced across multiple requirements.

2. GP
Class?: Yes
Reason: Distinct entity with its own identity and behaviour, owns its schedule and participates in the double-booking conflict check (FR-03, FR-04, FR-10, FR-11).

3. Appointment
Class?: Yes
Reason: Central transaction object linking one Patient and one GP. owns date/time, status, and cancellation/conflict behaviour (FR-03–FR-09).

4. Name
Class?: No
Reason: A plain string attribute belonging to Patient and GP (e.g. Patient.name). no identity or behaviour of its own.

5. Clinic
Class?: No 
Reason: No FR gives “the clinic” itself any distinct data or operations. the system models Patient/GP/Appointment directly rather than through a top level owning object. Could matter later if multi clinic support were required, but that's out of scope for v0.2.

6. Database
Class?: No
Reason: An infrastructure/persistence concern (how NFR-02 gets satisfied), not a domain concept, including it would mix implementation detail into the business model.

7. Cancellation
Class?: No
Reason: An action (verb), not a noun with its own identity, modelled as the cancel() operation on Appointment, not as a separate class.

8. Status
Class?: No
Reason:  Appointment Status has no independent identity or behaviour of its own. modelled as a plain attribute (status : str) on Appointment.



CRC Cards


1. Patient
Responsibilities:
Store patient identifying and contact details (FR-01)
Support search by name (FR-02)
Maintain a link to appointment history (FR-09)
Collaborators:
Appointment

2. GP
Responsibilities:
Store GP identifying details
Provide own schedule / appointment list (FR-10, FR-11)
Participate in double booking conflict check (FR-04)
Collaborators:
Appointment

3. Appointment
Responsibilities:
Store date, time and status, and link to one Patient and one GP (FR-03, FR-05)
Validate required fields before being saved (FR-05)
Detect conflicting bookings for the same GP/time (FR-04)
Change status when updated or cancelled (FR-07, FR-08)
Collaborators:
Patient
GP


Relationship Reasoning
1. Patient to Appointment: which relationship and why?
Association,  A Patient has appointments, but doesn't exclusively own them.each Appointment also belongs to a GP. It's a one to many association: one Patient links to zero or more Appointments (FR-03, FR-09), and each Appointment references exactly one Patient.

2. GP to Appointment: what multiplicity?
GP (1) to Appointment (0..*). A GP may have zero or more appointments scheduled, but each Appointment is tied to exactly one GP. this is also the basis of the double booking rule (FR-04): no two Appointments can share the same GP and the same date/time.

3. Should Appointment inherit from Patient?
No. Inheritance  would mean every Appointment is a specialised kind of Patient, which doesn't hold conceptually. an Appointment isn't a type of Patient, it's a separate concept that references one. Appointment should hold a reference to Patient (association), not extend it.

4. Does Clinic need to own every object?
No, not at this stage. A Clinic could conceptually be a top level container owning all Patients, GPs and Appointments, but no confirmed FR gives a Clinic object its own data or behaviour, so the system can be modelled as three peer classes without an umbrella Clinic class. consistent with the Candidate Concepts decision above. This might change if SmartCare needed to support multiple clinics/branches in future.


AI Model Critique
AI proposals to critique: PatientManager, PractitionerManager, AppointmentManager, ClinicController, NotificationManager, ScheduleEngine.


1. PatientManager / PractitionerManager / AppointmentManager
A manager class per entity is not yet needed, or even listen in the client brief. nothing in v0.2 yet requires shared operations beyond what a single Patient/Practitioner/Appointment class already covers. This mirrors the Service/Repository over design flagged in Stage 3 Lab Task F: worth asking the client once real persistence and cross entitys are implemented.

2. ClinicController
Directly contradicts the answer to Relationship Reasoning Q4 above: no FR gives the clinic itself any behaviour to control. Adding a controller class implies a top level operator that doesn't correspond to any requirement from the client brierf.

3. NotificationManager
Not grounded in any requirement at all. SMS reminders are explicitly provisional and out of scope in the SmartCare v0.2 brief/ this is a clear case of the AI inventing a feature the client brief never asked for.

4. ScheduleEngine
Vague and unscoped. no FR describes anything resembling an automated scheduling or optimisation “engine”. The actual requirements (FR-06, FR-10) just need simple viewing and GP based filtering of appointments, which the existing Appointment/Practitioner classes already cover. 
