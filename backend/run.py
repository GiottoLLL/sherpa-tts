#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS应用启动脚本
"""
import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import create_app
from config import Config

def setup_directories():
    """创建必要的目录"""
    directories = [
        Config.TTS_OUTPUT_DIR,
        'logs',
        'temp'
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {directory}")

def check_models():
    """检查模型文件是否存在"""
    models_dir = Path(Config.MODELS_DIR)
    if not models_dir.exists():
        print(f"警告: 模型目录不存在: {models_dir}")
        print("请确保模型文件已正确放置在指定目录中")
        return False
    
    missing_models = []
    for model_name, model_config in Config.MODEL_CONFIGS.items():
        model_path = models_dir / model_config['model_dir']
        if not model_path.exists():
            missing_models.append(model_name)
    
    if missing_models:
        print(f"警告: 以下模型目录不存在: {', '.join(missing_models)}")
        print("应用仍可启动，但这些模型将无法使用")
    
    return True

def setup_logging():
    """设置日志配置"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'tts_service.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """主函数"""
    print("=" * 50)
    print("Sherpa TTS Service 启动中...")
    print("=" * 50)
    
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 创建必要目录
        setup_directories()
        
        # 检查模型文件
        check_models()
        
        # 创建Flask应用
        app = create_app()
        
        # 获取配置
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8000))
        debug = os.getenv('ENVIRONMENT', 'production') == 'development'
        
        logger.info(f"启动服务器: http://{host}:{port}")
        logger.info(f"调试模式: {debug}")
        logger.info(f"环境: {os.getenv('ENVIRONMENT', 'production')}")
        
        # 启动应用
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
        
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务...")
    except Exception as e:
        logger.error(f"启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()