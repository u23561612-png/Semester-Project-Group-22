# Pick n Pay Wolmaransstad – Receiving Stock System

**Semester Project – Group 22**

## 1. Project Overview

- Manages receiving stock and shop floor inventory.
- Tracks stock shortages and replenishment tasks.
- Records stock movements and displays performance statistics.
- Recommends supplier order quantities using the Economic Order Quantity (EOQ) model.
- Uses Flask, Python and MySQL.

## 2. Software Requirements

- Python 3.12
- MySQL Server 8.0.16 or later
- MySQL Workbench
- Git
- A web browser
- Visual Studio Code (recommended)

## 3. Installation and Setup

### 3.1 Download the project

- Open your terminal and run:

```bash
git clone https://github.com/u23561612-png/Semester-Project-Group-22.git
cd Semester-Project-Group-22
```

### 3.2 Install Python packages

- macOS:

```bash
python3 -m pip install -r requirements.txt
```

- Windows:

```powershell
py -m pip install -r requirements.txt
```

### 3.3 Set up the database

- Start MySQL Server and open MySQL Workbench.
- Connect to your local MySQL server.
- Open and run `database/schema.sql` to create the database and its tables.
- Open and run `database/seed.sql` to add sample data.
- Only run these scripts on a fresh database to avoid duplicate records.

### 3.4 Set up the `.env` file

- Create a file called `.env` in the main project folder.
- Use `.env.example` as a guide:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_NAME=pnp_receiving
APP_ENV=development
DB_TEST_NAME=pnp_receiving_test
```

- Enter your own MySQL username and password.
- Never upload your `.env` file to GitHub. It contains private information.

### 3.5 Test the database connection

- macOS: `python3 test_db.py`
- Windows: `py test_db.py`
- A successful connection should show the `pnp_receiving` database and 30 products when using fresh sample data.

### 3.6 Start the website

- macOS: `python3 app.py`
- Windows: `py app.py`
- Open [http://127.0.0.1:5001](http://127.0.0.1:5001).
- Keep the terminal open while using the website.
- Press `Ctrl + C` to stop the server.

## 4. Demo Users

| User | Role |
| --- | --- |
| Sam | Store Manager |
| Alex | Floor Manager |
| Jamie | Staff Member |
| Jordan | Receiving Manager |

- Select a user from the Users tab or the profile in the top-right corner.
- This is a demo user-selection feature, not a secure login system.

## 5. Database Structure

The `pnp_receiving` database contains six tables:

- `products` – product names, codes and barcodes.
- `locations` – shelf and receiving locations.
- `users` – users and their roles.
- `inventory` – current stock and required shelf quantities.
- `replenishment_tasks` – tasks for moving stock to shelves.
- `stock_movements` – history of stock changes.

### 5.1 Entity Relationship Diagram (ERD)

![Receiving Stock System ERD](docs/ERD.png)

## 6. API Documentation

- The REST API connects the website to the database through Flask.
- It sends and receives data in JSON format.
- Base URL: `http://127.0.0.1:5001`

### 6.1 API endpoints

| Method | Endpoint | Purpose | Success code |
| --- | --- | --- | --- |
| GET | `/api/products` | View products and stock | 200 |
| GET | `/api/products/<id>` | View one product | 200 |
| POST | `/api/products` | Add a product and inventory record | 201 |
| PATCH | `/api/products/<id>` | Update a product | 200 |
| GET | `/api/tasks` | View replenishment tasks | 200 |
| GET | `/api/tasks/<id>` | View one task | 200 |
| POST | `/api/tasks` | Create a task | 201 |
| PATCH | `/api/tasks/<id>` | Complete a task | 200 |
| PATCH | `/api/inventory/<id>` | Update stock | 200 |
| GET | `/api/stock-movements` | View stock history | 200 |
| GET | `/api/users` | View users | 200 |
| GET | `/api/locations` | View locations | 200 |
| GET | `/api/dashboard` | View dashboard statistics | 200 |
| GET | `/api/products/<id>/eoq` | Get an EOQ recommendation | 200 |

### 6.2 Searching, filtering and pages

- `/api/products?page=1&size=10` – show the first 10 products.
- `/api/products?search=milk` – search by name, code or barcode.
- `/api/products?status=insufficient` – filter by stock status (`sufficient`, `insufficient` or `out_of_stock`).
- `/api/tasks?status=pending` – filter tasks by status, such as `pending` or `completed`.
- `/api/tasks?priority=high` – filter tasks by priority.
- `/api/locations?type=shelf` – filter locations by `shelf` or `receiving`.
- Page sizes must be between 1 and 100. Without page settings, all matching products are returned.

### 6.3 Example API requests and responses

**View a product:** `GET /api/products/1`

Example response:

