from src.models.rotation_element import RotationElement

def test_create_rotation_element():
    element = RotationElement(1, 1, 1, 45, 0, '---', '---', '---', 0, 0, 0, 0, 'False', 0, 'CE', 0, 0, 0, 0, None)
    assert element.id == 1
    assert element.parent_id == 1
    assert element.category_id == 1
    assert element.subcategory_id == 45
    assert element.data == 'CE'
    # Add more assertions for other attributes as needed

def test_rotation_element_str_representation():
    element = RotationElement(1, 1, 1, 45, 0, '---', '---', '---', 0, 0, 0, 0, 'False', 0, 'CE', 0, 0, 0, 0, None)
    assert str(element) == "RotationElement(1, 1, 1, 45, 0, '---', '---', '---', 0, 0, 0, 0, 'False', 0, 'CE', 0, 0, 0, 0, None)"

def test_rotation_element_equality():
    element1 = RotationElement(1, 1, 1, 45, 0, '---', '---', '---', 0, 0, 0, 0, 'False', 0, 'CE', 0, 0, 0, 0, None)
    element2 = RotationElement(1, 1, 1, 45, 0, '---', '---', '---', 0, 0, 0, 0, 'False', 0, 'CE', 0, 0, 0, 0, None)
    element3 = RotationElement(2, 1, 1, 46, 0, '---', '---', '---', 0, 0, 0, 0, 'False', 0, 'CM', 0, 0, 0, 0, None)
    assert element1 == element2
    assert element1 != element3