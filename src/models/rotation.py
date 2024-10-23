from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime
from .rotation_element import RotationElement, ElementType

@dataclass
class Rotation:
    """
    Represents a complete hour-long rotation.
    
    Attributes:
        name: Identifier for the rotation (e.g., 'Hr A')
        elements: Ordered list of RotationElements
        id: Database ID, if stored
        last_modified: Timestamp of last modification
    """
    
    name: str
    elements: List[RotationElement] = field(default_factory=list)
    id: Optional[int] = None
    last_modified: Optional[datetime] = None
    
    def __post_init__(self):
        """Validates rotation after initialization."""
        self._validate()
        self._sort_elements()
    
    def _validate(self) -> None:
        """
        Validates the rotation's structure.
        
        Raises:
            ValueError: If rotation structure is invalid
        """
        if not self.name:
            raise ValueError("Rotation name cannot be empty")
        
        # Check for duplicate positions
        positions = [elem.position for elem in self.elements]
        if len(positions) != len(set(positions)):
            raise ValueError("Duplicate positions found in rotation")
        
        # Validate position sequence
        if positions:
            if min(positions) < 0:
                raise ValueError("Negative positions are not allowed")
            if max(positions) >= len(positions):
                raise ValueError("Positions must be sequential without gaps")
            
            # Check that last element is a Power Ballad
            if self.elements:
                last_elem = self.elements[-1]
                if not (last_elem.category_name == "Music" and 
                       last_elem.subcategory_name == "PB"):
                    raise ValueError("Last element must be a Power Ballad (PB)")
    
    def _sort_elements(self) -> None:
        """Sorts elements by position."""
        self.elements.sort(key=lambda x: x.position)
    
    @property
    def length(self) -> int:
        """Returns the number of elements in the rotation."""
        return len(self.elements)
    
    @property
    def commercial_breaks(self) -> List[List[RotationElement]]:
        """Returns list of commercial break sequences."""
        breaks = []
        current_break = []
        
        for elem in self.elements:
            if elem.is_commercial:
                current_break.append(elem)
            elif current_break:
                breaks.append(current_break)
                current_break = []
        
        # No need to check for remaining break as last element must be PB
        return breaks
    
    @property
    def music_sets(self) -> List[List[RotationElement]]:
        """Returns list of music set sequences."""
        sets = []
        current_set = []
        
        for elem in self.elements:
            if elem.is_music:
                current_set.append(elem)
            elif current_set:
                sets.append(current_set)
                current_set = []
        
        # Make sure to include the last set if it exists
        if current_set:
            sets.append(current_set)
        
        return sets
    
    def category_counts(self) -> Dict[str, int]:
        """Returns count of elements by category."""
        counts = {}
        for elem in self.elements:
            counts[elem.category_name] = counts.get(elem.category_name, 0) + 1
        return counts
    
    def subcategory_counts(self) -> Dict[str, int]:
        """Returns count of elements by subcategory."""
        counts = {}
        for elem in self.elements:
            key = f"{elem.category_name}/{elem.subcategory_name}"
            counts[key] = counts.get(key, 0) + 1
        return counts
    
    def compare_with(self, other: 'Rotation') -> Tuple[float, Dict[str, int]]:
        """
        Compares this rotation with another, returning similarity metrics.
        
        Args:
            other: Rotation to compare with
            
        Returns:
            Tuple of:
                - Percentage of identical elements
                - Dictionary of category-level changes
        """
        if not isinstance(other, Rotation):
            raise TypeError("Can only compare with another Rotation")
            
        # Calculate element-level similarity
        common_elements = sum(1 for elem in self.elements 
                            if elem in other.elements)
        similarity = common_elements / max(len(self.elements), len(other.elements))
        
        # Calculate category-level changes
        self_counts = self.category_counts()
        other_counts = other.category_counts()
        
        changes = {}
        all_categories = set(self_counts.keys()) | set(other_counts.keys())
        
        for category in all_categories:
            self_count = self_counts.get(category, 0)
            other_count = other_counts.get(category, 0)
            changes[category] = other_count - self_count
            
        return similarity * 100, changes
    
    def add_element(self, element: RotationElement) -> None:
        """
        Adds a new element to the rotation.
        
        Args:
            element: RotationElement to add
            
        Raises:
            ValueError: If element position is invalid or would violate rules
        """
        if any(e.position == element.position for e in self.elements):
            raise ValueError(f"Position {element.position} already occupied")
        
        self.elements.append(element)
        self._sort_elements()
        self._validate()
    
    def remove_element(self, position: int) -> RotationElement:
        """
        Removes element at specified position.
        
        Args:
            position: Position of element to remove
            
        Returns:
            Removed RotationElement
            
        Raises:
            ValueError: If position is invalid
        """
        for i, elem in enumerate(self.elements):
            if elem.position == position:
                removed = self.elements.pop(i)
                self._validate()
                return removed
        
        raise ValueError(f"No element found at position {position}")
    
    def to_dict(self) -> dict:
        """
        Converts rotation to dictionary representation.
        
        Returns:
            Dictionary containing all rotation attributes
        """
        return {
            'name': self.name,
            'id': self.id,
            'last_modified': self.last_modified.isoformat() if self.last_modified else None,
            'elements': [elem.to_dict() for elem in self.elements]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Rotation':
        """
        Creates a Rotation instance from a dictionary.
        
        Args:
            data: Dictionary containing rotation attributes
            
        Returns:
            New Rotation instance
        """
        rotation_data = data.copy()
        elements_data = rotation_data.pop('elements', [])
        
        if rotation_data.get('last_modified'):
            rotation_data['last_modified'] = datetime.fromisoformat(
                rotation_data['last_modified']
            )
        
        rotation = cls(**rotation_data)
        
        for elem_data in elements_data:
            rotation.add_element(RotationElement.from_dict(elem_data))
        
        return rotation
    
    def __str__(self) -> str:
        """Returns human-readable string representation."""
        lines = [f"Rotation: {self.name}"]
        if self.id:
            lines[0] += f" (ID: {self.id})"
        
        lines.extend(str(elem) for elem in self.elements)
        
        counts = self.category_counts()
        lines.append("\nCategory Counts:")
        for category, count in sorted(counts.items()):
            lines.append(f"  {category}: {count}")
            
        return "\n".join(lines)