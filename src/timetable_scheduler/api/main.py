"""Main FastAPI application for the timetable scheduler."""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import uvicorn

from ..models import Course, Professor, Room, TimeSlot, Schedule
from ..schedulers import GeneticScheduler, ConstraintSatisfactionScheduler
from ..utils.config_loader import load_config
from ..utils.logger import setup_logger
from .schemas import (
    CourseCreate, CourseResponse,
    ProfessorCreate, ProfessorResponse,
    RoomCreate, RoomResponse,
    TimeSlotCreate, TimeSlotResponse,
    ScheduleRequest, ScheduleResponse,
    SchedulingConfig
)

# Initialize logger
logger = setup_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="IIIT Dharwad Timetable Scheduler API",
    description="Automatic Timetable Scheduling System for IIIT Dharwad",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration
try:
    config = load_config("default")
except Exception as e:
    logger.warning(f"Could not load config: {e}")
    config = {}

# Global storage (in production, use a proper database)
data_store = {
    "courses": {},
    "professors": {},
    "rooms": {},
    "time_slots": {},
    "schedules": {}
}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "IIIT Dharwad Timetable Scheduler API",
        "version": "0.1.0",
        "documentation": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2025-09-30T00:00:00Z"}


# Course endpoints
@app.post("/courses/", response_model=CourseResponse)
async def create_course(course: CourseCreate):
    """Create a new course."""
    try:
        course_obj = Course(
            id=course.id,
            name=course.name,
            code=course.code,
            credits=course.credits,
            duration=course.duration,
            course_type=course.course_type,
            capacity=course.capacity,
            professor_id=course.professor_id,
            required_equipment=course.required_equipment or [],
            prerequisites=course.prerequisites or [],
            is_elective=course.is_elective,
            semester=course.semester,
            branch=course.branch
        )
        
        data_store["courses"][course.id] = course_obj
        logger.info(f"Created course: {course.code}")
        
        return CourseResponse.from_course(course_obj)
    except Exception as e:
        logger.error(f"Failed to create course: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses/", response_model=List[CourseResponse])
async def get_courses():
    """Get all courses."""
    return [CourseResponse.from_course(course) for course in data_store["courses"].values()]


@app.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    """Get a specific course by ID."""
    if course_id not in data_store["courses"]:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course = data_store["courses"][course_id]
    return CourseResponse.from_course(course)


@app.delete("/courses/{course_id}")
async def delete_course(course_id: str):
    """Delete a course."""
    if course_id not in data_store["courses"]:
        raise HTTPException(status_code=404, detail="Course not found")
    
    del data_store["courses"][course_id]
    logger.info(f"Deleted course: {course_id}")
    return {"message": "Course deleted successfully"}


# Professor endpoints
@app.post("/professors/", response_model=ProfessorResponse)
async def create_professor(professor: ProfessorCreate):
    """Create a new professor."""
    try:
        professor_obj = Professor(
            id=professor.id,
            name=professor.name,
            email=professor.email,
            department=professor.department,
            designation=professor.designation,
            specializations=professor.specializations or [],
            max_hours_per_week=professor.max_hours_per_week,
            max_courses=professor.max_courses,
            office_location=professor.office_location,
            phone=professor.phone,
            is_active=professor.is_active
        )
        
        data_store["professors"][professor.id] = professor_obj
        logger.info(f"Created professor: {professor.name}")
        
        return ProfessorResponse.from_professor(professor_obj)
    except Exception as e:
        logger.error(f"Failed to create professor: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/professors/", response_model=List[ProfessorResponse])
async def get_professors():
    """Get all professors."""
    return [ProfessorResponse.from_professor(prof) for prof in data_store["professors"].values()]


# Room endpoints
@app.post("/rooms/", response_model=RoomResponse)
async def create_room(room: RoomCreate):
    """Create a new room."""
    try:
        room_obj = Room(
            id=room.id,
            name=room.name,
            building=room.building,
            floor=room.floor,
            capacity=room.capacity,
            room_type=room.room_type,
            features=room.features or [],
            is_accessible=room.is_accessible,
            is_available=room.is_available,
            dedicated_department=room.dedicated_department,
            booking_priority=room.booking_priority,
            notes=room.notes
        )
        
        data_store["rooms"][room.id] = room_obj
        logger.info(f"Created room: {room.name}")
        
        return RoomResponse.from_room(room_obj)
    except Exception as e:
        logger.error(f"Failed to create room: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/rooms/", response_model=List[RoomResponse])
