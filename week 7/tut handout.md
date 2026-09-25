

Encapsulation 

Class: Patient

Protected state / invariant: None of the attributes are truly protected once created   patient_id, name, contact_info and date_of_birth are plain public fields. The only enforcement is in __init__ (raises ValueError if patient_id/name/contact_info is blank, TypeError if date_of_birth isn't a real date), after construction, nothing stops code from overwriting them directly (e.g. patient.name = "").

Public operations: get_appointment_history() (read only view of this patient's appointments), record_appointment() (adds a booked appointment to that history).


Class: Practitioner

Protected state / invariant: Same pattern as Patient: practitioner_id, name and specialty are plain public fields, validated as non blank only in __init__. Not protected against being changed afterwards.

Public operations: get_schedule() (read only view of this practitioner's appointments), record_appointment() (adds a booked appointment to that schedule).

Class: Appointment

Protected state / invariant: status is the one genuinely protected attribute   held privately (self._status) and exposed only through a read only status property, it can only change via update_status()/cancel(), which check an allowed transitions table and raise InvalidStatusTransitionError otherwise. appointment_id, date, time, patient and practitioner are plain public attributes (appointment_id validated as non blank at construction, but not protected afterwards).

Public operations: cancel(), update_status(new_status), conflicts_with(other).



Composition or Inheritance?

Appointment and Patient -> ☑ Composition/association ☐ Inheritance Reason: A Patient can exist without an Appointment and can outlast it. A cancelled appointment remains, rather than being discarded, and a patient may have none, one, or multiple appointments throughout their life. Appointment only references a Patient (a "books" association), it doesn't control the Patient's lifecycle, thus it's an association, not composition.

Appointment and Practitioner -> ☑ Composition/association ☐ Inheritance Reason: The same logic applies as with Patient: a Practitioner exists independently of each individual Appointment and can be involved in multiple appointments over time (an "attends" association). Appointment refers to a Practitioner instead of possessing or including it.

Doctor and Practitioner (hypothetical) -> ☐ Composition/association ☑ Inheritance reason: Unlike Patient/Practitioner, this represents a true isa relationship: a Doctor is a specific type of Practitioner (e.g., possessing prescribing rights or additional scheduling protocols) while fundamentally remaining a Practitioner (identifier, name, specialty, get_schedule()). Since Doctor not only references but actually embodies a Practitioner, inheritance is suitable in this context—unlike Appointment's relationships mentioned earlier, which are distinctly has a rather than is a.

Clinic and Appointment -> ☑ Composition/association ☐ Inheritance reason: In contrast to Patient/Practitioner, an Appointment cannot survive or function independently from the Clinic that arranged it. it is illogical for a single Appointment to be transferred  or assigned among different clinics. The whole part, exclusive ownership relationship (if Clinic were removed, its Appointments wouldn’t logically transfer elsewhere) serves as the composition test, unlike the association of Appointment with Patient/Practitioner mentioned earlier. (Aligns with the Stage 3 conclusion that the Clinic is not a modeled class at this time since no FR necessitates it, this is a theoretical response in case it gets included.)



responsibility allocation 

1. Who decides whether SCHEDULED can become CANCELLED?

The appointment determines this autonomously. The update_status()/cancel() methods reference an allowed transitions table (BOOKED can transition to COMPLETED/CANCELLED/NO_SHOW, the latter three have no further transitions) and trigger an InvalidStatusTransitionError if the transition is not permitted—this rule exists within the object managing its state, not within the UI or a different class.

1. Who validates a patient name?

Patient validates its own name, in Patient.__init__ (raises ValueError if it's blank). Appointment doesn't re check it, and neither does a UI layer. each class is responsible for its own fields.

3. Should Appointment execute SQL? Why?

No. SQL/persistence is an infrastructural issue, not a domain one integrating it into Appointment would link a business rule (e.g. cancellation) to a specific database, render the class untestable without an actual database, and introduce two unrelated motivations for alteration. This same logic was applied in Stage 3 to dismiss AI's suggestion for a service/repository (Task F): persistence should exist in an independent layer that the domain class remains unaware of.

4. Should the UI decide whether a status transition is legal?

No. If the UI determined which transitions were permissible, the rule would either be repeated in every location that interacts with an appointment or applied inconsistently among them. The UI must solely invoke update_status()/cancel() and respond to the outcome (success or an InvalidStatusTransitionError). The validity of the transition is the responsibility of Appointment itself.


AI Code Critique


1. Public status mutation, Problem: if the status can be assigned directly (appointment.status = "Cancelled"). Any code may bypass the transition rules completely. Moving from COMPLETED to BOOKED, for instance. Correction: set the status to private with a read only attribute, and enforce all modifications through an update_status()/cancel() method that verifies an allowed transitions table and denies unauthorized changes (exactly as Appointment.status operates here).

2. SQL inside cancel(), Problem: Incorporating persistence directly into a domain method links a business rule to a particular database, rendering the class untestable without an active database connection, this also introduces two unrelated factors for class changes (the business rule and the database structure). Correction: ensure that cancel() is solely focused on the domain state transition, the responsibility for saving that transition should reside in a distinct data access/repository layer that the domain class is unaware of.

3. NotificationManger dependency, Problem: This is a fabricated dependency lacking any basis in requirements SMS/email reminders are clearly temporary and outside the parameters of the SmartCare brief, meaning Appointment doesn't need to be aware of the existence of notifications. Correction: eliminate the dependency. If reminders are introduced afterward, they ought to be activated by an external caller responding to a cancellation, not by the Appointment itself.

4. Inheritance from PatientRecord, problem: this suggests that every Appointment is a unique type of PatientRecord, which is incorrect, and it would inappropriately bring Patient's specific fields and behavior onto Appointment. An Appointment does not represent a category of Patient, it refers to one. Correction: maintain a reference to a Patient object as a field (association), rather than extending it.

5. Too Many Responsibilites at once, Problem: When considered collectively, this single class serves as a domain entity, a persistence layer, a notification dispatcher and (through inheritance) is intertwined with data from an unrelated entity—evidencing a clear violation of the Single Responsibility principle and representing a significantly larger instance of the same over design pattern identified in Stage 3 (Task F) regarding AI's service/repository recommendation. Correction: retain Appointment for attributes along with cancel()/update_status()/conflicts_with() only, persistence, notifications, and any managerial coordination should reside in distinct collaborating classes beyond the entity.


Why can code be object-oriented syntactically but still have poor object-oriented design?

The "object-oriented" syntax, classes, properties, inheritance, enums, does not ensure that these features are utilized effectively. Code can establish a class, encapsulate fields with properties, and apply inheritance while still allowing mutable state that can violate invariants, utilizing inheritance to represent a connection that is merely an association (Doctor-style inheritance used where a reference would do, or worse), giving one class excessive unrelated duties or relying on elements that no specification demanded. The AI-produced Appointment class from Task D serves as a concrete example: it used in a suitable class, an enum, and properties syntactically clear. Almost textbook quality yet encapsulated every attribute in a property when solely status required protection, and validated types when it was unnecessary to do so. Technically object-oriented. Excessively complex as a design. Effective objective oriented design involves intentionally utilizing these features in alignment with genuine requirements and authentic is a/has a relationships, rather than merely employing the syntax.