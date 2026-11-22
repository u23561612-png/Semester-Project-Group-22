# Tests for inventory and replenishment functions.

import unittest

from models.inventory_logic import (
    calculate_eoq,
    calculate_quantity_needed,
    checking_stock_status,
    complete_replenishment_task,
    reorder_supplier_stock,
    update_performance_stats
)


class TestInventoryLogic(unittest.TestCase):

    def test_eoq(self):
        """Test the EOQ calculation."""
        result = calculate_eoq(14600, 50.0, 2.50)
        self.assertAlmostEqual(result, 764.2, places=1)

    def test_quantity_needed(self):
        """Test the required replenishment quantity."""
        self.assertEqual(calculate_quantity_needed(25, 5), 20)

    def test_shelf_already_full(self):
        """Check that quantity needed cannot be negative."""
        self.assertEqual(calculate_quantity_needed(25, 30), 0)

    def test_sufficient_stock(self):
        """Test sufficient receiving stock."""
        result = checking_stock_status(20, 20)
        self.assertEqual(result.strip(), "Sufficient")

    def test_insufficient_stock(self):
        """Test insufficient receiving stock."""
        result = checking_stock_status(10, 20)
        self.assertEqual(result.strip(), "Insufficient")

    def test_out_of_stock(self):
        """Test empty receiving stock."""
        result = checking_stock_status(0, 20)
        self.assertEqual(result.strip(), "OUT OF STOCK")

    def test_dispatch_task(self):
        """Test performance statistics when creating a task."""
        result = update_performance_stats(0, 24, action="dispatch")
        self.assertEqual(result, (1, 24))

    def test_complete_task(self):
        """Test a successful stock transfer."""
        shelf_qty, receiving_qty, warning = complete_replenishment_task(
            shelf_qty=5,
            required_shelf_qty=25,
            receiving_qty=20,
            qty_to_move=20
        )

        self.assertEqual(shelf_qty, 25)
        self.assertEqual(receiving_qty, 0)
        self.assertIsNotNone(warning)

    def test_insufficient_receiving_stock(self):
        """Prevent transferring more stock than is available."""
        with self.assertRaises(ValueError):
            complete_replenishment_task(5, 25, 20, 36)

    def test_exceeding_shelf_requirement(self):
        """Prevent transferring more stock than needed."""
        with self.assertRaises(ValueError):
            complete_replenishment_task(5, 25, 50, 30)

    def test_negative_stock(self):
        """Prevent negative stock quantities."""
        with self.assertRaises(ValueError):
            complete_replenishment_task(-5, 25, 20, 10)

    def test_invalid_transfer_quantity(self):
        """Prevent transferring zero units."""
        with self.assertRaises(ValueError):
            complete_replenishment_task(5, 25, 20, 0)

    def test_supplier_reorder(self):
        """Test receiving additional supplier stock."""
        self.assertEqual(reorder_supplier_stock(0, 50), 50)

    def test_completed_task_statistics(self):
        """Test performance statistics after completing a task."""
        result = update_performance_stats(1, 24, action="complete")
        self.assertEqual(result, (0, 25))


if __name__ == "__main__":
    unittest.main(verbosity=2)