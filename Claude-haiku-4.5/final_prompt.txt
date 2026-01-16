# Issue #446 Fix Task Prompt

## Task Overview

You need to fix Issue #446 in the fake-useragent library. The current project has a functional bug: when creating a UserAgent instance with specific parameters, the generated user agents lack randomness and show significant repetition.

## Current Project Structure

```
issue_project/
├── src/
│   └── fake_useragent/
│       ├── __init__.py
│       ├── fake.py
│       ├── utils.py
│       ├── errors.py
│       ├── log.py
│       ├── get_version.py
│       ├── py.typed
│       └── data/
│           └── browsers.json
├── buggy_version.py
└── pyproject.toml
```

## Bug Reproduction

Run `buggy_version.py` to see the issue:

```python
ua = UserAgent(
    browsers=["Chrome", "Firefox", "Edge", "Opera", "Safari", "Android",
              "Samsung Internet", "Opera Mobile", "Mobile Safari", "Firefox Mobile",
              "Chrome Mobile", "Chrome Mobile iOS", "Mobile Safari UI/WKWebView", "Edge Mobile"],
    os=["Windows", "Chrome OS", "Mac OS X", "Android", "iOS"],
    min_version=131,
)

# Generate 10 user agents, you'll notice about 20% repetition rate
for i in range(10):
    print(ua.random)
```

**Expected Behavior**: Each call should return a different, random user agent string
**Actual Behavior**: Generated user agents show repetition, lacking sufficient randomness

## Your Tasks

### 1. Create Fixed Version Project

Create the fixed project under the `issue_project_fixed/` directory with the following structure:

```
issue_project_fixed/
├── src/
│   └── fake_useragent/
│       ├── __init__.py
│       ├── fake.py          # Fixed code
│       ├── utils.py         # Fixed code
│       ├── errors.py
│       ├── log.py
│       ├── get_version.py
│       ├── py.typed
│       └── data/
│           └── browsers.json
├── tests/                    # pytest test files
├── fixed_version.py          # Script demonstrating the fix
├── pyproject.toml
├── pytest.ini
├── README.md                 # Project usage and quick start guide
└── SOLUTION.md               # Explanation of fix, root cause, and test strategy
```

### 2. Code Fix Requirements

- Identify the root cause of insufficient randomness
- Fix the issue in relevant files (may involve `fake.py`, `utils.py`, etc.)
- Maintain backward compatibility
- Do not break existing functionality
- Code should be clean and maintainable

### 3. Testing Requirements

Write comprehensive tests using pytest to ensure the bug is fixed without introducing new issues:

- Write specific tests for this bug to verify the fix
- Write basic functionality tests to ensure existing features work properly
- Write edge case tests covering various extreme scenarios
- Ensure test cases are comprehensive and representative

All tests must pass - running `pytest -v` should show 100% pass rate.

### 4. Documentation Requirements

**README.md** should include:
- Project introduction and Issue #446 background
- Quick start guide (installation, running, testing)
- Usage examples
- Project structure explanation

**SOLUTION.md** should include:

1. **Problem Analysis**
   - What is the root cause of the bug?
   - Which code caused this issue?
   - Why does repetition occur?

2. **Solution**
   - What modifications did you make?
   - Which files were modified?
   - What is the purpose of each modification?

3. **Testing Strategy**
   - Test case design approach
   - How to verify the bug is fixed?
   - Edge case coverage

4. **Usage Instructions**
   - How to install the fixed version
   - How to run tests
   - How to verify the fix

### 5. Verification Requirements

Before submitting the fix, ensure:

- [ ] All pytest tests pass (`pytest -v`)
- [ ] `fixed_version.py` demonstrates the fix
- [ ] No new bugs introduced
- [ ] Backward compatibility maintained
- [ ] README.md provides clear usage guide
- [ ] SOLUTION.md documentation is complete and clear

## Important Notes

1. **Do not modify the original project**: All fixes should be in the `issue_project_fixed/` directory
2. **Do not use absolute paths**: All path references should use relative paths
3. **Test-driven**: Write tests first to reproduce the issue, then fix
4. **Complete documentation**: SOLUTION.md should enable other developers to understand your fix approach

## Delivery Standards

Upon completion, you should be able to:
1. Navigate to `issue_project_fixed/` directory
2. Run `pip install -e .` to install the fixed version
3. Run `pytest -v` to see all tests pass
4. Run `python fixed_version.py` to see the bug is fixed
5. Read `README.md` to quickly understand the project
6. Read `SOLUTION.md` to understand the fix approach

Let's start fixing!
