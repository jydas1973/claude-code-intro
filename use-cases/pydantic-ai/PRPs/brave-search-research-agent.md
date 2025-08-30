---
name: "Brave Search Research Agent PRP"
description: "Complete implementation plan for building a PydanticAI research agent with Brave Search API integration"
---

## Purpose

Build a simple but production-ready research agent using PydanticAI that can research topics with the Brave Search API. The agent will provide structured research capabilities with proper error handling, rate limiting, and security practices.

## Core Principles

1. **PydanticAI Best Practices**: Deep integration with PydanticAI patterns for agent creation, tools, and structured outputs
2. **Production Ready**: Include security, testing, and monitoring for production deployments
3. **Type Safety First**: Leverage PydanticAI's type-safe design and Pydantic validation throughout
4. **Context Engineering Integration**: Apply proven context engineering workflows to AI agent development
5. **Comprehensive Testing**: Use TestModel and FunctionModel for thorough agent validation

## ⚠️ Implementation Guidelines: Don't Over-Engineer

**IMPORTANT**: Keep your agent implementation focused and practical. Don't build unnecessary complexity.

### What NOT to do:
- ❌ **Don't create dozens of tools** - Build only the essential research tools needed
- ❌ **Don't over-complicate dependencies** - Keep dependency injection simple and focused
- ❌ **Don't add unnecessary abstractions** - Follow main_agent_reference patterns directly
- ❌ **Don't build complex workflows** unless specifically required
- ❌ **Don't add structured output** unless validation is specifically needed (default to string)
- ❌ **Don't build in the examples/ folder**

### What TO do:
- ✅ **Start simple** - Build the minimum viable research agent that meets requirements
- ✅ **Add tools incrementally** - Implement only what the agent needs to function
- ✅ **Follow main_agent_reference** - Use proven patterns, don't reinvent
- ✅ **Use string output by default** - Only add result_type when validation is required
- ✅ **Test early and often** - Use TestModel to validate as you build

### Key Question:
**"Does this agent really need this feature to accomplish research with Brave Search?"**

If the answer is no, don't build it. Keep it simple, focused, and functional.

---

## Goal

Create a PydanticAI research agent that can perform web research using the Brave Search API with:
- Natural language research queries
- Structured search result processing
- Rate limiting and error handling
- Security best practices for API key management
- Comprehensive testing with TestModel patterns

## Why

This agent solves the need for AI-powered research capabilities that:
- Provide access to current, real-time web information
- Maintain privacy through Brave's independent search index
- Integrate seamlessly with PydanticAI's type-safe architecture
- Enable structured data processing and analysis
- Serve as a foundation for more complex research workflows

## What

### Agent Type Classification
- [x] **Tool-Enabled Agent**: Agent with external tool integration capabilities
- [ ] **Chat Agent**: Conversational interface with memory and context
- [ ] **Workflow Agent**: Multi-step task processing and orchestration
- [ ] **Structured Output Agent**: Complex data validation and formatting

### Model Provider Requirements
- [x] **OpenAI**: `openai:gpt-4o` or `openai:gpt-4o-mini`
- [x] **Anthropic**: `anthropic:claude-3-5-sonnet-20241022` or `anthropic:claude-3-5-haiku-20241022`
- [x] **Google**: `gemini-1.5-flash` or `gemini-1.5-pro`
- [x] **Fallback Strategy**: Multiple provider support with automatic failover

### External Integrations
- [x] Brave Search API integration for web research
- [x] HTTP client with async support (httpx)
- [x] Rate limiting implementation (1 query/second for free tier)
- [ ] Database connections (PostgreSQL, MongoDB, etc.)
- [ ] File system operations
- [ ] Real-time data sources

### Success Criteria
- [x] Agent successfully handles research queries with Brave Search
- [x] All tools work correctly with proper error handling and rate limiting
- [x] String outputs provide clear, well-organized research summaries
- [x] Comprehensive test coverage with TestModel and FunctionModel
- [x] Security measures implemented (API keys, input validation, rate limiting)
- [x] Performance meets requirements (1 query/second rate limit compliance)

