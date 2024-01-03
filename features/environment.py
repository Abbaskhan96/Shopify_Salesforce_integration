import sys
sys.path.append("./Connection_Setup")
from testConnection import setup_connection, teardown_connection
from behave import fixture, use_fixture
import logging



@fixture
def connection_fixture(context):
    setup_connection()
    yield
    teardown_connection()




def before_all(context):
    use_fixture(connection_fixture, context)


def after_all(context):
    # No need to call teardown_connection() here since it is handled by the fixture
    pass
