from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restx import Api
from config import Config
import logging
import os

# 初始化扩展
db = SQLAlchemy()
cors = CORS()

def create_app(config_class=Config):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    cors.init_app(app)
    
    # 初始化日志系统
    from app.utils.logger import tts_logger
    tts_logger.init_app(app)
    
    # 创建API实例
    api = Api(
        app,
        version='1.0',
        title='Sherpa TTS API',
        description='基于Sherpa-ONNX的文本转语音服务API',
        doc='/docs/',
        prefix='/api/v1'
    )
    
    # 注册蓝图和命名空间
    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    
    # 注册API命名空间
    from app.api.tts import api as tts_ns
    from app.api.models import api as models_ns
    from app.api.system import api as system_ns
    
    api.add_namespace(tts_ns, path='/tts')
    api.add_namespace(models_ns, path='/models')
    api.add_namespace(system_ns, path='/system')
    
    # 在应用上下文中创建数据库表
    with app.app_context():
        db.create_all()
    
    # 注册错误处理器
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理器"""
    from app.exceptions import TTSException
    from app.utils.helpers import create_error_response
    
    @app.errorhandler(TTSException)
    def handle_tts_exception(e):
        """处理TTS异常"""
        app.logger.error(f"TTS异常: {str(e)}")
        return create_error_response(str(e), 'TTS_ERROR'), 500
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """处理404错误"""
        return create_error_response('请求的资源不存在', 'NOT_FOUND'), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """处理405错误"""
        return create_error_response('请求方法不被允许', 'METHOD_NOT_ALLOWED'), 405
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """处理500错误"""
        app.logger.error(f"内部服务器错误: {str(e)}")
        return create_error_response('内部服务器错误', 'INTERNAL_ERROR'), 500