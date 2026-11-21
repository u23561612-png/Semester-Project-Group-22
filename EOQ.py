"""
Pick n Pay Wolmaransstad - Economic Order Quantity Model

Calculates the recommended order quantity and annual inventory costs.
"""

import math


def calculate_eoq(annual_demand, ordering_cost, holding_cost):
    """Calculates the optimal supplier order quantity."""

    if annual_demand <= 0:
        raise ValueError("Annual demand must be greater than zero.")

    if ordering_cost <= 0:
        raise ValueError("Ordering cost must be greater than zero.")

    if holding_cost <= 0:
        raise ValueError("Holding cost must be greater than zero.")

    eoq = math.sqrt(
        (2 * annual_demand * ordering_cost) / holding_cost
    )

    return eoq


def calculate_orders_per_year(annual_demand, order_quantity):
    """Calculates the number of orders placed per year."""

    return annual_demand / order_quantity


def calculate_annual_ordering_cost(annual_demand, ordering_cost,
                                   order_quantity):
    """Calculates the annual ordering cost."""

    return (annual_demand / order_quantity) * ordering_cost


def calculate_annual_holding_cost(order_quantity, holding_cost):
    """Calculates the annual inventory holding cost."""

    return (order_quantity / 2) * holding_cost


def calculate_total_inventory_cost(annual_demand, ordering_cost,
                                   holding_cost, order_quantity):
    """Calculates the total annual ordering and holding costs."""

    annual_ordering = calculate_annual_ordering_cost(
        annual_demand, ordering_cost, order_quantity
    )

    annual_holding = calculate_annual_holding_cost(
        order_quantity, holding_cost
    )

    return annual_ordering + annual_holding


def run_eoq_model():

    # Example product and estimated input parameters

    product_name = "PnP Full Cream Milk 2L"

    annual_demand = 14600
    ordering_cost = 50.00
    holding_cost = 2.50

    # Calculate EOQ and inventory costs

    eoq = calculate_eoq(
        annual_demand, ordering_cost, holding_cost
    )

    orders_per_year = calculate_orders_per_year(
        annual_demand, eoq
    )

    annual_ordering = calculate_annual_ordering_cost(
        annual_demand, ordering_cost, eoq
    )

    annual_holding = calculate_annual_holding_cost(
        eoq, holding_cost
    )

    total_cost = calculate_total_inventory_cost(
        annual_demand, ordering_cost, holding_cost, eoq
    )

    # Display results

    print("--------------------------------------------")
    print("       ECONOMIC ORDER QUANTITY MODEL")
    print("--------------------------------------------")

    print(f"Product: {product_name}")
    print(f"Annual Demand: {annual_demand} units")
    print(f"Ordering Cost: R {ordering_cost:.2f}")
    print(f"Holding Cost: R {holding_cost:.2f}")

    print("\n--- EOQ Results ---")

    print(f"Economic Order Quantity: {eoq:.2f} units")
    print(f"Recommended Order: {round(eoq)} units")
    print(f"Orders per Year: {orders_per_year:.2f}")
    print(f"Annual Ordering Cost: R {annual_ordering:.2f}")
    print(f"Annual Holding Cost: R {annual_holding:.2f}")
    print(f"Total Annual Inventory Cost: R {total_cost:.2f}")

    print("--------------------------------------------")


if __name__ == "__main__":
    run_eoq_model()