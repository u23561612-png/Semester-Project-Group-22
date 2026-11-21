#this is the .test file for testing the inventory_logic.py functions

from inventory_logic import (
    calculate_eoq,
    calculate_quantity_needed,
    checking_stock_status,
    complete_replenishment_task,
    reorder_supplier_stock,
    update_performance_stats
)

def running_test():
    print("-------------------------------------------------------------------------------------------")
    print("                     TESTING INVENTORY & REPLENISHMENT LOGIC                               ")
    print("-------------------------------------------------------------------------------------------")

    #entering cutom parameters using products on dasboard
    product_name = "PnP Full Cream Milk 2L" #can import ny product and run the test, i just used this product as an exapmle
    shelf_qty = 5
    req_shelf_qty = 25
    receiving_qty = 20
    
    annual_demand = 14600  #  hypothetical units per year
    ordering_cost = 50.0   #  item ordering cost in Rand
    holding_cost = 2.50    #  holding cost in Rand per unit peryear

    # running the calcs
    #---------------------------------------------------------------
    qty_needed = calculate_quantity_needed(req_shelf_qty, shelf_qty)
    
    status = checking_stock_status(receiving_qty, qty_needed)
    
    eoq = calculate_eoq(annual_demand, ordering_cost, holding_cost)
    #----------------------------------------------------------------
    
    #printing the results
    print(f"\n[Initial status of product: {product_name}]")
    print(f"Current Shelf Qty:            {shelf_qty}")
    print(f"Required Shelf Qty:           {req_shelf_qty}")
    print(f"Quantity Needed:              {qty_needed}")
    print(f"Receiving Stock Qty:          {receiving_qty}")
    print(f"Initial Status:               {status}")
    print(f"Calculated EOQ:               {round(eoq, 1)} units")

    # testing the task of dispatching
    pending_tasks = 0
    completed_tasks = 24
    
    print("\n  Dispatching a Task ")
    pending_tasks, completed_tasks = update_performance_stats(pending_tasks, completed_tasks, action="dispatch")
    print(f"Pending Tasks: {pending_tasks} | Completed Tasks: {completed_tasks}")

    # testing the replenishment and stock deduction
    print("\n  Completing Task (Moving recieving Stock to the allocated Shelf) ")
    # Moving 36 units form recieving area to the shelves
    qty_to_move = 36
      
    new_shelf_qty, new_receiving_qty, warning = complete_replenishment_task(
        
        shelf_qty, req_shelf_qty, receiving_qty, qty_to_move
        
    )
    
    # Updating the statistics on the dashboard after the task is completed
    pending_tasks, completed_tasks = update_performance_stats(pending_tasks, completed_tasks, action="complete ")
    
    new_status = checking_stock_status(new_receiving_qty, calculate_quantity_needed(req_shelf_qty, new_shelf_qty))

    print(f"Updated Shelf Qty:     {new_shelf_qty}")
    print(f"Updated Receiving Qty: {new_receiving_qty}")
    print(f"New Stock Status:      {new_status}")
    print(f"Pending Tasks:         {pending_tasks} | Completed Tasks: {completed_tasks}")
    
    if warning:
        print(f"\n[POP-UP ALERT on Dasboard] {warning}")

    # 5. TEST REORDERING SUPPLIER STOCK
    if new_receiving_qty == 0:
        print("\n--- Placing Supplier Reorder ---")
        supplier_order_qty = 50
        restocked_receiving = reorder_supplier_stock(new_receiving_qty, supplier_order_qty)
        final_status = checking_stock_status(restocked_receiving, 0)
        
        print(f"Reordered Amount:      {supplier_order_qty} units")
        print(f"New Receiving Stock:   {restocked_receiving} units")
        print(f"Final Status:          {final_status}")

    print("\n--------------------------------------------------------------------------------")

if __name__ == "__main__":
    running_test()