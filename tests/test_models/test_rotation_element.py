import pytest
from src.models.rotation_element import RotationElement, ElementType

class TestRotationElement:
    """Test suite for RotationElement class."""
    
    @pytest.fixture
    def valid_music_element(self) -> RotationElement:
        """Fixture providing a valid music element."""
        return RotationElement(
            position=0,
            category_id=1,
            subcategory_id=45,
            category_name="Music",
            subcategory_name="CE",
            element_type=ElementType.MUSIC,
            data="Core Early",
            track_separation=120,
            artist_separation=60,
            title_separation=240,
            album_separation=120,
            repeat_rule=True
        )
    
    @pytest.fixture
    def valid_commercial_element(self) -> RotationElement:
        """Fixture providing a valid commercial element."""
        return RotationElement(
            position=10,
            category_id=7,
            subcategory_id=32,
            category_name="Commercials",
            subcategory_name="60",
            element_type=ElementType.COMMERCIAL,
            data="60 second spot"
        )
    
    def test_valid_initialization(self, valid_music_element):
        """Test that a valid element initializes correctly."""
        assert valid_music_element.position == 0
        assert valid_music_element.category_id == 1
        assert valid_music_element.subcategory_id == 45
        assert valid_music_element.category_name == "Music"
        assert valid_music_element.subcategory_name == "CE"
        assert valid_music_element.element_type == ElementType.MUSIC
        assert valid_music_element.data == "Core Early"
        assert valid_music_element.track_separation == 120
        assert valid_music_element.artist_separation == 60
        assert valid_music_element.title_separation == 240
        assert valid_music_element.album_separation == 120
        assert valid_music_element.repeat_rule is True
    
    @pytest.mark.parametrize("invalid_data", [
        {"position": -1},
        {"category_id": 0},
        {"subcategory_id": -1},
        {"category_name": ""},
        {"subcategory_name": ""},
        {"track_separation": -1},
        {"artist_separation": -1},
        {"title_separation": -1},
        {"album_separation": -1},
    ])
    def test_invalid_initialization(self, valid_music_element, invalid_data):
        """Test that invalid data raises appropriate errors."""
        element_data = valid_music_element.to_dict()
        element_data.update(invalid_data)
        
        with pytest.raises(ValueError):
            RotationElement.from_dict(element_data)
    
    def test_is_music(self, valid_music_element, valid_commercial_element):
        """Test is_music property."""
        assert valid_music_element.is_music is True
        assert valid_commercial_element.is_music is False
    
    def test_is_commercial(self, valid_music_element, valid_commercial_element):
        """Test is_commercial property."""
        assert valid_music_element.is_commercial is False
        assert valid_commercial_element.is_commercial is True
    
    def test_has_separation_rules(self, valid_music_element, valid_commercial_element):
        """Test has_separation_rules property."""
        assert valid_music_element.has_separation_rules is True
        assert valid_commercial_element.has_separation_rules is False
    
    def test_string_representation(self, valid_music_element, valid_commercial_element):
        """Test string representation of elements."""
        assert str(valid_music_element) == "00: Music/CE (Core Early) [SEP]"
        assert str(valid_commercial_element) == "10: Commercials/60 (60 second spot)"
    
    def test_equality(self, valid_music_element):
        """Test equality comparison."""
        same_element = RotationElement.from_dict(valid_music_element.to_dict())
        different_position = valid_music_element.copy_with_position(5)
        different_element = RotationElement(
            position=0,
            category_id=2,
            subcategory_id=46,
            category_name="Different",
            subcategory_name="Different",
            element_type=ElementType.MUSIC
        )
        
        assert valid_music_element == same_element
        assert valid_music_element == different_position
        assert valid_music_element != different_element
        assert valid_music_element != "not an element"
    
    def test_to_dict(self, valid_music_element):
        """Test conversion to dictionary."""
        element_dict = valid_music_element.to_dict()
        
        assert element_dict['position'] == 0
        assert element_dict['category_id'] == 1
        assert element_dict['subcategory_id'] == 45
        assert element_dict['category_name'] == "Music"
        assert element_dict['subcategory_name'] == "CE"
        assert element_dict['element_type'] == "Music"
        assert element_dict['data'] == "Core Early"
        assert element_dict['track_separation'] == 120
        assert element_dict['artist_separation'] == 60
        assert element_dict['title_separation'] == 240
        assert element_dict['album_separation'] == 120
        assert element_dict['repeat_rule'] is True
    
    def test_from_dict(self, valid_music_element):
        """Test creation from dictionary."""
        element_dict = valid_music_element.to_dict()
        new_element = RotationElement.from_dict(element_dict)
        
        assert new_element == valid_music_element
        assert new_element.position == valid_music_element.position
        assert new_element.data == valid_music_element.data
        assert new_element.repeat_rule == valid_music_element.repeat_rule
    
    def test_copy_with_position(self, valid_music_element):
            """Test copying with new position."""
            new_position = 5
            original_dict = valid_music_element.to_dict()
            copied = valid_music_element.copy_with_position(new_position)
            
            # Verify new position
            assert copied.position == new_position
            
            # Verify all other attributes remain the same
            copied_dict = copied.to_dict()
            original_dict.pop('position')
            copied_dict.pop('position')
            assert copied_dict == original_dict
            
            # Verify the objects are different instances
            assert id(copied) != id(valid_music_element)

    def test_element_type_enum(self):
        """Test ElementType enumeration."""
        assert ElementType.MUSIC.value == "Music"
        assert ElementType.COMMERCIAL.value == "Commercial"
        assert ElementType.PROMO.value == "Promo"
        assert ElementType.JINGLE.value == "Jingle"
        assert ElementType.STATION_ID.value == "Station ID"

    def test_is_jingle(self, valid_music_element):
        """Test is_jingle property."""
        assert not valid_music_element.is_jingle  # Test non-jingle first
        
        jingle_element = RotationElement(
            position=5,
            category_id=5,
            subcategory_id=35,
            category_name="Jingles",
            subcategory_name="B",
            element_type=ElementType.JINGLE,
            data=""
        )
        assert jingle_element.is_jingle

    def test_string_representation_no_data(self):
        """Test string representation of element without data field."""
        element = RotationElement(
            position=0,
            category_id=5,
            subcategory_id=35,
            category_name="Jingles",
            subcategory_name="B",
            element_type=ElementType.JINGLE
        )
        expected = "00: Jingles/B"
        assert str(element) == expected
        
        # Also test with explicit empty data
        element.data = ""
        assert str(element) == expected