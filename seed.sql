-- Pick n Pay Wolmaransstad
-- Receiving Stock System
-- Group 22: Sample Database Records

USE pnp_receiving;
START TRANSACTION;

-- Insert system users

INSERT INTO users (full_name, username, role)
VALUES
    ('Sam', 'sam', 'Store Manager'),
    ('Alex', 'alex', 'Floor Manager'),
    ('Jamie', 'jamie', 'Staff Member'),
    ('Jordan', 'jordan', 'Receiving Manager');

-- Insert the 30 grocery products

INSERT INTO products (product_code, product_name)
VALUES
    ('PRD-001', 'PnP Full Cream Milk 2L'),
    ('PRD-002', 'Albany Superior White Bread 700g'),
    ('PRD-003', 'Coca-Cola Original 2L'),
    ('PRD-004', 'PnP Large Eggs 30s'),
    ('PRD-005', 'Sasko Brown Bread 700g'),
    ('PRD-006', 'Nescafe Ricoffy 750g'),
    ('PRD-007', 'Tastic Long Grain Rice 2kg'),
    ('PRD-008', 'White Star Maize Meal 2.5kg'),
    ('PRD-009', 'Flora Light Spread 500g'),
    ('PRD-010', 'Clover Gouda Cheese 850g'),
    ('PRD-011', 'PnP Fresh Chicken Pack 1kg'),
    ('PRD-012', 'Koo Baked Beans 410g'),
    ('PRD-013', 'All Gold Tomato Sauce 700ml'),
    ('PRD-014', 'Huletts White Sugar 2kg'),
    ('PRD-015', 'Sunfoil Sunflower Oil 2L'),
    ('PRD-016', 'Simba Potato Chips 120g'),
    ('PRD-017', 'Cadbury Dairy Milk 150g'),
    ('PRD-018', 'Five Roses Tea Bags 100s'),
    ('PRD-019', 'Jacobs Kronung Coffee 200g'),
    ('PRD-020', 'Danone Ultra Mel Custard 1L'),
    ('PRD-021', 'McCain Cut Green Beans 1kg'),
    ('PRD-022', 'PnP Beef Sausage 1kg'),
    ('PRD-023', 'Handy Andy Cleaner 750ml'),
    ('PRD-024', 'Omo Auto Washing Powder 2kg'),
    ('PRD-025', 'Colgate Triple Action 100ml'),
    ('PRD-026', 'Baby Soft Toilet Paper 9s'),
    ('PRD-027', 'Kellogg''s Corn Flakes 1kg'),
    ('PRD-028', 'Bokomo Weet-Bix 450g'),
    ('PRD-029', 'Dettol Antiseptic 500ml'),
    ('PRD-030', 'Jungle Oats 1kg');

    -- Insert shop floor shelf locations

INSERT INTO locations
    (location_code, location_name, location_type)
