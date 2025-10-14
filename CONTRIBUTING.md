# Contributing to IBM ACE Migration Estimator

First off, thank you for considering contributing to the ACE Migration Estimator! 🎉

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Docker version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **Include mockups or examples if applicable**

### Your First Code Contribution

Unsure where to begin? You can start by looking through `good-first-issue` and `help-wanted` issues:

- **Good first issues** - issues that should only require a few lines of code
- **Help wanted issues** - issues that are more involved

## Development Setup

### Prerequisites
- Docker Desktop
- Node.js 18+ and npm
- Python 3.11+
- Git

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### Frontend Setup
```bash
cd frontend
npm install
```

### Running Tests

#### Backend Tests
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

#### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Coding Standards

### Python (Backend)

#### Style Guide
- Follow **PEP 8** style guide
- Use **Black** for code formatting: `black app/`
- Use **isort** for import sorting: `isort app/`
- Use **mypy** for type checking: `mypy app/`
- Maximum line length: 100 characters

#### Code Structure
```python
"""
Module docstring explaining purpose.
"""

from typing import List, Optional
import asyncio

from fastapi import APIRouter
from pydantic import BaseModel


class MyModel(BaseModel):
    """Class docstring."""
    
    field_name: str
    optional_field: Optional[int] = None


async def my_function(param: str) -> dict:
    """
    Function docstring explaining purpose.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    # Implementation
    pass
```

#### Naming Conventions
- **Classes**: `PascalCase`
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### TypeScript/React (Frontend)

#### Style Guide
- Follow **Airbnb Style Guide**
- Use **ESLint** for linting
- Use **Prettier** for formatting
- Maximum line length: 100 characters

#### Code Structure
```typescript
import React, { useState } from 'react';
import { Button } from '@carbon/react';
import './MyComponent.scss';

interface MyComponentProps {
  title: string;
  onSubmit?: () => void;
}

/**
 * Component description
 */
export const MyComponent: React.FC<MyComponentProps> = ({ title, onSubmit }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = () => {
    setIsLoading(true);
    onSubmit?.();
  };

  return (
    <div className="my-component">
      <h2>{title}</h2>
      <Button onClick={handleClick} disabled={isLoading}>
        Submit
      </Button>
    </div>
  );
};
```

#### Naming Conventions
- **Components**: `PascalCase`
- **Functions/Variables**: `camelCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `PascalCase.tsx` for components, `camelCase.ts` for utilities

### Documentation

- Write clear, concise comments
- Document all public APIs
- Include JSDoc/docstrings for functions
- Update README.md when adding features
- Add inline comments for complex logic

## Commit Guidelines

We follow **Conventional Commits** specification:

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Changes to build process or auxiliary tools

### Examples
```
feat(estimation): add support for ACE v13 migration

Add estimation rules and validation for App Connect Enterprise v13.
Includes updated rules engine and new test cases.

Closes #123
```

```
fix(frontend): resolve form validation issue

Fixed issue where flow count validation wasn't triggering
for values greater than 1000.

Fixes #456
```

```
docs(readme): update installation instructions

Added troubleshooting section for Docker setup issues.
```

### Rules
- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- First line should be 72 characters or less
- Reference issues and pull requests in footer

## Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git checkout main
   git pull upstream main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

4. **Test your changes**
   ```bash
   # Backend
   cd backend
   pytest
   black app/
   mypy app/
   
   # Frontend
   cd frontend
   npm test
   npm run lint
   npm run build
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

### Submitting the PR

1. Go to the original repository
2. Click "New Pull Request"
3. Select your feature branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. **Automated checks** will run (tests, linting, build)
2. **Maintainer review** - address any feedback
3. **Approval** - once approved, your PR will be merged

### After Merge

1. Delete your feature branch
2. Update your local repository
3. Celebrate! 🎉

## Additional Resources

### Learning Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Carbon Design System](https://carbondesignsystem.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Python Best Practices](https://docs.python-guide.org/)

### Development Tools
- **VS Code Extensions**:
  - Python
  - Pylance
  - ESLint
  - Prettier
  - Docker
  - GitLens

- **Chrome Extensions**:
  - React Developer Tools
  - Redux DevTools

### Communication
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Pull Requests for code review

## Questions?

Don't hesitate to ask questions! We're here to help:
- Open an issue with the `question` label
- Start a discussion in GitHub Discussions
- Reach out to maintainers

---

Thank you for contributing! 🚀
