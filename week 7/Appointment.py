from __future__ import annotations

import datetime
from enum import Enum, auto

from Patient import Patient
from Practitioner import Practitioner


class AppointmentStatus(Enum):
    """Lifecycle states of an Appointment (Scope item 5, BR-6)."""

    BOOKED = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    NO_SHOW = auto()


class InvalidStatusTransitionError(Exception):
    """Raised when an appointment's status is changed to a disallowed value."""

    def __init__(self, current: AppointmentStatus, requested: AppointmentStatus) -> None:
        super().__init__(f"Cannot move appointment from {current.name} to {requested.name}.")
        self.current = current
        self.requested = requested


class Appointment:
    """A booked meeting between a Patient and a Practitioner."""

    # BOOKED can move to any of the three final states; final states cannot
    # move anywhere else (BR-6, Story 4).
    _ALLOWED_NEXT = {
        AppointmentStatus.BOOKED: {
            AppointmentStatus.COMPLETED,
            AppointmentStatus.CANCELLED,
            AppointmentStatus.NO_SHOW,
        },
        AppointmentStatus.COMPLETED: set(),
        AppointmentStatus.CANCELLED: set(),
        AppointmentStatus.NO_SHOW: set(),
    }

    def __init__(
        self,
        appointment_id: str,
        date: datetime.date,
        time: datetime.time,
        patient: Patient,
        practitioner: Practitioner,
    ) -> None:
        if not appointment_id:
            raise ValueError("appointment_id is required.")

        self.appointment_id = appointment_id
        self.date = date
        self.time = time
        self.patient = patient
        self.practitioner = practitioner
        self._status = AppointmentStatus.BOOKED

    @property
    def status(self) -> AppointmentStatus:
        """Current status."""
        return self._status

    def cancel(self) -> None:
        """Cancel the appointment (FR-08)."""
        self.update_status(AppointmentStatus.CANCELLED)

    def update_status(self, new_status: AppointmentStatus) -> None:
        """Move to new_status if that transition is allowed (FR-07, BR-15)."""
        if new_status not in self._ALLOWED_NEXT[self._status]:
            raise InvalidStatusTransitionError(self._status, new_status)
        self._status = new_status

    def conflicts_with(self, other: "Appointment") -> bool:
        """True if both appointments would double-book the same practitioner
        (BR-1, FR-04). A cancelled appointment no longer occupies the slot."""
        if self.status is AppointmentStatus.CANCELLED or other.status is AppointmentStatus.CANCELLED:
            return False
        return (
            self.practitioner is other.practitioner
            and self.date == other.date
            and self.time == other.time
        )
 