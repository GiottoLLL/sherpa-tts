# -*- coding: utf-8 -*-
"""
应用配置文件
"""
import os
from datetime import timedelta

class Config:
    """基础配置类"""
    
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tts_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Flask-RESTX配置
    RESTX_MASK_SWAGGER = False
    RESTX_VALIDATE = True
    RESTX_JSON = {
        'ensure_ascii': False,
        'indent': 2
    }
    
    # CORS配置
    CORS_ORIGINS = ['*']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    
    # 服务器配置
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 9777)
    DEBUG = False
    THREADED = True
    
    # 请求配置
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT') or 30)  # 30秒
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # TTS配置
    TTS_MAX_TEXT_LENGTH = int(os.environ.get('TTS_MAX_TEXT_LENGTH') or 1000)
    TTS_OUTPUT_DIR = os.environ.get('TTS_OUTPUT_DIR') or 'outputs'
    TTS_AUDIO_FORMAT = 'wav'
    TTS_SAMPLE_RATE = int(os.environ.get('TTS_SAMPLE_RATE') or 22050)
    TTS_BIT_RATE = int(os.environ.get('TTS_BIT_RATE') or 16)
    
    # 模型配置
    MODELS_DIR = os.environ.get('MODELS_DIR') or '../models/sherpa-onnx'
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL') or 'sherpa-onnx-vits-zh-ll'
    
    # 模型路径配置
    MODEL_CONFIGS = {
        'sherpa-onnx-vits-zh-ll': {
            'type': 'vits',
            'model_dir': 'sherpa-onnx-vits-zh-ll',
            'vits_model': 'model.onnx',
            'vits_lexicon': 'lexicon.txt',
            'vits_tokens': 'tokens.txt',
            'tts_rule_fsts': 'date.fst,number.fst',
            'vits_dict_dir': 'dict',
            'sid': 0,
            'display_name': 'VITS 中文女声 (LL)',
            'language': 'zh-CN',
            'gender': 'female',
            'sample_rate': 22050
        },
        'matcha-icefall-zh-baker': {
            'type': 'matcha',
            'model_dir': 'matcha-icefall-zh-baker',
            'matcha_acoustic_model': 'model-steps-3.onnx',
            'matcha_vocoder': '',  # Matcha模型内置vocoder，不需要单独文件
            'matcha_lexicon': 'lexicon.txt',
            'matcha_tokens': 'tokens.txt',
            'tts_rule_fsts': 'date.fst,number.fst',
            'matcha_dict_dir': 'dict',
            'display_name': 'Matcha 中文女声 (Baker)',
            'language': 'zh-CN',
            'gender': 'female',
            'sample_rate': 22050
        }
    }
    
    # 支持的模型配置（用于API接口）
    SUPPORTED_MODELS = MODEL_CONFIGS
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/tts_app.log'
    LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES') or 10485760)  # 10MB
    LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT') or 5)
    
    # 统计配置
    STATS_RETENTION_DAYS = int(os.environ.get('STATS_RETENTION_DAYS') or 90)
    STATS_CLEANUP_INTERVAL = int(os.environ.get('STATS_CLEANUP_INTERVAL') or 24)  # 小时
    
    # 并发配置
    MAX_CONCURRENT_REQUESTS = int(os.environ.get('MAX_CONCURRENT_REQUESTS') or 5)
    QUEUE_TIMEOUT = int(os.environ.get('QUEUE_TIMEOUT') or 60)  # 秒
    
    # 缓存配置
    CACHE_TYPE = os.environ.get('CACHE_TYPE') or 'simple'
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT') or 300)
    
    @staticmethod
    def init_app(app):
        """初始化应用配置"""
        pass

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    PORT = 9777
    HOST = '127.0.0.1'
    LOG_LEVEL = 'DEBUG'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    PORT = 9778
    HOST = '127.0.0.1'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    PORT = 9777
    HOST = '0.0.0.0'
    LOG_LEVEL = 'WARNING'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # 生产环境特定配置
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/tts_service.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('TTS Service startup')

# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}