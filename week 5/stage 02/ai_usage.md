1. converstion for part F of lab handout

Act as a software requirements reviewer. Review the SmartCare requirements for ambiguity,
inconsistency, missing clarification questions and testability. Do NOT invent new client requirements. For every
suggestion, state whether it is based on evidence or is only a question/assumption requiring validation.
"Part A - Client Brief
SmartCare uses spreadsheets and paper records. Staff report duplicate bookings, difficulty finding patient
information, inconsistent appointment status and limited appointment history. Management wants a small,
maintainable patient, practitioner and appointment system.


Part B - Stakeholders and Scope:
Identify at least four stakeholders. Create In Scope and Out of Scope lists. Label uncertain features as provisional rather than confirmed

1. Reception staff: primary system users. book, view, update and cancel appoinments 
2. GP's: need to see their own schedule and patient's appointment hisotry 
3. Clinic manager: oversees clinic operations, needs visibility into bookings, cancellations and no shows
4. patients: indirectly affected by the system, their data being stored, their bookings being managed, not a dircet user but still affected.
5. system maintainer/ future developer: whoever supports the system after handover, relevant to the "maintable" requirement stated by the client. 



in scope 
1. creating, viewing and searching patient records
2. creating, viewing, updating and cancelling appointments
3. basic gp records 
4. preventing dupicate bookings 
5. appointment status tracking. for example, booked, completed, cancelled or no show.
6. appointment history of patients 
7. provisional: a daily report, the client mentions difficulty producing basic operational reports as a issue but managment hasn't explicitly confirmed reporting as a requriment 

out of scope 
1. patient self service booking 
2. online billing
3. AI clinical notes or diagnoses
4. multi location support 
5. provisional: patient SMS reminders 


Part C - Functional Requirements:
Write 8-12 numbered functional requirements using FR-01, FR-02 and so on. Each should describe one observable capability

1. FR-01: the system will allow receptionist to create a new patient record, storing name, contact info, date of birth and any other necessary information
2. FR-02: the system will allow receptionist to search for an existing patient record by name 
3. FR-03: the system will allow receptionist to create a new appointment by selecting a patient, gp, time and date. 
4. FR-04: the system will not allow a new appointment if the seleceted gp already has an appointment at the same time
5. FR-05: the system will require patient name, gp name and appointment time to be filled out before that appoinmtent can be saved
6. FR-06: the system will allow staff to view all required appointmens
7. FR-07: the system will allow receptionist to update appointment status
8. FR-08: the system will allow receptionist to cancel appointments when needed
9. FR-09: the system will retain all patient historys
10. FR-10: the sytem will allow recptionist to filter by gp's 


Part D - Non-Functional Requirements:
Write 4-6 numbered non-functional requirements covering appropriate qualities such as reliability, maintainability, usability, data integrity or testability

1. NRF-01: Appointment date and time should be stored as structured date-time value not free text, to support sorting and duplicate checks 
quaility attribute: data integrity 

2. NRF-02: all patient, GP and appointment data will remian persistant between session, no data loss when program closed
quaility attribute: reliablity 

3. NRF-03:(provisional) A receptionist with minimal training should be able to book an appointment in under X steps, further details to be confirmed with client 
quaility attribute: usability

4. NRF-04: The program will allow future developers to add features without modifying unreleated features
quaility attribute: maintainability 

5. NRF-05: each cpre function will be independently unit testable 
quailty attribute: testability 


Part E - User Stories and Acceptance Criteria:
Write 4-6 user stories. For at least three, create Given-When-Then acceptance criteria including one negative or failure scenario.

1. As a receptionist, I want to book a new appointment so that a patient has a confirmed time with a GP.

Successful scenario: Given a patient and an available GP time slot When the receptionist submits a booking with all required fields Then the appointment is saved and appears in the day's list

Failure scenario: Given the selected GP already has an appointment at that date/time When the receptionist attempts to book the same slot Then the system rejects the booking and shows a conflict message


2. As a receptionist, I want to search for a patient by name so I don't create a duplicate record.

Successful scenario: Given a patient record exists When I search by name Then matching records are returned

Failure scenario: Given the search field is left blank When I submit the search Then the system rejects the search and prompts me to enter a name, instead of returning every patient record


3. As a GP, I want to view my appointments for the day so I can prepare for consultations.

Successful scenario: Given appointments exist for me on a given date When I open my daily schedule Then all my appointments for that date are shown in time order

Failure scenario: Given the requested date is not a valid calendar date When I request my schedule for that date Then the system rejects the request and shows an error, rather than attempting to load and display bad data


4. As a receptionist, I want to cancel an appointment so the slot is freed and the record reflects the change.

Successful scenario: Given a valid, existing appointment When the receptionist cancels it Then its status is set to Cancelled and the slot becomes available again

Failure scenario: Given an appointment ID doesn't exist or was already cancelled When the receptionist attempts to cancel it Then the system shows an error and makes no change
" 


Here's a structured review of the SmartCare requirements, organized by issue type. Each point is tagged **[Evidence]** (a contradiction or gap directly visible within the document itself) or **[Assumption/Question]** (something that can't be resolved without client input).

## Ambiguity

