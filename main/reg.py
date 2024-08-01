from main.authentication.routes import a_route_bp
from main.user.routes import uroute_bp
from main.cluster.routes import groute_bp
from main.course.routes import croute_bp
from main.quiz.routes import qroute_bp
from main.admin.routes import admin_bp
from main.affiliate.routes import affiliate_bp

def register_routes(app):
    app.register_blueprint(a_route_bp, url_prefix='/')
    app.register_blueprint(uroute_bp, url_prefix='/')
    app.register_blueprint(groute_bp, url_prefix='/')
    app.register_blueprint(croute_bp, url_prefix='/')
    app.register_blueprint(qroute_bp, url_prefix='/')
    app.register_blueprint(admin_bp, url_prefix='/')
    app.register_blueprint(affiliate_bp, url_prefix='/')

