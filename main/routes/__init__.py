from .auth.auth import a_route_bp
from .admin.admin import ad_route_bp
from .cluster.cluster import groute_bp
from .course.course import croute_bp
from .quiz.quiz import qroute_bp

def register_routes(app):
    app.register_blueprint(a_route_bp, url_prefix='/')
    app.register_blueprint(ad_route_bp, url_prefix='/')
    app.register_blueprint(groute_bp, url_prefix='/')
    app.register_blueprint(croute_bp, url_prefix='/')
    app.register_blueprint(qroute_bp, url_prefix='/')

