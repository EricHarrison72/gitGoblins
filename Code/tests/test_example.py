import pytest

# TEST FILES
'''
> Must be in the folder 'tests'
> must start with 'test_'
'''

# FIXTURES
'''
> Use the `@pytest.fixture()` decorator
> Fixtures let you run some code that you might want to repeat for several tests
'''

@pytest.fixture()
def example_fixture():
    # here you initialize and return an object you want to use in several tests
    return 1

# TESTS
''' 
> Tests must start with 'test_'
> 1 Test for 1 method (or you can break it down more)
> Try not to initialize new objects in tests, although you can change stuff to check for error cases

> fixtures get passed as arguments to your tests. 
> You can give yourself 'type hints' with the syntax `: <expected-type>`
'''
def test_example_1(example_fixture : int):
    # here you run a method/operation of that object, and use assertions to test if it runs as expected

    sum = example_fixture + 1
    assert sum == 2