async def get_rooms():
    """Get all rooms."""
    return [RoomResponse.from_room(room) for room in data_store["rooms"].values()]


# Time slot endpoints
@app.post("/time-slots/", response_model=TimeSlotResponse)
async def create_time_slot(time_slot: TimeSlotCreate):
    """Create a new time slot."""
    try:
        time_slot_obj = TimeSlot(
            id=time_slot.id,
            day=time_slot.day,
            start_time=time_slot.start_time,
            end_time=time_slot.end_time,
            slot_type=time_slot.slot_type,
            duration_minutes=time_slot.duration_minutes,
            is_active=time_slot.is_active,
            break_after=time_slot.break_after,
            priority=time_slot.priority,
            name=time_slot.name,
            academic_period=time_slot.academic_period
        )
        
        data_store["time_slots"][time_slot.id] = time_slot_obj
        logger.info(f"Created time slot: {time_slot.id}")
        
        return TimeSlotResponse.from_time_slot(time_slot_obj)
    except Exception as e:
        logger.error(f"Failed to create time slot: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/time-slots/", response_model=List[TimeSlotResponse])
async def get_time_slots():
    """Get all time slots."""
    return [TimeSlotResponse.from_time_slot(ts) for ts in data_store["time_slots"].values()]


# Scheduling endpoints
@app.post("/schedule/generate", response_model=ScheduleResponse)
async def generate_schedule(request: ScheduleRequest):
    """Generate a new timetable schedule."""
    try:
        # Get data from store
        courses = list(data_store["courses"].values())
        professors = list(data_store["professors"].values())
        rooms = list(data_store["rooms"].values())
        time_slots = list(data_store["time_slots"].values())
        
        if not all([courses, professors, rooms, time_slots]):
            raise HTTPException(
                status_code=400, 
                detail="Insufficient data: need at least one course, professor, room, and time slot"
            )
        
        # Choose scheduler based on algorithm
        if request.algorithm == "genetic":
            scheduler = GeneticScheduler(request.config.dict() if request.config else {})
        elif request.algorithm == "constraint_satisfaction":
            scheduler = ConstraintSatisfactionScheduler(request.config.dict() if request.config else {})
        else:
            raise HTTPException(status_code=400, detail="Invalid algorithm specified")
        
        # Set data and generate schedule
        scheduler.set_data(courses, professors, rooms, time_slots)
        schedule = scheduler.generate_schedule()
        
        # Store the generated schedule
        data_store["schedules"][schedule.id] = schedule
        
        logger.info(f"Generated schedule: {schedule.id} using {request.algorithm}")
        
        return ScheduleResponse.from_schedule(schedule)
    
    except Exception as e:
        logger.error(f"Failed to generate schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schedules/", response_model=List[ScheduleResponse])
async def get_schedules():
    """Get all generated schedules."""
    return [ScheduleResponse.from_schedule(schedule) for schedule in data_store["schedules"].values()]


@app.get("/schedules/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: str):
    """Get a specific schedule by ID."""
    if schedule_id not in data_store["schedules"]:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule = data_store["schedules"][schedule_id]
    return ScheduleResponse.from_schedule(schedule)


@app.post("/schedules/{schedule_id}/validate")
async def validate_schedule(schedule_id: str):
    """Validate a specific schedule."""
    if schedule_id not in data_store["schedules"]:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule = data_store["schedules"][schedule_id]
    
    # Basic validation
    is_valid = not schedule.has_conflicts()
    conflict_count = schedule.get_conflict_count()
    
    return {
        "schedule_id": schedule_id,
        "is_valid": is_valid,
        "conflict_count": conflict_count,
        "total_assignments": len(schedule.assignments)
    }


@app.delete("/data/clear")
async def clear_all_data():
    """Clear all stored data (useful for testing)."""
    data_store.clear()
    data_store.update({
        "courses": {},
        "professors": {},
        "rooms": {},
        "time_slots": {},
        "schedules": {}
    })
    logger.info("Cleared all data")
    return {"message": "All data cleared successfully"}


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "timetable_scheduler.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )