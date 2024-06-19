import pytest
from dataclasses import dataclass


@dataclass
class FakeUserRepository():
    pass
    
@pytest.fixture
def user_repository():
    return FakeUserRepository()