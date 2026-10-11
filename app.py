import os
import sys
from flask import Flask, redirect, url_for, render_template
from config import config, Config
from extensions import db, login_manager
from utils.helpers import priority_badge_class, status_badge_class

def create_app(config_name=None):
    """Application factory creating and configuring the Flask app."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    cfg = config[config_name]
    app.config.from_object(cfg)

    # Determine database URI and test connectivity
    db_uri = cfg.get_database_uri()
    if not cfg.USE_SQLITE and db_uri.startswith('mysql'):
        try:
            import pymysql
            conn = pymysql.connect(
                host=cfg.MYSQL_HOST,
                user=cfg.MYSQL_USER,
                password=cfg.MYSQL_PASSWORD,
                port=int(cfg.MYSQL_PORT),
                connect_timeout=2
            )
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cfg.MYSQL_DB} CHARACTER SET utf8mb4;")
            conn.close()
            print(f"[INFO] Successfully connected to MySQL database: {cfg.MYSQL_DB}")
        except Exception as err:
            print(f"[WARNING] MySQL unreachable or credentials not configured: {err}")
            print("[INFO] Seamlessly falling back to local SQLite instance for continuous operation...")
            instance_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
            os.makedirs(instance_dir, exist_ok=True)
            db_uri = f"sqlite:///{os.path.join(instance_dir, 'hospital.db')}"

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.patients import patients_bp
    from routes.doctors import doctors_bp
    from routes.appointments import appointments_bp
    from routes.wards import wards_bp
    from routes.beds import beds_bp
    from routes.equipment import equipment_bp
    from routes.reports import reports_bp
    from routes.settings import settings_bp
    from routes.os_simulation import os_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(wards_bp)
    app.register_blueprint(beds_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(os_bp)

    # Root redirect
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))

    # Context processors for templates
    @app.context_processor
    def inject_global_template_vars():
        return {
            'app_name': 'Smart Hospital Resource Management System',
            'current_year': 2026,
            'priority_badge': priority_badge_class,
            'status_badge': status_badge_class
        }

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Auto-initialize database on startup
    with app.app_context():
        from database.db_init import init_database
        init_database(app)

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    print(f"================================================================")
    print(f" Smart Hospital Resource Management System")
    print(f" Running at: http://127.0.0.1:{port}")
    print(f" Default Accounts:")
    print(f"   Admin:        admin / admin123")
    print(f"   Doctor:       doctor / doctor123")
    print(f"   Receptionist: receptionist / reception123")
    print(f"================================================================")
    app.run(host='0.0.0.0', port=port, debug=True)
