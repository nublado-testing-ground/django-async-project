import logging
import asyncio

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger('django')


class ProjectAppConfig(AppConfig):
    name = "project_app"
    is_ready = False

    def ready(self):
        if not self.is_ready:
            dt = settings.DJANGO_TELEGRAM
            if dt['mode'] == settings.BOT_MODE_WEBHOOK:
                from django_telegram.apps import DjangoTelegramConfig

                for bot_name, conf in settings.DJANGO_TELEGRAM['bots'].items():
                    try:
                        bot_token = conf['token']
                        bot = DjangoTelegramConfig.bot_registry.get_bot(bot_token)
                        if bot:
                            pass             
                    except Exception as e:
                        error = "Bot {} doesn't exist or is improperly configured.".format(bot_name)
                        logger.error(error)
                        logger.error(e)
            self.is_ready = True