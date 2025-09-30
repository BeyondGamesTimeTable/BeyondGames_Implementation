"""Data validation utilities."""

from typing import List, Dict, Any, Tuple, Optional
from ..models import Course, Professor, Room, TimeSlot


def validate_course_data(course_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate course data dictionary.
    
    Args:
        course_data: Dictionary containing course information
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    required_fields = ['id', 'name', 'code', 'credits', 'duration', 'course_type', 'capacity']
    
    # Check required fields
    for field in required_fields:
        if field not in course_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate field types and values
    if 'credits' in course_data:
        if not isinstance(course_data['credits'], int) or course_data['credits'] <= 0:
            errors.append("Credits must be a positive integer")
    
    if 'duration' in course_data:
        if not isinstance(course_data['duration'], int) or course_data['duration'] <= 0:
            errors.append("Duration must be a positive integer")
    
    if 'capacity' in course_data:
        if not isinstance(course_data['capacity'], int) or course_data['capacity'] <= 0:
            errors.append("Capacity must be a positive integer")
    
    return len(errors) == 0, errors


def validate_professor_data(professor_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate professor data dictionary.
    
    Args:
        professor_data: Dictionary containing professor information
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    required_fields = ['id', 'name', 'email', 'department', 'designation']
    
    # Check required fields
    for field in required_fields:
        if field not in professor_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate email format (basic check)
    if 'email' in professor_data:
        email = professor_data['email']
        if not isinstance(email, str) or '@' not in email:
            errors.append("Invalid email format")
    
    # Validate max hours per week
    if 'max_hours_per_week' in professor_data:
        hours = professor_data['max_hours_per_week']
        if not isinstance(hours, int) or hours <= 0 or hours > 60:
            errors.append("Max hours per week must be between 1 and 60")
    
    return len(errors) == 0, errors


def validate_room_data(room_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate room data dictionary.
    
    Args:
        room_data: Dictionary containing room information
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    required_fields = ['id', 'name', 'building', 'floor', 'capacity', 'room_type']
    
    # Check required fields
    for field in required_fields:
        if field not in room_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate capacity
    if 'capacity' in room_data:
        capacity = room_data['capacity']
        if not isinstance(capacity, int) or capacity <= 0:
            errors.append("Capacity must be a positive integer")
    
    # Validate floor
    if 'floor' in room_data:
        floor = room_data['floor']
        if not isinstance(floor, int):
            errors.append("Floor must be an integer")
    
    return len(errors) == 0, errors


def validate_schedule_data(courses: List[Course], professors: List[Professor], 
                         rooms: List[Room], time_slots: List[TimeSlot]) -> Tuple[bool, List[str]]:
    """
    Validate that the input data is sufficient for scheduling.
    
    Args:
        courses: List of courses to schedule
        professors: List of available professors
        rooms: List of available rooms
        time_slots: List of available time slots
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Basic existence checks
    if not courses:
        errors.append("No courses provided for scheduling")
    if not professors:
        errors.append("No professors provided for scheduling")
    if not rooms:
        errors.append("No rooms provided for scheduling")
    if not time_slots:
        errors.append("No time slots provided for scheduling")
    
    # Check for duplicate IDs
    course_ids = [c.id for c in courses]
    if len(course_ids) != len(set(course_ids)):
        errors.append("Duplicate course IDs found")
    
    professor_ids = [p.id for p in professors]
    if len(professor_ids) != len(set(professor_ids)):
        errors.append("Duplicate professor IDs found")
    
    room_ids = [r.id for r in rooms]
    if len(room_ids) != len(set(room_ids)):
        errors.append("Duplicate room IDs found")
    
    time_slot_ids = [ts.id for ts in time_slots]
    if len(time_slot_ids) != len(set(time_slot_ids)):
        errors.append("Duplicate time slot IDs found")
    
    # Check if there are enough resources
    total_course_sessions = sum(c.get_sessions_per_week() for c in courses)
    available_slots = len([ts for ts in time_slots if ts.is_active])
    
    if total_course_sessions > available_slots:
        errors.append(f"Not enough time slots: need {total_course_sessions}, have {available_slots}")
    
    return len(errors) == 0, errors