## All Needed Context

### PydanticAI Documentation & Research

```yaml
# ESSENTIAL PYDANTIC AI DOCUMENTATION - Researched and documented
- url: https://ai.pydantic.dev/
  research_findings: |
    - Model-agnostic framework supporting OpenAI, Anthropic, Google, etc.
    - Built by Pydantic team with "FastAPI feeling for GenAI development"
    - Emphasizes type-safety and Python-centric design
    - Agent configuration: Agent('openai:gpt-4o', deps_type=SupportDependencies, system_prompt='...')
    - Supports dependency injection, tool registration, structured output validation
    - Seamless integration with Pydantic Logfire for monitoring

- url: https://ai.pydantic.dev/agents/
  research_findings: |
    - Agents are flexible, type-safe containers for LLM interactions
    - Multiple execution modes: run(), run_sync(), run_stream(), iter()
    - Dependency management with type-safe dependency injection
    - Static and dynamic system prompts
    - Usage limits and retry mechanisms for self-correction
    - Generic typing for dependencies and output types

- url: https://ai.pydantic.dev/tools/
  research_findings: |
    - Two decorators: @agent.tool (with context) and @agent.tool_plain (no context)
    - RunContext provides access to agent-level dependencies
    - Automatic parameter validation using Pydantic
    - Tools can return structured data, images, documents
    - Concurrent tool execution supported
    - Docstring descriptions automatically extracted for schemas

- url: https://ai.pydantic.dev/testing/
  research_findings: |
    - Use pytest as test harness with inline-snapshot and dirty-equals
    - TestModel generates valid structured data based on tool schemas
    - FunctionModel allows custom function calls to simulate model behavior
    - Agent.override() to replace models, dependencies, or toolsets
    - Block real model requests with ALLOW_MODEL_REQUESTS=False
    - Use capture_run_messages() to inspect agent-model interactions

- url: https://ai.pydantic.dev/models/
  research_findings: |
    - Supports OpenAI, Anthropic, Google, Groq, Mistral, Cohere, Bedrock, HuggingFace
    - FallbackModel for multiple model attempt strategies
    - Provider handles authentication and connections
    - Configure via environment variables (base_url, api_key)
    - Custom model support through base Model abstract class

# Codebase examples research
- path: examples/main_agent_reference/
  research_findings: |
    - Complete production-ready pattern: settings.py, providers.py, tools.py, research_agent.py
    - Environment-based configuration with pydantic-settings and load_dotenv()
    - get_llm_model() function for provider abstraction
    - Dataclass dependencies with proper typing
    - Tool implementation with search_web_tool() pattern already exists
    - Error handling and logging throughout

- path: examples/testing_examples/
  research_findings: |
    - Comprehensive testing patterns with TestModel and FunctionModel
    - Agent.override() for test isolation
    - Mock dependencies with AsyncMock and Mock
    - Tool validation and error handling tests
    - Pytest fixtures and async testing patterns

# Brave Search API research
- url: https://brave.com/search/api/
  research_findings: |
    - Authentication: X-Subscription-Token header
    - Free tier: 1 query/second, 5000 queries/month
    - Response format: JSON with web results, snippets, URLs
    - Rate limiting: 429 status code when exceeded
    - Independent index with 30+ billion pages, real-time updates
    - Example: requests.get("https://api.search.brave.com/res/v1/web/search", 
      headers={"X-Subscription-Token": "<KEY>"}, params={"q": "query", "count": 20})

# Rate limiting and async patterns research
integration_patterns:
  async_httpx: |
    - Use httpx.AsyncClient for async requests
    - Implement rate limiting with aiolimiter or aiometer
    - Exponential backoff for retry logic on 429 errors
    - Monitor rate limit headers (X-RateLimit-Remaining, X-RateLimit-Reset)
    
  security: |
    - Store API keys in environment variables
    - Use pydantic-settings with .env files
    - Never commit keys to version control
    - Validate all inputs and sanitize outputs
```

