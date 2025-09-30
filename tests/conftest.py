"""Test configuration and fixtures."""

import pytest
from datetime import time
from typing import List

from timetable_scheduler.models import Course, Professor, Room, TimeSlot
from timetable_scheduler.models.course import CourseType
from timetable_scheduler.models.professor import ProfessorType
from timetable_scheduler.models.room import RoomType, RoomFeature
from timetable_scheduler.models.time_slot import DayOfWeek, SlotType


@pytest.fixture
def sample_courses() -> List[Course]:
    """Fixture providing sample courses for testing."""
    return [
        Course(
            id="CS101",
            name="Introduction to Programming",
            code="CS101", 
            credits=4,
            duration=60,
            course_type=CourseType.LECTURE,
            capacity=60,
            semester=1,
            branch="CSE"
        ),
        Course(
            id="CS101L",
            name="Programming Laboratory",
            code="CS101L",
            credits=2, 
            duration=120,
            course_type=CourseType.LABORATORY,
            capacity=30,
            required_equipment=["computers", "projector"],
            semester=1,
            branch="CSE"
        ),
        Course(
            id="MA101",
            name="Engineering Mathematics I",
            code="MA101",
            credits=4,
            duration=60, 
            course_type=CourseType.LECTURE,
            capacity=60,
            semester=1,
            branch="CSE"
        )
    ]


@pytest.fixture
def sample_professors() -> List[Professor]:
    """Fixture providing sample professors for testing."""
    return [
        Professor(
            id="PROF001",
            name="Dr. John Smith",
            email="john.smith@iiitdharwad.edu.in",
            department="CSE",
            designation=ProfessorType.PROFESSOR,
            specializations=["Programming", "Algorithms", "Software Engineering"],
            max_hours_per_week=18,
            max_courses=3
        ),
        Professor(
            id="PROF002", 
            name="Dr. Jane Doe",
            email="jane.doe@iiitdharwad.edu.in",
            department="Mathematics",
            designation=ProfessorType.ASSOCIATE_PROFESSOR,
            specializations=["Mathematics", "Statistics", "Discrete Mathematics"],
            max_hours_per_week=16,
            max_courses=3
        ),
        Professor(
            id="PROF003",
            name="Mr. Bob Wilson", 
            email="bob.wilson@iiitdharwad.edu.in",
            department="CSE",
            designation=ProfessorType.ASSISTANT_PROFESSOR,
            specializations=["Programming", "Web Development"],
            max_hours_per_week=20,
            max_courses=4
        )
    ]


@pytest.fixture
def sample_rooms() -> List[Room]:
    """Fixture providing sample rooms for testing."""
    return [
        Room(
            id="CR101",
            name="Classroom 101",
            building="Academic Block A",
            floor=1,
            capacity=60,
            room_type=RoomType.CLASSROOM,
            features=[RoomFeature.PROJECTOR, RoomFeature.WHITEBOARD, RoomFeature.AIR_CONDITIONING]
        ),
        Room(
            id="LAB201",
            name="Computer Lab 201", 
            building="Academic Block A",
            floor=2,
            capacity=30,
            room_type=RoomType.COMPUTER_LAB,
            features=[RoomFeature.COMPUTERS, RoomFeature.PROJECTOR, RoomFeature.AIR_CONDITIONING]
        ),
        Room(
            id="CR102",
            name="Classroom 102",
            building="Academic Block A", 
            floor=1,
            capacity=80,
            room_type=RoomType.CLASSROOM,
            features=[RoomFeature.PROJECTOR, RoomFeature.SMART_BOARD, RoomFeature.AUDIO_SYSTEM]
        )
    ]


@pytest.fixture
def sample_time_slots() -> List[TimeSlot]:
    """Fixture providing sample time slots for testing."""
    return [
        TimeSlot(
            id="MON_0900_1000",
            day=DayOfWeek.MONDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            slot_type=SlotType.REGULAR,
            priority=3
        ),
        TimeSlot(
            id="MON_1000_1100", 
            day=DayOfWeek.MONDAY,
            start_time=time(10, 0),
            end_time=time(11, 0),
            slot_type=SlotType.REGULAR,
            priority=3
        ),
        TimeSlot(
            id="MON_1400_1600",
            day=DayOfWeek.MONDAY, 
            start_time=time(14, 0),
            end_time=time(16, 0),
            slot_type=SlotType.EXTENDED,
            priority=2,
            duration_minutes=120
        ),
        TimeSlot(
            id="TUE_0900_1000",
            day=DayOfWeek.TUESDAY,
            start_time=time(9, 0),
            end_time=time(10, 0),
            slot_type=SlotType.REGULAR,
            priority=3
        ),
        TimeSlot(
            id="TUE_1000_1100",
            day=DayOfWeek.TUESDAY,
            start_time=time(10, 0), 
            end_time=time(11, 0),
            slot_type=SlotType.REGULAR,
            priority=3
        )
    ]