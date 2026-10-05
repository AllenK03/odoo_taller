ERP Taller Mecánico (taller_mecanico)
Custom module developed on Odoo 17 Community Edition designed for the operational and financial management of the auto repair shop Autosercar, C.A. It manages the complete vehicle repair workflow, from vehicle check-in to PDF report generation and accounting integration.

🚀 Key Features
Vehicle Management: Unit registration linked to customers, license plate numbers, make, model, year, and serial numbers.

Work Orders (OT):

Automatic sequence generation (OT-XXXXX).

Workflow tracking for diagnostics, labor, and spare parts used.

Dynamic views in Kanban, List, Form, and Search filter formats.

PDF Reports (QWeb): Formatted printing for repair quotes and vehicle check-in receipts with custom company letterhead.

Accounting Integration: Direct connection to sales journals (sale) for invoice creation.

🛠️ Tech Stack
ERP: Odoo 17.0 (Community Edition)

Database: PostgreSQL 15

Containerization: Docker & Docker Compose

PDF Engine: Wkhtmltopdf

Languages: Python 3.10+, XML, QWeb, JS (OWL Framework)

📂 Project Structure
Plaintext
odoo_taller/
├── docker-compose.yml          # Container environment configuration (Odoo + PostgreSQL)
├── .gitignore                  # Git exclusions
├── README.md                   # Project documentation
└── custom_addons/
    └── taller_mecanico/        # Custom module
        ├── __manifest__.py     # Module manifest
        ├── security/           # Access rules (ir.model.access.csv)
        ├── data/               # Automatic sequences (taller_orden_sequence.xml)
        ├── models/             # Python data logic
        ├── views/              # XML views (Form, Tree, Kanban, Search)
        └── reports/            # QWeb PDF print templates
⚙️️ Prerequisites
Ensure you have the following installed on your host machine:

Docker Desktop (or Docker Engine + Docker Compose)

Git

📦 Local Installation & Deployment
Clone the repository:

Bash
git clone https://github.com/AllenK03/odoo_taller.git
cd odoo_taller
Start services with Docker Compose:

Bash
docker compose up -d
Install / Sync the module in the database (taller_db):

Bash
docker compose exec web odoo --db_host=db -r odoo -w odoo -i taller_mecanico -d taller_db --stop-after-init
Restart the Odoo web service:

Bash
docker compose restart web
Access the application:
Open your browser and navigate to: http://localhost:8069

⚙️ Recommended Initial Setup
When deploying to a new environment for the first time:

Company: Rename the main company, updating the ID, phone, address, and logo under Ajustes > Compañías.

Sales Journal: Verify under Facturación > Configuración > Diarios that a journal with type Ventas (sale) exists to enable invoice generation.

Document Layout: Adjust printing headers under Ajustes > Ajustes Generales > Diseño de documento.

👤 Author
Diego Giordano - Lead Developer - GitHub

📜 License
This project is licensed under LGPL-3.0. See the manifest file for details.
