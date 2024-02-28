import pytest

# FIXTURES

@pytest.fixture()
def example_fixture():
    # here you initialize and return an object you want to use in several tests
    return 1

# TESTS
# Tests must start with 'test_'
def test_example_1(example_fixture):
    # here you run a method/operation of that object, and use assertions to test if it runs as expected

    sum = example_fixture + 1
    assert sum == 2