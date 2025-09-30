"""Room model for representing classroom and laboratory spaces."""

from dataclasses import dataclass
from typing import List, Optional, Set
from enum import Enum


class RoomType(Enum):
    """Types of rooms available."""
    CLASSROOM = "classroom"
    LABORATORY = "laboratory"
    COMPUTER_LAB = "computer_lab"
    SEMINAR_HALL = "seminar_hall"
    AUDITORIUM = "auditorium"
    TUTORIAL_ROOM = "tutorial_room"


class RoomFeature(Enum):
    """Available room features and equipment."""
    PROJECTOR = "projector"
    WHITEBOARD = "whiteboard"
    BLACKBOARD = "blackboard"
    SMART_BOARD = "smart_board"
    COMPUTERS = "computers"
    AIR_CONDITIONING = "air_conditioning"
    AUDIO_SYSTEM = "audio_system"
    MICROPHONE = "microphone"
    INTERNET = "internet"
    POWER_OUTLETS = "power_outlets"
    LABORATORY_EQUIPMENT = "laboratory_equipment"


@dataclass
class Room:
    """
    Represents a room/classroom in the timetable system.
    
    Attributes:
        id: Unique identifier for the room
        name: Display name of the room
        building: Building where the room is located
        floor: Floor number
        capacity: Maximum number of students the room can accommodate
        room_type: Type of room (classroom, lab, etc.)
        features: List of available features/equipment
        is_accessible: Whether the room is wheelchair accessible
        is_available: Whether the room is currently available for scheduling
        maintenance_slots: Set of time slot IDs when room is under maintenance
        dedicated_department: Department that has priority for this room
        booking_priority: Priority level for room booking (higher = more priority)
        notes: Additional notes about the room
    """
    
    id: str
    name: str
    building: str
    floor: int
    capacity: int
    room_type: RoomType
    features: List[RoomFeature] = None
    is_accessible: bool = True
    is_available: bool = True
    maintenance_slots: Set[str] = None
    dedicated_department: Optional[str] = None
    booking_priority: int = 1
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.features is None:
            self.features = []
        if self.maintenance_slots is None:
            self.maintenance_slots = set()
    
    def has_feature(self, feature: RoomFeature) -> bool:
        """Check if room has a specific feature."""
        return feature in self.features
    
    def has_all_features(self, required_features: List[RoomFeature]) -> bool:
        """Check if room has all required features."""
        return all(feature in self.features for feature in required_features)
    
    def is_suitable_for_course(self, course_type: str, required_capacity: int, 
                              required_equipment: List[str] = None) -> bool:
        """
        Check if room is suitable for a specific course.
        
        Args:
            course_type: Type of course (lecture, lab, etc.)
            required_capacity: Minimum capacity needed
            required_equipment: List of required equipment
            
        Returns:
            True if room is suitable, False otherwise
        """
        # Check if room is available
        if not self.is_available:
            return False
        
        # Check capacity
        if self.capacity < required_capacity:
            return False
        
        # Check room type compatibility
        if course_type.lower() == "laboratory":
            if self.room_type not in [RoomType.LABORATORY, RoomType.COMPUTER_LAB]:
                return False
        elif course_type.lower() == "lecture":
            if self.room_type in [RoomType.LABORATORY, RoomType.COMPUTER_LAB]:
                # Labs can be used for lectures if needed, but not preferred
                pass
        
        # Check required equipment
        if required_equipment:
            required_features = []
            for equipment in required_equipment:
                try:
                    feature = RoomFeature(equipment.lower())
                    required_features.append(feature)
                except ValueError:
                    # Equipment not found in standard features
                    continue
            
            if not self.has_all_features(required_features):
                return False
        
        return True
    
    def is_available_at(self, time_slot_id: str) -> bool:
        """Check if room is available at a specific time slot."""
        return (self.is_available and 
                time_slot_id not in self.maintenance_slots)
    
    def add_maintenance_slot(self, time_slot_id: str):
        """Mark a time slot as maintenance time."""
        self.maintenance_slots.add(time_slot_id)
    
    def remove_maintenance_slot(self, time_slot_id: str):
        """Remove a maintenance time slot."""
        self.maintenance_slots.discard(time_slot_id)
    
    def get_utilization_score(self, assigned_capacity: int) -> float:
        """
        Calculate room utilization score.
        
        Args:
            assigned_capacity: Number of students assigned to the room
            
        Returns:
            Utilization score between 0 and 1
        """
        if self.capacity == 0:
            return 0.0
        return min(assigned_capacity / self.capacity, 1.0)
    
    def get_suitability_score(self, course_type: str, capacity_needed: int, 
                             required_equipment: List[str] = None) -> float:
        """
        Calculate how suitable this room is for a given requirement.
        
        Returns:
            Score between 0 and 1 (higher = more suitable)
        """
        if not self.is_suitable_for_course(course_type, capacity_needed, required_equipment):
            return 0.0
        
        # Base score
        score = 0.5
        
        # Bonus for exact room type match
        if course_type.lower() == "laboratory" and self.room_type in [RoomType.LABORATORY, RoomType.COMPUTER_LAB]:
            score += 0.3
        elif course_type.lower() == "lecture" and self.room_type == RoomType.CLASSROOM:
            score += 0.3
        
        # Capacity efficiency bonus (prefer rooms that match capacity closely)
        if capacity_needed > 0:
            capacity_ratio = capacity_needed / self.capacity
            if 0.7 <= capacity_ratio <= 0.9:  # Optimal utilization range
                score += 0.2
            elif capacity_ratio > 0.9:
                score += 0.1  # High utilization, but less preferred
        
        return min(score, 1.0)
    
    def __str__(self) -> str:
        """String representation of the room."""
        return f"{self.name} ({self.building}, Floor {self.floor}) - Capacity: {self.capacity}"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Room(id='{self.id}', name='{self.name}', "
                f"building='{self.building}', capacity={self.capacity}, "
                f"type={self.room_type.value})")