# Smart Hospital Resource Management System

A production-quality foundation web application (~40-50% complete) for hospital resource allocation, clinical management, and future Operating System algorithm integration (Scheduling, Deadlock Avoidance, Concurrency Control, and Dynamic Partitioning).

Built with **Python 3**, **Flask**, **SQLAlchemy ORM**, **Bootstrap 5**, **Font Awesome**, and **Chart.js**.

---

## Default Test Accounts

| Role | Username | Password | Default Redirect |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | `/dashboard/admin` |
| **Attending Doctor** | `doctor` | `doctor123` | `/dashboard/doctor` |
| **Receptionist** | `receptionist` | `reception123` | `/dashboard/receptionist` |

---

## Technology Stack

- **Backend:** Python 3.14, Flask 3.1, Flask-SQLAlchemy 3.1, Flask-Login, Flask-WTF, Werkzeug Password Hashing.
- **Database:** MySQL 8.0 (default via `PyMySQL`) with seamless local SQLite fallback (`instance/hospital.db`).
- **Frontend:** Bootstrap 5.3, Font Awesome 6.5, Chart.js 4.4, Custom Clinical Blue Theme (`static/css/style.css`).
- **Architecture:** MVC Pattern, Modular Flask Blueprints, Reusable UI Components.

---

## Folder Structure

```
SD_Assignment1/
├── app.py                      # Application factory & runner
├── config.py                   # MySQL / SQLite configuration & environment settings
├── extensions.py               # SQLAlchemy & LoginManager instances
├── requirements.txt            # Dependency specification
├── models/                     # SQLAlchemy Models (10 tables with relationships)
│   ├── __init__.py
│   ├── user.py                 # Users & Role-Based Access Control
│   ├── patient.py              # Inpatient / Outpatient medical records & triage
│   ├── doctor.py               # Attending physicians & availability states
│   ├── appointment.py          # Clinical consultation tokens & scheduling
│   ├── ward.py                 # Hospital wings (ICU, Emergency, Surgical, etc.)
│   ├── bed.py                  # Beds & Patient Allocation
│   ├── equipment.py            # Ventilators, Monitors, MRIs, Defibrillators
│   ├── resource.py             # Resource claims & allocation audit logs
│   └── deadlock.py             # Deadlock detection logs & mitigation actions
├── routes/                     # 11 Modular Flask Blueprints
│   ├── __init__.py
│   ├── auth.py                 # Login, Register, Forgot Password, Logout
│   ├── dashboard.py            # Role-tailored dashboards (Admin, Doctor, Receptionist)
│   ├── patients.py             # Patient CRUD, Triage Priority, Bed assignment
│   ├── doctors.py              # Doctor registry, Schedules, Availability toggle
│   ├── appointments.py         # Slot booking, Status progression
│   ├── wards.py                # Ward capacity & Bed tracking
│   ├── beds.py                 # Bed allocation, Discharge, Maintenance
│   ├── equipment.py            # Equipment inventory & Operational maintenance
│   ├── reports.py              # Visual analytics & Printable summaries
│   ├── settings.py             # User profile & Runtime metrics
│   └── os_simulation.py        # 6 OS Algorithm Simulation UI Views
├── services/                   # Placeholder OS Algorithm Services (NO ALGORITHMS IMPLEMENTED)
│   ├── __init__.py
│   ├── fcfs_scheduler.py       # FCFS queue scheduler architecture & comments
│   ├── priority_scheduler.py   # Preemptive priority & aging architecture
│   ├── banker_algorithm.py     # Banker's safe sequence matrix architecture
│   ├── deadlock_detection.py   # RAG / WFG cycle detection architecture
│   ├── resource_allocator.py   # Dynamic Best-Fit / First-Fit architecture
│   └── synchronization.py      # Mutex & Semaphore critical section architecture
├── database/                   # Database initializers
│   ├── __init__.py
│   └── db_init.py              # Schema creation & Demo dataset population
├── utils/                      # Decorators and Helpers
│   ├── __init__.py
│   ├── decorators.py           # @role_required, @admin_required
│   └── helpers.py              # Priority badges, status helpers, code generation
├── static/
│   ├── css/style.css           # Modern clinical dashboard theme (Blue, White, Light Gray)
│   └── js/
│       ├── main.js             # Sidebar toggle, Toast notifications, Modals
│       └── charts.js           # Chart.js initialization for dashboards & reports
├── templates/                  # Jinja2 responsive templates
│   ├── base.html               # Master layout
│   ├── components/             # Navbar, Sidebar, Footer, Toasts, Breadcrumbs
│   ├── auth/                   # login.html, register.html, forgot_password.html
│   ├── dashboard/              # admin.html, doctor.html, receptionist.html
│   ├── patients/               # list.html, add.html, edit.html, profile.html
│   ├── doctors/                # list.html, add.html, profile.html
│   ├── appointments/           # list.html, book.html, details.html
│   ├── wards/                  # list.html, details.html
│   ├── beds/                   # list.html, allocate.html
│   ├── equipment/              # list.html, details.html
│   ├── reports/                # index.html
│   ├── settings/               # index.html
│   ├── os_algorithms/          # fcfs.html, priority.html, banker.html, deadlock.html, sync.html, resource.html
│   └── errors/                 # 403.html, 404.html, 500.html
└── tests/
    └── test_app.py             # Automated unit and integration test suite
```

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database (Optional)
The system automatically connects to MySQL if available, or falls back to local SQLite (`instance/hospital.db`). To specify custom MySQL credentials, set environment variables:
```bash
set MYSQL_USER=root
set MYSQL_PASSWORD=your_password
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set MYSQL_DB=hospital_db
```

### 3. Launch Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

### 4. Run Automated Test Suite
```bash
python -m unittest tests/test_app.py
```

---

## Phase 2 Roadmap: Operating System Algorithms
All 6 service files in `services/` are architected with function signatures, schemas, and extensive comments ready for algorithm implementation:
- **FCFS Scheduling:** Completion time, waiting time, turnaround time, Gantt chart generation.
- **Priority Scheduling:** Preemptive triage context switching with starvation prevention (aging).
- **Banker's Algorithm:** Safety algorithm, Need matrix calculation, safe sequence generation.
- **Deadlock Detection:** RAG/WFG DFS cycle detection and victim preemption proposal.
- **Synchronization:** Operating Theater mutex and counting semaphores.
- **Dynamic Resource Allocation:** First-Fit, Best-Fit, and Worst-Fit ward partitioning.
