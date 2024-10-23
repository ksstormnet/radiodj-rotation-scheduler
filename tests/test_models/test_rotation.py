import pytest
from datetime import datetime
from src.models.rotation import Rotation
from src.models.rotation_element import RotationElement, ElementType

class TestRotation:
    """Test suite for Rotation class."""

    @pytest.fixture
    def power_ballad_element(self):
        """Fixture providing a valid Power Ballad element for rotation end."""
        return RotationElement(
            position=4,
            category_id=1,
            subcategory_id=56,
            category_name="Music",
            subcategory_name="PB",
            element_type=ElementType.MUSIC,
            data="Power Ballad"
        )
    
    @pytest.fixture
    def sample_elements(self, power_ballad_element):
        """Fixture providing a list of valid rotation elements."""
        return [
            RotationElement(
                position=0,
                category_id=1,
                subcategory_id=45,
                category_name="Music",
                subcategory_name="CE",
                element_type=ElementType.MUSIC,
                data="Core Early"
            ),
            RotationElement(
                position=1,
                category_id=6,
                subcategory_id=57,
                category_name="Promos",
                subcategory_name="TOH",
                element_type=ElementType.PROMO
            ),
            RotationElement(
                position=2,
                category_id=7,
                subcategory_id=32,
                category_name="Commercials",
                subcategory_name="60",
                element_type=ElementType.COMMERCIAL,
                data="60 second spot"
            ),
            RotationElement(
                position=3,
                category_id=1,
                subcategory_id=48,
                category_name="Music",
                subcategory_name="I",
                element_type=ElementType.MUSIC,
                data="Image"
            ),
            power_ballad_element  # Always end with a Power Ballad
        ]
    
    @pytest.fixture
    def valid_rotation(self, sample_elements):
        """Fixture providing a valid rotation with elements."""
        return Rotation(
            name="Hr A",
            elements=sample_elements,
            id=1,
            last_modified=datetime(2024, 1, 1, 12, 0)
        )

    def test_valid_initialization(self, valid_rotation, sample_elements):
        """Test that a valid rotation initializes correctly."""
        assert valid_rotation.name == "Hr A"
        assert valid_rotation.id == 1
        assert valid_rotation.length == len(sample_elements)
        assert valid_rotation.elements == sample_elements
        assert valid_rotation.elements[-1].subcategory_name == "PB"
        
    def test_empty_rotation_initialization(self):
        """Test initialization of empty rotation."""
        rotation = Rotation(name="Empty")
        assert rotation.length == 0
        assert rotation.elements == []

    @pytest.mark.parametrize("test_case", [
        {
            "name": "empty_name",
            "data": {"name": "", "elements": []},
            "expected_error": "Rotation name cannot be empty"
        },
        {
            "name": "duplicate_positions",
            "data": {"name": "Hr A", "elements": None},
            "expected_error": "Duplicate positions found in rotation"
        },
        {
            "name": "negative_position",
            "data": {"name": "Hr A", "elements": None},
            "expected_error": "Negative positions are not allowed"
        },
        {
            "name": "position_gap",
            "data": {"name": "Hr A", "elements": None},
            "expected_error": "Positions must be sequential without gaps"
        },
        {
            "name": "wrong_last_element",
            "data": {"name": "Hr A", "elements": None},
            "expected_error": "Last element must be a Power Ballad (PB)"
        }
    ])
    def test_invalid_initialization(self, test_case, power_ballad_element):
        """Test that invalid data raises appropriate errors."""
        invalid_data = test_case["data"].copy()
        
        if invalid_data["elements"] is None:
            if test_case["name"] == "duplicate_positions":
                invalid_data["elements"] = [
                    RotationElement(
                        position=0,
                        category_id=1,
                        subcategory_id=45,
                        category_name="Music",
                        subcategory_name="CE",
                        element_type=ElementType.MUSIC
                    ),
                    RotationElement(
                        position=0,  # Duplicate position
                        category_id=2,
                        subcategory_id=46,
                        category_name="Music",
                        subcategory_name="CM",
                        element_type=ElementType.MUSIC
                    ),
                    power_ballad_element  # Add PB to avoid that validation error
                ]
            elif test_case["name"] == "negative_position":
                invalid_data["elements"] = [
                    RotationElement(
                        position=-1,  # Negative position
                        category_id=1,
                        subcategory_id=45,
                        category_name="Music",
                        subcategory_name="CE",
                        element_type=ElementType.MUSIC
                    ),
                    power_ballad_element
                ]
            elif test_case["name"] == "position_gap":
                invalid_data["elements"] = [
                    RotationElement(
                        position=0,
                        category_id=1,
                        subcategory_id=45,
                        category_name="Music",
                        subcategory_name="CE",
                        element_type=ElementType.MUSIC
                    ),
                    RotationElement(
                        position=2,  # Gap in position (missing 1)
                        category_id=2,
                        subcategory_id=46,
                        category_name="Music",
                        subcategory_name="CM",
                        element_type=ElementType.MUSIC
                    ),
                    power_ballad_element
                ]
            elif test_case["name"] == "wrong_last_element":
                invalid_data["elements"] = [
                    RotationElement(
                        position=0,
                        category_id=1,
                        subcategory_id=45,
                        category_name="Music",
                        subcategory_name="CE",
                        element_type=ElementType.MUSIC
                    ),
                    RotationElement(
                        position=1,
                        category_id=1,
                        subcategory_id=48,
                        category_name="Music",
                        subcategory_name="I",
                        element_type=ElementType.MUSIC
                    )
                ]

        with pytest.raises(ValueError) as excinfo:
            Rotation(**invalid_data)
        assert test_case["expected_error"] in str(excinfo.value)

    def test_commercial_breaks(self, valid_rotation):
        """Test identification of commercial breaks."""
        breaks = valid_rotation.commercial_breaks
        assert len(breaks) == 1
        assert len(breaks[0]) == 1
        assert breaks[0][0].category_name == "Commercials"
        
    def test_music_sets(self, valid_rotation):
        """Test identification of music sets."""
        sets = valid_rotation.music_sets
        assert len(sets) == 2  # Two sets because interrupted by non-music elements
        
        # First set has one music element (Core Early)
        assert len(sets[0]) == 1
        assert sets[0][0].category_name == "Music"
        assert sets[0][0].subcategory_name == "CE"
        
        # Second set has two music elements (Image and Power Ballad)
        assert len(sets[1]) == 2
        assert sets[1][0].category_name == "Music"
        assert sets[1][0].subcategory_name == "I"
        assert sets[1][1].category_name == "Music"
        assert sets[1][1].subcategory_name == "PB"
        
        # Verify all elements are music
        assert all(elem.category_name == "Music" for set_ in sets for elem in set_)
        
    def test_category_counts(self, valid_rotation):
        """Test counting of categories."""
        counts = valid_rotation.category_counts()
        assert counts["Music"] == 3
        assert counts["Promos"] == 1
        assert counts["Commercials"] == 1
        
    def test_subcategory_counts(self, valid_rotation):
        """Test counting of subcategories."""
        counts = valid_rotation.subcategory_counts()
        assert counts["Music/CE"] == 1
        assert counts["Music/I"] == 1
        assert counts["Music/PB"] == 1
        assert counts["Promos/TOH"] == 1
        assert counts["Commercials/60"] == 1
        
    def test_compare_with(self, valid_rotation, sample_elements):
        """Test rotation comparison."""
        # Create a slightly different rotation
        modified_elements = sample_elements.copy()
        modified_elements[0] = RotationElement(
            position=0,
            category_id=1,
            subcategory_id=46,
            category_name="Music",
            subcategory_name="CM",
            element_type=ElementType.MUSIC
        )
        
        other_rotation = Rotation(
            name="Hr B",
            elements=modified_elements
        )
        
        similarity, changes = valid_rotation.compare_with(other_rotation)
        assert similarity == 80.0  # 4 out of 5 elements are the same
        assert changes["Music"] == 0  # Same number of music elements
        
        with pytest.raises(TypeError):
            valid_rotation.compare_with("not a rotation")
            
    def test_add_element(self, valid_rotation, power_ballad_element):
        """Test adding elements."""
        # Remove the last element (PB) to test adding it back
        valid_rotation.remove_element(power_ballad_element.position)
        
        original_length = valid_rotation.length
        valid_rotation.add_element(power_ballad_element)
        assert valid_rotation.length == original_length + 1
        assert valid_rotation.elements[-1] == power_ballad_element
        assert valid_rotation.elements[-1].subcategory_name == "PB"
        
        # Test adding element with duplicate position
        with pytest.raises(ValueError):
            valid_rotation.add_element(power_ballad_element)
            
    def test_remove_element(self, valid_rotation, power_ballad_element):
        """Test removing elements."""
        # Remove a non-PB element
        original_length = valid_rotation.length
        removed = valid_rotation.remove_element(0)
        assert valid_rotation.length == original_length - 1
        assert removed.position == 0
        # Verify PB is still last
        assert valid_rotation.elements[-1].subcategory_name == "PB"
        
        # Try to remove the PB element
        with pytest.raises(ValueError) as excinfo:
            valid_rotation.remove_element(power_ballad_element.position)
            assert "Last element must be a Power Ballad (PB)" in str(excinfo.value)
        
        # Try to remove non-existent position
        with pytest.raises(ValueError):
            valid_rotation.remove_element(99)
            
    def test_serialization(self, valid_rotation):
        """Test conversion to and from dictionary."""
        rotation_dict = valid_rotation.to_dict()
        assert rotation_dict["name"] == "Hr A"
        assert rotation_dict["id"] == 1
        assert len(rotation_dict["elements"]) == valid_rotation.length
        assert rotation_dict["elements"][-1]["subcategory_name"] == "PB"
        
        new_rotation = Rotation.from_dict(rotation_dict)
        assert new_rotation.name == valid_rotation.name
        assert new_rotation.id == valid_rotation.id
        assert new_rotation.length == valid_rotation.length
        assert new_rotation.elements[-1].subcategory_name == "PB"
        
        # Compare elements as dictionaries to avoid position issues
        for orig, new in zip(valid_rotation.elements, new_rotation.elements):
            orig_dict = orig.to_dict()
            new_dict = new.to_dict()
            orig_dict.pop('position')
            new_dict.pop('position')
            assert orig_dict == new_dict
        
    def test_string_representation(self, valid_rotation):
        """Test string representation."""
        string_rep = str(valid_rotation)
        assert valid_rotation.name in string_rep
        assert str(valid_rotation.id) in string_rep
        assert all(elem.category_name in string_rep for elem in valid_rotation.elements)
        assert "Category Counts:" in string_rep
        assert "PB" in string_rep