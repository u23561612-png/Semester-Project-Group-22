document.addEventListener('DOMContentLoaded', function () {
  // 1. Sidebar Tab Switching Logic
  const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
  const tabPanes = document.querySelectorAll('.tab-pane');

  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      navLinks.forEach(l => l.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('show', 'active'));

      this.classList.add('active');
      const targetId = this.getAttribute('data-bs-target');
      document.querySelector(targetId).classList.add('show', 'active');
    });
  });

  // 2. Table Filtering Logic ("Filter table products...")
  const tableSearchInput = document.getElementById('tableSearchInput');
  const inventoryTable = document.getElementById('inventoryTable');

  if (tableSearchInput && inventoryTable) {
    tableSearchInput.addEventListener('input', function (e) {
      const searchTerm = e.target.value.toLowerCase().trim();
      const rows = inventoryTable.querySelectorAll('tbody tr');

      rows.forEach(row => {
        const productText = row.textContent.toLowerCase();
        if (productText.includes(searchTerm)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  }

  // 3. Product Search View Logic
  const productSearchInput = document.getElementById('productSearchInput');
  const searchResultCard = document.getElementById('searchResultCard');

  if (productSearchInput && searchResultCard) {
    productSearchInput.addEventListener('input', function (e) {
      const query = e.target.value.toLowerCase().trim();
      if (query.includes('coke') || query.includes('480011254687') || query.includes('prd-000123')) {
        searchResultCard.classList.remove('d-none');
      } else if (query === '') {
        searchResultCard.classList.add('d-none');
      }
    });
  }

  // 4. Create Task Form Submission & Stats Update
  const taskForm = document.getElementById('replenishmentTaskForm');
  if (taskForm) {
    taskForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const productName = document.getElementById('modalProductName').value;
      const qty = document.getElementById('modalQtyNeeded').value;

      // Update UI feedback or stats counter
      alert(`Success! Replenishment task created for "${productName}" (${qty} units). Dashboard metrics updated.`);
      
      // Increment pending replenishment counter or update DOM if needed
      const pendingCounter = document.getElementById('pendingCount');
      if(pendingCounter) {
        pendingCounter.textContent = parseInt(pendingCounter.textContent || '5') + 1;
      }
      
      // Close modal
      const modalEl = document.getElementById('createTaskModal');
      const modal = bootstrap.Modal.getInstance(modalEl);
      if (modal) modal.hide();
    });
  }
});