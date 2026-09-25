from __future__ import annotations
 
import datetime
 
 
class Patient:
    """A clinic patient (FR-01, FR-02, FR-09)."""
 
    def __init__(
        self,
        patient_id: str,
        name: str,
        contact_info: str,
        date_of_birth: datetime.date,
    ) -> None:
        if not patient_id:
            raise ValueError("patient_id is required.")
        if not name:
            raise ValueError("name is required.")
        if not contact_info:
            raise ValueError("contact_info is required.")
        if not isinstance(date_of_birth, datetime.date):
            raise TypeError("date_of_birth must be a datetime.date.")
 
        self.patient_id = patient_id
        self.name = name
        self.contact_info = contact_info
        self.date_of_birth = date_of_birth
        self._appointments: list = []
 
    def record_appointment(self, appointment) -> None:
        """Link a booked appointment to this patient's history (FR-09)."""
        self._appointments.append(appointment)
 
    def get_appointment_history(self) -> list:
        """Return this patient's appointments (FR-09)."""
        return list(self._appointments)
 