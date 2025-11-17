# Contributing to Claude Autonomous Agent

Thank you for your interest in contributing to this experimental AI autonomy project!

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Node version)
- Relevant logs from `data/logs/agent.log`

### Suggesting Features

Feature suggestions are welcome! Please:
- Check existing issues first
- Describe the use case
- Explain why this would be valuable
- Consider how it fits with the project's vision of AI autonomy

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
   ```bash
   cd anthropic-quickstarts/autonomous-agent
   ./scripts/test_tools.sh
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: description of your feature"
   ```
6. **Push and create a pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/Claude-computer-use-from-the-Pi.git
cd Claude-computer-use-from-the-Pi

# Run installation
./install.sh

# Make changes in anthropic-quickstarts/autonomous-agent/
cd anthropic-quickstarts/autonomous-agent

# Test your changes
./scripts/test_tools.sh
```

## Code Style

- **Python**: Follow PEP 8 style guide
- **Bash**: Use shellcheck for scripts
- **Documentation**: Update README.md for significant changes
- **Comments**: Explain "why" not "what"

## Adding New Tools

To add a custom tool for Claude:

1. Create tool file in `src/tools/your_tool.py`:

```python
from claude_agent_sdk import tool

@tool(
    name="your_tool",
    description="Clear description of what this tool does",
    input_schema={
        "type": "object",
        "properties": {
            "param": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param"]
    }
)
async def your_tool(param: str):
    """Implementation of your tool"""
    # Your code here
    return {
        "content": [{
            "type": "text",
            "text": "Result of the operation"
        }]
    }
```

2. Register in `src/autonomous_agent.py`:
```python
from tools.your_tool import your_tool

# Add to tools list in create_mcp_server()
```

3. Add to `config/agent_config.yaml`:
```yaml
tools:
  allowed:
    - mcp__agent_tools__your_tool
```

4. Document in README.md

## Testing

Before submitting a PR:

```bash
# Test all tools work
make test

# Check agent starts successfully
make start
# (Let it run through one check-in, then Ctrl+C)

# Verify dashboard works
make dashboard
# Visit http://localhost:8080

# Check logs for errors
make logs
```

## Documentation

- Update README.md for user-facing changes
- Update QUICKSTART.md if commands change
- Add code comments for complex logic
- Update vision.md if changing project philosophy

## Project Philosophy

When contributing, keep in mind this project's core principles:

- **Autonomy**: Claude should make independent decisions
- **Transparency**: All actions should be logged and observable
- **Safety**: Prevent destructive operations
- **Simplicity**: Make it easy to understand and use
- **Experimentation**: Enable exploring AI capabilities

## Pull Request Process

1. Update documentation for any changed functionality
2. Add tests if introducing new features
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Request review from maintainers

## Questions?

- Check existing documentation
- Look at existing issues
- Create a discussion thread

## Code of Conduct

- Be respectful and constructive
- Focus on the project's goals
- Help others learn and contribute
- Acknowledge that this is experimental research

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping explore the future of AI autonomy!
