# Test Suite for High School Management System API

This directory contains comprehensive test coverage for the FastAPI application that manages extracurricular activities at Mergington High School.

## Test Structure

### `conftest.py`
- Contains pytest fixtures and configuration
- **`client` fixture**: Provides a FastAPI TestClient for making HTTP requests
- **`reset_activities` fixture**: Resets the activities data to its original state before each test

### `test_api.py`
Contains all test cases organized into logical classes:

#### `TestRootEndpoint`
- Tests the root URL redirect functionality

#### `TestActivitiesEndpoint`
- Tests the GET `/activities` endpoint
- Verifies data structure and content

#### `TestSignupEndpoint`
- Tests the POST `/activities/{activity_name}/signup` endpoint
- Covers success cases, duplicate signups, and error conditions
- Tests URL encoding handling

#### `TestUnregisterEndpoint`
- Tests the DELETE `/activities/{activity_name}/unregister` endpoint
- Covers success cases, non-existent participants, and error conditions
- Tests URL encoding handling

#### `TestIntegrationScenarios`
- Tests workflows that involve multiple API calls
- Tests participant count changes
- Tests signing up for multiple activities

## Running Tests

### Prerequisites
Install the test dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
# Simple test run
python -m pytest tests/

# Verbose output
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing

# Use the provided script
./run_tests.sh
```

### Run Specific Tests
```bash
# Run tests for a specific class
python -m pytest tests/test_api.py::TestSignupEndpoint -v

# Run a specific test
python -m pytest tests/test_api.py::TestSignupEndpoint::test_signup_success -v
```

## Test Coverage

The test suite achieves **100% code coverage** for the FastAPI application, testing:

✅ **All HTTP endpoints** (GET, POST, DELETE)  
✅ **Success and error cases** for each endpoint  
✅ **Data validation** and business logic  
✅ **URL encoding** handling  
✅ **Integration scenarios** across multiple operations  
✅ **State management** (participants list changes)  

## Test Features

- **Isolated tests**: Each test runs with fresh data via the `reset_activities` fixture
- **Comprehensive assertions**: Tests verify both HTTP status codes and response data
- **Error condition testing**: Tests handle invalid inputs, non-existent resources, and duplicate operations
- **Integration testing**: Tests workflows that span multiple API calls
- **URL encoding support**: Tests handle activity names with spaces and special characters

## Test Data

Tests use a consistent set of test data that mirrors the production activities:
- Chess Club, Programming Class, Gym Class
- Soccer Team, Basketball Club
- Art Workshop, Drama Club
- Mathletes, Science Club

Each activity has predefined participants that are restored before each test run.