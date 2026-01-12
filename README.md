
## course 
### 01_basic_agent
1. 安装依赖：pip install strands-agents
2. 在根目录的.env文件中环境变量：
   - 注册：https://tokenfactory.nebius.com/
   - NEBIUS_API_KEY=v1.XXXXXXXXXXXX
3. 运行示例：python main.py

### 02_session_management
1. 安装依赖：在course\02_session_management目录下执行  pip install -e .

### 04_mcp_agent
1. 安装依赖：在course\04_mcp_agent目录下执行  uv sync
2. 在根目录的.env文件中环境变量：
   - 注册：https://dashboard.exa.ai/api-keys
   - EXA_API_KEY=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
3. 执行：
   - python main.py
   - uv run multiple_mcp.py
3. 尝试手动排查的思路
   - 命令行执行：npx -y mcp-remote "https://mcp.exa.ai/mcp?exaApiKey=我的真实key" 

### 05_human_in_the_loop_agent
1. 安装依赖： 在course\05_human_in_the_loop_agent目录下执行  uv sync
2. 执行： uv run main.py
3. 预期输出：俩个交互场景
   - 场景1：Approval Request：Agent 请求格式化硬盘的许可
   - 场景2：Task Completion：Agent 完成任务并将控制权交还给您