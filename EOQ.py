#Economic order quantity model for the Pick N pay Wolmaransstad store
import math

def calculate_eoq (demand, ordering_cost, holding_cost):
    # Entering EOQ FORMULA square root of (2 x D x S / H)
    
    return math.sqrt((2 * demand * ordering_cost) / holding_cost)

def total_annual_cost (demand, ordering_cost, holding_cost, order_qty):
    # Total cost formula  = Ordering cost + Holding cost
    ordering_cost = (demand / order_qty) * ordering_cost
    
    holding_cost = (order_qty / 2) * holding_cost
    
    return ordering_cost + holding_cost

# examples of products sold in the Pick n Pay
# demand, ordering cost and holding cost data estimation has been changed to keep pick n pay data confidential
items_in_inventory = {
    "PnP Full Cream Milk 2L":           {"demand": 14600, "ordering_cost": 50, "holding_cost": 2.50},
    "Albany Superior White Bread 700g": {"demand": 18250, "ordering_cost": 40, "holding_cost": 1.50},
    "Coca-Cola Original 2L":            {"demand": 21900, "ordering_cost": 50, "holding_cost": 1.80},
    "PnP Large Eggs 30s":               {"demand": 8760,  "ordering_cost": 45, "holding_cost": 3.00},
    "Sasko Brown Bread 700g":           {"demand": 14600, "ordering_cost": 40, "holding_cost": 1.50}, 
    "Nescafe Ricoffy 750g":             {"demand": 7300,  "ordering_cost": 50, "holding_cost": 2.00},
    "White Star Maize Meal 2.5kg":      {"demand": 12775, "ordering_cost": 45, "holding_cost": 1.80},
    "Flora Light Spread 500g":          {"demand": 6570,  "ordering_cost": 40, "holding_cost": 2.20},
    "Clover Gouda Cheese 850g":         {"demand": 4380,  "ordering_cost": 50, "holding_cost": 5.00},
    "PnP Fresh Chicken Pack 1kg":       {"demand": 10950, "ordering_cost": 60, "holding_cost": 6.00},
    "Koo Baked Beans 410g":             {"demand": 18250, "ordering_cost": 35, "holding_cost": 1.00},
    "All Gold Tomato Sauce 700ml":      {"demand": 8030,  "ordering_cost": 40, "holding_cost": 1.50},
    "Huletts White Sugar 2kg":          {"demand": 10950, "ordering_cost": 45, "holding_cost": 2.00},
    "Simba Potato Chips 120g":          {"demand": 25550, "ordering_cost": 35, "holding_cost": 1.20},
    "Cadbury Dairy Milk 150g":          {"demand": 14600, "ordering_cost": 35, "holding_cost": 2.00},
    "Five Roses Tea Bags 100s":         {"demand": 7300,  "ordering_cost": 40, "holding_cost": 2.50},
    "Jacobs Kronung Coffee 200g":       {"demand": 5475,  "ordering_cost": 50, "holding_cost": 6.00},
    "McCain Cut Green Beans 1kg":       {"demand": 4380,  "ordering_cost": 45, "holding_cost": 3.50},
    "PnP Beef Sausage 1kg":             {"demand": 7300,  "ordering_cost": 60, "holding_cost": 5.00},
    "Handy Andy Cleaner 750ml":         {"demand": 7300,  "ordering_cost": 40, "holding_cost": 1.50},
    "Omo Auto Washing Powder 2kg":      {"demand": 5840,  "ordering_cost": 50, "holding_cost": 3.00},
    "Colgate Triple Action 100ml":      {"demand": 10950, "ordering_cost": 35, "holding_cost": 1.00},
    "Baby Soft Toilet Paper 9s":        {"demand": 12775, "ordering_cost": 50, "holding_cost": 2.50},
    "Kellogg's Corn Flakes 1kg":        {"demand": 9125,  "ordering_cost": 45, "holding_cost": 2.20},
    "Bokomo Weet-Bix 450g":             {"demand": 10220, "ordering_cost": 45, "holding_cost": 2.00},
    "Dettol Antiseptic 500ml":          {"demand": 5475,  "ordering_cost": 40, "holding_cost": 3.00},
    "Jungle Oats 1kg":                  {"demand": 7300,  "ordering_cost": 45, "holding_cost": 2.00}
    
}

if __name__ == "__main__": 
    
    print("----------- EOQ Calculations for Pick n Pay Wolmaransstad ----------- ")
    
    for item, data in items_in_inventory.items(): 
        
        d = data["demand"]
        s = data["ordering_cost"]
        h = data["holding_cost"]
        
        eoq = calculate_eoq(d, s, h)           #testing function by entering parameters into the eoq function
        orders = d / eoq                       #entering order formula
        days = 365 / orders                    # calculating the days inbetween orders
        cost = total_annual_cost(d, s, h, eoq) #calculating annual cost
        
        #Printing results
        print(f"\nProduct: {item}")
        print(f"Optimal Order Quantity (EOQ): {round(eoq, 1)}")  #rounding eoq to 1 decimal place
        print(f"Orders per year: {round(orders, 1)}")            #rounding orders to 1 decimal place
        print(f"Days between orders: {round(days, 1)}")          #rounding days to 1 decimal place
        print(f"Total annual cost: R{round(cost, 2)}")           #rounding cost to 2 decimal places