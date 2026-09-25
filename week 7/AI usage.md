Act as a Python pair programmer. Implement ONLY the Appointment class, an AppointmentStatus enum and one custom exception, InvalidStatusTransitionError, from the approved SmartCare UML below.

Patient and Practitioner classes already exist (from patient import Patient; from practitioner import Practitioner). Do not write, modify or subclass them.

APPROVED UML – Appointment
- appointment_id: str
- date: datetime.date
- time: datetime.time
- patient: Patient
- practitioner: Practitioner
- status: AppointmentStatus (always starts as BOOKED)
+ cancel() -> None
+ update_status(new_status: AppointmentStatus) -> None
+ conflicts_with(other: Appointment) -> bool

AppointmentStatus values: BOOKED, COMPLETED, CANCELLED, NO_SHOW

BUSINESS RULES
1. appointment_id must be a non-blank string. patient must be a Patient, practitioner must be a Practitioner, date must be a datetime.date (not a datetime), time must be a datetime.time. Reject invalid input with TypeError or ValueError.
2. A new appointment always starts as BOOKED.
3. Allowed transitions: BOOKED -> COMPLETED, CANCELLED or NO_SHOW. COMPLETED, CANCELLED and NO_SHOW are final. Any other transition, including cancelling an already-cancelled appointment, raises InvalidStatusTransitionError and leaves the status unchanged.
4. cancel() changes the status to CANCELLED. Cancelled appointments are never deleted; the object remains for appointment history.
5. conflicts_with() returns True only when both appointments have the same practitioner, same date and same time, and neither is CANCELLED.
6. Status must not be publicly settable. Store it privately, expose it as a read-only property, and only change it through cancel() or update_status().

CONSTRAINTS
- Python 3.10+, standard library only.
- No database, file I/O, persistence, UI, printing, logging, notifications, or service/repository/manager classes.
- No inheritance except Enum and Exception.
- Do not add public attributes or methods that are not in the UML above.
- Type hints on everything; short docstrings.

OUTPUT
1. The complete code for one file, appointment.py.
2. A short list of every decision you made that is not directly visible in the UML or rules above, with the reason for each.

"""Appointment domain class for SmartCare.

Implements only the Appointment class, the AppointmentStatus enum and the
InvalidStatusTransitionError exception, per the approved UML. Patient and
Practitioner are treated as existing, unmodified dependencies.
"""

from __future__ import annotations

import datetime
from enum import Enum, auto

from patient import Patient
from practitioner import Practitioner


class AppointmentStatus(Enum):
    """Lifecycle states of an Appointment."""

    BOOKED = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    NO_SHOW = auto()


class InvalidStatusTransitionError(Exception):
    """Raised when an Appointment's status is changed to a disallowed value."""

    def __init__(self, current: AppointmentStatus, requested: AppointmentStatus) -> None:
        """Build a message describing the disallowed current -> requested move."""
        message = f"Cannot transition appointment from {current.name} to {requested.name}."
        super().__init__(message)
        self.current: AppointmentStatus = current
        self.requested: AppointmentStatus = requested


class Appointment:
    """A scheduled meeting between a Patient and a Practitioner."""

    # Statuses reachable from each status. BOOKED is the only non-final
    # status; COMPLETED, CANCELLED and NO_SHOW are terminal (empty targets).
    _ALLOWED_TRANSITIONS: dict[AppointmentStatus, frozenset[AppointmentStatus]] = {
        AppointmentStatus.BOOKED: frozenset(
            {
                AppointmentStatus.COMPLETED,
                AppointmentStatus.CANCELLED,
                AppointmentStatus.NO_SHOW,
            }
        ),
        AppointmentStatus.COMPLETED: frozenset(),
        AppointmentStatus.CANCELLED: frozenset(),
        AppointmentStatus.NO_SHOW: frozenset(),
    }

    def __init__(
        self,
        appointment_id: str,
        date: datetime.date,
        time: datetime.time,
        patient: Patient,
        practitioner: Practitioner,
    ) -> None:
        """Create a new appointment. Status always starts as BOOKED."""
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("appointment_id must be a non-blank string.")
        if isinstance(date, datetime.datetime) or not isinstance(date, datetime.date):
            raise TypeError("date must be a datetime.date (not a datetime).")
        if not isinstance(time, datetime.time):
            raise TypeError("time must be a datetime.time.")
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient instance.")
        if not isinstance(practitioner, Practitioner):
            raise TypeError("practitioner must be a Practitioner instance.")

        self._appointment_id: str = appointment_id
        self._date: datetime.date = date
        self._time: datetime.time = time
        self._patient: Patient = patient
        self._practitioner: Practitioner = practitioner
        self._status: AppointmentStatus = AppointmentStatus.BOOKED

    @property
    def appointment_id(self) -> str:
        """Unique identifier of the appointment."""
        return self._appointment_id

    @property
    def date(self) -> datetime.date:
        """Calendar date of the appointment."""
        return self._date

    @property
    def time(self) -> datetime.time:
        """Time of day of the appointment."""
        return self._time

    @property
    def patient(self) -> Patient:
        """Patient attending the appointment."""
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        """Practitioner running the appointment."""
        return self._practitioner

    @property
    def status(self) -> AppointmentStatus:
        """Current status. Read-only; change via cancel() or update_status()."""
        return self._status

    def cancel(self) -> None:
        """Cancel the appointment.

        Raises InvalidStatusTransitionError if the appointment is not
        currently BOOKED (e.g. it is already CANCELLED or otherwise final).
        The appointment object is never deleted, only marked CANCELLED.
        """
        self.update_status(AppointmentStatus.CANCELLED)

    def update_status(self, new_status: AppointmentStatus) -> None:
        """Move the appointment to new_status if that transition is allowed.

        Raises TypeError if new_status is not an AppointmentStatus, or
        InvalidStatusTransitionError if the move is not permitted, leaving
        the current status unchanged.
        """
        if not isinstance(new_status, AppointmentStatus):
            raise TypeError("new_status must be an AppointmentStatus.")
        if new_status not in self._ALLOWED_TRANSITIONS[self._status]:
            raise InvalidStatusTransitionError(self._status, new_status)
        self._status = new_status

    def conflicts_with(self, other: Appointment) -> bool:
        """True if both appointments share a practitioner, date and time.

        Returns False if either appointment is CANCELLED, since a cancelled
        slot no longer occupies the practitioner's schedule.
        """
        if not isinstance(other, Appointment):
            raise TypeError("other must be an Appointment.")
        if self.status is AppointmentStatus.CANCELLED or other.status is AppointmentStatus.CANCELLED:
            return False
        return (
            self.practitioner == other.practitioner
            and self.date == other.date
            and self.time == other.time
        )