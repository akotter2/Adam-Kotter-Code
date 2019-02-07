# linked_lists.py
"""Volume 2: Linked Lists.
Adam Kotter
Math 321 - 1
9/13/18
"""


# Problem 1
class Node:
    """A basic node class for storing numeric or string data. Raises a TypeError 
    if data of type other than int, float, or str is entered. """
    def __init__(self, data):
        """Store the data in the value attribute."""
        if type(data) != str and type(data) != int and type(data) != float:
            raise TypeError("Only str, int, and float input allowed.")
        self.value = data


class LinkedListNode(Node):
    """A node class for doubly linked lists. Inherits from the Node class.
    Contains references to the next and previous nodes in the linked list.
    """
    def __init__(self, data):
        """Store the data in the value attribute and initialize
        attributes for the next and previous nodes in the list.
        """
        Node.__init__(self, data)       # Use inheritance to set self.value.
        self.next = None                # Reference to the next node.
        self.prev = None                # Reference to the previous node.


# Problems 2-5
class LinkedList:
    """Doubly linked list data structure class.

    Attributes:
        head (LinkedListNode): the first node in the list.
        tail (LinkedListNode): the last node in the list.
    """
    def __init__(self):
        """Initialize the head and tail attributes by setting
        them to None, since the list is empty initially.
        """
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        """Append a new node containing the data to the end of the list."""
        # Create a new node to store the input data.
        new_node = LinkedListNode(data)
        if self.head is None:
            # If the list is empty, assign the head and tail attributes to
            # new_node, since it becomes the first and last node in the list.
            self.head = new_node
            self.tail = new_node
        else:
            # If the list is not empty, place new_node after the tail.
            self.tail.next = new_node               # tail --> new_node
            new_node.prev = self.tail               # tail <-- new_node
            # Now the last node in the list is new_node, so reassign the tail.
            self.tail = new_node
        self.size += 1

    # Problem 2
    def find(self, data):
        """Return the first node in the list containing the data.

        Raises:
            ValueError: if the list does not contain the data.

        Examples:
            >>> l = LinkedList()
            >>> for x in ['a', 'b', 'c', 'd', 'e']:
            ...     l.append(x)
            ...
            >>> node = l.find('b')
            >>> node.value
            'b'
            >>> l.find('f')
            ValueError: <message>
        """
        #Raises a ValueError if the list is empty.
        if self.head is None:
            raise ValueError("List is empty")
        #Set node "index" iterator to the first in the list.
        current_node = self.head
        #Loop until the end of the list or the desired value is reached.
        end_of_list = False
        while not end_of_list:
            if current_node.value == data:
                return current_node
            else:
                current_node = current_node.next
            if current_node is None:
                end_of_list = True
        #Raise a value error if the end of the list is reached before the 
        #value is found.
        raise ValueError("List does not contain given value.")

    # Problem 2
    def get(self, i):
        """Return the i-th node in the list.

        Raises:
            IndexError: if i is negative or greater than or equal to the
                current number of nodes.

        Examples:
            >>> l = LinkedList()
            >>> for x in ['a', 'b', 'c', 'd', 'e']:
            ...     l.append(x)
            ...
            >>> node = l.get(3)
            >>> node.value
            'd'
            >>> l.get(5)
            IndexError: <message>
        """
        #Return errors for invalid indices.
        if i < 0:
            raise IndexError("Index cannot be negative!")
        if i >= self.size:
            raise IndexError("Index out of range!")
        current_node = self.head
        index = 0
        while index < i:
            current_node = current_node.next
            index += 1
        return current_node

    # Problem 3
    def __len__(self):
        """Return the number of nodes in the list.

        Examples:
            >>> l = LinkedList()
            >>> for i in (1, 3, 5):
            ...     l.append(i)
            ...
            >>> len(l)
            3
            >>> l.append(7)
            >>> len(l)
            4
        """
        return self.size

    # Problem 3
    def __str__(self):
        """String representation: the same as a standard Python list.

        Examples:
            >>> l1 = LinkedList()       |   >>> l2 = LinkedList()
            >>> for i in [1,3,5]:       |   >>> for i in ['a','b',"c"]:
            ...     l1.append(i)        |   ...     l2.append(i)
            ...                         |   ...
            >>> print(l1)               |   >>> print(l2)
            [1, 3, 5]                   |   ['a', 'b', 'c']
        """
        node_list = []
        for i in range(self.size):
            node_list.append(self.get(i).value)
        return(str(node_list))

    # Problem 4
    def remove(self, data):
        """Remove the first node in the list containing the data. Decrements the
        size attribute by 1.

        Raises:
            ValueError: if the list is empty or does not contain the data.

        Examples:
            >>> print(l1)               |   >>> print(l2)
            ['a', 'e', 'i', 'o', 'u']   |   [2, 4, 6, 8]
            >>> l1.remove('i')          |   >>> l2.remove(10)
            >>> l1.remove('a')          |   ValueError: <message>
            >>> l1.remove('u')          |   >>> l3 = LinkedList()
            >>> print(l1)               |   >>> l3.remove(10)
            ['e', 'o']                  |   ValueError: <message>
        """
        #Finds the node to be removed. The find() function raises a ValueError if 
        #the specified node doesn't exist.
        target = self.find(data)
        #Removing only node
        if self.size == 1:
            self.head = None
            self.tail = None
            self.size -= 1
        #Removing head
        elif self.head.value == target.value:
            self.head = target.next
            target.next.prev = None
            self.size -= 1
        #Removing tail
        elif self.tail.value == target.value:
            self.tail = target.prev
            target.prev.next = None
            self.size -= 1
        #Removing middle node
        else:
            target.next.prev = target.prev
            target.prev.next = target.next
            self.size -= 1

    # Problem 5
    def insert(self, index, data):
        """Insert a node containing data into the list immediately before the
        node at the index-th location. Increments the size attribute by 1.

        Raises:
            IndexError: if index is negative or strictly greater than the
                current number of nodes.

        Examples:
            >>> print(l1)               |   >>> len(l2)
            ['b']                       |   5
            >>> l1.insert(0, 'a')       |   >>> l2.insert(6, 'z')
            >>> print(l1)               |   IndexError: <message>
            ['a', 'b']                  |
            >>> l1.insert(2, 'd')       |   >>> l3 = LinkedList()
            >>> print(l1)               |   >>> l3.insert(1, 'a')
            ['a', 'b', 'd']             |   IndexError: <message>
            >>> l1.insert(2, 'c')       |
            >>> print(l1)               |
            ['a', 'b', 'c', 'd']        |
        """
        #Return errors for invalid indices.
        if index < 0:
            raise IndexError("Index cannot be negative!")
        if index > self.size:
            raise IndexError("Index out of range!")
        #Create new node
        new_node = LinkedListNode(data)
        #After tail or empty
        if index == self.size:
            self.append(new_node.value)
        #Before head
        elif index == 0:
            #Get head
            old_head = self.head
            #Set head prev to new node
            old_head.prev = new_node
            #Set new node next to head
            new_node.next = old_head
            #Set new node as head
            self.head = new_node
            #Increment size
            self.size += 1
        #In the middle
        else:
            #Get index-th node
            ith_node = self.get(index)
            #Set index-th node prev to new node
            ith_node.prev = new_node
            #Set new node next to index-th node
            new_node.next = ith_node
            #Get (index-1)-th node
            prev_node = self.get(index-1)
            #Set (index-1)-th node next to new node
            prev_node.next = new_node
            #Set new node prev to (index-1)-th node
            new_node.prev = prev_node
            #Increment size
            self.size += 1


