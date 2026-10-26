"""
Test Runner for Pick n Pay Inventory Logic Functions
"""

from inventory_logic import (
    calculate_eoq,
    calculate_quantity_needed,
    check_stock_status,
    complete_replenishment_task,
    reorder_supplier_stock,
    update_performance_stats
)

def run_custom_test():
    print("-------------------------------------------------------------------------------------------")
    print("                     TESTING INVENTORY & REPLENISHMENT LOGIC     ")
    print("-------------------------------------------------------------------------------------------")

    # 1. ENTER YOUR CUSTOM PARAMETERS HERE
    product_name = "PnP Full Cream Milk 2L"
    shelf_qty = 5
    req_shelf_qty = 25
    receiving_qty = 20
    
    annual_demand = 14600  # units/year
    ordering_cost = 50.0   # Rand
    holding_cost = 2.50    # Rand/unit/year

    # 2. RUN CALCULATIONS
    qty_needed = calculate_quantity_needed(req_shelf_qty, shelf_qty)
    status = check_stock_status(receiving_qty, qty_needed)
    eoq = calculate_eoq(annual_demand, ordering_cost, holding_cost)

    print(f"\n[PRODUCT INITIAL STATE: {product_name}]")
    print(f"Current Shelf Qty:    {shelf_qty}")
    print(f"Required Shelf Qty:   {req_shelf_qty}")
    print(f"Quantity Needed:      {qty_needed}")
    print(f"Receiving Stock Qty:  {receiving_qty}")
    print(f"Initial Status:       {status}")
    print(f"Calculated EOQ:       {round(eoq, 1)} units")

    # 3. TEST TASK DISPATCH & PERFORMANCE METRICS
    pending_tasks = 0
    completed_tasks = 24
    
    print("\n--- Dispatching a Task ---")
    pending_tasks, completed_tasks = update_performance_stats(pending_tasks, completed_tasks, action="dispatch")
    print(f"Pending Tasks: {pending_tasks} | Completed Tasks: {completed_tasks}")

    # 4. TEST TASK COMPLETION & STOCK DEDUCTION
    print("\n--- Completing Task (Moving Stock to Shelf) ---")
    # Move 20 units from receiving to shelf
    qty_to_move = 20  
    new_shelf_qty, new_receiving_qty, warning = complete_replenishment_task(
        shelf_qty, req_shelf_qty, receiving_qty, qty_to_move
    )
    
    # Update stats
    pending_tasks, completed_tasks = update_performance_stats(pending_tasks, completed_tasks, action="complete")
    new_status = check_stock_status(new_receiving_qty, calculate_quantity_needed(req_shelf_qty, new_shelf_qty))

    print(f"Updated Shelf Qty:     {new_shelf_qty}")
    print(f"Updated Receiving Qty: {new_receiving_qty}")
    print(f"New Stock Status:      {new_status}")
    print(f"Pending Tasks: {pending_tasks} | Completed Tasks: {completed_tasks}")
    
    if warning:
        print(f"\n[POP-UP ALERT] {warning}")

    # 5. TEST REORDERING SUPPLIER STOCK
    if new_receiving_qty == 0:
        print("\n--- Placing Supplier Reorder ---")
        supplier_order_qty = 50
        restocked_receiving = reorder_supplier_stock(new_receiving_qty, supplier_order_qty)
        final_status = check_stock_status(restocked_receiving, 0)
        
        print(f"Reordered Amount:      {supplier_order_qty} units")
        print(f"New Receiving Stock:   {restocked_receiving} units")
        print(f"Final Status:          {final_status}")

    print("\n==================================================")

if __name__ == "__main__":
    run_custom_test()