VALUES
    ('A1-S1', 'Aisle 1, Shelf 1', 'Shelf'),
    ('A1-S2', 'Aisle 1, Shelf 2', 'Shelf'),
    ('A1-S3', 'Aisle 1, Shelf 3', 'Shelf'),
    ('A1-S4', 'Aisle 1, Shelf 4', 'Shelf'),

    ('A2-S1', 'Aisle 2, Shelf 1', 'Shelf'),
    ('A2-S2', 'Aisle 2, Shelf 2', 'Shelf'),
    ('A2-S3', 'Aisle 2, Shelf 3', 'Shelf'),
    ('A2-S4', 'Aisle 2, Shelf 4', 'Shelf'),

    ('A3-S1', 'Aisle 3, Shelf 1', 'Shelf'),
    ('A3-S2', 'Aisle 3, Shelf 2', 'Shelf'),
    ('A3-S3', 'Aisle 3, Shelf 3', 'Shelf'),
    ('A3-S4', 'Aisle 3, Shelf 4', 'Shelf'),

    ('A4-S1', 'Aisle 4, Shelf 1', 'Shelf'),
    ('A4-S2', 'Aisle 4, Shelf 2', 'Shelf'),
    ('A4-S3', 'Aisle 4, Shelf 3', 'Shelf'),
    ('A4-S4', 'Aisle 4, Shelf 4', 'Shelf'),

    ('A5-S1', 'Aisle 5, Shelf 1', 'Shelf'),
    ('A5-S2', 'Aisle 5, Shelf 2', 'Shelf'),
    ('A5-S3', 'Aisle 5, Shelf 3', 'Shelf'),
    ('A5-S4', 'Aisle 5, Shelf 4', 'Shelf'),

    ('A6-S1', 'Aisle 6, Shelf 1', 'Shelf'),
    ('A6-S2', 'Aisle 6, Shelf 2', 'Shelf'),
    ('A6-S3', 'Aisle 6, Shelf 3', 'Shelf'),
    ('A6-S4', 'Aisle 6, Shelf 4', 'Shelf'),

    ('A7-S1', 'Aisle 7, Shelf 1', 'Shelf'),
    ('A7-S2', 'Aisle 7, Shelf 2', 'Shelf'),
    ('A7-S3', 'Aisle 7, Shelf 3', 'Shelf'),
    ('A7-S4', 'Aisle 7, Shelf 4', 'Shelf'),

    ('A8-S1', 'Aisle 8, Shelf 1', 'Shelf'),
    ('A8-S2', 'Aisle 8, Shelf 2', 'Shelf'),
    ('A8-S3', 'Aisle 8, Shelf 3', 'Shelf'),
    ('A8-S4', 'Aisle 8, Shelf 4', 'Shelf'),

    ('A9-S1', 'Aisle 9, Shelf 1', 'Shelf'),
    ('A9-S2', 'Aisle 9, Shelf 2', 'Shelf'),
    ('A9-S3', 'Aisle 9, Shelf 3', 'Shelf'),
    ('A9-S4', 'Aisle 9, Shelf 4', 'Shelf'),

    ('BUT-S1', 'Butchery, Shelf 1', 'Shelf'),
    ('BUT-S2', 'Butchery, Shelf 2', 'Shelf'),
    ('BUT-S3', 'Butchery, Shelf 3', 'Shelf'),
    ('BUT-S4', 'Butchery, Shelf 4', 'Shelf'),

    -- Receiving area locations

    ('REC-01', 'Receiving - Refrigerated Dairy', 'Receiving'),
    ('REC-02', 'Receiving - Bakery', 'Receiving'),
    ('REC-03', 'Receiving - Beverages', 'Receiving'),
    ('REC-04', 'Receiving - Dry Groceries', 'Receiving'),
    ('REC-05', 'Receiving - Frozen Stock', 'Receiving'),
    ('REC-06', 'Receiving - Household Products', 'Receiving'),
    ('REC-07', 'Receiving - Refrigerated Meat', 'Receiving'),
    ('REC-08', 'Receiving - Toiletries', 'Receiving');

    -- Insert starting inventory quantities

INSERT INTO inventory (
    product_id,
    receiving_location_id,
    shelf_location_id,
    receiving_qty,
    shelf_qty,
    required_shelf_qty
)
SELECT
    p.product_id,
    r.location_id,
    s.location_id,
    d.receiving_qty,
    d.shelf_qty,
    d.required_shelf_qty
FROM (
    SELECT 'PRD-001' AS product_code,
           'REC-01' AS receiving_code,
           'A1-S1' AS shelf_code,
           20 AS receiving_qty,
           5 AS shelf_qty,
           25 AS required_shelf_qty

    UNION ALL SELECT 'PRD-002', 'REC-02', 'A2-S1', 12, 4, 30
    UNION ALL SELECT 'PRD-003', 'REC-03', 'A3-S1', 50, 8, 40
    UNION ALL SELECT 'PRD-004', 'REC-01', 'A1-S2', 8, 3, 15
    UNION ALL SELECT 'PRD-005', 'REC-02', 'A2-S2', 35, 6, 25
    UNION ALL SELECT 'PRD-006', 'REC-04', 'A4-S1', 25, 10, 20
    UNION ALL SELECT 'PRD-007', 'REC-04', 'A4-S2', 5, 2, 18
    UNION ALL SELECT 'PRD-008', 'REC-04', 'A4-S2', 40, 5, 35
    UNION ALL SELECT 'PRD-009', 'REC-01', 'A1-S3', 20, 7, 15
    UNION ALL SELECT 'PRD-010', 'REC-01', 'A1-S3', 4, 2, 12
    UNION ALL SELECT 'PRD-011', 'REC-07', 'BUT-S1', 8, 6, 20
    UNION ALL SELECT 'PRD-012', 'REC-04', 'A5-S1', 60, 12, 50
    UNION ALL SELECT 'PRD-013', 'REC-04', 'A5-S2', 15, 4, 22
    UNION ALL SELECT 'PRD-014', 'REC-04', 'A4-S3', 45, 8, 30
    UNION ALL SELECT 'PRD-015', 'REC-04', 'A4-S3', 10, 3, 25
    UNION ALL SELECT 'PRD-016', 'REC-04', 'A6-S1', 60, 15, 45
    UNION ALL SELECT 'PRD-017', 'REC-04', 'A6-S2', 12, 10, 30
    UNION ALL SELECT 'PRD-018', 'REC-04', 'A4-S1', 25, 5, 20
    UNION ALL SELECT 'PRD-019', 'REC-04', 'A4-S1', 18, 4, 15
    UNION ALL SELECT 'PRD-020', 'REC-01', 'A1-S4', 30, 8, 24
    UNION ALL SELECT 'PRD-021', 'REC-05', 'A7-S1', 6, 3, 12
    UNION ALL SELECT 'PRD-022', 'REC-07', 'BUT-S2', 22, 5, 18
    UNION ALL SELECT 'PRD-023', 'REC-06', 'A8-S1', 30, 6, 20
    UNION ALL SELECT 'PRD-024', 'REC-06', 'A8-S2', 9, 4, 16
    UNION ALL SELECT 'PRD-025', 'REC-08', 'A9-S1', 40, 14, 30
    UNION ALL SELECT 'PRD-026', 'REC-06', 'A8-S3', 15, 2, 20
    UNION ALL SELECT 'PRD-027', 'REC-04', 'A4-S4', 35, 6, 25
    UNION ALL SELECT 'PRD-028', 'REC-04', 'A4-S4', 30, 9, 28
    UNION ALL SELECT 'PRD-029', 'REC-08', 'A9-S2', 20, 5, 15
    UNION ALL SELECT 'PRD-030', 'REC-04', 'A4-S4', 25, 7, 20

) AS d

