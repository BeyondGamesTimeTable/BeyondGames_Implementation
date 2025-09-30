"""Constraint model for representing scheduling constraints."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable
from enum import Enum


class ConstraintType(Enum):
    """Types of constraints."""
    HARD = "hard"
    SOFT = "soft"


class ConstraintPriority(Enum):
    """Priority levels for constraints."""
    CRITICAL = "critical"
    HIGH = "high" 
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Constraint:
    """
    Represents a scheduling constraint.
    
    Attributes:
        id: Unique identifier for the constraint
        name: Human-readable name of the constraint
        description: Detailed description of what the constraint enforces
        constraint_type: Whether this is a hard or soft constraint
        priority: Priority level of the constraint
        weight: Numerical weight for optimization (higher = more important)
        validator_function: Function to validate if constraint is satisfied
        parameters: Additional parameters for the constraint
        is_active: Whether the constraint is currently active
    """
    
    id: str
    name: str
    description: str
    constraint_type: ConstraintType
    priority: ConstraintPriority = ConstraintPriority.MEDIUM
    weight: float = 1.0
    validator_function: Optional[Callable] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool = True
    
    def __post_init__(self):
        """Initialize default values after object creation."""
        if self.parameters is None:
            self.parameters = {}
    
    def validate(self, assignment: Any, context: Dict[str, Any] = None) -> bool:
        """
        Validate if an assignment satisfies this constraint.
        
        Args:
            assignment: The assignment to validate
            context: Additional context for validation
            
        Returns:
            True if constraint is satisfied, False otherwise
        """
        if not self.is_active or self.validator_function is None:
            return True
            
        try:
            return self.validator_function(assignment, self.parameters, context or {})
        except Exception:
            # If validation fails, assume constraint is violated
            return False
    
    def get_violation_penalty(self) -> float:
        """
        Get the penalty for violating this constraint.
        
        Returns:
            Penalty value (higher for more important constraints)
        """
        base_penalty = self.weight
        
        # Multiply by constraint type factor
        if self.constraint_type == ConstraintType.HARD:
            base_penalty *= 1000  # Hard constraints have very high penalty
        
        # Multiply by priority factor
        priority_multipliers = {
            ConstraintPriority.CRITICAL: 5.0,
            ConstraintPriority.HIGH: 3.0,
            ConstraintPriority.MEDIUM: 1.0,
            ConstraintPriority.LOW: 0.5
        }
        
        return base_penalty * priority_multipliers.get(self.priority, 1.0)
    
    def __str__(self) -> str:
        """String representation of the constraint."""
        return f"{self.name} ({self.constraint_type.value})"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return (f"Constraint(id='{self.id}', name='{self.name}', "
                f"type={self.constraint_type.value}, priority={self.priority.value})")