<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pick n Pay Wolmaransstad - Receiving Stock System</title>
  <!-- Bootstrap 5 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Bootstrap Icons -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
  
  <style>
    :root {
      --pnp-red: #e2001a;
      --pnp-dark-blue: #002b49;
      --sidebar-bg: #ffffff;
      --bg-main: #f4f6f9;
      --border-color: #dee2e6;
    }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: var(--bg-main);
      color: #333333;
      overflow-x: hidden;
      margin: 0;
    }

    .app-container {
      display: flex;
      min-height: 100vh;
    }

    .sidebar {
      width: 260px;
      background-color: var(--sidebar-bg);
      border-right: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      position: fixed;
      top: 0;
      bottom: 0;
      z-index: 100;
    }

    .sidebar-header {
      padding: 1.25rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .sidebar-nav {
      padding: 1rem 0;
      list-style: none;
      margin: 0;
    }

    .sidebar-nav .nav-link {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.75rem 1.5rem;
      color: #495057;
      font-weight: 600;
      text-decoration: none;
      border-left: 4px solid transparent;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .sidebar-nav .nav-link:hover, 
    .sidebar-nav .nav-link.active {
      background-color: #f8f9fa;
      color: var(--pnp-dark-blue);
      border-left-color: var(--pnp-dark-blue);
    }

    .main-content {
      margin-left: 260px;
      flex: 1;
      padding: 2rem;
    }

    .top-header {
      background: white;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 0.75rem 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .card-metric {
      background: white;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1.25rem;
    }

    .card-metric .metric-value {
      font-size: 1.8rem;
      font-weight: 700;
    }

    .badge-sufficient {
      background-color: #d1e7dd;
      color: #0f5132;
      font-weight: 600;
    }

    .badge-insufficient {
      background-color: #f8d7da;
      color: #842029;
      font-weight: 600;
    }

    .badge-outofstock {
      background-color: #721c24;
      color: white;
      font-weight: 700;
    }

    .priority-high { background-color: #dc3545; color: white; }
    .priority-medium { background-color: #fd7e14; color: white; }
    .priority-low { background-color: #ffc107; color: #212529; }
  </style>
</head>
<body>

  <!-- Toast Notification Container for Out of Stock Pop-ups -->
  <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1055;">
    <div id="outOfStockToast" class="toast align-items-center text-white bg-danger border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body" id="toastMessage">
          <strong>ALERT:</strong> Item is now Out of Stock!
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  </div>

  <div class="app-container">
    
    <!-- LEFT SIDEBAR NAVIGATION -->
    <nav class="sidebar">
      <div class="sidebar-header">
        <i class="bi bi-box-seam-fill text-warning fs-3"></i>
        <div>
          <span class="fw-bold text-dark fs-6">Receiving System</span>
          <small class="text-muted d-block" style="font-size: 0.75rem;">Pick n Pay Wolmaransstad</small>
        </div>
      </div>

      <ul class="sidebar-nav" role="tablist">
        <li class="nav-item">
          <a class="nav-link active" data-bs-toggle="tab" data-bs-target="#dashboard-panel">
            <i class="bi bi-grid-fill"></i> Dashboard
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" data-bs-target="#search-panel">
            <i class="bi bi-search"></i> Stock Search
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" data-bs-target="#tasks-panel">
            <i class="bi bi-clipboard-check"></i> Replenishment Tasks <span class="badge bg-danger ms-1" id="taskBadgeCount">0</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" data-bs-target="#performance-panel">
            <i class="bi bi-bar-chart-fill"></i> Performance
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" data-bs-target="#users-panel">
            <i class="bi bi-people-fill"></i> Users
          </a>
        </li>
      </ul>
    </nav>

    <!-- MAIN CONTENT VIEW -->
    <main class="main-content">
      
      <header class="top-header shadow-sm">
        <div class="d-flex align-items-center gap-2">
          <span class="badge bg-dark fs-6">1</span>
          <h1 class="h5 fw-bold mb-0 text-dark">Receiving Inventory Dashboard</h1>
        </div>
        <div class="d-flex align-items-center gap-3">
          <button class="btn btn-light position-relative border"><i class="bi bi-bell"></i></button>
          <div class="d-flex align-items-center gap-2">
            <i class="bi bi-person-circle fs-4 text-danger"></i>
            <span class="fw-bold small">Floor Manager</span>
          </div>
        </div>
      </header>

      <div class="tab-content">
        
        <!-- 1. DASHBOARD PANEL -->
        <div class="tab-pane fade show active" id="dashboard-panel">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <p class="text-muted mb-0">Overview of shelf requirements vs receiving area stock</p>
            <button class="btn btn-primary" id="openNewTaskModalBtn">
              <i class="bi bi-plus-lg me-1"></i> New Replenishment Task
            </button>
          </div>

          <!-- Dynamic Metrics Cards Header -->
          <div class="row g-3 mb-4">
            <div class="col-md-3"><div class="card-metric shadow-sm"><span class="text-muted small fw-semibold">Total products</span><div class="metric-value" id="kpiTotalProducts">30</div></div></div>
            <div class="col-md-3"><div class="card-metric shadow-sm"><span class="text-muted small fw-semibold">Receiving stock</span><div class="metric-value" id="kpiReceivingStock">0</div></div></div>
            <div class="col-md-3"><div class="card-metric shadow-sm border-danger"><span class="text-muted small fw-semibold">Insufficient stock items</span><div class="metric-value text-danger" id="kpiInsufficient">0</div></div></div>
            <div class="col-md-3"><div class="card-metric shadow-sm border-success"><span class="text-muted small fw-semibold">Sufficient stock items</span><div class="metric-value text-success" id="kpiSufficient">0</div></div></div>
          </div>

          <div class="row g-4">
            <div class="col-lg-8">
              <div class="card border-0 shadow-sm">
                <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
                  <h2 class="h6 fw-bold mb-0">Stock Replenishment Table</h2>
                  <input type="text" id="tableSearchInput" class="form-control form-control-sm w-50" placeholder="Filter 30 products...">
                </div>
                <div class="table-responsive" style="max-height: 520px; overflow-y: auto;">
                  <table class="table table-hover align-middle mb-0" id="inventoryTable">
                    <thead class="table-dark sticky-top">
                      <tr>
                        <th>Product</th>
                        <th>Shelf Qty</th>
                        <th>Req. Shelf Qty</th>
                        <th>Qty Needed</th>
                        <th>Receiving Stock</th>
                        <th>Status</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody id="inventoryTableBody">
                      <!-- Populated dynamically -->
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Priority Items Widget -->
            <div class="col-lg-4">
              <div class="card border-0 shadow-sm">
                <div class="card-header bg-white py-3"><h2 class="h6 fw-bold mb-0">Critical Stock Alerts</h2></div>
                <div class="card-body" id="priorityWidgetBody">
                  <!-- Populated automatically -->
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. STOCK SEARCH PANEL -->
        <div class="tab-pane fade" id="search-panel">
          <div class="card border-0 shadow-sm p-4">
            <h3 class="h5 fw-bold mb-3">Product Search</h3>
            <input type="text" id="productSearchInput" class="form-control form-control-lg" placeholder="Search product name, barcode or SKU...">
          </div>
        </div>

        <!-- 3. TASKS PANEL -->
        <div class="tab-pane fade" id="tasks-panel">
          <div class="card border-0 shadow-sm p-4">
            <h3 class="h5 fw-bold mb-3">Active Replenishment Tasks</h3>
            <div id="tasksContainer">
              <p class="text-muted" id="noTasksMsg">No active replenishment tasks dispatched yet.</p>
            </div>
          </div>
        </div>

        <!-- 4. PERFORMANCE PANEL -->
        <div class="tab-pane fade" id="performance-panel">
          <div class="card border-0 shadow-sm p-4">
            <h3 class="h5 fw-bold mb-3">Performance Monitoring</h3>
            <div class="row">
              <div class="col-md-4"><div class="card p-3 shadow-sm bg-light">Pending Tasks: <span id="perfPending" class="fw-bold text-warning fs-4">0</span></div></div>
              <div class="col-md-4"><div class="card p-3 shadow-sm bg-light">Completed Today: <span id="perfCompleted" class="fw-bold text-success fs-4">0</span></div></div>
              <div class="col-md-4"><div class="card p-3 shadow-sm bg-light">Avg Response Time: <span class="fw-bold text-primary fs-4">12 mins</span></div></div>
            </div>
          </div>
        </div>

        <!-- 5. USERS PANEL -->
        <div class="tab-pane fade" id="users-panel">
          <div class="card border-0 shadow-sm p-4"><h3 class="h5 fw-bold">User Role Management</h3><p class="text-muted">Manage system users and access privileges.</p></div>
        </div>

      </div>
    </main>
  </div>

  <!-- Dispatch Modal -->
  <div class="modal fade" id="createTaskModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-dark text-white">
          <h5 class="modal-title fw-bold">Dispatch Replenishment Task</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form id="replenishmentTaskForm">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Product Name</label>
              <input type="text" id="modalProductName" class="form-control" placeholder="Type item name" required>
            </div>
            <div class="row g-2 mb-3">
              <div class="col-md-6">
                <label class="form-label fw-semibold">Quantity Needed</label>
                <input type="number" id="modalQtyNeeded" class="form-control" required min="1">
              </div>
              <div class="col-md-6">
                <label class="form-label fw-semibold">Select Priority</label>
                <select id="modalPriority" class="form-select">
                  <option value="High">High Priority</option>
                  <option value="Medium" selected>Medium Priority</option>
                  <option value="Low">Low Priority</option>
                </select>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Shelf Location</label>
              <input type="text" id="modalShelfLoc" class="form-control" value="Aisle 3, Shelf 2" required>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Dispatch Task</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Supplier Reorder Modal -->
  <div class="modal fade" id="reorderModal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header bg-danger text-white">
          <h5 class="modal-title fw-bold"><i class="bi bi-truck me-2"></i>Place Supplier Reorder</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <form id="reorderStockForm">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label fw-semibold">Product Name</label>
              <input type="text" id="reorderProductName" class="form-control" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label fw-semibold">Quantity to Order into Receiving</label>
              <input type="number" id="reorderQty" class="form-control" value="50" min="10" required>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="submit" class="btn btn-danger" data-bs-dismiss="modal">Receive New Supplier Stock</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Bootstrap JS Bundle -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    // 30 Fast-Moving Pick n Pay Grocery Products
    const productsData = [
      { name: "PnP Full Cream Milk 2L", shelfQty: 5, reqQty: 25, receivingQty: 20, aisle: "Aisle 1 (Dairy)" },
      { name: "Albany Superior White Bread 700g", shelfQty: 4, reqQty: 30, receivingQty: 12, aisle: "Aisle 2 (Bakery)" },
      { name: "Coca-Cola Original 2L", shelfQty: 8, reqQty: 40, receivingQty: 50, aisle: "Aisle 3 (Beverages)" },
      { name: "PnP Large Eggs 30s", shelfQty: 3, reqQty: 15, receivingQty: 8, aisle: "Aisle 1 (Dairy)" },
      { name: "Sasko Brown Bread 700g", shelfQty: 6, reqQty: 25, receivingQty: 35, aisle: "Aisle 2 (Bakery)" },
      { name: "Nescafe Ricoffy 750g", shelfQty: 10, reqQty: 20, receivingQty: 25, aisle: "Aisle 4 (Pantry)" },
      { name: "Tastic Long Grain Rice 2kg", shelfQty: 2, reqQty: 18, receivingQty: 5, aisle: "Aisle 4 (Pantry)" },
      { name: "White Star Maize Meal 2.5kg", shelfQty: 5, reqQty: 35, receivingQty: 40, aisle: "Aisle 4 (Pantry)" },
      { name: "Flora Light Spread 500g", shelfQty: 7, reqQty: 15, receivingQty: 20, aisle: "Aisle 1 (Dairy)" },
      { name: "Clover Gouda Cheese 850g", shelfQty: 2, reqQty: 12, receivingQty: 4, aisle: "Aisle 1 (Dairy)" },
      { name: "PnP Fresh Chicken Pack 1kg", shelfQty: 6, reqQty: 20, receivingQty: 8, aisle: "Butchery" },
      { name: "Koo Baked Beans 410g", shelfQty: 12, reqQty: 50, receivingQty: 60, aisle: "Aisle 5 (Canned)" },
      { name: "All Gold Tomato Sauce 700ml", shelfQty: 4, reqQty: 22, receivingQty: 15, aisle: "Aisle 5 (Condiments)" },
      { name: "Huletts White Sugar 2kg", shelfQty: 8, reqQty: 30, receivingQty: 45, aisle: "Aisle 4 (Pantry)" },
      { name: "Sunfoil Sunflower Oil 2L", shelfQty: 3, reqQty: 25, receivingQty: 10, aisle: "Aisle 4 (Pantry)" },
      { name: "Simba Potato Chips 120g", shelfQty: 15, reqQty: 45, receivingQty: 60, aisle: "Aisle 6 (Snacks)" },
      { name: "Cadbury Dairy Milk 150g", shelfQty: 10, reqQty: 30, receivingQty: 12, aisle: "Aisle 6 (Sweets)" },
      { name: "Five Roses Tea Bags 100s", shelfQty: 5, reqQty: 20, receivingQty: 25, aisle: "Aisle 4 (Pantry)" },
      { name: "Jacobs Kronung Coffee 200g", shelfQty: 4, reqQty: 15, receivingQty: 18, aisle: "Aisle 4 (Pantry)" },
      { name: "Danone Ultra Mel Custard 1L", shelfQty: 8, reqQty: 24, receivingQty: 30, aisle: "Aisle 1 (Dairy)" },
      { name: "McCain Cut Green Beans 1kg", shelfQty: 3, reqQty: 12, receivingQty: 6, aisle: "Aisle 7 (Frozen)" },
      { name: "PnP Beef Sausage 1kg", shelfQty: 5, reqQty: 18, receivingQty: 22, aisle: "Butchery" },
      { name: "Handy Andy Cleaner 750ml", shelfQty: 6, reqQty: 20, receivingQty: 30, aisle: "Aisle 8 (Household)" },
      { name: "Omo Auto Washing Powder 2kg", shelfQty: 4, reqQty: 16, receivingQty: 9, aisle: "Aisle 8 (Household)" },
      { name: "Colgate Triple Action 100ml", shelfQty: 14, reqQty: 30, receivingQty: 40, aisle: "Aisle 9 (Toiletries)" },
      { name: "Baby Soft Toilet Paper 9s", shelfQty: 2, reqQty: 20, receivingQty: 15, aisle: "Aisle 8 (Household)" },
      { name: "Kellogg's Corn Flakes 1kg", shelfQty: 6, reqQty: 25, receivingQty: 35, aisle: "Aisle 4 (Cereal)" },
      { name: "Bokomo Weet-Bix 450g", shelfQty: 9, reqQty: 28, receivingQty: 30, aisle: "Aisle 4 (Cereal)" },
      { name: "Dettol Antiseptic 500ml", shelfQty: 5, reqQty: 15, receivingQty: 20, aisle: "Aisle 9 (Health)" },
      { name: "Jungle Oats 1kg", shelfQty: 7, reqQty: 20, receivingQty: 25, aisle: "Aisle 4 (Cereal)" }
    ];

    document.addEventListener('DOMContentLoaded', function() {
      const tbody = document.getElementById('inventoryTableBody');
      const taskModal = new bootstrap.Modal(document.getElementById('createTaskModal'));
      const reorderModal = new bootstrap.Modal(document.getElementById('reorderModal'));
      const priorityWidget = document.getElementById('priorityWidgetBody');
      const toastEl = document.getElementById('outOfStockToast');
      const toast = new bootstrap.Toast(toastEl);

      function renderTable() {
        tbody.innerHTML = '';
        priorityWidget.innerHTML = '';

        let sumReceiving = 0;
        let insufficientCount = 0;
        let sufficientCount = 0;

        productsData.forEach((p) => {
          const qtyNeeded = Math.max(0, p.reqQty - p.shelfQty);
          const isSufficient = p.receivingQty >= qtyNeeded && p.receivingQty > 0;
          const isOutOfStock = p.receivingQty === 0;

          sumReceiving += p.receivingQty;
          if (isSufficient) sufficientCount++;
          else insufficientCount++;

          let badgeHTML = `<span class="badge badge-sufficient">Sufficient</span>`;
          if (isOutOfStock) {
            badgeHTML = `<span class="badge badge-outofstock">OUT OF STOCK</span>`;
          } else if (!isSufficient) {
            badgeHTML = `<span class="badge badge-insufficient">Insufficient</span>`;
          }

          let actionBtn = `
            <button class="btn btn-sm btn-outline-primary restock-btn" 
              data-product="${p.name}" 
              data-qty="${qtyNeeded}" 
              data-aisle="${p.aisle}">
              Restock
            </button>
          `;

          if (isOutOfStock) {
            actionBtn = `
              <button class="btn btn-sm btn-danger reorder-btn" 
                data-product="${p.name}">
                <i class="bi bi-cart-plus me-1"></i>Reorder
              </button>
            `;
          }

          const row = document.createElement('tr');
          row.innerHTML = `
            <td class="fw-bold">${p.name}</td>
            <td>${p.shelfQty}</td>
            <td>${p.reqQty}</td>
            <td class="${qtyNeeded > 0 ? 'text-danger fw-bold' : 'text-success'}">${qtyNeeded}</td>
            <td class="${isOutOfStock ? 'text-danger fw-bold fs-6' : ''}">${p.receivingQty}</td>
            <td>${badgeHTML}</td>
            <td>${actionBtn}</td>
          `;
          tbody.appendChild(row);

          // Populate Top Critical Alerts Side Widget
          if (!isSufficient && priorityWidget.children.length < 3) {
            const alertBox = document.createElement('div');
            alertBox.className = `p-2 mb-2 bg-light border-start border-4 ${isOutOfStock ? 'border-dark' : 'border-danger'} rounded`;
            alertBox.innerHTML = `
              <div class="d-flex justify-content-between">
                <span class="fw-bold">${p.name}</span>
                <span class="badge ${isOutOfStock ? 'bg-dark' : 'priority-high'}">${isOutOfStock ? 'OUT OF STOCK' : 'High Alert'}</span>
              </div>
              <small class="text-muted">Receiving Stock: <strong>${p.receivingQty}</strong> units</small>
              <button class="btn ${isOutOfStock ? 'btn-danger' : 'btn-outline-danger'} btn-sm w-100 mt-2 ${isOutOfStock ? 'reorder-btn' : 'restock-btn'}" data-product="${p.name}" data-qty="${qtyNeeded}" data-aisle="${p.aisle}">
                ${isOutOfStock ? 'Place Reorder' : 'Create Urgent Task'}
              </button>
            `;
            priorityWidget.appendChild(alertBox);
          }
        });

        // Update Header Displays
        document.getElementById('kpiTotalProducts').textContent = productsData.length;
        document.getElementById('kpiReceivingStock').textContent = sumReceiving;
        document.getElementById('kpiInsufficient').textContent = insufficientCount;
        document.getElementById('kpiSufficient').textContent = sufficientCount;
      }

      // Initial Render
      renderTable();

      // Main Blue "+ New Replenishment Task" Button Event
      const openModalBtn = document.getElementById('openNewTaskModalBtn');
      if (openModalBtn) {
        openModalBtn.addEventListener('click', function() {
          document.getElementById('modalProductName').value = "";
          document.getElementById('modalQtyNeeded').value = "10";
          document.getElementById('modalPriority').value = "Medium";
          document.getElementById('modalShelfLoc').value = "Aisle 1, Shelf 1";
          taskModal.show();
        });
      }

      // Action Handlers
      document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('restock-btn')) {
          const prodName = e.target.getAttribute('data-product');
          const qty = e.target.getAttribute('data-qty');
          const aisle = e.target.getAttribute('data-aisle');

          document.getElementById('modalProductName').value = prodName;
          document.getElementById('modalQtyNeeded').value = qty > 0 ? qty : 10;
          document.getElementById('modalShelfLoc').value = aisle;
          taskModal.show();
        }

        if (e.target && e.target.classList.contains('reorder-btn')) {
          const prodName = e.target.getAttribute('data-product');
          document.getElementById('reorderProductName').value = prodName;
          reorderModal.show();
        }
      });

      // Handle Reorder Form Submission
      const reorderForm = document.getElementById('reorderStockForm');
      if (reorderForm) {
        reorderForm.addEventListener('submit', function(e) {
          e.preventDefault();
          const prodName = document.getElementById('reorderProductName').value;
          const reorderQty = parseInt(document.getElementById('reorderQty').value || '50');

          const foundProduct = productsData.find(p => p.name.toLowerCase() === prodName.toLowerCase());
          if (foundProduct) {
            foundProduct.receivingQty += reorderQty;
            renderTable();
            alert(`Stock Received! Added ${reorderQty} units of ${prodName} into Receiving Stock.`);
          }
        });
      }

      // Sidebar Tab Switching
      document.querySelectorAll('.sidebar-nav .nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          document.querySelectorAll('.sidebar-nav .nav-link').forEach(l => l.classList.remove('active'));
          document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('show', 'active'));
          this.classList.add('active');
          const target = document.querySelector(this.getAttribute('data-bs-target'));
          if(target) target.classList.add('show', 'active');
        });
      });

      // Table Filter Search
      const tableSearch = document.getElementById('tableSearchInput');
      if(tableSearch) {
        tableSearch.addEventListener('input', function(e) {
          const term = e.target.value.toLowerCase();
          document.querySelectorAll('#inventoryTable tbody tr').forEach(row => {
            row.style.display = row.textContent.toLowerCase().includes(term) ? '' : 'none';
          });
        });
      }

      // Task Form Submission Dispatch
      const taskForm = document.getElementById('replenishmentTaskForm');
      const tasksContainer = document.getElementById('tasksContainer');
      const noTasksMsg = document.getElementById('noTasksMsg');
      const taskBadgeCount = document.getElementById('taskBadgeCount');
      const perfPending = document.getElementById('perfPending');
      const perfCompleted = document.getElementById('perfCompleted');

      if(taskForm) {
        taskForm.addEventListener('submit', function(e) {
          e.preventDefault();
          const prodName = document.getElementById('modalProductName').value;
          const qtyNeeded = parseInt(document.getElementById('modalQtyNeeded').value);
          const priority = document.getElementById('modalPriority').value;
          const shelfLoc = document.getElementById('modalShelfLoc').value;

          if (noTasksMsg) noTasksMsg.style.display = 'none';

          const badgeClass = priority === 'High' ? 'priority-high' : (priority === 'Medium' ? 'priority-medium' : 'priority-low');
          const borderClass = priority === 'High' ? 'border-danger' : (priority === 'Medium' ? 'border-warning' : 'border-info');

          const newTaskHTML = `
            <div class="card mb-3 border-start border-4 ${borderClass} shadow-sm task-card" data-product="${prodName}" data-qty="${qtyNeeded}">
              <div class="card-body d-flex justify-content-between align-items-center">
                <div>
                  <h5 class="fw-bold mb-1">${prodName}</h5>
                  <p class="text-muted small mb-0">Quantity Needed: <strong>${qtyNeeded}</strong> | Location: <strong>${shelfLoc}</strong> | Priority: <span class="badge ${badgeClass}">${priority}</span></p>
                </div>
                <button class="btn btn-success btn-sm mark-complete-btn">Mark Complete</button>
              </div>
            </div>
          `;
          tasksContainer.insertAdjacentHTML('beforeend', newTaskHTML);

          let currentPending = parseInt(taskBadgeCount.textContent || '0') + 1;
          taskBadgeCount.textContent = currentPending;
          perfPending.textContent = currentPending;

          attachCompleteHandlers();
        });
      }

      function attachCompleteHandlers() {
        document.querySelectorAll('.mark-complete-btn').forEach(btn => {
          btn.onclick = function() {
            const card = this.closest('.task-card');
            if (card) {
              const prodName = card.getAttribute('data-product');
              const qtyNeeded = parseInt(card.getAttribute('data-qty') || '0');

              // Deduct stock from receiving inventory
              const foundProduct = productsData.find(p => p.name.toLowerCase() === prodName.toLowerCase());
              if (foundProduct) {
                foundProduct.shelfQty += qtyNeeded;
                if (foundProduct.shelfQty > foundProduct.reqQty) foundProduct.shelfQty = foundProduct.reqQty;

                // Subtract from Receiving Stock
                foundProduct.receivingQty = Math.max(0, foundProduct.receivingQty - qtyNeeded);

                // If receiving stock hits 0, trigger pop-up alert
                if (foundProduct.receivingQty === 0) {
                  document.getElementById('toastMessage').innerHTML = `<strong>WARNING:</strong> ${foundProduct.name} is now <strong>OUT OF STOCK</strong> in Receiving! Please place a reorder.`;
                  toast.show();
                }
              }

              card.remove();

              // Re-render table & widgets
              renderTable();

              let currentPending = Math.max(0, parseInt(taskBadgeCount.textContent || '1') - 1);
              taskBadgeCount.textContent = currentPending;
              perfPending.textContent = currentPending;
              perfCompleted.textContent = parseInt(perfCompleted.textContent || '0') + 1;

              if (tasksContainer.querySelectorAll('.task-card').length === 0 && noTasksMsg) {
                noTasksMsg.style.display = 'block';
              }
            }
          };
        });
      }
    });
  </script>
</body>
</html>