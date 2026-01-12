# `multiple_mcp.py` 代码详细解析

## 1. 导入模块部分

```python
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models.litellm import LiteLLMModel
from strands.tools.mcp import MCPClient
import os
from dotenv import load_dotenv
```

### 语法解析：
- `from ... import ...`：从指定模块导入特定类/函数，避免导入整个模块
- `import os`：导入Python标准库的os模块，用于操作系统相关功能

### 库的解释：
- **mcp**：Model Context Protocol库，用于与外部服务进行通信的协议
  - `stdio_client`：创建标准输入输出客户端，用于与MCP服务器通信
  - `StdioServerParameters`：定义MCP服务器参数的类
- **strands**：一个AI代理框架
  - `Agent`：创建AI代理的核心类
  - `strands.models.litellm`：集成LiteLLM模型的模块
    - `LiteLLMModel`：用于调用各种LLM模型的封装类
  - `strands.tools.mcp`：MCP工具模块
    - `MCPClient`：管理MCP客户端连接的类
- **dotenv**：用于从.env文件加载环境变量的库
  - `load_dotenv`：加载.env文件中的环境变量到系统环境

## 2. 加载环境变量

```python
load_dotenv()
```

### 语法解析：
- 函数调用：执行load_dotenv函数，无参数

### 业务逻辑：
- 从项目根目录或当前目录的.env文件中加载环境变量
- 这一步必须在使用环境变量之前执行

## 3. API密钥验证

```python
# Validate required API keys
nebius_api_key = os.getenv("NEBIUS_API_KEY")
ex_api_key = os.getenv("EXA_API_KEY")
if not nebius_api_key:
    raise ValueError("NEBIUS_API_KEY environment variable is required")
if not exa_api_key:
    raise ValueError("EXA_API_KEY environment variable is required")
```

### 语法解析：
- `os.getenv("KEY_NAME")`：从环境变量中获取指定键的值，不存在则返回None
- `if not variable:`：检查变量是否为空值
- `raise ValueError("message")`：抛出值错误异常，中断程序执行

### 业务逻辑：
- 从环境变量中获取两个必要的API密钥
- **NEBIUS_API_KEY**：用于访问Nebius平台上的DeepSeek模型
- **EXA_API_KEY**：用于访问Exa AI的网络搜索服务
- 如果任何一个密钥缺失，抛出异常并终止程序，确保后续操作有必要的认证信息

## 4. 语言模型配置

```python
# Configure the language model
model = LiteLLMModel(
    client_args={"api_key": nebius_api_key},
    model_id="nebius/deepseek-ai/DeepSeek-V3-0324",
)
```

### 语法解析：
- 类实例化：创建LiteLLMModel类的实例
- 关键字参数：使用key=value形式传递参数
- 字典字面量：`{"api_key": nebius_api_key}` 创建包含API密钥的字典

### 业务逻辑：
- 配置用于AI代理的语言模型
- **client_args**：传递给底层LLM客户端的参数，这里包含Nebius API密钥
- **model_id**：指定要使用的具体模型，这里是Nebius平台上的DeepSeek-V3-0324模型
- 这个模型将用于处理用户查询和生成响应

## 5. Exa AI网络搜索MCP客户端配置

```python
# Set up the Exa AI web search MCP client
web_search_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "mcp-remote",
                f"https://mcp.exa.ai/mcp?exaApiKey={exa_api_key}"
            ]
        )
    )
)
```

### 语法解析：
- **lambda函数**：`lambda: stdio_client(...)` 创建一个匿名函数，不接受参数，返回stdio_client实例
- **f-string**：`f"https://mcp.exa.ai/mcp?exaApiKey={exa_api_key}"` 用于字符串插值
- 嵌套函数调用：MCPClient接受一个返回客户端的可调用对象

### 业务逻辑：
- 创建连接到Exa AI网络搜索服务的MCP客户端
- **MCPClient**：管理MCP连接的高级客户端
- **stdio_client**：创建标准输入输出连接
- **StdioServerParameters**：配置MCP服务器参数
  - **command="npx"**：使用npx命令执行MCP服务器
  - **args**：npx的参数
    - `-y`：自动确认所有提示
    - `mcp-remote`：MCP远程客户端包
    - `https://mcp.exa.ai/mcp?exaApiKey={exa_api_key}`：Exa AI MCP服务器地址，包含API密钥

## 6. Airbnb MCP客户端配置

```python
# Set up the Airbnb MCP client
# Set up the Airbnb MCP client
airbnb_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="npx",
            args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
        )
    )
)
```

### 语法解析：
- 与Exa AI客户端配置类似，使用相同的嵌套结构
- 注意这里有重复的注释行（可能是代码编辑时的错误）

### 业务逻辑：
- 创建连接到Airbnb服务的MCP客户端
- **command="npx"**：同样使用npx命令
- **args**：
  - `-y`：自动确认所有提示
  - `@openbnb/mcp-server-airbnb`：Airbnb MCP服务器包
  - `--ignore-robots-txt`：忽略robots.txt文件的限制

## 7. 上下文管理器使用

```python
# Use both servers together and create agent
with web_search_mcp_client, airbnb_mcp_client:
    # Combine tools from both servers
    web_search_tools = web_search_mcp_client.list_tools_sync()
    airbnb_tools = airbnb_mcp_client.list_tools_sync()
    all_tools = web_search_tools + airbnb_tools
```

