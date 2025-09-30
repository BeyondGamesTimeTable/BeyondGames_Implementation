"""Course model for representing academic courses."""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class CourseType(Enum):
    """Types of courses available."""
    LECTURE = "lecture"
    LABORATORY = "laboratory"
    TUTORIAL = "tutorial"
    SEMINAR = "seminar"


@dataclass
class Course:
    """
    Represents an academic course in the timetable system.
    
    Attributes:
        id: Unique identifier for the course
        name: Full name of the course
        code: Course code (e.g., "CS101")
        credits: Number of credits for the course
        duration: Duration of each class session in minutes
        course_type: Type of course (lecture, lab, etc.)
        capacity: Maximum number of students
        professor_id: ID of the assigned professor
        required_equipment: List of equipment needed
        prerequisites: List of prerequisite course IDs
        is_elective: Whether the course is an elective
        semester: Target semester (1-8)
        branch: Department/branch (CSE, ECE, etc.)
    """
    
    id: str
    name: str
    code: str
    credits: int
    duration: int  # in minutes
    course_type: CourseType
    capacity: int
    professor_id: Optional[str] = None
    required_equipment: List[str] = None
    prerequisites: List[str] = None
    is_elective: bool = False
    semester: int = 1
    branch: str = "CSE"
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.required_equipment is None:
            self.required_equipment = []
        if self.prerequisites is None:
            self.prerequisites = []
    
    def has_equipment_requirement(self, equipment: str) -> bool:
        """Check if course requires specific equipment."""
        return equipment.lower() in [eq.lower() for eq in self.required_equipment]
    
    def is_prerequisite_satisfied(self, completed_courses: List[str]) -> bool:
        """Check if all prerequisites are satisfied."""
        return all(prereq in completed_courses for prereq in self.prerequisites)
    
    def get_sessions_per_week(self) -> int:
        """Calculate number of sessions per week based on credits and type."""
        if self.course_type == CourseType.LABORATORY:
            return self.credits  # Labs typically meet for number of sessions equal to credits
        elif self.course_type == CourseType.LECTURE:
            return max(1, self.credits // 2)  # Lectures typically 1-2 times per week
        else:
            return 1  # Tutorials and seminars typically once per week
    
    def __str__(self) -> str:
        """String representation of the course."""
        return f"{self.code}: {self.name} ({self.credits} credits)"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Course(id='{self.id}', code='{self.code}', "
                f"name='{self.name}', credits={self.credits}, "
                f"type={self.course_type.value})")