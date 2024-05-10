from .a_routes import a_route_bp
from .g_routes import groute_bp
from .c_routes import croute_bp
from .q_routes import qroute_bp

def register_routes(app):
    app.register_blueprint(a_route_bp, url_prefix='/')
    app.register_blueprint(groute_bp, url_prefix='/')
    app.register_blueprint(croute_bp, url_prefix='/')
    app.register_blueprint(qroute_bp, url_prefix='/')

