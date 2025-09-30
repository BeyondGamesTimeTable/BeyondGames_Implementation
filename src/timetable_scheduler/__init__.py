"""
IIIT Dharwad Automatic Timetable Scheduling System

A comprehensive timetable scheduling solution that uses advanced algorithms
to generate optimal class schedules while respecting various constraints.
"""

__version__ = "0.1.0"
__author__ = "IIIT Dharwad"
__email__ = "contact@iiitdharwad.edu.in"

from .schedulers.base import BaseScheduler
from .schedulers.genetic import GeneticScheduler
from .schedulers.constraint_satisfaction import ConstraintSatisfactionScheduler

__all__ = [
    "BaseScheduler",
    "GeneticScheduler", 
    "ConstraintSatisfactionScheduler",
]