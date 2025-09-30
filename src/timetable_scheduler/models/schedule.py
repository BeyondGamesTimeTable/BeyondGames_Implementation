"""Schedule and Assignment models for representing generated timetables."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class Assignment:
    """
    Represents a single class assignment in the timetable.
    
    Attributes:
        id: Unique identifier for the assignment
        course_id: ID of the assigned course
        professor_id: ID of the assigned professor
        room_id: ID of the assigned room
        time_slot_id: ID of the assigned time slot
        session_number: Session number for courses with multiple sessions
        metadata: Additional metadata about the assignment
    """
    
    id: str
    course_id: str
    professor_id: str
    room_id: str
    time_slot_id: str
    session_number: int = 1
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert assignment to dictionary representation."""
        return {
            "id": self.id,
            "course_id": self.course_id,
            "professor_id": self.professor_id,
            "room_id": self.room_id,
            "time_slot_id": self.time_slot_id,
            "session_number": self.session_number,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Assignment':
        """Create Assignment from dictionary representation."""
        return cls(
            id=data["id"],
            course_id=data["course_id"],
            professor_id=data["professor_id"],
            room_id=data["room_id"],
            time_slot_id=data["time_slot_id"],
            session_number=data.get("session_number", 1),
            metadata=data.get("metadata", {})
        )


@dataclass 
class Schedule:
    """
    Represents a complete timetable schedule.
    
    Attributes:
        id: Unique identifier for the schedule
        name: Display name for the schedule
        assignments: List of class assignments
        created_at: Timestamp when schedule was created
        algorithm_used: Name of the algorithm used to generate the schedule
        quality_score: Quality score of the schedule
        statistics: Statistics about the schedule
        constraints_satisfied: Number of constraints satisfied
        total_constraints: Total number of constraints
        metadata: Additional metadata about the schedule
    """
    
    id: str
    name: str
    assignments: List[Assignment]
    created_at: Optional[datetime] = None
    algorithm_used: Optional[str] = None
    quality_score: Optional[float] = None
    statistics: Optional[Dict[str, Any]] = None
    constraints_satisfied: int = 0
    total_constraints: int = 0
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.statistics is None:
            self.statistics = {}
        if self.metadata is None:
            self.metadata = {}
    
    def add_assignment(self, assignment: Assignment):
        """Add an assignment to the schedule."""
        self.assignments.append(assignment)
    
    def remove_assignment(self, assignment_id: str) -> bool:
        """
        Remove an assignment from the schedule.
        
        Args:
            assignment_id: ID of the assignment to remove
            
        Returns:
            True if assignment was removed, False if not found
        """
        for i, assignment in enumerate(self.assignments):
            if assignment.id == assignment_id:
                self.assignments.pop(i)
                return True
        return False
    
    def get_assignment_by_id(self, assignment_id: str) -> Optional[Assignment]:
        """Get an assignment by its ID."""
        for assignment in self.assignments:
            if assignment.id == assignment_id:
                return assignment
        return None
    
    def get_assignments_by_course(self, course_id: str) -> List[Assignment]:
        """Get all assignments for a specific course."""
        return [a for a in self.assignments if a.course_id == course_id]
    
    def get_assignments_by_professor(self, professor_id: str) -> List[Assignment]:
        """Get all assignments for a specific professor."""
        return [a for a in self.assignments if a.professor_id == professor_id]
    
    def get_assignments_by_room(self, room_id: str) -> List[Assignment]:
        """Get all assignments for a specific room.""" 
        return [a for a in self.assignments if a.room_id == room_id]
    
    def get_assignments_by_time_slot(self, time_slot_id: str) -> List[Assignment]:
        """Get all assignments for a specific time slot."""
        return [a for a in self.assignments if a.time_slot_id == time_slot_id]
    
    def has_conflicts(self) -> bool:
        """
        Check if the schedule has any conflicts.
        
        Returns:
            True if conflicts exist, False otherwise
        """
        # Check for professor conflicts (same professor, same time slot)
        professor_time_pairs = set()
        for assignment in self.assignments:
            pair = (assignment.professor_id, assignment.time_slot_id)
            if pair in professor_time_pairs:
                return True
            professor_time_pairs.add(pair)
        
        # Check for room conflicts (same room, same time slot)
        room_time_pairs = set()
        for assignment in self.assignments:
            pair = (assignment.room_id, assignment.time_slot_id)
            if pair in room_time_pairs:
                return True
            room_time_pairs.add(pair)
        
        return False
    
    def get_conflict_count(self) -> int:
        """
        Count the number of conflicts in the schedule.
        
        Returns:
            Number of conflicts found
        """
        conflicts = 0
        
        # Group assignments by time slot
        time_slot_assignments = {}
        for assignment in self.assignments:
            if assignment.time_slot_id not in time_slot_assignments:
                time_slot_assignments[assignment.time_slot_id] = []
            time_slot_assignments[assignment.time_slot_id].append(assignment)
        
        # Check for conflicts within each time slot
        for assignments in time_slot_assignments.values():
            if len(assignments) <= 1:
                continue
                
            # Check professor conflicts
            professors = [a.professor_id for a in assignments]
            conflicts += len(professors) - len(set(professors))
            
            # Check room conflicts  
            rooms = [a.room_id for a in assignments]
            conflicts += len(rooms) - len(set(rooms))
        
        return conflicts
    
    def get_utilization_stats(self) -> Dict[str, Any]:
        """
        Get utilization statistics for the schedule.
        
        Returns:
            Dictionary containing utilization statistics
        """
        if not self.assignments:
            return {"professors": {}, "rooms": {}, "time_slots": {}}
        
        professor_usage = {}
        room_usage = {}
        time_slot_usage = {}
        
        for assignment in self.assignments:
            professor_usage[assignment.professor_id] = professor_usage.get(assignment.professor_id, 0) + 1
            room_usage[assignment.room_id] = room_usage.get(assignment.room_id, 0) + 1
            time_slot_usage[assignment.time_slot_id] = time_slot_usage.get(assignment.time_slot_id, 0) + 1
        
        return {
            "professors": professor_usage,
            "rooms": room_usage, 
            "time_slots": time_slot_usage,
            "total_assignments": len(self.assignments),
            "unique_professors": len(professor_usage),
            "unique_rooms": len(room_usage),
            "unique_time_slots": len(time_slot_usage)
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert schedule to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "assignments": [a.to_dict() for a in self.assignments],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "algorithm_used": self.algorithm_used,
            "quality_score": self.quality_score,
            "statistics": self.statistics,
            "constraints_satisfied": self.constraints_satisfied,
            "total_constraints": self.total_constraints,
            "metadata": self.metadata
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert schedule to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Schedule':
        """Create Schedule from dictionary representation."""
        assignments = [Assignment.from_dict(a) for a in data.get("assignments", [])]
        
        created_at = None
        if data.get("created_at"):
            try:
                created_at = datetime.fromisoformat(data["created_at"])
            except (ValueError, TypeError):
                created_at = datetime.now()
        
        return cls(
            id=data["id"],
            name=data["name"],
            assignments=assignments,
            created_at=created_at,
            algorithm_used=data.get("algorithm_used"),
            quality_score=data.get("quality_score"),
            statistics=data.get("statistics", {}),
            constraints_satisfied=data.get("constraints_satisfied", 0),
            total_constraints=data.get("total_constraints", 0),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Schedule':
        """Create Schedule from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __len__(self) -> int:
        """Return the number of assignments in the schedule."""
        return len(self.assignments)
    
    def __str__(self) -> str:
        """String representation of the schedule."""
        return f"Schedule '{self.name}' with {len(self.assignments)} assignments"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Schedule(id='{self.id}', name='{self.name}', "
                f"assignments={len(self.assignments)}, "
                f"quality_score={self.quality_score})")