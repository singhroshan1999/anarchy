import operator


class Heap(object):
    """"
    Attributes:
        heap: List representation of the heap
        compare(p, c): comparator function, returns true if the relation between p and c is parent-chield
    """
    def __init__(self, heap=None, compare=operator.gt):
        self.heap = [] if heap is None else heap
        self.compare = compare

    def __repr__(self):
        return 'Heap({!r}, {!r})'.format(self.heap, self.compare)

    def _inv_heapify(self, child_index):
        """
        Do heapifying starting from bottom till it reaches the root.
        """
        heap, compare = self.heap, self.compare
        child = child_index
        while child > 0:
            parent = child // 2
            if compare(heap[parent], heap[child]):
                return
            heap[parent], heap[child] = heap[child], heap[parent]
            child = parent

    def _heapify(self, parent_index):
        """
        Do heepifying starting from the root.
        """
        heap, compare = self.heap, self.compare
        length = len(heap)
        if length == 1:
            return
        parent = parent_index
        while 2 * parent < length:
            child = 2 * parent
            if child + 1 < length and compare(heap[child + 1], heap[child]):
                child += 1
            if compare(heap[parent], heap[child]):
                return
            heap[parent], heap[child] = heap[child], heap[parent]
            parent = child

    def del_min(self):
        heap = self.heap
        last_element = heap.pop()
        if not heap:
            return last_element
        item = heap[0]
        heap[0] = last_element
        self._heapify(0)
        return item

    def min(self):
        if not self.heap:
            return None
        return self.heap[0]

    def add(self, element):
        self.heap.append(element)
        self._inv_heapify(len(self.heap) - 1)

if __name__ == "__main__":
    def cmp(a,b):
        return a-b
    l = []
    heapp = Heap(l)
    for i in range(100):
        heapp.add(i)
    for i in range(100):
        print(heapp.del_min())