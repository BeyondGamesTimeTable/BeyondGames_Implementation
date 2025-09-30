"""Professor model for representing faculty members."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Set
from enum import Enum


class ProfessorType(Enum):
    """Types of professors."""
    PROFESSOR = "professor"
    ASSOCIATE_PROFESSOR = "associate_professor"
    ASSISTANT_PROFESSOR = "assistant_professor"
    VISITING_FACULTY = "visiting_faculty"
    ADJUNCT_FACULTY = "adjunct_faculty"


class Availability(Enum):
    """Availability status for time slots."""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    PREFERRED = "preferred"
    NOT_PREFERRED = "not_preferred"


@dataclass
class Professor:
    """
    Represents a professor/faculty member in the timetable system.
    
    Attributes:
        id: Unique identifier for the professor
        name: Full name of the professor
        email: Email address
        department: Department/branch (CSE, ECE, etc.)
        designation: Type of professor
        specializations: List of areas of expertise
        max_hours_per_week: Maximum teaching hours per week
        max_courses: Maximum number of courses that can be assigned
        preferred_time_slots: Dictionary mapping time slots to availability
        unavailable_slots: Set of time slots when professor is unavailable
        office_location: Office room number or location
        phone: Contact phone number
        is_active: Whether the professor is currently active
    """
    
    id: str
    name: str
    email: str
    department: str
    designation: ProfessorType
    specializations: List[str] = None
    max_hours_per_week: int = 20
    max_courses: int = 4
    preferred_time_slots: Dict[str, Availability] = None
    unavailable_slots: Set[str] = None
    office_location: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.specializations is None:
            self.specializations = []
        if self.preferred_time_slots is None:
            self.preferred_time_slots = {}
        if self.unavailable_slots is None:
            self.unavailable_slots = set()
    
    def can_teach_course(self, course_code: str, course_specialization: str = "") -> bool:
        """Check if professor can teach a specific course."""
        if not self.is_active:
            return False
        
        # Check if professor has relevant specialization
        if course_specialization and self.specializations:
            return any(spec.lower() in course_specialization.lower() 
                      for spec in self.specializations)
        
        # If no specific specialization required, professor can teach
        return True
    
    def is_available_at(self, time_slot_id: str) -> bool:
        """Check if professor is available at a specific time slot."""
        if time_slot_id in self.unavailable_slots:
            return False
        
        availability = self.preferred_time_slots.get(time_slot_id, Availability.AVAILABLE)
        return availability in [Availability.AVAILABLE, Availability.PREFERRED]
    
    def get_preference_score(self, time_slot_id: str) -> float:
        """
        Get preference score for a time slot.
        Returns: 1.0 for preferred, 0.5 for available, 0.0 for unavailable/not preferred
        """
        if time_slot_id in self.unavailable_slots:
            return 0.0
        
        availability = self.preferred_time_slots.get(time_slot_id, Availability.AVAILABLE)
        
        if availability == Availability.PREFERRED:
            return 1.0
        elif availability == Availability.AVAILABLE:
            return 0.5
        else:
            return 0.0
    
    def add_unavailable_slot(self, time_slot_id: str):
        """Mark a time slot as unavailable."""
        self.unavailable_slots.add(time_slot_id)
        # Remove from preferred slots if it exists
        if time_slot_id in self.preferred_time_slots:
            del self.preferred_time_slots[time_slot_id]
    
    def set_preference(self, time_slot_id: str, availability: Availability):
        """Set availability preference for a time slot."""
        if availability == Availability.UNAVAILABLE:
            self.add_unavailable_slot(time_slot_id)
        else:
            self.preferred_time_slots[time_slot_id] = availability
            # Remove from unavailable slots if it exists
            self.unavailable_slots.discard(time_slot_id)
    
    def get_weekly_load(self, assigned_courses: List[str]) -> int:
        """Calculate current weekly teaching load in hours."""
        # This would typically query the database for assigned courses
        # For now, return a placeholder calculation
        return len(assigned_courses) * 3  # Assuming 3 hours per course on average
    
    def can_accommodate_additional_course(self, course_hours: int) -> bool:
        """Check if professor can accommodate additional course load."""
        # This would calculate current load and check against maximum
        return True  # Placeholder implementation
    
    def __str__(self) -> str:
        """String representation of the professor."""
        return f"{self.name} ({self.designation.value}) - {self.department}"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Professor(id='{self.id}', name='{self.name}', "
                f"department='{self.department}', "
                f"designation={self.designation.value})")