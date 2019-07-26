class Heap:
    """
        Based on heap implementation from 
        https://runestone.academy/runestone/books/published/pythonds/Trees/BinaryHeapImplementation.html
    """
    def __init__(self):
        self.heapList = [(0, 0)]
        self.currentSize = 0

        self.total = 0 # keeps track of the total of items added to the heap
        self.orderedMap = { } # keeps track of the warehouse and itemAmount for the items added to the heap

    def get_min_child(self):
        return self.heapList[1]

    def perc_up(self, i):
        while i // 2 > 0:
            if self.heapList[i][1] <= self.heapList[i // 2][1]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i = i // 2
    
    def insert(self, k):
        self.heapList.append(k)

        self.total += k[1]
        self.orderedMap[k[0]] = k[1]

        self.currentSize = self.currentSize + 1
        self.perc_up(self.currentSize)
    
    def perc_down(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.min_child(i)
            if self.heapList[i][1] > self.heapList[mc][1]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def min_child(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1
    
    def del_min(self):
        retval = self.heapList[1]
        
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.total -= self.heapList[1][1]

        self.orderedMap.pop(retval[0])

        self.heapList.pop()
        self.perc_down(1)
        return retval
    
    def update_shipment(self, shipment, itemName, itemAmount):
        total = itemAmount
        for warehouse, amount in self.orderedMap.items():
            if not (warehouse in shipment):
                shipment[warehouse] = {}

            if total <= amount:
                shipment[warehouse].update({ itemName: total })
                return
            else:
                total -= amount
                shipment[warehouse].update({ itemName: amount })



