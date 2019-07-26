from Heap import Heap

"""
    I use Python 3.7, it is only important because the order of keys is preserved in dictionaries.

    Assumption made:
        * Format for order and warehouseDistributionList have checked to meet acceptable format
        * We prefer to order from as few warehouses as possible so in the case that we have the 
            option to order from two close warehouses, we would prefer to order the same item
            from a single farther warehouse
        * if order amount is zero or less, then it is not included in the result
    
    Reason for the heap and How the Heap works

    The heap was used to support the idea of wanting as few warehouses as possible in the event
    we need to split the order across different warehouses. To order from as few warehouses as possible.
    We only want to store as few options in our heap as possible
    The rule for removing items from our Heap is once the total of all items in the 
    Heap is greater than the ordered amount, we want to check that if by removing the smallest item in 
    our heap, we still have a total that is atleast as large as the ordered amount.

    One thing about removing the smallest item is the case if the amount of a particular item is the same
    across different warehouses. We want to remove the rightmost item warehouse first. The Heap also supports
    this behavior of removing items. By allowing items to "move up" the heap even if it is equal to its parent but
    items can only "move down" the heap only if they are greater than their children. The order of insertion into
    the Heap is based on the cost, so the cheapest to ship from is inserted first with the most expensive inserted
    last.
"""
class InventoryAllocator:
    def __init__(self, order, warehouseDistributionList):
        self.order = order
        self.warehouseDistributionList = warehouseDistributionList
        
        # catalog works as sort of a reverse index
        # so we simply use the name of the item we are looking for to 
        # lookup warehouses that contain the item

        # catalog format 
        # catalog['name of item'] = {'total': 'total number of all items ', 'distribution': ['warehouse': 'amount']}
        self.catalog = {}
        self._create_catalog()
    
    def _create_catalog(self):
        for inventoryDistribution in self.warehouseDistributionList:
            warehouse = inventoryDistribution['name']
            inventory = inventoryDistribution['inventory']

            for itemName, itemAmount in inventory.items():
                # check if item is in catalog
                if not (itemName in self.catalog):
                    self.catalog[itemName] = { 'total': 0, 'distribution': [] }
                
                self.catalog[itemName]['total'] += itemAmount
                self.catalog[itemName]['distribution'].append((warehouse, itemAmount))
    
    def _create_shipment_from_heap(self, distributionHeap, shipment, itemName, itemAmount):
        distributionHeap.update_shipment(shipment, itemName, itemAmount)
    
    def allocate_inventory(self):
        shipment = { }
        
        for itemName, itemAmount in self.order.items():
            # is item in catalog
            if not (itemName in self.catalog):
                return []

            # can ordered amount be met through some combination of items 
            # contained in available warehouses
            # if not then no point to continue
            if itemAmount > self.catalog[itemName]['total']:
                return []
            
            if itemAmount <= 0:
                continue
            
            distributionHeap = Heap()
            itemTotalAmount = self.catalog[itemName]['total']

            for warehouse, amountInWarehouse in self.catalog[itemName]['distribution']:
                if itemAmount <= amountInWarehouse:
                    # if we get into if statement means our order for a particular item
                    # can be found at a single warehouse
                    if not (warehouse in shipment):
                        shipment[warehouse] = {}
                    shipment[warehouse].update({ itemName: itemAmount })
                    break
                else:
                    itemTotalAmount -= amountInWarehouse
                    distributionHeap.insert((warehouse, amountInWarehouse))

                    # To order from as few warehouses as possible 
                    # We only want to store as few options in our heap as possible
                    # The rule for removing items from our Heap is once the total of all items in the 
                    # Heap is greater than the ordered amount, we want to check that if by removing the smallest item in 
                    # our heap, we still have a total that is atleast as large as the ordered amount
                    if distributionHeap.total - distributionHeap.get_min_child()[1] >= itemAmount:
                        # eject smallest
                        distributionHeap.del_min()
                    
                    # once itemTotalAmount is zero, then we have viewed every possible warehouse
                    if itemTotalAmount == 0:
                        # process amount
                        self._create_shipment_from_heap(distributionHeap, shipment, itemName, itemAmount)
                        break
        return [ { warehouse: order } for warehouse, order in shipment.items() ]
