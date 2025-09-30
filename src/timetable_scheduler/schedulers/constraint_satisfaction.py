"""Constraint satisfaction scheduler implementation."""

from typing import List, Dict, Any, Optional, Set, Tuple
from ..models import Course, Professor, Room, TimeSlot, Schedule, Assignment
from .base import BaseScheduler


class ConstraintSatisfactionScheduler(BaseScheduler):
    """
    Constraint Satisfaction Problem (CSP) based timetable scheduler.
    
    This scheduler formulates timetable scheduling as a CSP and uses
    backtracking with constraint propagation to find valid solutions.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the CSP scheduler with configuration."""
        super().__init__(config)
        
        # CSP parameters
        self.use_arc_consistency = self.config.get('use_arc_consistency', True)
        self.use_forward_checking = self.config.get('use_forward_checking', True)
        self.variable_ordering = self.config.get('variable_ordering', 'mrv')  # Most Remaining Values
        self.value_ordering = self.config.get('value_ordering', 'lcv')  # Least Constraining Value
    
    def generate_schedule(self) -> Schedule:
        """
        Generate a timetable schedule using CSP techniques.
        
        Returns:
            Generated Schedule object
        """
        # Preprocess data
        self.preprocess_data()
        
        # Initialize CSP domains
        domains = self._initialize_domains()
        
        # Apply initial constraint propagation
        if self.use_arc_consistency:
            domains = self._apply_arc_consistency(domains)
        
        # Solve using backtracking
        solution = self._backtrack_search({}, domains)
        
        if solution:
            return self._solution_to_schedule(solution)
        else:
            return Schedule("failed", "No Solution Found", [])
    
    def validate_schedule(self, schedule: Schedule) -> bool:
        """
        Validate if a schedule satisfies all constraints.
        
        Args:
            schedule: Schedule to validate
            
        Returns:
            True if valid, False otherwise
        """
        return self._check_all_constraints(schedule)
    
    def optimize_schedule(self, schedule: Schedule) -> Schedule:
        """
        Optimize an existing schedule by trying to improve soft constraints.
        
        Args:
            schedule: Schedule to optimize
            
        Returns:
            Optimized schedule
        """
        # For CSP, we can try to find alternative solutions that satisfy soft constraints better
        return self._improve_soft_constraints(schedule)
    
    def _initialize_domains(self) -> Dict[str, Set[Tuple[str, str, str]]]:
        """
        Initialize domains for each course (variable).
        Domain contains possible (professor_id, room_id, time_slot_id) tuples.
        """
        domains = {}
        
        for course in self.courses:
            domain = set()
            
            # Find all valid combinations for this course
            for professor in self.professors:
                if self._can_professor_teach_course(professor, course):
                    for room in self.rooms:
                        if self._can_room_host_course(room, course):
                            for time_slot in self.time_slots:
                                if self._can_schedule_at_time(course, professor, room, time_slot):
                                    domain.add((professor.id, room.id, time_slot.id))
            
            domains[course.id] = domain
        
        return domains
    
    def _can_professor_teach_course(self, professor: Professor, course: Course) -> bool:
        """Check if professor can teach the course."""
        return (professor.is_active and 
                professor.department == course.branch and
                professor.can_teach_course(course.code))
    
    def _can_room_host_course(self, room: Room, course: Course) -> bool:
        """Check if room can host the course."""
        return room.is_suitable_for_course(
            course.course_type.value,
            course.capacity,  # Assuming course.capacity represents expected enrollment
            course.required_equipment
        )
    
    def _can_schedule_at_time(self, course: Course, professor: Professor, 
                            room: Room, time_slot: TimeSlot) -> bool:
        """Check if course can be scheduled at the given time."""
        return (time_slot.is_suitable_for_course_type(course.course_type.value) and
                time_slot.can_accommodate_duration(course.duration) and
                professor.is_available_at(time_slot.id) and
                room.is_available_at(time_slot.id))
    
    def _apply_arc_consistency(self, domains: Dict[str, Set[Tuple[str, str, str]]]) -> Dict[str, Set[Tuple[str, str, str]]]:
        """Apply AC-3 algorithm for arc consistency."""
        # Create queue of arcs (constraints between variables)
        queue = []
        course_ids = list(domains.keys())
        
        # Add all arcs
        for i in range(len(course_ids)):
            for j in range(i + 1, len(course_ids)):
                queue.append((course_ids[i], course_ids[j]))
                queue.append((course_ids[j], course_ids[i]))
        
        while queue:
            course1_id, course2_id = queue.pop(0)
            
            if self._revise_domain(domains, course1_id, course2_id):
                if not domains[course1_id]:
                    # Domain became empty - no solution
                    return domains
                
                # Add affected arcs back to queue
                for course3_id in course_ids:
                    if course3_id != course1_id and course3_id != course2_id:
                        queue.append((course3_id, course1_id))
        
        return domains
    
    def _revise_domain(self, domains: Dict[str, Set[Tuple[str, str, str]]], 
                      course1_id: str, course2_id: str) -> bool:
        """Revise domain of course1 based on constraints with course2."""
        revised = False
        to_remove = set()
        
        for assignment1 in domains[course1_id]:
            prof1_id, room1_id, time1_id = assignment1
            
            # Check if there's any valid assignment for course2 that doesn't conflict
            has_valid_assignment = False
            for assignment2 in domains[course2_id]:
                prof2_id, room2_id, time2_id = assignment2
                
                # Check for conflicts
                if not self._assignments_conflict(assignment1, assignment2):
                    has_valid_assignment = True
                    break
            
            if not has_valid_assignment:
                to_remove.add(assignment1)
                revised = True
        
        domains[course1_id] -= to_remove
        return revised
    
    def _assignments_conflict(self, assignment1: Tuple[str, str, str], 
                            assignment2: Tuple[str, str, str]) -> bool:
        """Check if two assignments conflict."""
        prof1_id, room1_id, time1_id = assignment1
        prof2_id, room2_id, time2_id = assignment2
        
        # Same time slot conflicts
        if time1_id == time2_id:
            # Same professor or same room at same time
            return prof1_id == prof2_id or room1_id == room2_id
        
        return False
    
    def _backtrack_search(self, assignment: Dict[str, Tuple[str, str, str]], 
                         domains: Dict[str, Set[Tuple[str, str, str]]]) -> Optional[Dict[str, Tuple[str, str, str]]]:
        """Backtracking search algorithm."""
        # Check if assignment is complete
        if len(assignment) == len(self.courses):
            return assignment
        
        # Select unassigned variable
        course_id = self._select_unassigned_variable(assignment, domains)
        
        if course_id is None:
            return assignment
        
        # Try each value in domain
        for value in self._order_domain_values(course_id, domains):
            if self._is_consistent(course_id, value, assignment):
                # Make assignment
                new_assignment = assignment.copy()
                new_assignment[course_id] = value
                
                # Forward checking
                new_domains = domains
                if self.use_forward_checking:
                    new_domains = self._forward_check(course_id, value, domains.copy())
                    if any(not domain for domain in new_domains.values() if domain is not None):
                        continue  # Some domain became empty
                
                # Recursive call
                result = self._backtrack_search(new_assignment, new_domains)
                if result is not None:
                    return result
        
        return None
    
    def _select_unassigned_variable(self, assignment: Dict[str, Tuple[str, str, str]], 
                                  domains: Dict[str, Set[Tuple[str, str, str]]]) -> Optional[str]:
        """Select next unassigned variable using heuristic."""
        unassigned = [course_id for course_id in domains.keys() if course_id not in assignment]
        
        if not unassigned:
            return None
        
        if self.variable_ordering == 'mrv':
            # Most Remaining Values - choose variable with smallest domain
            return min(unassigned, key=lambda course_id: len(domains[course_id]))
        else:
            # First available
            return unassigned[0]
    
    def _order_domain_values(self, course_id: str, domains: Dict[str, Set[Tuple[str, str, str]]]) -> List[Tuple[str, str, str]]:
        """Order domain values using heuristic."""
        values = list(domains[course_id])
        
        if self.value_ordering == 'lcv':
            # Least Constraining Value - order by how much they constrain other variables
            return sorted(values, key=lambda val: self._count_conflicts(course_id, val, domains))
        else:
            # No specific ordering
            return values
    
    def _count_conflicts(self, course_id: str, value: Tuple[str, str, str], 
                        domains: Dict[str, Set[Tuple[str, str, str]]]) -> int:
        """Count how many values this assignment would eliminate from other domains."""
        conflicts = 0
        
        for other_course_id, other_domain in domains.items():
            if other_course_id == course_id:
                continue
            
            for other_value in other_domain:
                if self._assignments_conflict(value, other_value):
                    conflicts += 1
        
        return conflicts
    
    def _is_consistent(self, course_id: str, value: Tuple[str, str, str], 
                      assignment: Dict[str, Tuple[str, str, str]]) -> bool:
        """Check if assignment is consistent with current partial assignment."""
        for assigned_course_id, assigned_value in assignment.items():
            if self._assignments_conflict(value, assigned_value):
                return False
        return True
    
    def _forward_check(self, assigned_course_id: str, assigned_value: Tuple[str, str, str], 
                      domains: Dict[str, Set[Tuple[str, str, str]]]) -> Dict[str, Set[Tuple[str, str, str]]]:
        """Apply forward checking to prune domains."""
        new_domains = {}
        
        for course_id, domain in domains.items():
            if course_id == assigned_course_id:
                new_domains[course_id] = {assigned_value}
            else:
                new_domain = set()
                for value in domain:
                    if not self._assignments_conflict(assigned_value, value):
                        new_domain.add(value)
                new_domains[course_id] = new_domain
        
        return new_domains
    
    def _solution_to_schedule(self, solution: Dict[str, Tuple[str, str, str]]) -> Schedule:
        """Convert CSP solution to Schedule object."""
        assignments = []
        
        for course_id, (professor_id, room_id, time_slot_id) in solution.items():
            assignment = Assignment(
                id=f"{course_id}_{professor_id}_{room_id}_{time_slot_id}",
                course_id=course_id,
                professor_id=professor_id,
                room_id=room_id,
                time_slot_id=time_slot_id
            )
            assignments.append(assignment)
        
        schedule = Schedule("csp_solution", "CSP Generated Schedule", assignments)
        schedule.algorithm_used = "ConstraintSatisfactionScheduler"
        return schedule
    
    def _check_all_constraints(self, schedule: Schedule) -> bool:
        """Check if schedule satisfies all constraints."""
        # Basic conflict checking
        if schedule.has_conflicts():
            return False
        
        # Additional constraint checking can be added here
        return True
    
    def _improve_soft_constraints(self, schedule: Schedule) -> Schedule:
        """Try to improve soft constraint satisfaction."""
        # This is a placeholder for soft constraint optimization
        # Could implement techniques like local search
        return schedule