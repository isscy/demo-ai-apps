import os
from uuid import uuid4
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from elevenlabs import ElevenLabs
import streamlit as st

# Streamlit 页面基本设置： 设置浏览器标签页标题和图标
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")

# 浏览器sidebar输入 API Keys
st.sidebar.header("🔑 API Keys")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
elevenlabs_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Blog URL Input
url = st.text_input("Enter Blog URL:", "")

# Generate Button
# all() 是 Python 内置函数，判断列表中所有元素是否为真值 （非空字符串为真）
if st.button("🎙️ Generate Podcast", disabled=not all([openai_key, elevenlabs_key, firecrawl_key])):
    if not url.strip():
        st.warning("Please enter a blog URL")
    else:
        with st.spinner("Scraping blog and generating podcast..."):
            try:
                # 把用户输入的 Key 塞进环境变量（很多库会自动读取 os.environ）
                os.environ["OPENAI_API_KEY"] = openai_key
                os.environ["FIRECRAWL_API_KEY"] = firecrawl_key

                # 创建 AI Agent， 使用网页抓取工具，并指定系统提示词（prompt）
                agent = Agent(
                    name="Blog Summarizer",
                    model=OpenAIChat(id="gpt-4o"),
                    tools=[FirecrawlTools()],
                    instructions=[
                        "Scrape the blog URL and create a concise, engaging summary (max 2000 characters) suitable for a podcast.",
                        "The summary should be conversational and capture the main points."
                    ],
                )

                # agent.run()：调用，agno 将会：调用 Firecrawl 工具 → 抓取网页 → 让 GPT-4o 总结 → 返回结果
                response: RunOutput = agent.run(f"Scrape and summarize this blog for a podcast: {url}")
                summary = response.content if hasattr(response, 'content') else str(response)

                if summary:
                    # Initialize ElevenLabs client and generate audio
                    client = ElevenLabs(api_key=elevenlabs_key)

                    # convert() 返回的是生成器（stream 方式），适合大文件
                    audio_generator = client.text_to_speech.convert(
                        text=summary,
                        voice_id="JBFqnCBsd6RMkjVDRZzb",   # 常用男声之一
                        model_id="eleven_multilingual_v2"  # 支持多语言的高质量模型
                    )

                    # 逐块收集 → 合并成完整的 bytes（mp3 格式）
                    audio_chunks = []
                    for chunk in audio_generator:
                        if chunk:
                            audio_chunks.append(chunk)
                    audio_bytes = b"".join(audio_chunks)

                    # 在 Streamlit 显示结果
                    st.success("Podcast generated! 🎧")
                    st.audio(audio_bytes, format="audio/mp3")

                    # Download button
                    st.download_button(
                        "Download Podcast",
                        audio_bytes,
                        "podcast.mp3",
                        "audio/mp3"
                    )

                    # st.expander：可折叠的总结文本展示区
                    with st.expander("📄 Podcast Summary"):
                        st.write(summary)
                else:
                    st.error("Failed to generate summary")

            except Exception as e:
                st.error(f"Error: {e}")