"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import time, datetime
from enum import Enum

from ..models.course import CourseType
from ..models.professor import ProfessorType
from ..models.room import RoomType, RoomFeature
from ..models.time_slot import DayOfWeek, SlotType


# Course schemas
class CourseCreate(BaseModel):
    """Schema for creating a new course."""
    id: str = Field(..., description="Unique course identifier")
    name: str = Field(..., description="Course name")
    code: str = Field(..., description="Course code (e.g., CS101)")
    credits: int = Field(..., ge=1, le=10, description="Number of credits")
    duration: int = Field(..., ge=30, le=240, description="Duration in minutes")
    course_type: CourseType = Field(..., description="Type of course")
    capacity: int = Field(..., ge=1, description="Maximum students")
    professor_id: Optional[str] = Field(None, description="Assigned professor ID")
    required_equipment: Optional[List[str]] = Field(None, description="Required equipment")
    prerequisites: Optional[List[str]] = Field(None, description="Prerequisite course IDs")
    is_elective: bool = Field(False, description="Is this an elective course")
    semester: int = Field(1, ge=1, le=8, description="Target semester")
    branch: str = Field("CSE", description="Department/branch")

    class Config:
        use_enum_values = True


class CourseResponse(BaseModel):
    """Schema for course response."""
    id: str
    name: str
    code: str
    credits: int
    duration: int
    course_type: str
    capacity: int
    professor_id: Optional[str]
    required_equipment: List[str]
    prerequisites: List[str]
    is_elective: bool
    semester: int
    branch: str

    @classmethod
    def from_course(cls, course) -> 'CourseResponse':
        """Create response from Course model."""
        return cls(
            id=course.id,
            name=course.name,
            code=course.code,
            credits=course.credits,
            duration=course.duration,
            course_type=course.course_type.value,
            capacity=course.capacity,
            professor_id=course.professor_id,
            required_equipment=course.required_equipment,
            prerequisites=course.prerequisites,
            is_elective=course.is_elective,
            semester=course.semester,
            branch=course.branch
        )


# Professor schemas
class ProfessorCreate(BaseModel):
    """Schema for creating a new professor."""
    id: str = Field(..., description="Unique professor identifier")
    name: str = Field(..., description="Professor's full name")
    email: str = Field(..., description="Email address")
    department: str = Field(..., description="Department/branch")
    designation: ProfessorType = Field(..., description="Professor type")
    specializations: Optional[List[str]] = Field(None, description="Areas of expertise")
    max_hours_per_week: int = Field(20, ge=1, le=60, description="Maximum teaching hours per week")
    max_courses: int = Field(4, ge=1, le=10, description="Maximum courses")
    office_location: Optional[str] = Field(None, description="Office location")
    phone: Optional[str] = Field(None, description="Phone number")
    is_active: bool = Field(True, description="Is professor active")

    class Config:
        use_enum_values = True


class ProfessorResponse(BaseModel):
    """Schema for professor response."""
    id: str
    name: str
    email: str
    department: str
    designation: str
    specializations: List[str]
    max_hours_per_week: int
    max_courses: int
    office_location: Optional[str]
    phone: Optional[str]
    is_active: bool

    @classmethod
    def from_professor(cls, professor) -> 'ProfessorResponse':
        """Create response from Professor model."""
        return cls(
            id=professor.id,
            name=professor.name,
            email=professor.email,
            department=professor.department,
            designation=professor.designation.value,
            specializations=professor.specializations,
            max_hours_per_week=professor.max_hours_per_week,
            max_courses=professor.max_courses,
            office_location=professor.office_location,
            phone=professor.phone,
            is_active=professor.is_active
        )


# Room schemas
class RoomCreate(BaseModel):
    """Schema for creating a new room."""
    id: str = Field(..., description="Unique room identifier")
    name: str = Field(..., description="Room name")
    building: str = Field(..., description="Building name")
    floor: int = Field(..., description="Floor number")
    capacity: int = Field(..., ge=1, description="Room capacity")
    room_type: RoomType = Field(..., description="Type of room")
    features: Optional[List[RoomFeature]] = Field(None, description="Available features")
    is_accessible: bool = Field(True, description="Is wheelchair accessible")
    is_available: bool = Field(True, description="Is available for scheduling")
    dedicated_department: Optional[str] = Field(None, description="Dedicated department")
    booking_priority: int = Field(1, ge=1, le=10, description="Booking priority")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        use_enum_values = True


