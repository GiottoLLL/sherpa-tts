# Sherpa-TTS

基于 [sherpa-onnx](https://k2-fsa.github.io/sherpa/onnx/python/index.html) 框架构建的高质量中文文字转语音(TTS)服务，采用前后端分离架构，提供简洁易用的Web界面和RESTful API。

## ✨ 特性

- 🎯 **高质量语音合成**: 基于先进的神经网络TTS模型
- 🌐 **前后端分离**: React + TypeScript前端 + FastAPI后端，架构清晰
- 📱 **现代化界面**: 响应式设计，支持移动端访问
- 📊 **历史记录管理**: 完整的转换历史记录和统计
- 🔧 **多模型支持**: 支持多种TTS模型切换
- 📝 **完整日志**: 详细的操作日志和错误追踪
- 🚀 **高性能**: 模型预加载，快速响应
- 🔒 **安全可靠**: 输入验证，错误处理，文件管理

## 🎵 支持的模型

- **Matcha TTS (Baker)**: 基于Matcha架构的中文TTS模型
- **VITS 多说话人**: 基于VITS的中文多说话人TTS模型

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- 4GB+ 内存
- 10GB+ 可用存储空间

### 1. 克隆项目

```bash
git clone https://github.com/GiottoLLL/sherpa-tts.git
cd sherpa-tts
```

### 2. 后端设置

```bash
# 创建虚拟环境
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动后端服务
python run.py
```

### 3. 前端设置

```bash
# 安装依赖
cd frontend
npm install

# 启动开发服务器
npm start
```

### 4. 访问应用

- 前端界面: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/api/v1/system/health

## 📁 项目结构

```
sherpa-tts/
├── backend/                    # 后端代码
│   ├── app/                   # 应用核心
│   │   ├── api/              # API路由
│   │   ├── services/         # 业务逻辑
│   │   ├── utils/            # 工具函数
│   │   ├── models.py         # 数据模型
│   │   └── exceptions.py     # 异常处理
│   ├── config.py             # 配置文件
│   ├── run.py                # 应用启动文件
│   ├── init_db.py            # 数据库初始化
│   └── requirements.txt      # Python依赖
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── components/       # React组件
│   │   │   ├── TTSForm.tsx   # TTS输入表单
│   │   │   ├── AudioPlayer.tsx # 音频播放器
│   │   │   └── HistoryList.tsx # 历史记录列表
│   │   ├── services/         # API服务
│   │   │   └── api.ts        # API接口封装
│   │   └── App.tsx           # 主应用
│   ├── package.json          # Node.js依赖
│   └── tsconfig.json         # TypeScript配置
├── models/sherpa-onnx/        # TTS模型文件
│   ├── matcha-icefall-zh-baker/
│   └── sherpa-onnx-vits-zh-ll/
└── docs/                      # 项目文档
    ├── development-guide.md   # 开发指南
    ├── api-documentation.md   # API文档
    └── deployment-guide.md    # 部署指南
```

## 🔧 配置说明

### 后端配置 (.env)

```bash
# 数据库配置
DATABASE_URL=sqlite:///tts_service.db

# 模型配置
MODELS_PATH=../models/sherpa-onnx
DEFAULT_MODEL=matcha-icefall-zh-baker

# 服务配置
ENVIRONMENT=development
SECRET_KEY=your-secret-key

# API配置
MAX_TEXT_LENGTH=1000
CORS_ORIGINS=http://localhost:3000
```

## 📖 API 使用示例

### 文字转语音

```javascript
const response = await fetch('/api/v1/tts/synthesize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: '你好，这是一个测试',
        model: 'matcha-icefall-zh-baker'
    })
})

const audioBlob = await response.blob()
const audioUrl = URL.createObjectURL(audioBlob)
```

### 获取可用模型

```javascript
const response = await fetch('/api/v1/models')
const models = await response.json()
console.log(models)
```

### 系统健康检查

```javascript
const response = await fetch('/api/v1/system/health')
const status = await response.json()
console.log(status)
```

### 获取历史记录

```javascript
const response = await fetch('/api/tts/history?page=1&limit=10')
const result = await response.json()
console.log('历史记录:', result.data.records)
```

## 🎯 主要功能

### 前端功能
- ✅ 文字输入和TTS转换
- ✅ 音频播放和下载
- ✅ 模型选择
- ✅ 历史记录查看
- ✅ 响应式设计

### 后端功能
- ✅ TTS API服务
- ✅ 多模型支持
- ✅ 历史记录管理
- ✅ 文件管理
- ✅ 日志记录
- ✅ 健康检查

## 🔍 监控和日志

### 健康检查
```bash
curl http://localhost:5000/api/system/health
```

### 查看日志
```bash
# 实时日志
tail -f backend/logs/tts_service.log

# 错误日志
grep "ERROR" backend/logs/tts_service.log
```

### 系统统计
```bash
curl http://localhost:5000/api/system/stats
```

## 🚀 生产部署

### 使用Docker

```bash
# 构建和启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 使用Nginx + Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动后端服务
gunicorn -c gunicorn.conf.py run:app

# 配置Nginx代理
# 参考 docs/deployment-guide.md
```

## 📚 文档

- [开发指南](docs/development-guide.md) - 详细的开发文档和架构说明
- [API文档](docs/api-documentation.md) - 完整的API接口文档
- [部署指南](docs/deployment-guide.md) - 生产环境部署指南

## 🤝 贡献

欢迎提交Issue和Pull Request！

### 开发流程

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- Python代码遵循PEP 8规范
- JavaScript代码使用ES6+语法
- 提交信息使用英文，格式清晰
- 添加必要的注释和文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) - 优秀的语音处理框架
- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架
- [React](https://reactjs.org/) - 现代化前端框架
- [Ant Design](https://ant.design/) - 企业级UI组件库

## 📞 支持

如果您在使用过程中遇到问题，可以通过以下方式获取帮助：

- 📋 [提交Issue](../../issues)
- 📧 发送邮件到: support@example.com
- 💬 加入讨论群: [链接]

---

**⭐ 如果这个项目对您有帮助，请给我们一个Star！**