# Problem 6: Deque class.
class Deque(LinkedList):
    """A class for a deque data structure. Inherits from the LinkedList class. 
    Nodes can only be added or removed from the beginning or end of the list."""
    
    def __init__(self):
        """Initializes a new deque based on inheritance from the LinkedList class."""
        LinkedList.__init__(self)
    
    def pop(self):
        """Removes the last node from the list and returns its data"""
        #Raise ValueError for empty list
        if self.size == 0:
            raise ValueError("Deque is empty!")
        #Stores data to be returned
        data = self.tail.value
        #Size one list
        if self.size == 1:
            #Remove head and tail
            self.head = None
            self.tail = None
        #All other cases
        else:
            #Sets second-to-last as tail
            self.tail = self.tail.prev
            #Removes reference to former tail
            self.tail.next = None
        #Decrements size
        self.size -= 1
        #Returns data
        return data

    def popleft(self):
        """Removes the first node from the list using the LinkedList remove() method 
        and returns its data"""
        #Raise ValueError for empty list
        if self.size == 0:
            raise ValueError("Deque is empty!")
        #Stores data to be returned
        data = self.head.value
        #Removes head, decrementing size and removing other references as appropriate
        LinkedList.remove(self, self.head.value)
        #Returns data
        return data

    def appendleft(self, data):
        """Append a new node containing the data to the beginning of the list using 
        the LinkedList insert() method."""
        #Cases with zero, one, or more elements and incrementing are handled by the 
        #inherited insert() method
        LinkedList.insert(self,0,data)

    def remove(*args, **kwargs):
        """Overrides the LinkedList remove() method to disable it"""
        raise NotImplementedError("Use pop() or popleft() for removal")
    
    def insert(*args, **kwargs):
        """Overrides the LinkedList insert() method to disable it"""
        raise NotImplementedError("Use append() or appendleft() for insertion")
       
    

# Problem 7
def prob7(infile, outfile):
    """Reverse the contents of a file by line and write the results to
    another file.

    Parameters:
        infile (str): the file to read from.
        outfile (str): the file to write to.
    """
    #Reads the contents of the infile
    with open(infile, "r") as file:
        contents = file.read()
    #Splits the contents into lines
    lines = contents.split("\n")
    #Add lines to a stack, in this case a deque only accessed from one side
    stack = Deque()
    for i in range(len(lines)):
        stack.append(lines[i])
    #Pop lines off of the stack into a queue, in this case a list
    reversed_lines = []
    for j in range(len(stack)):
        reversed_lines.append(stack.pop())
    #Write new reversed order to the outfile. Asks for new input if outfile already
    #exists, or overwrites the file if "OVERWRITE" is input. Repeats if more invalid 
    #input is given
    done = False
    while not done:
        try:
            with open(outfile, "x") as out_file:
                #Writes a new line after each line of the reversed list unless the last 
                #line is reached
                for k in range(len(reversed_lines)):
                    if k != len(reversed_lines)-1:
                        out_file.write(str(reversed_lines[k]) + "\n")
                    else:
                        out_file.write(str(reversed_lines[k]))
                        done = True
        except FileExistsError:
            the_input = input(str(outfile) + " already exists. Please input new file name, enter OVERWRITE to overwrite existing file, or enter ABORT to quit: ")
            if the_input == "OVERWRITE":
                #See above comment
                with open(outfile, "w") as out_file:
                    for k in range(len(reversed_lines)):
                        if k != len(reversed_lines)-1:
                            out_file.write(str(reversed_lines[k]) + "\n")
                        else:
                            out_file.write(str(reversed_lines[k]))
                            done = True
            elif the_input == "ABORT":
                done = True
                break
            else:
                outfile = the_input
    
"""#For testing purposes only
if __name__ == "__main__":
    prob7("english.txt","test_english.txt")
    prob7("test_2.txt","test_2_reversal.txt")"""