from dataclasses import dataclass


@dataclass
class Setup:
    model: str = "gpt-4o-mini"
    path_bronze: str = "data/bronze/data"
    path_silver: str = "data/silver/data"

@dataclass
class SetupPersonalProfessional(Setup):
    name: str = "personal_professional"
    version: str = "v2"


@dataclass
class SetupRecommendation(Setup):
    name: str = "recommendation"
    version: str = "v1"


@dataclass
class SetupStrengthsWeaknesses(Setup):
    name : str  = "strengths_weaknesses"
    version : str = "v2"
