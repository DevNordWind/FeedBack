from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text
from dishka.integrations.aiogram import CONTAINER_NAME
from fluentogram import TranslatorRunner


class GetText(Text):
    """This class produced by Translator"""

    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data: dict, manager: DialogManager, **kwargs) -> str:
        translator: TranslatorRunner = await manager.middleware_data[CONTAINER_NAME].get(TranslatorRunner)
        return str(translator.get(self.key, **data))
