"""
Конфигурация проекта
"""

from pathlib import Path
import os

# Пути
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
EXTERNAL_DATA = DATA_DIR / 'external'
PROCESSED_DATA = DATA_DIR / 'processed'

# API Ключи (заполнить своими)
API_KEYS = {
    'IEA': os.getenv('IEA_API_KEY'),
    'IMF': os.getenv('IMF_API_KEY')
}

# URL источников
URLS = {
    'nasa_climate': "https://data.giss.nasa.gov/gistemp/graphs_v4/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt",
    'un_population': "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2022_TotalPopulationBySex.csv",
    'imf_gdp': "https://www.imf.org/external/datamapper/api/v2/NGDP_RPCH",
    'who_health': "https://cdn.who.int/media/docs/default-source/gho-documents/global-health-estimates/life-expectancy.csv",
    'iea_energy': "https://www.iea.org/reports/world-energy-outlook-2023"
}