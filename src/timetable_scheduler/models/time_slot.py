"""Time slot model for representing scheduling time periods."""

from dataclasses import dataclass
from typing import Optional
from datetime import time, datetime
from enum import Enum


class DayOfWeek(Enum):
    """Days of the week."""
    MONDAY = "monday"
    TUESDAY = "tuesday"  
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class SlotType(Enum):
    """Types of time slots."""
    REGULAR = "regular"
    BREAK = "break"
    LUNCH = "lunch"
    EXTENDED = "extended"  # For labs or longer sessions


@dataclass
class TimeSlot:
    """
    Represents a time slot in the timetable system.
    
    Attributes:
        id: Unique identifier for the time slot
        day: Day of the week
        start_time: Start time of the slot
        end_time: End time of the slot
        slot_type: Type of time slot
        duration_minutes: Duration in minutes
        is_active: Whether the slot is available for scheduling
        break_after: Whether there's a break after this slot
        priority: Priority for scheduling (higher = preferred)
        name: Display name for the slot
        academic_period: Which academic period this belongs to
    """
    
    id: str
    day: DayOfWeek
    start_time: time
    end_time: time
    slot_type: SlotType = SlotType.REGULAR
    duration_minutes: Optional[int] = None
    is_active: bool = True
    break_after: bool = False
    priority: int = 1
    name: Optional[str] = None
    academic_period: Optional[str] = None
    
    def __post_init__(self):
        """Calculate duration and set default name if not provided."""
        if self.duration_minutes is None:
            # Calculate duration from start and end times
            start_dt = datetime.combine(datetime.today(), self.start_time)
            end_dt = datetime.combine(datetime.today(), self.end_time)
            
            # Handle next day scenarios
            if end_dt <= start_dt:
                end_dt = end_dt.replace(day=end_dt.day + 1)
            
            duration = end_dt - start_dt
            self.duration_minutes = int(duration.total_seconds() / 60)
        
        if self.name is None:
            self.name = f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this time slot overlaps with another time slot."""
        if self.day != other.day:
            return False
        
        # Check time overlap
        return (self.start_time < other.end_time and 
                self.end_time > other.start_time)
    
    def is_adjacent_to(self, other: 'TimeSlot') -> bool:
        """Check if this time slot is adjacent to another time slot."""
        if self.day != other.day:
            return False
        
        return (self.end_time == other.start_time or 
                self.start_time == other.end_time)
    
    def can_accommodate_duration(self, required_minutes: int) -> bool:
        """Check if this slot can accommodate a class of given duration."""
        return self.duration_minutes >= required_minutes
    
    def is_suitable_for_course_type(self, course_type: str) -> bool:
        """
        Check if this time slot is suitable for a specific course type.
        
        Args:
            course_type: Type of course (lecture, laboratory, etc.)
            
        Returns:
            True if suitable, False otherwise
        """
        if not self.is_active:
            return False
        
        # Break slots cannot be used for courses
        if self.slot_type in [SlotType.BREAK, SlotType.LUNCH]:
            return False
        
        # Laboratory courses might need extended slots
        if course_type.lower() == "laboratory":
            # Prefer extended slots for labs, but allow regular slots if needed
            return self.slot_type in [SlotType.REGULAR, SlotType.EXTENDED]
        
        return self.slot_type == SlotType.REGULAR
    
    def get_time_preference_score(self) -> float:
        """
        Get preference score based on time of day.
        
        Returns:
            Score between 0 and 1 (higher = more preferred)
        """
        hour = self.start_time.hour
        
        # Morning slots (9 AM - 12 PM) are generally preferred
        if 9 <= hour < 12:
            return 1.0
        # Early afternoon (12 PM - 2 PM) is good
        elif 12 <= hour < 14:
            return 0.8
        # Late afternoon (2 PM - 5 PM) is acceptable
        elif 14 <= hour < 17:
            return 0.6
        # Early morning (8 AM - 9 AM) is less preferred
        elif 8 <= hour < 9:
            return 0.4
        # Evening slots (after 5 PM) are least preferred
        else:
            return 0.2
    
    def format_time_range(self) -> str:
        """Format the time slot as a readable string."""
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    def to_dict(self) -> dict:
        """Convert time slot to dictionary representation."""
        return {
            "id": self.id,
            "day": self.day.value,
            "start_time": self.start_time.strftime('%H:%M'),
            "end_time": self.end_time.strftime('%H:%M'),
            "duration_minutes": self.duration_minutes,
            "slot_type": self.slot_type.value,
            "name": self.name,
            "is_active": self.is_active
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TimeSlot':
        """Create TimeSlot from dictionary representation."""
        return cls(
            id=data["id"],
            day=DayOfWeek(data["day"]),
            start_time=datetime.strptime(data["start_time"], '%H:%M').time(),
            end_time=datetime.strptime(data["end_time"], '%H:%M').time(),
            slot_type=SlotType(data.get("slot_type", "regular")),
            duration_minutes=data.get("duration_minutes"),
            name=data.get("name"),
            is_active=data.get("is_active", True)
        )
    
    def __str__(self) -> str:
        """String representation of the time slot."""
        return f"{self.day.value.title()} {self.format_time_range()}"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"TimeSlot(id='{self.id}', day={self.day.value}, "
                f"time='{self.format_time_range()}', "
                f"duration={self.duration_minutes}min)")