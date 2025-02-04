from dataclasses import dataclass

@dataclass
class Setup:
    model: str = "gpt-4o-mini"
    strengths_weaknesses_version: str = "v2"
    personal_professional_version: str = "V2"
    recommendation_version: str = "v1"
    path_bronze: str = "data/bronze/data"