### Agent Architecture Research

```yaml
# PydanticAI Architecture Patterns (following main_agent_reference)
agent_structure:
  configuration:
    - settings.py: Environment-based config with pydantic-settings and load_dotenv()
    - providers.py: get_llm_model() abstraction for multiple providers
    - Never hardcode model strings - use environment variables
  
  agent_definition:
    - Default to string output (no result_type unless structured output needed)
    - System prompt as string constant focused on research capabilities
    - Dataclass dependencies for Brave API key and HTTP client
    - Use get_llm_model() from providers.py
  
  tool_integration:
    - @agent.tool for context-aware search tool with RunContext[DepsType]
    - Pure function implementation that can be tested independently
    - Proper error handling for API failures and rate limits
    - Dependency injection for API key and HTTP client through RunContext.deps
  
  testing_strategy:
    - TestModel for rapid development validation without API calls
    - FunctionModel for custom search response simulation
    - Agent.override() for test isolation
    - Mock HTTP client and API responses for comprehensive testing
```

### Security and Production Considerations

```yaml
# PydanticAI Security Patterns (researched and documented)
security_requirements:
  api_management:
    environment_variables: ["LLM_API_KEY", "BRAVE_API_KEY"]
    secure_storage: "Use .env files, never commit keys"
    configuration: "pydantic-settings with load_dotenv() pattern"
  
  input_validation:
    sanitization: "Validate search queries with type hints and Pydantic"
    rate_limiting: "Implement 1 query/second limit for Brave API free tier"
    error_handling: "Graceful degradation on API failures"
  
  output_security:
    data_filtering: "Return only public search results, no sensitive data"
    content_validation: "Validate search result format and structure"
    logging_safety: "Log search activities without exposing API keys"

# Production patterns from main_agent_reference
production_patterns:
  error_handling:
    - Try/except blocks in all tools
    - Specific exception types for different failure modes
    - Graceful fallbacks when search API is unavailable
  
  logging:
    - Python logging module with structured logging
    - Log search queries, results count, and errors
    - Performance monitoring for API response times
  
  monitoring:
    - Track API usage and rate limit compliance
    - Monitor search success rates and error patterns
    - Integration with Pydantic Logfire for agent execution monitoring
```

### Common PydanticAI Gotchas (researched and documented)

```yaml
# Agent-specific gotchas researched and solutions documented
implementation_gotchas:
  async_patterns:
    issue: "Mixing sync and async agent calls inconsistently"
    research_findings: "PydanticAI supports both run() async and run_sync() patterns"
    solution: "Use async throughout for HTTP client, provide sync wrapper if needed"
  
  model_limits:
    issue: "Different models have different capabilities and token limits"
    research_findings: "OpenAI GPT-4o has 128k context, Claude has 200k, Gemini has 1M+"
    solution: "Design system prompts to work within common limits, use fallback models"
  
  dependency_complexity:
    issue: "Complex dependency graphs can be hard to debug"
    research_findings: "PydanticAI uses dataclass dependencies with type safety"
    solution: "Keep dependencies simple: API key, HTTP client, optional config only"
  
  tool_error_handling:
    issue: "Tool failures can crash entire agent runs"
    research_findings: "Tools should return error messages as strings rather than raising"
    solution: "Wrap all API calls in try/except, return structured error responses"
  
  rate_limiting:
    issue: "Brave API free tier allows only 1 query/second, exceeding causes 429 errors"
    research_findings: "Use aiolimiter, implement exponential backoff, monitor headers"
    solution: "AsyncLimiter(1, 1) for 1 query/second, retry logic for 429 responses"
```

## Implementation Blueprint

### Technology Research Phase

**RESEARCH COMPLETE ✅** - All necessary research documented above

