"""Genetic algorithm scheduler implementation."""

from typing import List, Dict, Any, Optional
import random
from ..models import Course, Professor, Room, TimeSlot, Schedule, Assignment
from .base import BaseScheduler


class GeneticScheduler(BaseScheduler):
    """
    Genetic Algorithm-based timetable scheduler.
    
    This scheduler uses evolutionary computation principles to generate
    optimal timetable schedules through selection, crossover, and mutation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the genetic scheduler with configuration."""
        super().__init__(config)
        
        # Genetic algorithm parameters
        self.population_size = self.config.get('population_size', 50)
        self.generations = self.config.get('generations', 100)
        self.mutation_rate = self.config.get('mutation_rate', 0.1)
        self.crossover_rate = self.config.get('crossover_rate', 0.8)
        self.elite_size = self.config.get('elite_size', 5)
    
    def generate_schedule(self) -> Schedule:
        """
        Generate a timetable schedule using genetic algorithm.
        
        Returns:
            Generated Schedule object
        """
        # Preprocess data
        self.preprocess_data()
        
        # Initialize population
        population = self._initialize_population()
        
        best_schedule = None
        best_fitness = float('-inf')
        
        for generation in range(self.generations):
            # Evaluate fitness for all individuals
            fitness_scores = [self._calculate_fitness(schedule) for schedule in population]
            
            # Track best schedule
            current_best_idx = fitness_scores.index(max(fitness_scores))
            current_best_fitness = fitness_scores[current_best_idx]
            
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_schedule = population[current_best_idx]
            
            # Selection and reproduction
            new_population = self._select_and_reproduce(population, fitness_scores)
            population = new_population
        
        return best_schedule or Schedule("empty", "Empty Schedule", [])
    
    def validate_schedule(self, schedule: Schedule) -> bool:
        """
        Validate if a schedule satisfies constraints.
        
        Args:
            schedule: Schedule to validate
            
        Returns:
            True if valid, False otherwise
        """
        return not schedule.has_conflicts()
    
    def optimize_schedule(self, schedule: Schedule) -> Schedule:
        """
        Optimize an existing schedule.
        
        Args:
            schedule: Schedule to optimize
            
        Returns:
            Optimized schedule
        """
        # Apply local optimization techniques
        return self._local_optimization(schedule)
    
    def _initialize_population(self) -> List[Schedule]:
        """Initialize a random population of schedules."""
        population = []
        
        for i in range(self.population_size):
            schedule = self._create_random_schedule(f"individual_{i}")
            population.append(schedule)
        
        return population
    
    def _create_random_schedule(self, schedule_id: str) -> Schedule:
        """Create a random schedule."""
        schedule = Schedule(schedule_id, f"Random Schedule {schedule_id}", [])
        
        for course in self.courses:
            # Try to assign each course randomly
            assignment = self._create_random_assignment(course)
            if assignment:
                schedule.add_assignment(assignment)
        
        return schedule
    
    def _create_random_assignment(self, course: Course) -> Optional[Assignment]:
        """Create a random assignment for a course."""
        # Random selection of professor, room, and time slot
        available_professors = [p for p in self.professors if p.department == course.branch]
        available_rooms = [r for r in self.rooms if r.is_suitable_for_course(
            course.course_type.value, course.capacity, course.required_equipment)]
        available_time_slots = [ts for ts in self.time_slots if ts.is_active]
        
        if not (available_professors and available_rooms and available_time_slots):
            return None
        
        professor = random.choice(available_professors)
        room = random.choice(available_rooms)
        time_slot = random.choice(available_time_slots)
        
        return Assignment(
            id=f"{course.id}_{professor.id}_{room.id}_{time_slot.id}",
            course_id=course.id,
            professor_id=professor.id,
            room_id=room.id,
            time_slot_id=time_slot.id
        )
    
    def _calculate_fitness(self, schedule: Schedule) -> float:
        """Calculate fitness score for a schedule."""
        if not schedule.assignments:
            return 0.0
        
        # Start with base quality score
        fitness = self.calculate_schedule_quality(schedule)
        
        # Penalize conflicts heavily
        conflicts = schedule.get_conflict_count()
        fitness -= conflicts * 1000  # Heavy penalty for conflicts
        
        return fitness
    
    def _select_and_reproduce(self, population: List[Schedule], fitness_scores: List[float]) -> List[Schedule]:
        """Select parents and create next generation."""
        new_population = []
        
        # Elite selection - keep best individuals
        elite_indices = sorted(range(len(fitness_scores)), 
                             key=lambda i: fitness_scores[i], reverse=True)[:self.elite_size]
        for idx in elite_indices:
            new_population.append(population[idx])
        
        # Generate rest through crossover and mutation
        while len(new_population) < self.population_size:
            parent1 = self._tournament_selection(population, fitness_scores)
            parent2 = self._tournament_selection(population, fitness_scores)
            
            if random.random() < self.crossover_rate:
                child = self._crossover(parent1, parent2)
            else:
                child = parent1
            
            if random.random() < self.mutation_rate:
                child = self._mutate(child)
            
            new_population.append(child)
        
        return new_population[:self.population_size]
    
    def _tournament_selection(self, population: List[Schedule], fitness_scores: List[float]) -> Schedule:
        """Tournament selection for parent selection."""
        tournament_size = min(3, len(population))
        tournament_indices = random.sample(range(len(population)), tournament_size)
        
        best_idx = max(tournament_indices, key=lambda i: fitness_scores[i])
        return population[best_idx]
    
    def _crossover(self, parent1: Schedule, parent2: Schedule) -> Schedule:
        """Create offspring through crossover."""
        # Simple one-point crossover
        child_assignments = []
        crossover_point = len(parent1.assignments) // 2
        
        child_assignments.extend(parent1.assignments[:crossover_point])
        child_assignments.extend(parent2.assignments[crossover_point:])
        
        child = Schedule(f"child_{random.randint(1000, 9999)}", "Crossover Child", child_assignments)
        return child
    
    def _mutate(self, schedule: Schedule) -> Schedule:
        """Apply mutation to a schedule."""
        if not schedule.assignments:
            return schedule
        
        # Random mutation - modify one assignment
        mutated_assignments = schedule.assignments.copy()
        mutation_idx = random.randint(0, len(mutated_assignments) - 1)
        
        # Try to reassign the selected assignment
        assignment = mutated_assignments[mutation_idx]
        course = next((c for c in self.courses if c.id == assignment.course_id), None)
        
        if course:
            new_assignment = self._create_random_assignment(course)
            if new_assignment:
                mutated_assignments[mutation_idx] = new_assignment
        
        mutated_schedule = Schedule(f"mutant_{random.randint(1000, 9999)}", 
                                  "Mutated Schedule", mutated_assignments)
        return mutated_schedule
    
    def _local_optimization(self, schedule: Schedule) -> Schedule:
        """Apply local optimization to improve schedule quality."""
        # This is a placeholder for local optimization techniques
        # Could implement hill climbing, simulated annealing, etc.
        return schedule