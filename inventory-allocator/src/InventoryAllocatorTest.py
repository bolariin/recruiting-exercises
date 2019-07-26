import unittest
from InventoryAllocator import InventoryAllocator

class InventoryAllocatorTest(unittest.TestCase):

    # If an order is provided, we can only expect an empty list as the result
    def test_only_empty_order(self):
        order = { }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 5 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])
    
    # if an empty warehouse distribution list is provided, we can only expect an empty list as the result
    def test_only_empty_warehouse_distribution_list(self):
        order = { 'apple': 6 }
        warehouseDistributionList = []

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])

    # if both an empty order and empty warehouse distribution list is provided, we can only expect an empty list as the result
    def test_both_empty_order_and_warehouse_distribution_list(self):
        order = { }
        warehouseDistributionList = []

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])
    
    # if a particular ordered item is not present in any warehouse, it returns an empty list so we can be aware of an error with the 
    # order
    def test_order_item_not_present_in_any_warehouse(self):
        order = { 'apple': 6, 'orange': 4, 'banana': 10 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 7 } }, { 'name': 'dm', 'inventory': { 'orange': 5 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])
    
    # if ordered amount for an item is zero, no need to include it in the result
    def test_order_amount_is_zero(self):
        order = { 'apple': 0, 'orange': 4 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 7 } }, { 'name': 'dm', 'inventory': { 'orange': 5 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'dm': { 'orange': 4 } }])
    
    # We expect everything to work as expected even if the inventory for a warehouse is empty as long the order can
    # be met by other warehouses
    def test_empty_inventory_for_one_warehouse(self):
        order = { 'apple': 6, 'orange': 4 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { } }, { 'name': 'dm', 'inventory': { 'apple' : 10, 'orange': 5 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'dm': { 'apple': 6, 'orange': 4 } }])
    
    # We expect everything to work as expected even if the inventory for multiple warehouses is empty as long the order 
    # can be met by other warehouses
    def test_empty_inventory_for_multiple_warehouses(self):
        order = { 'apple': 6, 'orange': 4 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { } }, { 'name': 'dm', 'inventory': { 'apple' : 10, 'orange': 5 } },
        { 'name': 'om', 'inventory': { }} ]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'dm': { 'apple': 6, 'orange': 4 } }])
    
    # We expect an empty list because even if the order amount is zero, ordering an item that does not exist in any warehouse 
    # should be consistent, just in case a mistake was made
    def test_order_amount_is_zero_and_item_not_in_any_warehouse(self):
        order = { 'apple': 6, 'orange': 4, 'banana': 0 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 7 } }, { 'name': 'dm', 'inventory': { 'orange': 5 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])
    
    # Test case where we have a single item in our order and it is out of stock at the warehouses available
    def test_single_order_item_out_of_stock(self):
        order = { 'apple': 6 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }, { 'name': 'dm', 'inventory': { 'orange': 0 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])
    
    # Simple case where an order can be met by multiple warehouses available
    def test_split_items_across_warehouses_to_meet_order_v1(self):
        order = { 'apple': 10 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'owd': { 'apple': 5 }}, { 'dm': { 'apple': 5 } }])

    # Simple case where an order can be met by multiple warehouses but the amount is the same for all warehouses
    # This is just to see that the two cheaper warehouses are chosen.
    def test_split_items_across_warehouses_to_meet_order_v2(self):
        order = { 'apple': 8 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 4 } }, { 'name': 'dm', 'inventory': { 'apple': 4 }},
            { 'name': 'om', 'inventory': { 'apple': 4 } }]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'owd': { 'apple': 4 }}, { 'dm': { 'apple': 4 } }])

    # Simple case where an order can be met by multiple warehouses but it's better to choose a further warehouse
    def test_split_items_across_warehouses_to_meet_order_v3(self):
        order = { 'apple': 11 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5 }},
            { 'name': 'om', 'inventory': { 'apple': 6 }}]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'owd': { 'apple': 5 }}, { 'om': { 'apple': 6 } }])
    
    # This is to test a complicated case where we might have some items matched exactly at a warehouse or matchec through multiple
    # warehouses
    def testSplitItemsAcrossWarehousesToMeetOrderv4(self):
        order = { 'toothpaste': 31, 'tissue box': 19, 'sand paper': 1, 'face wash': 44, 'twezzers': 43, 'packing peanuts': 52, 'teddies': 18, 
                    'money': 14, 'sharpie': 39, 'brocolli': 19, 'ice cube tray':20, 'thermometer': 15, 
                    'bananas': 37, 'table': 24, 'white out': 41, 'perfume': 18, 'rubber duck': 28, 
                    'cookie jar': 33, 'sandal': 36, 'rug': 15, 'radio': 39, 'seat belt': 19, 'glasses':24, 
                    'remote': 41, 'chair': 31, 'sponge': 48, 'candle': 23, 'bowl': 30, 'blanket': 28, 'key chain': 45 }

        warehouseDistributionList = [{'name': 'v0', 'inventory': {'cookie jar': 18, 'packing peanuts': 18, 'rubber band': 13, 
            'tooth picks': 16, 'tissue box': 10, 'sharpie': 16}}, {'name': 'v1', 'inventory': {'sponge': 6, 'chair': 9, 'face wash': 13, 
            'leg warmers': 1, 'candle': 4, 'toothpaste': 13, 'lamp shade': 13, 'flowers': 1, 'twezzers': 14, 'eraser': 20, 'money': 8, 
            'thermometer': 14, 'shoes': 12, 'bottle cap': 4, 'checkbook': 12, 'tooth picks': 13, 'lamp': 16, 'perfume': 12, 'glasses': 5,
            'sharpie': 14, 'blanket': 8, 'bowl': 3, 'rubber duck': 5, 'washing machine': 20}}, 
            {'name': 'v2', 'inventory': {'sand paper': 18, 'remote': 7, 'soy sauce packet': 19, 'leg warmers': 14, 'helmet': 7, 'glasses': 1, 
            'air freshener': 15, 'checkbook': 15}}, {'name': 'v3', 'inventory': {'twezzers': 12, 'seat belt': 12, 'bowl': 19, 'rug': 12, 'air freshener': 1, 
            'lamp shade': 13, 'sponge': 6, 'rubber band': 6, 'shoes': 13, 'key chain': 10}}, {'name': 'v4', 'inventory': {'sharpie': 17, 'perfume': 8, 
            'seat belt': 15}}, {'name': 'v5', 'inventory': {'cookie jar': 16, 'ice cube tray': 14, 'air freshener': 6, 'tissue box': 20, 'seat belt': 9, 
            'pencil': 12, 'perfume': 17}}, {'name': 'v6', 'inventory': {'shoes': 3, 'leg warmers': 5, 'pencil': 20, 'twezzers': 3, 'remote': 17, 
            'blanket': 5, 'bananas': 18, 'bowl': 11, 'key chain': 5, 'lamp': 13, 'rug': 3, 'ice cube tray': 20, 'radio': 2, 'money': 20, 
            'air freshener': 13, 'sand paper': 18, 'flowers': 15, 'rubber duck': 2, 'chair': 1, 'balloon': 12, 'rubber band': 4, 'boom box': 18, 
            'soy sauce packet': 5, 'tissue box': 3, 'eraser': 10, 'candle': 17}}, {'name': 'v7', 'inventory': {'brocolli': 16, 'washing machine': 2, 
            'helmet': 7, 'toothpaste': 5, 'teddies': 10, 'pencil': 4, 'soy sauce packet': 1, 'sharpie': 20, 'air freshener': 14, 'shoes': 4, 'button': 20,
            'twezzers': 3, 'remote': 14, 'table': 6, 'bottle cap': 9, 'thermometer': 12, 'sponge': 9, 'white out': 3, 'tire swing': 8, 
            'face wash': 19, 'eraser': 9, 'perfume': 14}}, {'name': 'v8', 'inventory': {'tire swing': 4, 'shoes': 3, 'seat belt': 5, 
            'leg warmers': 15, 'money': 17, 'eraser': 4, 'twezzers': 12, 'sand paper': 7, 'air freshener': 5, 'face wash': 9, 'rug': 3, 
            'pencil': 5, 'balloon': 4}}, {'name': 'v9', 'inventory': {'twezzers': 13, 'air freshener': 12, 'thermometer': 10, 'seat belt': 6, 
            'washing machine': 19, 'rug': 2, 'tissue box': 10, 'glasses': 13, 'sponge': 9, 'helmet': 15, 'boom box':7, 'teddies': 8, 'sandal': 5, 
            'checkbook': 20, 'blanket': 1, 'pencil': 9, 'tire swing': 7, 'leg warmers': 15, 'lamp shade': 13, 'soy sauce packet': 17, 'face wash': 2, 
            'bowl': 7}}, {'name': 'v10', 'inventory': {'sand paper': 14, 'tooth picks': 9, 'remote': 19, 'bananas': 3, 'rubber duck': 16, 'tissue box': 18,
            'table': 15, 'twezzers': 19, 'pencil': 17, 'soy sauce packet':15, 'toothpaste': 19, 'seat belt': 19, 'washing machine': 14, 'perfume': 13, 
            'leg warmers': 12, 'tire swing': 2, 'face wash': 14, 'rubber band': 2, 'white out': 30, 'checkbook': 8, 'candle': 2, 'flowers': 17, 'balloon': 12}}, 
            {'name': 'v11', 'inventory': {'shoes': 2, 'washing machine': 7, 'air freshener': 2, 'checkbook': 14, 'sand paper': 12, 'soy sauce packet': 15, 
            'seat belt': 10, 'lamp': 20, 'flowers': 12, 'perfume': 11, 'tire swing': 2, 'radio': 6, 'lamp shade': 4, 'toothpaste': 10, 'remote': 14}}, 
            {'name': 'v12', 'inventory': {'bowl': 5, 'tissue box': 16, 'blanket': 2, 'balloon': 1, 'seat belt': 13, 'money': 13, 'remote': 1, 'button': 5, 
            'checkbook': 12, 'shoes': 9, 'pencil': 9, 'sponge': 20, 'sand paper': 4, 'air freshener': 7, 'lamp shade': 5, 'teddies': 8, 'ice cube tray': 2, 
            'boom box': 14, 'face wash': 8, 'washing machine': 15, 'bottle cap': 17, 'tooth picks': 1, 'leg warmers': 4, 'twezzers': 16, 'rubber band': 13, 
            'chair': 16}}, {'name': 'v13', 'inventory': {'seat belt': 7, 'boom box': 10, 'blanket': 10, 'candle': 8, 'perfume': 14, 'ice cube tray': 13, 
            'washing machine': 20, 'balloon': 10, 'tissuebox': 6}}, {'name': 'v14', 'inventory': {'table': 2, 'teddies': 17, 'ice cube tray': 4, 'tire swing': 5, 
            'face wash': 8, 'pencil': 4, 'glasses': 12, 'tissue box': 16, 'checkbook': 3, 'washing machine': 10, 'white out': 3, 'twezzers': 16, 'sandal': 19, 
            'remote': 7, 'bowl': 16, 'boom box': 13, 'rubber band': 10, 'rug': 10, 'sand paper': 18, 'air freshener': 5, 'brocolli': 11, 'radio': 12, 'money': 9, 
            'bottle cap': 3, 'bananas': 20, 'thermometer': 5}}, {'name': 'v15', 'inventory': {'tooth picks': 4, 'chair': 11, 'button': 8, 'shoes': 4, 'checkbook': 7, 
            'remote': 18}}, {'name': 'v16', 'inventory': {'lamp shade': 6, 'rug': 1, 'pencil': 14, 'leg warmers': 11, 'remote': 5, 'soy sauce packet': 2, 'boom box': 13, 
            'sharpie': 5, 'blanket': 4, 'ice cube tray': 8, 'candle': 18, 'balloon': 2, 'tissue box': 4, 'face wash': 20, 'table': 1, 'key chain': 15, 'lamp': 14, 
            'eraser':6, 'radio': 10, 'rubber band': 14, 'tire swing': 5, 'white out': 14, 'perfume': 16, 'chair': 15, 'tooth picks': 11, 'cookie jar': 2, 
            'toothpaste': 11}}, {'name': 'v17', 'inventory': {'radio': 14, 'glasses': 19, 'seat belt': 1, 'brocolli': 11, 'key chain': 10, 'shoes': 16, 
            'cookie jar': 5, 'bananas': 6, 'tire swing': 18, 'perfume': 16, 'twezzers': 2}}, {'name': 'v18', 'inventory': {'packing peanuts': 16, 
            'air freshener': 15, 'bowl': 18, 'balloon': 18, 'candle': 14, 'sponge': 18, 'shoes': 18, 'twezzers': 16, 'bananas': 9, 'chair': 11, 
            'soy sauce packet': 13, 'perfume': 15, 'radio': 10, 'face wash': 17, 'helmet': 9, 'tooth picks': 14}}, 
            {'name': 'v19', 'inventory': {'radio': 7, 'glasses': 12, 'sponge': 10, 'packing peanuts': 4, 'blanket': 2, 'boom box': 10, 'bananas': 18, 
            'sand paper': 17, 'twezzers': 19, 'tissue box': 8, 'perfume': 6, 'chair': 14, 'seat belt': 4, 'rubber band': 7, 'lamp': 17, 'candle': 18, 
            'toothpaste': 7, 'lamp shade': 20, 'button': 18, 'leg warmers': 12}}, {'name': 'v20', 'inventory': {'balloon': 13, 'teddies': 6}}, 
            {'name': 'v21', 'inventory': {'key chain': 19, 'sponge': 9, 'eraser': 18, 'air freshener': 17, 'balloon': 10, 'thermometer': 15, 
            'perfume': 6, 'button': 3, 'pencil': 8}}, {'name': 'v22', 'inventory': {'packing peanuts': 40, 'perfume': 16, 'face wash': 6, 
            'rubber band': 15, 'helmet': 20, 'air freshener': 6, 'thermometer': 18, 'balloon': 2, 'sandal': 18, 'bowl': 10, 'table': 7}}, 
            {'name': 'v23', 'inventory': {'white out': 3, 'tooth picks': 7, 'candle': 11, 'cookie jar': 2, 'key chain': 5, 'ice cube tray': 4, 
            'leg warmers': 9, 'checkbook': 16, 'table': 5, 'twezzers': 2, 'lamp': 1, 'face wash': 20, 'rubber duck': 9, 'helmet': 8, 
            'washing machine': 18, 'sandal': 11, 'toothpaste': 11, 'sponge': 18, 'money': 2, 'blanket': 5, 'teddies': 17, 'brocolli': 18}}, 
            {'name': 'v24', 'inventory': {'radio': 16, 'sharpie': 10, 'air freshener': 13, 'checkbook': 19}}, {'name': 'v25', 'inventory': 
            {'washing machine': 8, 'sharpie': 6, 'tissue box': 6, 'seat belt': 19, 'tooth picks': 1, 'air freshener': 9, 'candle': 5, 'table': 18, 
            'tire swing': 13, 'teddies': 1, 'toothpaste': 1, 'ice cube tray': 2, 'key chain': 3, 'brocolli': 16, 'soy sauce packet': 7, 'chair': 11, 
            'lamp shade': 8, 'balloon': 19}}, {'name': 'v26', 'inventory': {'rubber duck': 19, 'thermometer': 20, 'boom box': 10, 
            'remote': 4, 'money': 19, 'table': 8, 'shoes': 15, 'chair': 18, 'lamp': 16, 'rug': 1}}]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        expectedShipment = [{'v1': {'toothpaste': 13, 'blanket': 8}}, 
        {'v10': {'toothpaste': 18, 'face wash': 14, 'twezzers': 19, 'table': 15, 'white out': 30, 'rubber duck': 16, 'seat belt': 19, 'remote': 10}}, 
        {'v5': {'tissue box': 19, 'perfume': 17, 'cookie jar': 15}}, {'v2': {'sand paper': 1}}, 
        {'v7': {'face wash': 19, 'sharpie': 6, 'brocolli': 16, 'table': 6, 'white out': 3, 'perfume': 1, 'remote': 14}}, 
        {'v8': {'face wash': 9, 'twezzers': 12}}, {'v16': {'face wash': 2, 'white out': 8, 'radio': 10, 'chair': 4, 'candle': 6, 'blanket': 4, 'key chain': 15}}, 
        {'v12': {'twezzers': 12, 'chair': 16, 'sponge': 20}}, {'v0': {'packing peanuts': 18, 'sharpie': 16, 'cookie jar': 18}}, 
        {'v18': {'packing peanuts': 16, 'radio': 3, 'sponge': 18}}, {'v22': {'packing peanuts': 18, 'table': 3, 'sandal': 17}}, 
        {'v14': {'teddies': 17, 'bananas': 19, 'sandal': 19, 'rug': 3, 'radio': 12, 'glasses': 11}}, 
        {'v23': {'teddies': 1, 'brocolli': 3, 'rubber duck': 9}}, 
        {'v6': {'money': 14, 'ice cube tray': 20, 'bananas': 18, 'remote': 17, 'candle': 17, 'bowl': 11, 'blanket': 5}}, 
        {'v4': {'sharpie': 17}}, {'v21': {'thermometer': 15, 'key chain': 10}}, {'v26': {'rubber duck': 3}}, 
        {'v3': {'rug': 12, 'bowl': 19, 'key chain': 10}}, {'v17': {'radio': 14, 'key chain': 10}},
        {'v9': {'glasses': 13, 'sponge': 9}}, {'v15': {'chair': 11}}, {'v19': {'sponge': 1, 'blanket': 1}}, {'v13': {'blanket': 10}}]

        self.assertEqual(shipment, expectedShipment)
    
    # Testing case where we have multiple ordered items that happen to be out of stock at the warehouses available
    def test_multiple_order_items_out_of_stock(self):
        order = { 'apple': 6, 'orange': 4, 'banana': 5 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 0 } }, { 'name': 'dm', 'inventory': { 'orange': 0 } },
        { 'name': 'om', 'inventory': { 'apple': 4, 'banana': 6  }} ]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [])
    
    # This is to test where ordered amount is matched exactly at a single warehouse
    def test_exact_order_match_from_single_warehouse(self):
        order = { 'apple': 6 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 7 } }, { 'name': 'dm', 'inventory': { 'orange': 5 } },
        { 'name': 'om', 'inventory': { 'apple': 6 }} ]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'owd': { 'apple': 6 }} ])

    # This is to test where ordered amount of an item is met at a different warehouse for each item
    def test_exact_order_match_from_multiple_warehouses(self):
        order = { 'apple': 6, 'orange': 4, 'banana': 10 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 7 } }, { 'name': 'dm', 'inventory': { 'orange': 5 } },
        { 'name': 'om', 'inventory': { 'banana': 10 }} ]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'owd': { 'apple': 6 }}, { 'dm': { 'orange': 4 } }, { 'om': { 'banana': 10 } }])
    
    # This is to test case where we can find an exact match at a farther warehouse and chose that over processing the order at multiple closer
    # warehouses
    def test_exact_order_match_from_warehouse(self):
        order = { 'apple': 10 }
        warehouseDistributionList = [{ 'name': 'owd', 'inventory': { 'apple': 5 } }, { 'name': 'dm', 'inventory': { 'apple': 5 } },
        { 'name': 'om', 'inventory': { 'apple': 10 }} ]

        inventoryAllocator = InventoryAllocator(order, warehouseDistributionList)
        shipment = inventoryAllocator.allocate_inventory()

        self.assertEqual(shipment, [{ 'om': { 'apple': 10 } }])
    

if __name__ == "__main__":
    unittest.main()