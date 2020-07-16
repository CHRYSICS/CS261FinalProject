# hash_map.py
# ===================================================
# Implement a hash map with chaining
# Christopher Eckerson
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def reset(self):
        """Reset linked list to contain no nodes"""
        self.head = None
        self.size = 0

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        # get list of buckets in hash table
        buckets = self._buckets
        # for each bucket, reset so that its head contains none and size is zero
        for bucket in buckets:
            bucket.reset()
        # after buckets have been clears, reset size to zero
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # create hash from key with provided hash function
        hash = self._hash_function(key)
        # convert hash into an index value within the capacity of the buckets list
        index = hash % self.capacity
        # get linked list stored at index value
        bucket = self._buckets[index]
        # get node from linked list that contains the key
        node = bucket.contains(key)
        # if no node was returned, return false
        if node is None:
            return None
        # else return the value stored in node with given key
        else:
            return node.value

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # initialize new instant of Hashtable with given capacity
        newHashTable = HashMap(capacity, self._hash_function)
        # get list of buckets from current hash table
        buckets = self._buckets
        # for each bucket in current hash table
        for bucket in buckets:
            # Loop through linked list,
            # get key and value from head node,
            # put in new hash table,
            # reassign head to next node until end of linked list is reached (returns None)
            while bucket.head is not None:
                node = bucket.head
                newHashTable.put(node.key, node.value)
                bucket.head = node.next
        # after all key/value pairs have been rehashed to new table,
        # assign attributes of new hash table to current hash table
        self._buckets = newHashTable._buckets
        self.capacity = newHashTable.capacity
        self.size = newHashTable.size
        # at this point current hash table is updated, exit function, freeing new hash table

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        # create hash from key with provided hash function
        hash = self._hash_function(key)
        # convert hash into an index value within the capacity of the buckets list
        index = hash % self.capacity
        # get linked list stored at index value
        bucket = self._buckets[index]
        # get node from linked list that contains the key
        node = bucket.contains(key)
        # if no node was returned to contain the key
        if node is None:
            # increment hash table size by one
            self.size += 1
            # add a new node to the linked list with the given key and value pair
            bucket.add_front(key, value)
        # else a node was returned that contained the key
        else:
            # update node value to the given value
            node.value = value

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # create hash from key with provided hash function
        hash = self._hash_function(key)
        # convert hash into an index value within the capacity of the buckets list
        index = hash % self.capacity
        # get linked list stored at index value
        bucket = self._buckets[index]
        bucket.remove(key)

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # create hash from key with provided hash function
        hash = self._hash_function(key)
        # convert hash into an index value within the capacity of the buckets list
        index = hash % self.capacity
        # get linked list stored at index value
        bucket = self._buckets[index]
        # get node from linked list that contains the key
        node = bucket.contains(key)
        # if no node was returned to contain the key
        if node is None:
            return False
        # else the key was found in the bucket
        else:
            return True

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        # initialize empty bucket counter variable
        count = 0
        # iterate through buckets in hash table
        for bucket in self._buckets:
            # if the linked list bucket is empty
            if bucket.head is None:
                # iterate counter by 1
                count += 1
            # else head of linked list contains node, bucket not empty
            else:
                # continue to next bucket
                continue
        # after iterating through hash table, return the counter value
        return count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        # calculate table load radio
        tableLoad = self.size/self.capacity
        return tableLoad

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
