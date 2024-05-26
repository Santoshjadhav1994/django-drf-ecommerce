from pytest_factoryboy import register
import pytest

from .factories import CategoryFactory,BrandFactory,ProductFactory,ProductLineFactory
from rest_framework.test import APIClient

register(CategoryFactory)
register(BrandFactory)
register(ProductFactory)
register(ProductLineFactory)

@pytest.fixture
def api_client():
    return APIClient