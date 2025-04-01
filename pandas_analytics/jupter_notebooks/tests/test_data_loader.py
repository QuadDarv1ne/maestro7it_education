import pytest
from src.data_loader import DataLoader

@pytest.fixture
def loader():
    return DataLoader()

def test_climate_loading(loader):
    df = loader.load_climate()
    assert not df.empty
    assert {'Year', 'Temp'}.issubset(df.columns)
    assert df[df['Year'] == 2025]['Temp'].values[0] > 1.0

def test_population_filter(loader):
    df = loader.load_population(["China", "India"])
    assert df['Country'].nunique() == 2