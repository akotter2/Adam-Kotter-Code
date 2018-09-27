#test_linked_lists.py
"""A program for testing linked_lists.py."""

import linked_lists
import pytest

@pytest.fixture
def set_up_lists():
    """Sets up four LinkedLists with different types of contents.
        Note: Will not work properly is the append_next_prev test fails."""
    #Integers
    list_1 = linked_lists.LinkedList()
    for i in range(1,11):
        list_1.append(i)
    #Floats
    list_f = linked_lists.LinkedList()
    for i in range(1,10,2):
        list_f.append(i/2)
    #Strings
    list_a = linked_lists.LinkedList()
    for x in ['a',"b",'c',"d",'e',"f",'g']:
        list_a.append(x)
    #Mixed
    list_a1 = linked_lists.LinkedList()
    for stuff in [1,'a',"3",3,"stuff","person","cow",2.7]:
        list_a1.append(stuff)
    return list_1, list_f, list_a, list_a1

def test_init():
    """Tests initialization of the LinkedList class."""
    list = linked_lists.LinkedList()
    assert list.head is None, "failed on initialize head"
    assert list.tail is None, "failed on initialize tail"
    assert list.size == 0, "failed on initialize size"

def test_append_next_prev(set_up_lists):
    """Tests the append() function in the LinkedList class and the next/prev
    attributes in the LinkedListNode class."""
    list_1, list_f, list_a, list_a1 = set_up_lists
    #Integer list tests
    assert list_1.head.value is 1, "failed on integer head"
    assert list_1.head.next.value is 2, "failed on integer next"
    assert list_1.tail.value is 10, "failed on integer tail"
    assert list_1.tail.prev.value is 9, "failed on integer prev"
    #Float list tests
    assert list_f.head.value == 0.5, "failed on float head"
    assert list_f.head.next.value == 1.5, "failed on float next"
    assert list_f.tail.value == 4.5, "failed on float tail"
    assert list_f.tail.prev.value == 3.5, "failed on float prev"
    #String list tests
    assert list_a.head.value == "a", "failed on string head"
    assert list_a.head.next.value == "b", "failed on string next"
    assert list_a.tail.value == "g", "failed on string tail"
    assert list_a.tail.prev.value == "f", "failed on string prev"
    #Mixed list tests
    assert list_a1.head.value == 1, "failed on mixed head"
    assert list_a1.head.next.value == "a", "failed on mixed next"
    assert list_a1.tail.value == 2.7, "failed on mixed tail"
    assert list_a1.tail.prev.value == "cow", "failed on mixed prev"
    #Size tests
    assert list_1.size == 10, "failed on size incrementation - 10, integer"
    assert list_f.size == 5, "failed on size incrementation - 5, float"
    assert list_a1.size == 8, "failed on size incrementation - 8, mixed"
    #Appending invalid things
    list_oops = linked_lists.LinkedList()
    with pytest.raises(TypeError) as type_error_test1:
        list_oops.append([1,2,3])
    assert type_error_test1.value.args[0] == "Only str, int, and float input allowed."
    with pytest.raises(TypeError) as type_error_test2:
        list_oops.append({1})
    assert type_error_test2.value.args[0] == "Only str, int, and float input allowed."

def test_find(set_up_lists):
    """Tests the find() function in the LinkedList class."""
    list_1, list_f, list_a, list_a1 = set_up_lists
    #Tests empty list
    list_oops = linked_lists.LinkedList()
    with pytest.raises(ValueError) as value_error_test1:
        list_oops.find(1)
    assert value_error_test1.value.args[0] == "List is empty"
    #Tests finding an integer
    assert list_1.find(4).value == 4
    assert list_a1.find(3).value == 3
    #Tests finding a float
    assert list_f.find(2.5).value == 2.5
    assert list_a1.find(2.7).value == 2.7
    #Tests finding a string
    assert list_a.find("c").value == "c"
    assert list_a1.find("3").value == "3"
    assert list_a1.find("a").value == "a"
    #Tests finding something not in the list
    with pytest.raises(ValueError) as value_error_test2:
        list_1.find("3")
    assert value_error_test2.value.args[0] == "List does not contain given value."

