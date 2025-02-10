import pandas as pd
import pytest


class TestPrompt:
    """Classe de testes para DataFrame com pytest"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega o DataFrame antes de cada teste"""
        self.df_silver = pd.read_csv("data/silver/data/personal_professional/gpt-4o-mini/v1/training.csv",
                                     delimiter=";")
        self.df_raw = pd.read_csv("tests/data/training.csv")

    def test_should_return_equal_number_rows(self):
        """Verifica se o DataFrame não está vazio"""
        assert self.df_silver.nickname.count() == self.df_raw["Qual o @ (identifica a rede)"].count()
        assert not self.df_silver.empty, "O DataFrame está vazio!"

    def test_dataframe_not_be_return_sentiment_with_undefined(self):
        assert (self.df_silver[self.df_silver["nickname"] == "@dragbox"]["personality"] == "indefinido").all()
        assert (self.df_silver[self.df_silver["nickname"] == "@dragbox"]["professional"] == "indefinido").all()

    @pytest.fixture(params=[
        ("positivo", ("@gildovigor", "@tchulim - Instagram"))
    ])
    def reviews_positive(self, request):
        return request.param

    def test_should_return_review_positive_personality_and_professional(self, reviews_positive):
        review, nick_name = reviews_positive
        assert (self.df_silver[self.df_silver["nickname"] == nick_name]["personality"] == "positivo").all()
        assert (self.df_silver[self.df_silver["nickname"] == nick_name]["professional"] == "positivo").all()

    @pytest.fixture(params=[
        ("negativo", ("blogueirinha", "@mohindi"))
    ])
    def reviews_negative(self, request):
        return request.param

    def test_should_return_review_negative_personality_and_professional(self, reviews_negative):
        review, nick_name = reviews_negative
        assert (self.df_silver[self.df_silver["nickname"] == nick_name]["personality"] == "negativo").all()
        assert (self.df_silver[self.df_silver["nickname"] == nick_name]["professional"] == "unprofessional").all()
