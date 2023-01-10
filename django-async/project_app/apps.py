import logging

from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger('django')


class ProjectAppConfig(AppConfig):
    name = "project_app"

    def ready(self):
        dt = settings.DJANGO_TELEGRAM
        if dt['mode'] == settings.BOT_MODE_WEBHOOK:
            from django_telegram.apps import DjangoTelegramConfig
            from core.utils import remove_lead_and_trail_slash

            for bot_name, conf in settings.DJANGO_TELEGRAM['bots'].items():
                msg = "Setting webhook for {bot_name}".format(bot_name=bot_name)
                logger.info(msg)
                try:
                    bot_token = conf['token']
                    bot = DjangoTelegramConfig.bot_registry.get_bot(bot_token)
                    if bot:
                        pass
                        # r = requests.post(set_webhook_url, data={})
                        # logger.info(r.status_code)
                        # if r.status_code == requests.codes.ok:
                        #     msg = "Bot {} webhook is configured.".format(bot_name)
                        #     logger.info(msg)
                        # else:
                        #     error = "Bot {} webhook is improperly configured.".format(bot_name)
                        #     logger.error(error)                
                except Exception as e:
                    error = "Bot {} doesn't exist or is improperly configured.".format(bot_name)
                    logger.error(error)
                    logger.error(e)