def test_get(set_up_lists):
    """Tests the get() function in the LinkedList class."""
    list_1, list_f, list_a, list_a1 = set_up_lists
    #Tests getting valid indices
    assert list_1.get(0).value == 1
    assert list_1.get(9).value == 10
    #Tests getting invalid indices
    with pytest.raises(IndexError) as index_error_test1:
        list_1.get(-1)
    assert index_error_test1.value.args[0] == "Index cannot be negative!"
    with pytest.raises(IndexError) as index_error_test2:
        list_1.get(10)
    assert index_error_test2.value.args[0] == "Index out of range!"

def test_len(set_up_lists):
    """Tests the __len__() magic method in the LinkedList class."""
    list_1, list_f, list_a, list_a1 = set_up_lists
    assert len(list_1) == 10, "failed on __len__() - integers, 10"
    assert len(list_a) == 7, "failed on __len__() - strings, 7"
    assert len(list_a1) == 8, "failed on __len__() - mixed, 8"

def test_str(set_up_lists):
    """Tests the __str__() magic method in the LinkedList class."""
    #Set up lists to test
    list_1, list_f, list_a, list_a1 = set_up_lists
    list_str = linked_lists.LinkedList()
    for stuff in ["A'A",'B"B',"C"]:
        list_str.append(stuff)
    #Call str()
    assert str(list_1) == "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "failed on __str__() - integers"
    assert str(list_f) == "[0.5, 1.5, 2.5, 3.5, 4.5]", "failed on __str__() - floats"
    assert str(list_a) == "['a', 'b', 'c', 'd', 'e', 'f', 'g']", "failed on __str__() - strings"
    assert str(list_str) == """["A'A", 'B"B', 'C']""", "failed on __str__() - strings with quotes"
    assert str(list_a1) == "[1, 'a', '3', 3, 'stuff', 'person', 'cow', 2.7]", "failed on __str__() - mixed"
    
def test_remove(set_up_lists):
    """Tests the remove() method in the LinkedList class."""
    #Set up lists
    list_1, list_f, list_a, list_a1 = set_up_lists
    list_only = linked_lists.LinkedList()
    list_only.append("Stuff")
    #Test head removal
    list_1.remove(1)
    assert str(list_1) == "[2, 3, 4, 5, 6, 7, 8, 9, 10]", "failed on head removal"
    assert list_1.head.value == 2, "failed on head removal"
    #Test tail removal
    list_f.remove(4.5)
    assert str(list_f) == "[0.5, 1.5, 2.5, 3.5]", "failed on tail removal"
    assert list_f.tail.value == 3.5, "failed on tail removal"
    #Test removing only node
    list_only.remove("Stuff")
    assert str(list_only) == "[]", "failed on removing only node"
    assert list_only.head is None, "failed on removing head with only one node"
    assert list_only.tail is None, "failed on removing tail with only one node"
    #Test removing other node
    list_a1.remove("cow")
    assert str(list_a1) == "[1, 'a', '3', 3, 'stuff', 'person', 2.7]", "failed on removing middle node"
    #Test removing non-existant node
    with pytest.raises(ValueError) as value_error_test1:
        list_1.remove("3")
    assert value_error_test1.value.args[0] == "List does not contain given value."

def test_insert(set_up_lists):
    """Tests the insert() method in the LinkedList class"""
    #Set up lists
    list_1, list_f, list_a, list_a1 = set_up_lists
    list_only1 = linked_lists.LinkedList()
    list_only1.append("Stuff")
    list_only2 = linked_lists.LinkedList()
    list_only2.append("Stuffs")
    list_empty = linked_lists.LinkedList()
    #Test insertion before head
    list_1.insert(0,3)
    assert str(list_1) == "[3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "failed on insertion before head"
    assert list_1.head.value == 3, "failed on insertion before head, new head"
    #Test insertion after tail
    list_f.insert(5, 2.5)
    assert str(list_f) == "[0.5, 1.5, 2.5, 3.5, 4.5, 2.5]", "failed on insertion after tail"
    assert list_f.tail.value == 2.5, "failed on insertion after tail, new tail"
    #Test insertion after one-element list
    list_only1.insert(1,"Wow")
    assert str(list_only1) == "['Stuff', 'Wow']", "failed on insertion after tail, one element"
    assert list_only1.tail.value == "Wow", "failed on insertion after tail, new tail, one element"
    #Test insertion before one-element list
    list_only2.insert(0, "Cow")
    assert str(list_only2) == "['Cow', 'Stuffs']", "failed on insertion before head, one element"
    assert list_only2.head.value == "Cow", "failed on insertion before head, new head, one element"
    #Test insertion in empty list
    list_empty.insert(0,"Nada")
    assert str(list_empty) == "['Nada']", "failed on insertion in empty list"
    assert list_empty.head.value == "Nada", "failed on insertion in empty list, new head"
    assert list_empty.tail.value == "Nada", "failed on insertion in empty list, new tail"
    #Test insertion in middle
    list_a.insert(2,"7")
    assert str(list_a) == "['a', 'b', '7', 'c', 'd', 'e', 'f', 'g']", "failed on insertion in middle"
    #Test insertion with a negative index or too-large index
    with pytest.raises(IndexError) as index_error_test1:
        list_a1.insert(-1,"Oops")
    assert index_error_test1.value.args[0] == "Index cannot be negative!"
    with pytest.raises(IndexError) as index_error_test2:
        list_a1.insert(9, "Why?!")
    assert index_error_test2.value.args[0] == "Index out of range!"
    