class RoomResponse(BaseModel):
    """Schema for room response."""
    id: str
    name: str
    building: str
    floor: int
    capacity: int
    room_type: str
    features: List[str]
    is_accessible: bool
    is_available: bool
    dedicated_department: Optional[str]
    booking_priority: int
    notes: Optional[str]

    @classmethod
    def from_room(cls, room) -> 'RoomResponse':
        """Create response from Room model."""
        return cls(
            id=room.id,
            name=room.name,
            building=room.building,
            floor=room.floor,
            capacity=room.capacity,
            room_type=room.room_type.value,
            features=[f.value for f in room.features],
            is_accessible=room.is_accessible,
            is_available=room.is_available,
            dedicated_department=room.dedicated_department,
            booking_priority=room.booking_priority,
            notes=room.notes
        )


# Time slot schemas
class TimeSlotCreate(BaseModel):
    """Schema for creating a new time slot."""
    id: str = Field(..., description="Unique time slot identifier")
    day: DayOfWeek = Field(..., description="Day of the week")
    start_time: time = Field(..., description="Start time")
    end_time: time = Field(..., description="End time")
    slot_type: SlotType = Field(SlotType.REGULAR, description="Type of slot")
    duration_minutes: Optional[int] = Field(None, description="Duration in minutes")
    is_active: bool = Field(True, description="Is slot active")
    break_after: bool = Field(False, description="Is there a break after this slot")
    priority: int = Field(1, ge=1, le=5, description="Scheduling priority")
    name: Optional[str] = Field(None, description="Display name")
    academic_period: Optional[str] = Field(None, description="Academic period")

    class Config:
        use_enum_values = True
        json_encoders = {
            time: lambda v: v.strftime('%H:%M')
        }


class TimeSlotResponse(BaseModel):
    """Schema for time slot response."""
    id: str
    day: str
    start_time: str
    end_time: str
    slot_type: str
    duration_minutes: int
    is_active: bool
    break_after: bool
    priority: int
    name: Optional[str]
    academic_period: Optional[str]

    @classmethod
    def from_time_slot(cls, time_slot) -> 'TimeSlotResponse':
        """Create response from TimeSlot model."""
        return cls(
            id=time_slot.id,
            day=time_slot.day.value,
            start_time=time_slot.start_time.strftime('%H:%M'),
            end_time=time_slot.end_time.strftime('%H:%M'),
            slot_type=time_slot.slot_type.value,
            duration_minutes=time_slot.duration_minutes,
            is_active=time_slot.is_active,
            break_after=time_slot.break_after,
            priority=time_slot.priority,
            name=time_slot.name,
            academic_period=time_slot.academic_period
        )


# Assignment schema
class AssignmentResponse(BaseModel):
    """Schema for assignment response."""
    id: str
    course_id: str
    professor_id: str
    room_id: str
    time_slot_id: str
    session_number: int
    metadata: Dict[str, Any]

    @classmethod
    def from_assignment(cls, assignment) -> 'AssignmentResponse':
        """Create response from Assignment model."""
        return cls(
            id=assignment.id,
            course_id=assignment.course_id,
            professor_id=assignment.professor_id,
            room_id=assignment.room_id,
            time_slot_id=assignment.time_slot_id,
            session_number=assignment.session_number,
            metadata=assignment.metadata
        )


# Schedule schemas
class SchedulingConfig(BaseModel):
    """Configuration for scheduling algorithm."""
    population_size: Optional[int] = Field(50, description="Population size for genetic algorithm")
    generations: Optional[int] = Field(100, description="Number of generations")
    mutation_rate: Optional[float] = Field(0.1, description="Mutation rate")
    crossover_rate: Optional[float] = Field(0.8, description="Crossover rate")
    use_arc_consistency: Optional[bool] = Field(True, description="Use arc consistency in CSP")
    use_forward_checking: Optional[bool] = Field(True, description="Use forward checking in CSP")


class ScheduleRequest(BaseModel):
    """Schema for schedule generation request."""
    algorithm: str = Field(..., description="Algorithm to use (genetic or constraint_satisfaction)")
    config: Optional[SchedulingConfig] = Field(None, description="Algorithm configuration")
    name: Optional[str] = Field(None, description="Name for the generated schedule")


class ScheduleResponse(BaseModel):
    """Schema for schedule response."""
    id: str
    name: str
    assignments: List[AssignmentResponse]
    created_at: Optional[datetime]
    algorithm_used: Optional[str]
    quality_score: Optional[float]
    statistics: Dict[str, Any]
    constraints_satisfied: int
    total_constraints: int
    metadata: Dict[str, Any]

    @classmethod
    def from_schedule(cls, schedule) -> 'ScheduleResponse':
        """Create response from Schedule model."""
        return cls(
            id=schedule.id,
            name=schedule.name,
            assignments=[AssignmentResponse.from_assignment(a) for a in schedule.assignments],
            created_at=schedule.created_at,
            algorithm_used=schedule.algorithm_used,
            quality_score=schedule.quality_score,
            statistics=schedule.statistics,
            constraints_satisfied=schedule.constraints_satisfied,
            total_constraints=schedule.total_constraints,
            metadata=schedule.metadata
        )

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }