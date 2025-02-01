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
        assert self.df_bronze.nickname.count() == self.df_raw["Qual o @ (identifica a rede)"].count()
        assert not self.df_bronze.empty, "O DataFrame está vazio!"


    def test_dataframe_not_be_return_sentiment_with_undefined(self):
        assert (self.df_bronze[self.df_bronze["nickname"] == "@dragbox"]["personality"] == "undefined").all()
        assert (self.df_bronze[self.df_bronze["nickname"] == "@dragbox"]["professional"] == "undefined").all()



    @pytest.fixture(params=[
        ("positive", ("@gildovigor", "@tchulim - Instagram"))
    ])
    def reviews_positive(self, request):
        return request.param

    def test_should_return_review_positive_personality_and_professional(self, reviews_positive):
        review, nick_name = reviews_positive
        assert (self.df_bronze[self.df_bronze["nickname"] == nick_name]["personality"] == "positive").all()
        assert (self.df_bronze[self.df_bronze["nickname"] == nick_name]["professional"] == "positive").all()

    @pytest.fixture(params=[
        ("positive", ("blogueirinha", "@mohindi"))
    ])
    def reviews_negative(self, request):
        return request.param

    def test_should_return_review_negative_personality_and_professional(self, reviews_negative):
        review, nick_name = reviews_negative
        assert (self.df_bronze[self.df_bronze["nickname"] == nick_name]["personality"] == "negative").all()
        assert (self.df_bronze[self.df_bronze["nickname"] == nick_name]["professional"] == "unprofessional").all()