JOIN products p
    ON p.product_code = d.product_code

JOIN locations r
    ON r.location_code = d.receiving_code

JOIN locations s
    ON s.location_code = d.shelf_code;

-- Insert sample pending replenishment tasks

INSERT INTO replenishment_tasks (
    product_id,
    shelf_location_id,
    created_by,
    quantity,
    priority,
    status
)
SELECT
    p.product_id,
    i.shelf_location_id,
    u.user_id,
    d.quantity,
    d.priority,
    'Pending'
FROM (
    SELECT 'PRD-002' AS product_code,
           12 AS quantity,
           'High' AS priority

    UNION ALL SELECT 'PRD-003', 32, 'High'
    UNION ALL SELECT 'PRD-006', 10, 'Medium'

) AS d

JOIN products p
    ON p.product_code = d.product_code

JOIN inventory i
    ON i.product_id = p.product_id

JOIN users u
    ON u.username = 'alex';

-- Insert a historical completed replenishment task

INSERT INTO replenishment_tasks (
    product_id,
    shelf_location_id,
    created_by,
    completed_by,
    quantity,
    priority,
    status,
    created_at,
    completed_at
)
SELECT
    p.product_id,
    i.shelf_location_id,
    creator.user_id,
    employee.user_id,
    5,
    'High',
    'Completed',
    NOW() - INTERVAL 30 MINUTE,
    NOW() - INTERVAL 18 MINUTE

FROM products p

JOIN inventory i
    ON i.product_id = p.product_id

JOIN users creator
    ON creator.username = 'alex'

JOIN users employee
    ON employee.username = 'jamie'

WHERE p.product_code = 'PRD-001';

-- Historical supplier delivery

INSERT INTO stock_movements (
    product_id,
    user_id,
    movement_type,
    receiving_before,
    receiving_after,
    shelf_before,
    shelf_after,
    reason,
    created_at
)
SELECT
    p.product_id,
    u.user_id,
    'Stock Received',
    5,
    25,
    0,
    0,
    'Sample supplier delivery',
    NOW() - INTERVAL 60 MINUTE

FROM products p

JOIN users u
    ON u.username = 'jordan'

WHERE p.product_code = 'PRD-001';

-- Stock transferred from receiving to the shop floor

INSERT INTO stock_movements (
    product_id,
    user_id,
    task_id,
    movement_type,
    receiving_before,
    receiving_after,
    shelf_before,
    shelf_after,
    reason,
    created_at
)
SELECT
    t.product_id,
    t.completed_by,
    t.task_id,
    'Replenishment',
    25,
    20,
    0,
    5,
    'Sample completed replenishment task',
    t.completed_at

FROM replenishment_tasks t

JOIN products p
    ON p.product_id = t.product_id

WHERE p.product_code = 'PRD-001'
    AND t.status = 'Completed';

-- Sample damaged stock transaction

INSERT INTO stock_movements (
    product_id,
    user_id,
    movement_type,
    receiving_before,
    receiving_after,
    shelf_before,
    shelf_after,
    reason
)
SELECT
    p.product_id,
    u.user_id,
    'Damaged Stock',
    14,
    12,
    4,
    4,
    'Two damaged bread packages removed'

FROM products p

JOIN users u
    ON u.username = 'jordan'

WHERE p.product_code = 'PRD-002';

-- Sample physical stock reconciliation

INSERT INTO stock_movements (
    product_id,
    user_id,
    movement_type,
    receiving_before,
    receiving_after,
    shelf_before,
    shelf_after,
    reason
)
SELECT
    p.product_id,
    u.user_id,
    'Stock Reconciliation',
    52,
    50,
    8,
    8,
    'Physical count identified a shortage of two units'

FROM products p

JOIN users u
    ON u.username = 'jordan'

WHERE p.product_code = 'PRD-003';

COMMIT;