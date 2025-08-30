# Brave Search Research Agent

A production-ready PydanticAI agent for web research using the Brave Search API. Built with simplicity, security, and reliability in mind.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `pydantic-ai` - Core PydanticAI framework
- `httpx` - Async HTTP client for API requests
- `aiolimiter` - Rate limiting (1 query/second for Brave API)
- `pydantic-settings` - Configuration management
- `python-dotenv` - Environment variable loading
- `pytest` & `pytest-asyncio` - Testing framework

### 2. Configure Environment

Copy the environment template and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# REQUIRED: Get from https://brave.com/search/api/
BRAVE_API_KEY=your_brave_api_key_here

# REQUIRED: Get from your LLM provider
LLM_API_KEY=your_llm_api_key_here
LLM_MODEL=gpt-4o
LLM_PROVIDER=openai
```

### 3. Basic Usage

```python
import asyncio
from brave_search_agent.agent import run_research

async def main():
    # Simple research query
    result = await run_research("latest developments in quantum computing")
    print(result)

# Run the research
asyncio.run(main())
```

### 4. Advanced Usage

```python
from brave_search_agent.agent import research_agent
from brave_search_agent.dependencies import BraveSearchDependencies

async def advanced_research():
    # Create dependencies
    deps = await BraveSearchDependencies.create(session_id="my-session")
    
    try:
        # Run research with custom parameters
        result = await research_agent.run(
            "AI safety research 2024",
            deps=deps
        )
        print(f"Research Result: {result.data}")
        
    finally:
        # Always clean up
        await deps.close()

asyncio.run(advanced_research())
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/test_agent.py -v          # Agent functionality tests
pytest tests/test_tools.py -v          # Search tools and rate limiting
pytest tests/test_settings.py -v       # Configuration management
pytest tests/test_dependencies.py -v   # Dependency injection
pytest tests/test_providers.py -v      # Model provider configuration

# Run with coverage (optional)
pytest tests/ --cov=brave_search_agent --cov-report=html
```

## 📖 API Reference

### Core Functions

#### `run_research(query, session_id=None, max_results=10)`
Convenience function for simple research queries.

**Parameters:**
- `query` (str): Research question or topic
- `session_id` (str, optional): Session identifier for tracking
- `max_results` (int): Maximum search results (1-20, default 10)

**Returns:**
- `str`: Formatted research summary with sources

#### `research_agent.run(query, deps=dependencies)`
Direct agent execution with custom dependencies.

**Parameters:**
- `query` (str): Research question or topic  
- `deps` (BraveSearchDependencies): Configured dependencies

**Returns:**
- `RunResult`: Agent result with `.data` containing research summary

### Configuration Classes

#### `Settings`
Environment-based configuration using pydantic-settings.

**Key Fields:**
- `llm_api_key`: LLM provider API key
- `brave_api_key`: Brave Search API key
- `llm_model`: Model name (default: "gpt-4o")
- `llm_provider`: Provider name (default: "openai")

#### `BraveSearchDependencies`
Dependency injection container for agent execution.

**Fields:**
- `brave_api_key`: Brave Search API key
- `session`: HTTP client session
- `session_id`: Optional session identifier

## 🛠️ Architecture

### Design Principles

This agent follows PydanticAI best practices and implements:

- **KISS Principle**: Simple, focused design without over-engineering
- **String Output**: Natural language responses (no unnecessary structured output)  
- **Rate Limiting**: 1 query/second compliance with Brave API free tier
- **Security First**: Environment variables, no hardcoded secrets
- **Test Coverage**: Comprehensive testing with TestModel/FunctionModel patterns

### Project Structure

```
brave_search_agent/
├── agent.py              # 🤖 Main PydanticAI agent definition
├── tools.py              # 🔧 Brave Search tool with rate limiting
├── settings.py           # ⚙️ Environment configuration
├── dependencies.py       # 📦 Dependency injection setup
├── providers.py          # 🔌 LLM model provider abstraction
├── requirements.txt      # 📋 Python dependencies
├── .env.example         # 📝 Environment template
├── .gitignore           # 🚫 Security exclusions
└── tests/               # 🧪 Comprehensive test suite
    ├── test_agent.py
    ├── test_tools.py
    ├── test_settings.py
    ├── test_dependencies.py
    └── test_providers.py
