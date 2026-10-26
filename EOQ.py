import math

def calculating_EOQ(demand, order_cost, hold_cost):            #function for creating the EOQ FORMULA
                                                               # EOQ formula is square root of ((2 x D x S) / H)
    return math.sqrt((2 * demand * order_cost) / hold_cost)

def calculate_total_annual_cost(demand, order_cost, hold_cost, order_qty): #Calculating annual cost 
                                                                           # Total cost = Ordering cost + Holding cost
    ordering = (demand / order_qty) * order_cost
    holding = (order_qty / 2) * hold_cost
    return ordering + holding

# Sample data for Pick n Pay products used in the dashboard
items_in_inventory = {
    "PnP Full Cream Milk 2L":           {"demand": 14600, "order_cost": 50, "hold_cost": 2.50}, #demand, ordering cost and holding costs are hypothetical
    "Albany Superior White Bread 700g": {"demand": 18250, "order_cost": 40, "hold_cost": 1.50}, # in order to preserve confidentiality
    "Coca-Cola Original 2L":            {"demand": 21900, "order_cost": 50, "hold_cost": 1.80},
    "PnP Large Eggs 30s":               {"demand": 8760,  "order_cost": 45, "hold_cost": 3.00},
    "Sasko Brown Bread 700g":           {"demand": 14600, "order_cost": 40, "hold_cost": 1.50},
    "Nescafe Ricoffy 750g":             {"demand": 7300,  "order_cost": 50, "hold_cost": 4.00},
    "Tastic Long Grain Rice 2kg":       {"demand": 5475,  "order_cost": 50, "hold_cost": 2.00},
    "White Star Maize Meal 2.5kg":      {"demand": 12775, "order_cost": 45, "hold_cost": 1.80},
    "Flora Light Spread 500g":          {"demand": 6570,  "order_cost": 40, "hold_cost": 2.20},
    "Clover Gouda Cheese 850g":         {"demand": 4380,  "order_cost": 50, "hold_cost": 5.00},
    "PnP Fresh Chicken Pack 1kg":       {"demand": 10950, "order_cost": 60, "hold_cost": 6.00},
    "Koo Baked Beans 410g":             {"demand": 18250, "order_cost": 35, "hold_cost": 1.00},
    "All Gold Tomato Sauce 700ml":      {"demand": 8030,  "order_cost": 40, "hold_cost": 1.50},
    "Huletts White Sugar 2kg":          {"demand": 10950, "order_cost": 45, "hold_cost": 2.00},
    "Sunfoil Sunflower Oil 2L":         {"demand": 9125,  "order_cost": 50, "hold_cost": 2.50},
    "Simba Potato Chips 120g":          {"demand": 25550, "order_cost": 35, "hold_cost": 1.20},
    "Cadbury Dairy Milk 150g":          {"demand": 14600, "order_cost": 35, "hold_cost": 2.00},
    "Five Roses Tea Bags 100s":         {"demand": 7300,  "order_cost": 40, "hold_cost": 2.50},
    "Jacobs Kronung Coffee 200g":       {"demand": 5475,  "order_cost": 50, "hold_cost": 6.00},
    "Danone Ultra Mel Custard 1L":      {"demand": 8760,  "order_cost": 45, "hold_cost": 2.00},
    "McCain Cut Green Beans 1kg":       {"demand": 4380,  "order_cost": 45, "hold_cost": 3.50},
    "PnP Beef Sausage 1kg":             {"demand": 7300,  "order_cost": 60, "hold_cost": 5.00},
    "Handy Andy Cleaner 750ml":         {"demand": 7300,  "order_cost": 40, "hold_cost": 1.50},
    "Omo Auto Washing Powder 2kg":      {"demand": 5840,  "order_cost": 50, "hold_cost": 3.00},
    "Colgate Triple Action 100ml":      {"demand": 10950, "order_cost": 35, "hold_cost": 1.00},
    "Baby Soft Toilet Paper 9s":        {"demand": 12775, "order_cost": 50, "hold_cost": 2.50},
    "Kellogg's Corn Flakes 1kg":        {"demand": 9125,  "order_cost": 45, "hold_cost": 2.20},
    "Bokomo Weet-Bix 450g":             {"demand": 10220, "order_cost": 45, "hold_cost": 2.00},
    "Dettol Antiseptic 500ml":          {"demand": 5475,  "order_cost": 40, "hold_cost": 3.00},
    "Jungle Oats 1kg":                  {"demand": 7300,  "order_cost": 45, "hold_cost": 2.00}
    
}

if __name__ == "__main__":
    print("--- EOQ Calculations for Pick n Pay Wolmaransstad ---")
    
    for item, data in items_in_inventory.items():
        d = data["demand"]
        s = data["order_cost"]
        h = data["hold_cost"]
        
        eoq = calculating_EOQ(d, s, h)
        orders = d / eoq
        days = 365 / orders
        cost = calculate_total_annual_cost(d, s, h, eoq)
        
        print(f"\nProduct: {item}")
        print(f"Optimal Order Quantity (EOQ): {round(eoq, 1)}")
        print(f"Orders per year: {round(orders, 1)}")
        print(f"Days between orders: {round(days, 1)}")
        print(f"Total annual cost: R{round(cost, 2)}")