- **FR-01** — "any other necessary information" is undefined. As written this isn't testable — a tester can't verify what "necessary" means. **[Evidence]** — the vagueness is visible in the text itself; what fields are actually needed is a **[Question]** for the client.
- **FR-02** — "search... by name" doesn't specify partial vs. exact match, or first/last/full name handling. **[Question]**
- **FR-06** — "view all required appointments" is unclear — likely a typo or leftover phrasing. Does this mean all appointments, appointments for a selected day, or appointments matching some filter? **[Evidence]** the phrase itself is internally unclear; the intended meaning is a **[Question]**.
- **FR-10** — "filter by gp's" doesn't state *what* is being filtered (presumably the appointment list from FR-06, but this link isn't stated). **[Evidence]** of an unstated dependency; confirm with client **[Question]**.
- **NFR-04** ("add features without modifying unrelated features") is a reasonable maintainability goal but isn't independently verifiable through a normal acceptance test — it's closer to a design principle than a testable requirement. **[Assumption]** — suggest either accepting it as a qualitative/code-review-checked NFR, or asking the client/dev team what proxy measure (e.g., modular structure, documented interfaces) would count as evidence of compliance.

## Inconsistency

- **FR-03 vs FR-05**: FR-03 lists four inputs for creating an appointment (patient, GP, time, **date**). FR-05's validation rule only requires patient name, GP name, and appointment time — **date is missing** from the mandatory field list. **[Evidence]** — this is a direct textual mismatch worth fixing regardless of client input.
- **Scope item 6 ("appointment history of patients") vs FR-09 ("retain all patient historys")**: scope limits this to appointment history; FR-09 uses the broader, undefined term "patient history," which could be read as including clinical notes, record edits, etc. — none of which are otherwise in scope. **[Evidence]** of scope drift; recommend narrowing FR-09 to match the scope wording, but confirm intended breadth with the client **[Question]**.
- **FR-07 (update status) vs FR-08 (cancel) vs User Story 4**: FR-08 treats "cancel" as a separate action from "update status" (FR-07), even though "Cancelled" is listed as one of the status values in scope item 5 — implying cancelling might just be a status update. However, Story 4's acceptance criteria adds a behavior neither FR mentions: cancelling also **frees the appointment slot**, while a normal status update presumably wouldn't. **[Evidence]** — the FR text and the acceptance criteria aren't aligned; clarify whether "cancel" is a distinct capability with side effects (freeing the slot) or a special case of FR-07 **[Question]**.
- **Scope item 3 ("basic gp records") has no corresponding FR.** FR-03 assumes a GP can be "selected," implying GP records already exist somewhere, but nothing in Part C describes how they're created, viewed, or maintained. **[Evidence]** of a scope-to-FR gap; whether GP record management needs its own FRs is a **[Question]** for the client, not something to assume.

## Missing Clarification Questions

- **No FR addresses duplicate *patient* records**, only duplicate *bookings* (FR-04). Story 2 relies on manual search to avoid creating a duplicate patient, but there's no system-enforced check (e.g., matching name + DOB). Given "difficulty finding patient information" was a stated client pain point, it's worth asking whether manual search is sufficient or whether automatic duplicate-patient detection is expected. **[Question]**
- **No appointment duration/length is defined anywhere.** FR-04 blocks a new appointment only "at the same time" as an existing one — it's unclear whether this checks exact start-time collisions only, or overlapping time ranges (e.g., a 30-minute slot). This materially affects how "duplicate booking prevention" is implemented and tested. **[Question]**
- **No authentication/role model is defined**, despite Story 3 implying GPs should see only their *own* schedule (distinct from reception staff, who need broader visibility per stakeholder 3). Nothing in the FRs or NFRs specifies login, roles, or access control. This is a notable gap given the multi-role stakeholder list. **[Question]** — recommend explicitly asking the client whether role-based access is in scope, since it currently sits in a blind spot between stakeholder needs and functional requirements.
- **Patient-side double-booking isn't addressed** — FR-04 only prevents a GP being double-booked; it doesn't say whether the same patient can be booked into two overlapping appointments (e.g., with different GPs). **[Question]**
- **FR-02's blank-search rejection** (introduced in Story 2's failure scenario) isn't reflected back in FR-02 itself. Either FR-02 should be updated to state this validation rule, or it should be confirmed as an AC-only detail. **[Evidence]** of a documentation gap between Part C and Part E.

## Testability

- **FR-01, FR-09**: as discussed above, "any other necessary information" and "patient historys" are too vague to derive pass/fail test cases from. **[Evidence]**
- **FR-06**: "all required appointments" can't be turned into a test case without knowing what "required" filters or scopes are meant. **[Evidence]**
- **FR-07**: testable in principle, but would be stronger if it explicitly referenced the allowed status values (booked/completed/cancelled/no-show) already listed in scope item 5, rather than leaving the valid value set implicit. **[Assumption]** — a documentation improvement suggestion, not a new requirement.
- **NRF-03**: already correctly flagged as provisional pending a concrete step count — good practice, no action needed beyond following up with the client as planned.
- **NRF-04**: as noted above, hard to express as a pass/fail test without an agreed proxy metric. **[Assumption]**

## Summary
Overall the document is well-structured and most FRs/NFRs/stories are testable and internally consistent. The most important items to validate with the client before development are: appointment duration/overlap handling, role-based access (GP vs. reception visibility), whether duplicate-patient detection is expected beyond manual search, and whether GP record management is in scope. The FR-03/FR-05 date-field mismatch and the FR-07/FR-08/Story-4 "does cancel free the slot" inconsistency should be corrected regardless of client input, since they're internal contradictions rather than open questions.