```json
{
  "product_id": 1,
  "product_code": "PRD-001",
  "product_name": "PnP Full Cream Milk 2L",
  "barcode": null,
  "shelf_qty": 5,
  "required_shelf_qty": 25,
  "receiving_qty": 20,
  "quantity_needed": 20,
  "shelf_location_id": 1,
  "receiving_location_id": 41,
  "shelf_location": "Aisle 1, Shelf 1",
  "receiving_location": "Receiving - Refrigerated Dairy"
}
```

**Add a product:** `POST /api/products`

```json
{"product_code":"PRD-031","product_name":"PnP Orange Juice 1L","receiving_location_id":43,"shelf_location_id":9,"required_shelf_qty":25}
```

Response: `{"message":"Product created successfully.","product_id":31}`

**Update a product:** `PATCH /api/products/31`

```json
{"product_name":"PnP Orange Juice 2L"}
```

Response: `{"message":"Product updated successfully.","product_id":31}`

**Create a task:** `POST /api/tasks`

```json
{"product_id":1,"quantity":20,"priority":"High","username":"alex"}
```

Response: `{"message":"Replenishment task created.","task_id":5}`

**Complete a task:** `PATCH /api/tasks/5`

```json
{"username":"jamie"}
```

Response: `{"message":"Replenishment task completed.","receiving_qty":0,"shelf_qty":25}`

**Receive stock:** `PATCH /api/inventory/1`

```json
{"action":"receive","quantity":30,"username":"jordan","reason":"Supplier delivery received."}
```

- Stock actions: `receive`, `damage`, `reconcile` and `shelf`.
- Each successful stock transaction creates a stock movement record.
- Example IDs and quantities may change as the system is used.

### 6.4 API status codes

| Code | Meaning |
| --- | --- |
| 200 | Request successful |
| 201 | Record created |
| 400 | Invalid input |
| 404 | Record not found |
| 405 | Method not allowed |
| 500 | Server or database error |

Example error: `{"error":"Product not found."}`

## 7. Validation and Error Handling

- Checks required fields, data types and valid locations.
- Prevents duplicate product codes, barcodes and pending tasks.
- Prevents negative stock and invalid task quantities.
- Prevents moving more stock than is available or needed.
- Checks search filters and page settings.
- Uses safe SQL queries with separate input values.
- Uses database transactions to undo unfinished changes when an operation fails.
- Returns clear JSON errors and records errors using Python logging.

## 8. Project Files and Configuration

| File | Purpose |
| --- | --- |
| `app.py` | Starts Flask and registers the Blueprint |
| `routes/api.py` | Handles API requests and errors |
| `routes/__init__.py` | Makes routes a Python package |
| `config.py` | Stores application settings |
| `db.py` | Connects to MySQL |
| `templates/index.html` | Displays the website |
| `EOQ.py` | Calculates supplier order recommendations |
| `database/schema.sql` | Creates database tables |
| `database/seed.sql` | Adds sample records |
| `test_db.py` | Tests the database connection |
| `requirements.txt` | Lists Python packages |

The application has three settings:

- **Development:** for building and testing locally.
- **Testing:** uses a separate test database.
- **Production:** runs with debugging disabled.

## 9. Economic Order Quantity (EOQ)

EOQ helps decide how much stock to order from suppliers.

- Open Inventory Control.
- Select a product, such as Milk 2L.
- Scroll to EOQ Supplier Order Recommendation.
- Click Calculate EOQ Recommendation.

The model calculates:

- Recommended order quantity.
- Number of orders per year.
- Days between orders.
- Total annual ordering and holding costs.

The model uses estimated demand and costs to protect store information. It does not automatically order or add stock. Real orders must also consider shelf life, storage space and supplier limits.

## 10. Testing and Deployment

- Start Flask before testing the website or API.
- View registered API routes with `python3 -m flask --app app routes` (macOS) or `py -m flask --app app routes` (Windows).
- Test GET requests using a browser, and other requests using Postman, PowerShell or the Flask test client.
- The project runs locally on Windows and macOS for demos and testing.
- A live website would need secure hosting, proper login security and a production WSGI server.

## 11. Team Members and Contributions

### 11.1 Sofia Stavrou - u23546787
- MySQL database design and ERD.
- Flask and MySQL integration.
- Inventory management and stock movements.
- EOQ model integration.
- Database backup and recovery.
- README documentation.

### 11.2 Stefan Potgieter - 23561612
- Dashboard development.
- Frontend design and functionality.
- REST API development.
- Input validation, filtering and pagination.
- Flask Blueprint structure.

### 11.3 Shared Responsibilities
- Project proposal.
- System integration.
- Testing and debugging.
- GitHub collaboration.
- Final project report.

## 12. Automated Testing

The project includes 14 automated tests for inventory and replenishment logic.

### Run tests

macOS:
```bash
python3 -m unittest discover -s tests -v
```

Windows:
```powershell
py -m unittest discover -s tests -v
```

### Tested functions

- EOQ calculations.
- Stock availability.
- Required shelf quantities.
- Replenishment tasks.
- Invalid stock quantities.
- Supplier stock orders.
- Performance statistics.

All 14 tests passed successfully.