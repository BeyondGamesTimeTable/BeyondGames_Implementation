"""Base scheduler class defining the interface for all scheduling algorithms."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..models import Course, Professor, Room, TimeSlot, Schedule


class BaseScheduler(ABC):
    """
    Abstract base class for all timetable scheduling algorithms.
    
    This class defines the common interface that all scheduling algorithms
    must implement, ensuring consistency across different approaches.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the scheduler with configuration parameters.
        
        Args:
            config: Dictionary containing algorithm-specific configuration
        """
        self.config = config or {}
        self.courses: List[Course] = []
        self.professors: List[Professor] = []
        self.rooms: List[Room] = []
        self.time_slots: List[TimeSlot] = []
        self.constraints: List[Any] = []
        
    def set_data(self, courses: List[Course], professors: List[Professor], 
                 rooms: List[Room], time_slots: List[TimeSlot]):
        """
        Set the input data for scheduling.
        
        Args:
            courses: List of courses to be scheduled
            professors: List of available professors
            rooms: List of available rooms
            time_slots: List of available time slots
        """
        self.courses = courses
        self.professors = professors
        self.rooms = rooms
        self.time_slots = time_slots
        
    def add_constraint(self, constraint: Any):
        """
        Add a scheduling constraint.
        
        Args:
            constraint: Constraint object to be added
        """
        self.constraints.append(constraint)
        
    @abstractmethod
    def generate_schedule(self) -> Schedule:
        """
        Generate a complete timetable schedule.
        
        Returns:
            Schedule object containing the generated timetable
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    def validate_schedule(self, schedule: Schedule) -> bool:
        """
        Validate if a schedule satisfies all constraints.
        
        Args:
            schedule: Schedule to validate
            
        Returns:
            True if schedule is valid, False otherwise
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    def optimize_schedule(self, schedule: Schedule) -> Schedule:
        """
        Optimize an existing schedule to improve quality metrics.
        
        Args:
            schedule: Existing schedule to optimize
            
        Returns:
            Optimized schedule
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        pass
    
    def get_algorithm_name(self) -> str:
        """
        Get the name of the scheduling algorithm.
        
        Returns:
            String name of the algorithm
        """
        return self.__class__.__name__
    
    def get_configuration(self) -> Dict[str, Any]:
        """
        Get the current configuration of the scheduler.
        
        Returns:
            Dictionary containing configuration parameters
        """
        return self.config.copy()
    
    def update_configuration(self, new_config: Dict[str, Any]):
        """
        Update the scheduler configuration.
        
        Args:
            new_config: Dictionary containing new configuration parameters
        """
        self.config.update(new_config)
        
    def preprocess_data(self):
        """
        Preprocess input data before scheduling.
        
        This method can be overridden by subclasses to perform
        algorithm-specific preprocessing steps.
        """
        # Sort courses by priority (e.g., number of credits, year)
        self.courses.sort(key=lambda c: (c.semester, -c.credits, c.code))
        
        # Sort professors by availability
        self.professors.sort(key=lambda p: (p.department, p.name))
        
        # Sort rooms by capacity and type
        self.rooms.sort(key=lambda r: (r.room_type.value, -r.capacity))
        
        # Sort time slots by day and start time
        self.time_slots.sort(key=lambda ts: (ts.day.value, ts.start_time))
    
    def calculate_schedule_quality(self, schedule: Schedule) -> float:
        """
        Calculate a quality score for the schedule.
        
        Args:
            schedule: Schedule to evaluate
            
        Returns:
            Quality score (higher is better)
        """
        if not schedule or not schedule.assignments:
            return 0.0
            
        total_score = 0.0
        total_assignments = len(schedule.assignments)
        
        for assignment in schedule.assignments:
            # Basic scoring factors
            score = 1.0  # Base score for successful assignment
            
            # Time preference bonus
            time_slot = next((ts for ts in self.time_slots if ts.id == assignment.time_slot_id), None)
            if time_slot:
                score += time_slot.get_time_preference_score() * 0.2
            
            # Professor availability bonus
            professor = next((p for p in self.professors if p.id == assignment.professor_id), None)
            if professor and time_slot:
                score += professor.get_preference_score(assignment.time_slot_id) * 0.3
            
            # Room suitability bonus
            room = next((r for r in self.rooms if r.id == assignment.room_id), None)
            course = next((c for c in self.courses if c.id == assignment.course_id), None)
            if room and course:
                # Estimate course enrollment (could be actual data)
                estimated_enrollment = course.capacity if hasattr(course, 'capacity') else 30
                suitability = room.get_suitability_score(
                    course.course_type.value, estimated_enrollment, course.required_equipment
                )
                score += suitability * 0.2
            
            total_score += score
            
        return total_score / total_assignments if total_assignments > 0 else 0.0
    
    def get_statistics(self, schedule: Schedule) -> Dict[str, Any]:
        """
        Get statistics about the generated schedule.
        
        Args:
            schedule: Schedule to analyze
            
        Returns:
            Dictionary containing various statistics
        """
        if not schedule or not schedule.assignments:
            return {"total_assignments": 0, "courses_scheduled": 0}
        
        stats = {
            "total_assignments": len(schedule.assignments),
            "courses_scheduled": len(set(a.course_id for a in schedule.assignments)),
            "professors_assigned": len(set(a.professor_id for a in schedule.assignments)),
            "rooms_used": len(set(a.room_id for a in schedule.assignments)),
            "time_slots_used": len(set(a.time_slot_id for a in schedule.assignments)),
            "quality_score": self.calculate_schedule_quality(schedule),
            "algorithm": self.get_algorithm_name(),
        }
        
        # Calculate room utilization
        room_usage = {}
        for assignment in schedule.assignments:
            room_usage[assignment.room_id] = room_usage.get(assignment.room_id, 0) + 1
        
        if room_usage:
            stats["avg_room_utilization"] = sum(room_usage.values()) / len(room_usage)
            stats["max_room_usage"] = max(room_usage.values())
        
        return stats