```

### Key Components

#### Agent (`agent.py`)
- PydanticAI agent with focused research system prompt
- Single `search_web` tool using `@agent.tool` decorator
- String output for natural research summaries
- Error handling and dependency injection

#### Tools (`tools.py`)
- `brave_search_tool()`: Standalone search function
- Rate limiting: 1 query/second using `aiolimiter`
- HTTP error handling (429 rate limits, auth errors)
- Response formatting and validation

#### Settings (`settings.py`)
- `pydantic-settings` with `load_dotenv()` integration
- API key validation and environment loading
- Support for multiple LLM providers
- Fallback configuration for testing

#### Dependencies (`dependencies.py`)
- `BraveSearchDependencies` dataclass
- HTTP client configuration with proper timeouts
- Async context management and cleanup
- Session isolation for concurrent usage

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BRAVE_API_KEY` | ✅ Yes | - | Brave Search API key |
| `LLM_API_KEY` | ✅ Yes | - | LLM provider API key |
| `LLM_MODEL` | No | `gpt-4o` | Model name |
| `LLM_PROVIDER` | No | `openai` | Provider name |
| `LLM_BASE_URL` | No | `https://api.openai.com/v1` | API endpoint |
| `APP_ENV` | No | `development` | Environment |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `DEBUG` | No | `false` | Debug mode |

### LLM Provider Examples

#### OpenAI (Default)
```env
LLM_API_KEY=sk-your-openai-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
LLM_BASE_URL=https://api.openai.com/v1
```

#### Anthropic Claude
```env
LLM_API_KEY=your-anthropic-key-here
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_BASE_URL=https://api.anthropic.com
```

#### Google Gemini
```env
LLM_API_KEY=your-google-api-key-here
LLM_PROVIDER=google
LLM_MODEL=gemini-1.5-flash
LLM_BASE_URL=https://generativelanguage.googleapis.com
```

## 🔒 Security

### Best Practices Implemented

- ✅ **Environment Variables**: All sensitive data in `.env` files
- ✅ **Git Exclusion**: `.gitignore` prevents committing secrets
- ✅ **No Hardcoded Keys**: Code contains no embedded secrets
- ✅ **Input Validation**: All search queries are validated and sanitized
- ✅ **Rate Limiting**: API quota compliance built-in
- ✅ **Error Handling**: Sensitive data not exposed in error messages

### API Key Management

1. **Get Brave Search API Key**: Visit [brave.com/search/api](https://brave.com/search/api/)
2. **Get LLM API Key**: From your chosen provider (OpenAI, Anthropic, Google)
3. **Store Securely**: Add to `.env` file (never commit to git)
4. **Validate**: Agent will validate keys on startup

## 📊 Rate Limits & Usage

### Brave Search API
- **Free Tier**: 1 query/second, 5000 queries/month
- **Implementation**: Built-in rate limiting with `aiolimiter`
- **Error Handling**: Automatic retry on 429 responses
- **Monitoring**: Usage tracking and quota management

### LLM Provider Limits
- **Varies by Provider**: Check your provider's documentation
- **Fallback Support**: Multiple model providers supported
- **Token Management**: Efficient prompting to minimize usage

## 🐛 Troubleshooting

### Common Issues

#### "No module named 'pydantic_ai'"
```bash
pip install -r requirements.txt
```

#### "API key cannot be empty"
Check your `.env` file contains:
```env
BRAVE_API_KEY=your_actual_key_here
LLM_API_KEY=your_actual_key_here
```

#### "Rate limit exceeded"
The agent includes built-in rate limiting, but if you hit quota:
- Check your Brave API usage at [brave.com/search/api](https://brave.com/search/api/)
- Consider upgrading to paid tier for higher limits

#### "Invalid Brave API key"
- Verify your API key at [brave.com/search/api](https://brave.com/search/api/)
- Ensure no extra spaces or characters in `.env` file

### Debug Mode

Enable debug logging:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

### Test Validation

Run the validation script:
```bash
python final_validation.py
```

## 🤝 Contributing

### Development Setup

1. Clone and install dependencies:
```bash
git clone <repository>
cd brave_search_agent
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Add your API keys to .env
```

3. Run tests:
```bash
pytest tests/ -v
```

### Code Standards

- Follow PEP 8 style guidelines  
- Use type hints throughout
- Add docstrings for public functions
- Include tests for new functionality
- Update README for API changes

### Testing Patterns

This project uses PydanticAI testing best practices:

- **TestModel**: For rapid development without API calls
- **FunctionModel**: For custom response simulation
- **Agent.override()**: For test isolation  
- **Mock Dependencies**: For unit testing
- **Async Testing**: With pytest-asyncio

## 📄 License

This project is part of the PydanticAI examples and follows the same licensing terms.

## 🙏 Acknowledgments

- Built with [PydanticAI](https://ai.pydantic.dev/) framework
- Uses [Brave Search API](https://brave.com/search/api/) for web research
- Follows patterns from PydanticAI official examples
- Implements security best practices from the PydanticAI community

---

**Ready to research?** Start with the Quick Start guide above! 🚀