✅ **PydanticAI Framework Deep Dive:**
- [x] Agent creation patterns and best practices (documented from ai.pydantic.dev)
- [x] Model provider configuration and fallback strategies (OpenAI, Anthropic, Google support)
- [x] Tool integration patterns (@agent.tool with RunContext for dependencies)
- [x] Dependency injection system and type safety (dataclass dependencies)
- [x] Testing strategies with TestModel and FunctionModel (pytest patterns documented)

✅ **Agent Architecture Investigation:**
- [x] Project structure conventions (agent.py, tools.py, models.py, dependencies.py)
- [x] System prompt design (static string focused on research capabilities)
- [x] String output by default (no structured output needed for this agent)
- [x] Async patterns and HTTP client integration (httpx with rate limiting)
- [x] Error handling and retry mechanisms (try/except with structured responses)

✅ **Security and Production Patterns:**
- [x] API key management and secure configuration (pydantic-settings + .env)
- [x] Input validation and rate limiting (1 query/second for Brave API)
- [x] Rate limiting and monitoring strategies (aiolimiter + exponential backoff)
- [x] Logging and observability patterns (Python logging + Pydantic Logfire)
- [x] Deployment and scaling considerations (environment-based configuration)

### Agent Implementation Plan

```yaml
Implementation Task 1 - Agent Architecture Setup:
  CREATE brave_search_agent project structure:
    - settings.py: Environment config with BRAVE_API_KEY and LLM settings
    - providers.py: get_llm_model() following main_agent_reference pattern
    - agent.py: Main agent definition with string output (no result_type)
    - tools.py: Brave Search integration tool with rate limiting
    - dependencies.py: HTTP client and API key dependency dataclass
    - tests/: Comprehensive test suite with TestModel patterns
    - .env.example: Template for environment variables

Implementation Task 2 - Core Agent Development:
  IMPLEMENT agent.py following main_agent_reference patterns:
    - Import get_llm_model() from providers.py for model configuration
    - System prompt focused on research capabilities and source citation
    - BraveSearchDependencies dataclass with API key and HTTP client
    - String output (no result_type) for natural research summaries
    - Error handling and logging throughout

Implementation Task 3 - Brave Search Tool Integration:
  DEVELOP tools.py with production-ready search tool:
    - @agent.tool decorator with RunContext[BraveSearchDependencies]
    - Async HTTP client (httpx) with proper headers and authentication
    - Rate limiting implementation (aiolimiter at 1 query/second)
    - Error handling for 429 rate limits, network errors, API failures
    - Structured response parsing and formatting
    - Retry logic with exponential backoff
    - Input validation and sanitization

Implementation Task 4 - Configuration and Dependencies:
  CREATE settings.py and dependencies.py:
    - pydantic-settings with load_dotenv() for environment variables
    - BraveSearchDependencies dataclass with httpx.AsyncClient
    - API key validation and secure storage patterns
    - Configuration for development/production environments

Implementation Task 5 - Comprehensive Testing:
  IMPLEMENT testing suite following examples/testing_examples:
    - TestModel integration for rapid agent validation
    - FunctionModel tests for custom search behavior simulation
    - Agent.override() patterns for test isolation
    - Mock HTTP client and API responses
    - Rate limiting and error scenario testing
    - Integration tests with real Brave API (optional, for validation)

Implementation Task 6 - Security and Production Setup:
  SETUP security and deployment patterns:
    - .env file management with secure API key storage
    - Input sanitization for search queries
    - Rate limiting compliance with Brave API terms
    - Structured logging without exposing sensitive data
    - Error monitoring and alerting capabilities
```

## Validation Loop

### Level 1: Agent Structure Validation

```bash
# Verify complete agent project structure
find brave_search_agent -name "*.py" | sort
test -f brave_search_agent/agent.py && echo "Agent definition present"
test -f brave_search_agent/tools.py && echo "Tools module present" 
test -f brave_search_agent/settings.py && echo "Settings module present"
test -f brave_search_agent/dependencies.py && echo "Dependencies module present"
test -f brave_search_agent/providers.py && echo "Providers module present"

# Verify proper PydanticAI imports
grep -q "from pydantic_ai import Agent" brave_search_agent/agent.py
grep -q "@agent.tool" brave_search_agent/tools.py  
grep -q "from pydantic_settings import BaseSettings" brave_search_agent/settings.py
grep -q "load_dotenv()" brave_search_agent/settings.py

# Expected: All required files with proper PydanticAI patterns
# If missing: Generate missing components with correct patterns
```

