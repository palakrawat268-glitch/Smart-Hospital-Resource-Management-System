"""
================================================================================
DBMS MODULE INSPECTOR - Smart Hospital Resource Management System
================================================================================
Run: python inspect_db.py
Inspects active database connection, registered tables, schemas, and record counts.
================================================================================
"""

import os
import sys

# Ensure root directory is on path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from extensions import db
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.ward import Ward
from models.bed import Bed
from models.equipment import Equipment
from models.resource import ResourceRequest, ResourceAllocation
from models.deadlock import DeadlockLog

def inspect_database():
    app = create_app()
    with app.app_context():
        print("=" * 70)
        print(" SMART HOSPITAL DBMS MODULE INSPECTION REPORT")
        print("=" * 70)
        print(f"Active Database Engine URI : {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"SQLAlchemy Dialect         : {db.engine.dialect.name.upper()}")
        print("-" * 70)

        # Inspect all tables in metadata
        tables = [
            ("users", User),
            ("patients", Patient),
            ("doctors", Doctor),
            ("appointments", Appointment),
            ("wards", Ward),
            ("beds", Bed),
            ("equipment", Equipment),
            ("resource_requests", ResourceRequest),
            ("resource_allocations", ResourceAllocation),
            ("deadlock_logs", DeadlockLog)
        ]

        print(f"{'TABLE NAME':<24} | {'RECORD COUNT':<14} | {'COLUMNS':<30}")
        print("-" * 70)

        for table_name, model in tables:
            try:
                count = model.query.count()
                columns = ", ".join([col.name for col in model.__table__.columns[:4]]) + "..."
                print(f"{table_name:<24} | {count:<14} | {columns:<30}")
            except Exception as e:
                print(f"{table_name:<24} | ERROR: {e}")

        print("=" * 70)
        print(" SAMPLE RECORDS PREVIEW")
        print("=" * 70)

        # 1. Users & Roles
        print("\n[1] Users & Roles (users):")
        for u in User.query.all():
            print(f"  - ID: {u.id:02d} | Username: {u.username:<12} | Role: {u.role:<12} | Name: {u.full_name}")

        # 2. Patients & Triage
        print("\n[2] Patients & Triage Priority (patients):")
        for p in Patient.query.limit(4).all():
            bed_str = p.current_bed.bed_number if p.current_bed else "Unassigned"
            print(f"  - {p.patient_id} | {p.patient_name:<18} | Priority: {p.priority_level:<9} | Status: {p.patient_status:<9} | Bed: {bed_str}")

        # 3. Wards & Capacity
        print("\n[3] Hospital Wards (wards):")
        for w in Ward.query.all():
            print(f"  - {w.ward_id} | {w.ward_name:<26} | Type: {w.ward_type:<10} | Occ: {w.occupied_beds}/{w.capacity} beds")

        # 4. Equipment
        print("\n[4] Medical Equipment (equipment):")
        for eq in Equipment.query.all():
            print(f"  - {eq.equipment_id} | {eq.equipment_name:<34} | Status: {eq.equipment_status:<12} | Avail: {eq.availability}")

        # 5. Deadlock Logs
        print("\n[5] Deadlock Audit Logs (deadlock_logs):")
        for dl in DeadlockLog.query.all():
            print(f"  - {dl.log_id} | Cycle: {dl.cycle_detected} | Action: {dl.resolution_action}")

        print("=" * 70)

if __name__ == '__main__':
    inspect_database()
