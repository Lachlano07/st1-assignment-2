from __future__ import annotations
 
 
class Practitioner:
    """A clinic practitioner / GP (Scope item 3, FR-10, FR-11)."""
 
    def __init__(self, practitioner_id: str, name: str, specialty: str) -> None:
        if not practitioner_id:
            raise ValueError("practitioner_id is required.")
        if not name:
            raise ValueError("name is required.")
        if not specialty:
            raise ValueError("specialty is required.")
 
        self.practitioner_id = practitioner_id
        self.name = name
        self.specialty = specialty
        self._appointments: list = []
 
    def record_appointment(self, appointment) -> None:
        """Add a booked appointment to this practitioner's schedule (FR-10)."""
        self._appointments.append(appointment)
 
    def get_schedule(self) -> list:
        """Return this practitioner's appointments (FR-10, FR-11, Story 3)."""
        return list(self._appointments)
 