### Level 2: Agent Functionality Validation

```bash
# Test agent can be imported and instantiated
cd brave_search_agent
python -c "
from agent import research_agent
print('Agent created successfully')
print(f'Model: {research_agent.model}')  
print(f'Tools: {len(research_agent.tools)}')
"

# Test with TestModel for validation (no API calls)
python -c "
from pydantic_ai.models.test import TestModel
from agent import research_agent
from dependencies import BraveSearchDependencies
from unittest.mock import Mock

test_model = TestModel()
mock_deps = BraveSearchDependencies(brave_api_key='test', session=Mock())

with research_agent.override(model=test_model):
    result = research_agent.run_sync('Research quantum computing', deps=mock_deps)
    print(f'Agent response type: {type(result.data)}')
    print(f'Response preview: {str(result.data)[:100]}...')
"

# Expected: Agent instantiation works, tools registered, TestModel validation passes
# If failing: Debug agent configuration and tool registration
```

### Level 3: Brave Search API Integration Validation

```bash
# Test HTTP client and rate limiting (without real API calls)
cd brave_search_agent
python -c "
import asyncio
from aiolimiter import AsyncLimiter
from tools import brave_search_tool
from unittest.mock import AsyncMock, Mock

async def test_rate_limiting():
    # Mock HTTP client
    mock_session = AsyncMock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'web': {'results': [{'title': 'Test', 'url': 'http://test.com', 'description': 'Test result'}]}
    }
    mock_session.get.return_value.__aenter__.return_value = mock_response
    
    # Mock context
    mock_ctx = Mock()
    mock_ctx.deps.brave_api_key = 'test_key'
    mock_ctx.deps.session = mock_session
    
    # Test tool call
    result = await brave_search_tool(mock_ctx, 'test query', 5)
    print(f'Tool result type: {type(result)}')
    print(f'Mock API called: {mock_session.get.called}')
    return result

asyncio.run(test_rate_limiting())
"

# Expected: Mock HTTP calls work, rate limiting configured, tool returns structured data
# If failing: Debug HTTP client setup and tool implementation
```

### Level 4: Comprehensive Testing Validation

```bash
# Run complete test suite
cd brave_search_agent
python -m pytest tests/ -v --tb=short

# Test specific agent components
python -m pytest tests/test_agent.py::test_agent_with_test_model -v
python -m pytest tests/test_tools.py::test_brave_search_tool_mocked -v  
python -m pytest tests/test_settings.py::test_environment_loading -v

# Test error handling and edge cases
python -m pytest tests/test_tools.py::test_rate_limit_handling -v
python -m pytest tests/test_tools.py::test_api_error_handling -v

# Expected: All tests pass, comprehensive coverage achieved
# If failing: Fix implementation based on test failures
```

### Level 5: Production Readiness Validation

```bash
# Verify security patterns
cd brave_search_agent
grep -r "BRAVE_API_KEY" . --exclude-dir=tests | grep -v ".py:" # Should not expose keys in code
test -f .env.example && echo "Environment template present"
grep -q "load_dotenv()" settings.py && echo "Environment loading configured"

# Check error handling coverage
grep -r "try:" . --include="*.py" | wc -l  # Should have error handling
grep -r "except" . --include="*.py" | wc -l  # Should have exception handling
grep -r "logger\|logging" . --include="*.py" | wc -l  # Should have logging

# Verify rate limiting implementation
grep -q "AsyncLimiter" tools.py && echo "Rate limiting implemented"
grep -q "429" tools.py && echo "Rate limit error handling present"

# Expected: Security measures in place, error handling comprehensive, logging configured
# If issues: Implement missing security and production patterns
```

