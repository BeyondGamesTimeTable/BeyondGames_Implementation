"""Models package for timetable scheduling system."""

from .course import Course
from .professor import Professor
from .room import Room
from .time_slot import TimeSlot
from .schedule import Schedule, Assignment
from .constraint import Constraint

__all__ = [
    "Course",
    "Professor", 
    "Room",
    "TimeSlot",
    "Schedule",
    "Assignment",
    "Constraint",
]