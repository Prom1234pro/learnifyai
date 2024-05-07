from .routes import route_bp, load_active_sessions, save_active_sessions
from .g_routes import groute_bp
from .c_routes import croute_bp
from .q_routes import qroute_bp

def register_routes(app):
    app.register_blueprint(route_bp, url_prefix='/')
    app.register_blueprint(groute_bp, url_prefix='/')
    app.register_blueprint(croute_bp, url_prefix='/')
    app.register_blueprint(qroute_bp, url_prefix='/')