def test_deque():
    """Tests the Deque class"""
    #Initialize deque
    deque = linked_lists.Deque()
    #Test initialization
    assert deque.head is None, "failed on initialize head"
    assert deque.tail is None, "failed on initialize tail"
    assert deque.size == 0, "failed on initialize size"
    #Test append()
    deque.append("Cool")
    assert deque.head.value == "Cool", "failed on append, one, head"
    assert deque.tail.value == "Cool", "failed on append, one, tail"
    assert deque.get(0).value == "Cool", "failed on append, one, middle"
    deque.append("Stuff")
    assert deque.head.value == "Cool", "failed on append, two, head"
    assert deque.tail.value == "Stuff", "failed on append, two, tail"
    assert deque.get(0).value == "Cool", "failed on append, two, middle"
    assert deque.get(1).value == "Stuff", "failed on append, two, middle"
    #Test appendleft()
    deque.appendleft("Wowzers")
    assert deque.head.value == "Wowzers", "failed on appendleft, head"
    assert deque.tail.value == "Stuff", "failed on appendleft, tail"
    assert deque.get(0).value == "Wowzers", "failed on appendleft, get head"
    assert deque.get(1).value == "Cool", "failed on appendleft, get middle"
    deque.appendleft("Daaang...")
    assert deque.head.value == "Daaang...", "failed on appendleft, head"
    assert deque.tail.value == "Stuff", "failed on appendleft, tail"
    assert deque.get(0).value == "Daaang...", "failed on appendleft, get head"
    assert deque.get(2).value == "Cool", "failed on appendleft, get middle"
    #Test pop()
    pop_right = deque.pop()
    assert pop_right == "Stuff", "failed on pop"
    assert deque.tail.value == "Cool", "failed on pop, tail"
    assert deque.get(2).value == "Cool", "failed on pop, index"
    #Test popleft()
    pop_left = deque.popleft()
    assert pop_left == "Daaang...", "failed on popleft"
    assert deque.head.value == "Wowzers", "failed on popleft, head"
    assert deque.get(0).value == "Wowzers", "failed on pop, index"
    #Test removal of remove()
    with pytest.raises(NotImplementedError) as implementation_test1:
        deque.remove("Cool")
    assert implementation_test1.value.args[0] == "Use pop() or popleft() for removal"
    #Test removal of insert()
    with pytest.raises(NotImplementedError) as implementation_test2:
        deque.insert(0,"Cool")
    assert implementation_test2.value.args[0] == "Use append() or appendleft() for insertion"

def test_prob_7():
    """Tests Problem 7 by assuring that the outfile is the reversal of the infile"""
    #Creates file to be tested
    linked_lists.prob7("english.txt", "test_english.txt")
    #Reads the files and splits them into lines
    with open("english.txt", "r") as file:
        english = file.read()
    english_lines = english.split("\n")
    with open("test_english.txt", "r") as file:
        test_english = file.read()
    english_lines = english.split("\n")
    test_lines = test_english.split("\n")
    #Loops forward through one file and backwards through the other to assure that 
    #each file is the reversed form of the other
    for i in range(len(english_lines)):
        assert english_lines[i] == test_lines[-i-1], "failed on reversal of file"
    
