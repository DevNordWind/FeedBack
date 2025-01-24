from aiogram_dialog import DialogManager
from dishka import FromDishka
from fluentogram import TranslatorRunner

from src.bot.injections import inject_getter
from src.db.enums import LangCode


@inject_getter
async def lang_getter(dialog_manager: DialogManager, translator: FromDishka[TranslatorRunner], **kwargs) -> dict:
    prefix = 'lang-select'
    btns = [
        (translator.get(f'{prefix}.{lang_code.lower()}'), lang_code) for lang_code in LangCode.__members__
    ]
    return {
        'btns': btns
    }