## Final Validation Checklist

### Agent Implementation Completeness

- [ ] Complete agent project structure: `agent.py`, `tools.py`, `settings.py`, `dependencies.py`, `providers.py`
- [ ] Agent instantiation with get_llm_model() provider configuration
- [ ] Brave Search tool with @agent.tool decorator and RunContext integration
- [ ] String output format for natural research summaries (no structured output)
- [ ] BraveSearchDependencies with HTTP client and API key injection
- [ ] Comprehensive test suite with TestModel and mock API responses

### PydanticAI Best Practices

- [ ] Type safety throughout with proper type hints and RunContext[DepsType]
- [ ] Security patterns implemented (API keys via environment, input validation, rate limiting)
- [ ] Error handling and retry mechanisms for robust operation (try/except, exponential backoff)
- [ ] Async patterns consistent with httpx.AsyncClient and aiolimiter
- [ ] Documentation and code comments for maintainability

### Brave Search API Integration

- [ ] Authentication with X-Subscription-Token header
- [ ] Rate limiting compliance (1 query/second for free tier)
- [ ] Response parsing and formatting from JSON to readable research summaries
- [ ] Error handling for 429 rate limits, network failures, API errors
- [ ] Input validation and query sanitization

### Production Readiness

- [ ] Environment configuration with .env files and pydantic-settings
- [ ] Logging setup without exposing sensitive data (API keys, personal info)
- [ ] Performance monitoring and error tracking capabilities
- [ ] Deployment readiness with proper configuration management
- [ ] Maintenance and update strategies documented in README

---

## Anti-Patterns to Avoid

### PydanticAI Agent Development

- ❌ Don't skip TestModel validation - always test with TestModel during development
- ❌ Don't hardcode API keys - use environment variables with pydantic-settings
- ❌ Don't ignore async patterns - use async/await consistently with httpx
- ❌ Don't create complex tool chains - keep the search tool focused and simple
- ❌ Don't skip error handling - implement comprehensive retry and fallback mechanisms

### Brave Search API Integration

- ❌ Don't ignore rate limiting - free tier is limited to 1 query/second
- ❌ Don't expose API keys in logs or error messages
- ❌ Don't retry indefinitely on failures - implement exponential backoff with limits
- ❌ Don't parse responses without validation - handle missing fields gracefully

### Agent Architecture

- ❌ Don't use structured output unless needed - default to string for research summaries
- ❌ Don't ignore dependency injection - use RunContext[DepsType] for clean testing
- ❌ Don't skip input validation - sanitize search queries for safety
- ❌ Don't forget tool documentation - include clear docstrings for schema generation

### Security and Production

- ❌ Don't commit .env files - only commit .env.example templates
- ❌ Don't skip input sanitization - validate all user queries
- ❌ Don't ignore monitoring - track API usage and error rates
- ❌ Don't deploy without comprehensive testing - validate with TestModel first

**RESEARCH STATUS: [COMPLETED]** ✅ - Comprehensive PydanticAI and Brave Search API research completed with all patterns, gotchas, and implementation details documented.

---

## PRP Confidence Score: 9/10

**Confidence Assessment:**
- ✅ **Complete research coverage** - Both PydanticAI and Brave Search API thoroughly researched
- ✅ **Existing codebase patterns identified** - main_agent_reference provides complete architecture template  
- ✅ **Security and production considerations documented** - Rate limiting, API key management, error handling
- ✅ **Testing strategy comprehensive** - TestModel, FunctionModel, and mock patterns detailed
- ✅ **Implementation blueprint specific** - Step-by-step tasks with validation loops
- ✅ **Gotchas and anti-patterns documented** - Common issues and solutions identified
- ✅ **Context complete for one-pass implementation** - All necessary information provided

**Remaining risk (1 point deduction):**
- Minor complexity in rate limiting implementation with async patterns
- Brave Search API response format variations may require minor adjustments

This PRP provides comprehensive context for successful one-pass implementation of a production-ready Brave Search research agent using PydanticAI best practices.