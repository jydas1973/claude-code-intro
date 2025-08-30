# Task Completion Workflow

## Standard Workflow for Issues/Features
1. **Understand the Problem**
   - Use `gh issue view [number]` to get issue details
   - Analyze the problem described in the issue
   
2. **Search and Analyze Codebase**
   - Use `rg` for searching (not grep/find)
   - Search for relevant files and patterns
   - Understand existing code structure and conventions

3. **Implement Changes**
   - Follow project conventions from CLAUDE.md
   - Keep changes focused and minimal
   - Use existing patterns and libraries

4. **Testing and Validation**
   - For this documentation project: Verify examples work
   - Check that documentation is accurate and complete
   - Ensure no broken links or references

5. **Code Quality Checks**
   - Since this is primarily documentation, focus on:
     - Markdown formatting consistency
     - Link validity
     - Example accuracy
     - File structure clarity

6. **Git Workflow**
   - Create descriptive commit messages (NO Claude Code references)
   - Follow conventional commit format: `<type>(<scope>): <subject>`
   - Types: feat, fix, docs, style, refactor, test, chore

7. **Pull Request Creation**
   - Use `gh pr create` with descriptive title and body
   - Include summary of changes
   - Reference the issue being fixed

## Special Considerations for This Project
- Primary focus is documentation quality and accuracy
- Examples should be runnable and demonstrate concepts clearly  
- Maintain consistency with existing guide structure
- Ensure all Claude Code features are properly documented