### 语法解析：
- **with语句**：上下文管理器，用于自动管理资源的获取和释放
- **多个上下文管理器**：Python 3.10+支持使用逗号分隔多个上下文管理器
- **list_tools_sync()**：同步获取MCP服务器提供的工具列表
- **列表合并**：`web_search_tools + airbnb_tools` 将两个列表合并

### 业务逻辑：
- 同时启动两个MCP客户端连接
- 从Exa AI客户端获取网络搜索工具
- 从Airbnb客户端获取住宿搜索工具
- 将两个工具列表合并，供后续代理使用
- 上下文管理器确保在代码块结束时自动关闭MCP连接

## 8. 工具列表打印

```python
print(f"Loaded {len(web_search_tools)} web search tools")
print(f"Loaded {len(airbnb_tools)} Airbnb tools")
print(f"Total tools available: {len(all_tools)}")
```

### 语法解析：
- **f-string**：用于字符串插值，包含变量和表达式
- **len()**：获取列表的长度

### 业务逻辑：
- 打印已加载的工具数量，用于调试和信息展示
- 显示从每个MCP服务器获取的工具数量
- 显示合并后的总工具数量

## 9. AI代理创建

```python
# Create agent with all tools from both servers
agent = Agent(
    tools=all_tools,
    model=model,
    system_prompt=(
        "You are a helpful travel assistant with access to both web search "
        "and accommodation search capabilities. Use the appropriate tools "
        "to help users find information and plan their travels."
    ),
)
```

### 语法解析：
- **多行字符串**：使用括号和换行创建多行字符串
- **Agent类实例化**：创建AI代理的核心对象

### 业务逻辑：
- 创建一个集成了所有工具的AI代理
- **tools=all_tools**：将合并后的工具列表传递给代理
- **model=model**：使用之前配置的DeepSeek语言模型
- **system_prompt**：定义代理的角色和行为准则
  - 指定代理是旅行助手
  - 说明代理有网络搜索和住宿搜索能力
  - 指导代理使用适当的工具

## 10. 第一个用户查询

```python
# Query the agent
user_query = "What's the fastest way to get to Barcelona from London?"
print(f"\n--- Querying with Multiple MCP Servers ---")
print(f"User Query: {user_query}\n")

response = agent(user_query)

print("--- Agent Response ---")
print(response)
```

### 语法解析：
- **代理调用**：`agent(user_query)` 直接调用代理对象，将查询作为参数
- 字符串格式化：使用\n创建换行，---作为分隔线

### 业务逻辑：
- 定义第一个用户查询：从伦敦到巴塞罗那的最快方式
- 打印查询信息
- 向代理发送查询并获取响应
- 打印代理的响应
- 这个查询会触发代理使用网络搜索工具获取相关信息

## 11. 第二个用户查询

```python
user_query_2 = "Find rooms in Barcelona for 2 people for 2 nights?"
print(f"\n--- Querying with Multiple MCP Servers ---")
print(f"User Query: {user_query_2}\n")

response = agent(user_query_2)

print("--- Agent Response ---")
print(response)
```

### 语法解析：
- 与第一个查询的结构完全相同

### 业务逻辑：
- 定义第二个用户查询：在巴塞罗那找2人住2晚的房间
- 打印查询信息
- 向代理发送查询并获取响应
- 打印代理的响应
- 这个查询会触发代理使用Airbnb工具搜索住宿信息

## 整体业务流程

1. **初始化阶段**：
   - 加载环境变量
   - 验证API密钥
   - 配置语言模型

2. **MCP客户端设置**：
   - 创建Exa AI网络搜索MCP客户端
   - 创建Airbnb住宿搜索MCP客户端

3. **代理创建与工具集成**：
   - 启动MCP客户端连接
   - 获取所有可用工具
   - 创建集成这些工具的AI代理

4. **用户交互**：
   - 接收用户查询
   - 代理根据查询选择合适的工具
   - 工具执行并返回结果
   - 代理整合结果并生成响应
   - 返回响应给用户

## 关键技术点

1. **MCP (Model Context Protocol)**：
   - 用于连接AI模型和外部工具的协议
   - 允许AI模型调用外部服务的工具

2. **stdio_client**：
   - 通过标准输入输出与MCP服务器通信
   - 支持通过命令行工具启动MCP服务器

3. **npx**：
   - Node.js的包执行工具
   - 用于临时安装并执行npm包

4. **strands代理框架**：
   - 提供创建AI代理的高级抽象
   - 支持集成多种工具和模型

5. **LiteLLM**：
   - 统一的LLM调用接口
   - 支持多种LLM模型提供商

## 潜在问题与注意事项

1. **Node.js依赖**：
   - 代码使用npx命令，需要系统安装Node.js
   - 如果没有安装Node.js，会导致MCP客户端初始化失败

2. **API密钥**：
   - 需要有效的NEBIUS_API_KEY和EXA_API_KEY
   - 密钥错误会导致认证失败

3. **网络连接**：
   - 需要稳定的网络连接来访问MCP服务器
   - 网络问题会导致连接关闭错误

4. **工具可用性**：
   - MCP服务器可能会更改或移除工具
   - 需要确保MCP服务器版本兼容性

## 总结

`multiple_mcp.py` 展示了如何使用 strands 和 mcp 库创建一个集成多个外部服务的AI代理。通过配置两个MCP客户端，代理可以同时使用Exa AI的网络搜索和Airbnb的住宿搜索功能，为用户提供全面的旅行信息服务。代码结构清晰，使用了现代Python语法和最佳实践，包括上下文管理器、环境变量管理和错误处理。