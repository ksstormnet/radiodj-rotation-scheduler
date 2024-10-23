from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set

class ElementType(Enum):
    """Enumeration of possible element types in a rotation."""
    MUSIC = "Music"
    COMMERCIAL = "Commercial"
    PROMO = "Promo"
    JINGLE = "Jingle"
    STATION_ID = "Station ID"

@dataclass
class RotationElement:
    """
    Represents a single element in a radio rotation.
    
    Attributes:
        position: Integer position in the rotation (0-based)
        category_id: ID of the category from the database
        subcategory_id: ID of the subcategory from the database
        category_name: Name of the category
        subcategory_name: Name of the subcategory
        element_type: Type of element (music, commercial, etc.)
        data: Additional data/label for the element
        track_separation: Minutes before this track can repeat
        artist_separation: Minutes before this artist can repeat
        title_separation: Minutes before this title can repeat
        album_separation: Minutes before this album can repeat
        repeat_rule: Whether separation rules apply to this element
    """
    
    position: int
    category_id: int
    subcategory_id: int
    category_name: str
    subcategory_name: str
    element_type: ElementType
    data: str = ""
    track_separation: int = 0
    artist_separation: int = 0
    title_separation: int = 0
    album_separation: int = 0
    repeat_rule: bool = False
    
    def __post_init__(self):
        """Validates the element after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """
        Validates the element's attributes.
        
        Raises:
            ValueError: If any attributes are invalid
        """
        if self.position < 0:
            raise ValueError("Position must be non-negative")
            
        if self.category_id < 1:
            raise ValueError("Category ID must be positive")
            
        if self.subcategory_id < 1:
            raise ValueError("Subcategory ID must be positive")
            
        if not self.category_name:
            raise ValueError("Category name cannot be empty")
            
        if not self.subcategory_name:
            raise ValueError("Subcategory name cannot be empty")
            
        if any(sep < 0 for sep in [
            self.track_separation,
            self.artist_separation,
            self.title_separation,
            self.album_separation
        ]):
            raise ValueError("Separation values must be non-negative")
    
    @property
    def is_music(self) -> bool:
        """Returns True if this is a music element."""
        return self.element_type == ElementType.MUSIC
    
    @property
    def is_commercial(self) -> bool:
        """Returns True if this is a commercial element."""
        return self.element_type == ElementType.COMMERCIAL
    
    @property
    def is_jingle(self) -> bool:
        """Returns True if this is a jingle element."""
        return self.element_type == ElementType.JINGLE
    
    @property
    def has_separation_rules(self) -> bool:
        """Returns True if this element has any separation rules."""
        return any([
            self.track_separation > 0,
            self.artist_separation > 0,
            self.title_separation > 0,
            self.album_separation > 0
        ])
    
    def __str__(self) -> str:
        """Returns a human-readable string representation of the element."""
        base = f"{self.position:02d}: {self.category_name}/{self.subcategory_name}"
        if self.data:
            base += f" ({self.data})"
        if self.has_separation_rules:
            base += " [SEP]"
        return base
    
    def __eq__(self, other: object) -> bool:
            """
            Compares this element to another for equality.
            
            Two elements are equal if all their attributes match except for position.
            This allows for comparing elements across different positions in rotations.
            
            Args:
                other: Object to compare with
                
            Returns:
                bool: True if elements are equal, False otherwise
            """
            if not isinstance(other, RotationElement):
                return NotImplemented
                
            return (
                self.category_id == other.category_id and
                self.subcategory_id == other.subcategory_id and
                self.category_name == other.category_name and
                self.subcategory_name == other.subcategory_name and
                self.element_type == other.element_type and
                self.data == other.data and
                self.track_separation == other.track_separation and
                self.artist_separation == other.artist_separation and
                self.title_separation == other.title_separation and
                self.album_separation == other.album_separation and
                self.repeat_rule == other.repeat_rule
            )
    
    def to_dict(self) -> dict:
        """
        Converts the element to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all element attributes
        """
        return {
            'position': self.position,
            'category_id': self.category_id,
            'subcategory_id': self.subcategory_id,
            'category_name': self.category_name,
            'subcategory_name': self.subcategory_name,
            'element_type': self.element_type.value,
            'data': self.data,
            'track_separation': self.track_separation,
            'artist_separation': self.artist_separation,
            'title_separation': self.title_separation,
            'album_separation': self.album_separation,
            'repeat_rule': self.repeat_rule
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RotationElement':
        """
        Creates a RotationElement instance from a dictionary.
        
        Args:
            data: Dictionary containing element attributes
            
        Returns:
            RotationElement: New instance created from the dictionary
        """
        element_data = data.copy()
        element_data['element_type'] = ElementType(element_data['element_type'])
        return cls(**element_data)
    
    def copy_with_position(self, new_position: int) -> 'RotationElement':
        """
        Creates a copy of this element with a new position.
        
        Args:
            new_position: New position for the copied element
            
        Returns:
            RotationElement: New instance with updated position
        """
        element_dict = self.to_dict()
        element_dict['position'] = new_position
        return self.from_dict(element_dict)