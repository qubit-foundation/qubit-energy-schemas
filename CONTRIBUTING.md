# Contributing to Qubit Energy Schemas

Thank you for your interest in contributing to the Qubit Energy Schemas project! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept responsibility for mistakes

## 🚀 Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/qubit-energy-schemas.git
   cd qubit-energy-schemas
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Types of Contributions

### Adding New Schemas

1. **Discuss First**: Open an issue to discuss the new schema before implementation
2. **Follow Conventions**: Read [docs/schema-conventions.md](docs/schema-conventions.md)
3. **Include**:
   - Schema file in `schemas/v0.1/`
   - Example in `examples/`
   - Tests in validation script
   - Documentation updates

### Improving Existing Schemas

1. **Backward Compatibility**: Don't break existing implementations
2. **Versioning**: Major changes require version bump discussion
3. **Testing**: Update examples and tests accordingly

### Documentation

- Fix typos and clarify explanations
- Add real-world usage examples
- Improve API integration guides
- Translate documentation (create issue first)

### Bug Fixes

1. **Reproduce**: Provide steps to reproduce the issue
2. **Test**: Include test case that catches the bug
3. **Fix**: Apply minimal change to resolve issue

## 🔧 Development Workflow

### 1. Make Your Changes

Follow our schema conventions:
- Use consistent ID patterns (`org_`, `sit_`, `ast_`, etc.)
- All timestamps in UTC ISO 8601
- SI units for measurements
- Include descriptions for all fields

### 2. Validate Your Work

```bash
# Run validation on all examples
python scripts/validate.py

# Run specific validation
python scripts/validate.py examples/your-new-example.json

# Run tests
pytest tests/

# Format code
black scripts/
ruff check scripts/
```

### 3. Update Documentation

- Update README.md if adding new schemas
- Add/update examples
- Update standards mapping if relevant

### 4. Commit Your Changes

Write clear commit messages:
```
feat: add battery storage asset schema

- Add battery-specific fields for capacity, charge rate
- Include degradation tracking
- Add example for grid-scale battery
```

Commit message prefixes:
- `feat:` New feature or schema
- `fix:` Bug fix
- `docs:` Documentation only
- `test:` Test additions/changes
- `refactor:` Code restructuring
- `chore:` Maintenance tasks

### 5. Submit Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request** with:
   - Clear title and description
   - Link to related issue
   - Summary of changes
   - Screenshots if relevant

3. **PR Checklist**:
   - [ ] Tests pass locally
   - [ ] Documentation updated
   - [ ] Examples validate
   - [ ] Backward compatible
   - [ ] Follows conventions

## 🎯 Schema Design Principles

1. **Simplicity First**: Start minimal, extend as needed
2. **Real-World Focus**: Based on actual energy industry needs
3. **Interoperability**: Compatible with existing standards
4. **Extensibility**: Support custom fields via `metadata`
5. **Clarity**: Self-documenting with clear descriptions

## 📋 Review Process

1. **Automated Checks**: CI validates schemas and examples
2. **Peer Review**: At least one maintainer review
3. **Discussion**: Address feedback constructively
4. **Merge**: Maintainer merges when approved

## 🏷️ Versioning Strategy

- **v0.x**: Development versions, breaking changes allowed
- **v1.0**: Stable release, backward compatibility required
- **Major**: Breaking changes (v1 → v2)
- **Minor**: New features, backward compatible (v1.0 → v1.1)
- **Patch**: Bug fixes (v1.0.0 → v1.0.1)

## 💡 Tips for Success

1. **Start Small**: One schema or fix at a time
2. **Ask Questions**: Use discussions for clarification
3. **Show Examples**: Real-world usage helps explain needs
4. **Be Patient**: Reviews ensure quality for everyone
5. **Stay Engaged**: Respond to feedback promptly

## 🆘 Getting Help

- **Discussions**: Technical questions and ideas
- **Issues**: Bugs and feature requests
- **Discord**: Real-time chat with community
- **Email**: maintainers@qubit.energy

## 🏆 Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- Annual contributor spotlight

## 📚 Resources

- [JSON Schema Documentation](https://json-schema.org/)
- [Energy Data Standards](docs/standards-mapping.md)
- [Schema Conventions](docs/schema-conventions.md)
- [API Integration Guide](docs/api-integration.md)

Thank you for helping build the open energy data ecosystem!