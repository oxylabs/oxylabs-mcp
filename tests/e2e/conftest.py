import dotenv
import pytest


dotenv.load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def environment():
    pass
