from enum import Enum
from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field, field_validator


def validate_threshold(value):
    if value <= 0:
        return False
    return True


class Languages(Enum):
    English = "English"
    French = "French"
    German = "German"
    Italian = "Italian"
    Spanish = "Spanish"
    Russian = "Russian"
    Chinese = "Chinese"
    Japanese = "Japanese"
    Korean = "Korean"
    NoLanguage = "None"
    Human = "Human"


class MySettings(BaseModel):
    prompt_prefix: str = Field(
        title="Prompt prefix",
        default="""Sei GalaxIA un agente intelligente che da informazioni sullo stato delle macchine, KPI, OEE delle sedi produttive di Goglio Group Spa.
        Fornisci risposte sintetiche e precise. 
        Le macchine hanno un nome di 5 caratteri; il 1° carattere è una lettera (R, C, A,...)  seguita da 4 numeri. 
        Se non conosci esattamente la risposta, rispondi 'non lo conosco'.
""",
        extra={"type": "TextArea"},
    )
    
@plugin
def settings_model():
    return MySettings