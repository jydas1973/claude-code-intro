# Code Conventions and Style Guidelines

## General Principles
From CLAUDE.md, this project follows:

### Core Philosophy
- **KISS (Keep It Simple, Stupid)** - Choose straightforward solutions
- **YAGNI (You Aren't Gonna Need It)** - Implement only when needed
- **Dependency Inversion** - Depend on abstractions
- **Open/Closed Principle** - Open for extension, closed for modification
- **Single Responsibility** - Each component has one clear purpose
- **Fail Fast** - Check for errors early

## File Structure Guidelines
- **Files**: Never exceed 500 lines of code
- **Functions**: Under 50 lines with single responsibility
- **Classes**: Under 100 lines representing single concept
- **Line Length**: Max 100 characters
- **Organization**: Group by feature/responsibility

## Python-Specific (from CLAUDE.md)
- **Style**: Follow PEP8 with 100 character line length
- **Strings**: Use double quotes
- **Type Hints**: Always use for function signatures and class attributes
- **Formatter**: Use `ruff format`
- **Validation**: Use `pydantic` v2
- **Docstrings**: Google-style for all public functions/classes

## Naming Conventions
- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`
- **Type Aliases**: `PascalCase`
- **Enum Values**: `UPPER_SNAKE_CASE`

## Documentation Standards
- Every module should have a docstring explaining purpose
- Public functions must have complete docstrings
- Complex logic should have inline comments with `# Reason:` prefix
- Keep README.md updated with setup instructions and examples
- Maintain CHANGELOG.md for version history

## Search Command Requirements (CRITICAL)
- **ALWAYS use `rg` (ripgrep) instead of `grep`**
- **Use `rg --files | rg pattern` instead of `find -name`**
- This is enforced for better performance and features