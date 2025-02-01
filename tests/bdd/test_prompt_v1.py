import pandas as pd
import pytest

class TestPromptV1:
    """Classe de testes para DataFrame com pytest"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega o DataFrame antes de cada teste"""
        self.df_bronze = pd.read_csv("src/bronze/data/v1/training.csv", delimiter=";")
        self.df_raw = pd.read_csv("tests/data/training.csv")

    def test_given_llm_receives_one_record_invalid_then_should_return_one_less(self):
        """Verifica se o DataFrame não está vazio"""
        assert self.df_bronze.nickname.count() + 1 == self.df_raw["Qual o @ (identifica a rede)"].count()
        assert not self.df_bronze.empty, "O DataFrame está vazio!"


    def test_dataframe_not_be_return_invalid_data(self):
        """Não deve encontrar influencer com review com texto ilegivel"""
        assert self.df_bronze[self.df_bronze["nickname"] == "@dragbox"].empty
