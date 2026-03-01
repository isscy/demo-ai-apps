

## 2_demo_app
特色AI项目
### 01_blog_to_podcast_agent
1. 技术选型
- agno：ai agent框架
- 基于Streamlit, 将任意博客文章快速转换成播客音频
- OpenAI GPT-4 模型进行内容总结
-  Firecrawl 负责抓取博客正文
- ElevenLabs API 负责生成真人般的语音播客
2. 所需 API 密钥

- OpenAI API Key：在 OpenAI 官网注册并获取
- ElevenLabs API Key：在 ElevenLabs 官网注册并获取（语音合成服务）
- Firecrawl API Key：在 Firecrawl 官网注册并获取（网页抓取服务）

3. 安装依赖：pip install -r requirements.txt
4. 启动 Streamlit 应用： streamlit run blog_to_podcast_agent.py
5. 在浏览器打开的应用界面中操作：
- 在左侧侧边栏输入你的 OpenAI、ElevenLabs 和 Firecrawl API 密钥
- 在主界面输入想要转换的博客文章 URL
- 点击 “🎙️ 生成播客” 按钮
- 等待处理完成后，即可在线播放生成的播客音频，或下载 mp3 文件

### 02_breakup_recovery_multi_agent
1. 主要功能
- Multi-Agent
- 支持上传聊天记录截图
- 并行执行：多个智能体以协调模式（coordination mode）同时处理输入
2. 技术选型
- agno：ai agent框架
- Streamlit：纯 Python Web 框架
- PIL：图像处理 用于显示上传的截图
- OpenAI GPT-4 模型进行内容总结
- Google Gemini Vision：文本提取、分析 直接分析聊天截图中的内容
- Streamlit 的 st.session_state 安全存储 Gemini API Key（无需 .env 文件）


### 03_Data Analysis Agent
1. 主要功能
- 轻松分析自己的数据文件（CSV、Excel）
- AI 自动转换成精确 SQL 查询
2. 核心业务逻辑：
- 用户上传 CSV/Excel → 预处理 + 存成临时 CSV → 用 DuckDB 加载成表 → 用 gpt-4o + Agno Agent 把自然语言问题转成 SQL → 执行查询 → 返回结果
3. 技术选型
- DuckDB  高效的内存数据库
- pandas  数据处理：csv / EXCEL 类型转换 数据清洗


### 04_medical_imaging_agent
1. 主要功能
- 对各种医学影像进行 AI 辅助分析轻松分析自己的数据文件（CSV、Excel）
- 影像类型识别：自动判断是 X光片、MRI、CT扫描、超声等哪一种模态
2. 核心业务逻辑：
- 用户上传医学影像 → 判断类型 + 判断部位 → 找出异常 + 给出可能的诊断 → 大白话解释 → 搜索文献
3. 技术选型
- PIL  Python Imaging Library
- duckduckgo  上网搜资源 的工具

