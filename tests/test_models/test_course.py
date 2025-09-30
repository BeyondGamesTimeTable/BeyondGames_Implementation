"""Tests for the Course model."""

import pytest
from timetable_scheduler.models.course import Course, CourseType


def test_course_creation():
    """Test basic course creation."""
    course = Course(
        id="CS101",
        name="Introduction to Programming", 
        code="CS101",
        credits=4,
        duration=60,
        course_type=CourseType.LECTURE,
        capacity=60
    )
    
    assert course.id == "CS101"
    assert course.name == "Introduction to Programming"
    assert course.code == "CS101"
    assert course.credits == 4
    assert course.duration == 60
    assert course.course_type == CourseType.LECTURE
    assert course.capacity == 60
    assert course.required_equipment == []
    assert course.prerequisites == []
    assert course.is_elective is False
    assert course.semester == 1
    assert course.branch == "CSE"


def test_course_with_equipment():
    """Test course creation with required equipment."""
    course = Course(
        id="CS101L",
        name="Programming Lab",
        code="CS101L", 
        credits=2,
        duration=120,
        course_type=CourseType.LABORATORY,
        capacity=30,
        required_equipment=["computers", "projector"]
    )
    
    assert course.has_equipment_requirement("computers")
    assert course.has_equipment_requirement("projector") 
    assert not course.has_equipment_requirement("whiteboard")


def test_course_prerequisites():
    """Test course prerequisite functionality."""
    course = Course(
        id="CS201",
        name="Data Structures",
        code="CS201",
        credits=4,
        duration=60,
        course_type=CourseType.LECTURE,
        capacity=60,
        prerequisites=["CS101", "MA101"]
    )
    
    # Test with all prerequisites satisfied
    completed = ["CS101", "MA101", "PH101"]
    assert course.is_prerequisite_satisfied(completed)
    
    # Test with missing prerequisite
    completed = ["CS101"]
    assert not course.is_prerequisite_satisfied(completed)
    
    # Test with no prerequisites
    course_no_prereq = Course(
        id="CS101",
        name="Intro to Programming",
        code="CS101",
        credits=4,
        duration=60,
        course_type=CourseType.LECTURE,
        capacity=60
    )
    assert course_no_prereq.is_prerequisite_satisfied([])


def test_sessions_per_week():
    """Test sessions per week calculation."""
    # Lecture course
    lecture = Course(
        id="CS101",
        name="Programming",
        code="CS101",
        credits=4,
        duration=60,
        course_type=CourseType.LECTURE,
        capacity=60
    )
    assert lecture.get_sessions_per_week() == 2  # 4 credits / 2
    
    # Laboratory course
    lab = Course(
        id="CS101L", 
        name="Programming Lab",
        code="CS101L",
        credits=3,
        duration=120,
        course_type=CourseType.LABORATORY,
        capacity=30
    )
    assert lab.get_sessions_per_week() == 3  # Equal to credits for labs
    
    # Tutorial course
    tutorial = Course(
        id="CS101T",
        name="Programming Tutorial", 
        code="CS101T",
        credits=1,
        duration=60,
        course_type=CourseType.TUTORIAL,
        capacity=30
    )
    assert tutorial.get_sessions_per_week() == 1  # Always 1 for tutorials


def test_course_string_representations():
    """Test string representations of course."""
    course = Course(
        id="CS101",
        name="Introduction to Programming",
        code="CS101",
        credits=4,
        duration=60,
        course_type=CourseType.LECTURE,
        capacity=60
    )
    
    expected_str = "CS101: Introduction to Programming (4 credits)"
    assert str(course) == expected_str
    
    expected_repr = ("Course(id='CS101', code='CS101', "
                     "name='Introduction to Programming', credits=4, "
                     "type=lecture)")
    assert repr(course) == expected_repr