

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









