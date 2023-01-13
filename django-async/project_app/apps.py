import logging

import httpx

from django.apps import AppConfig
from django.conf import settings

from core.utils import remove_lead_and_trail_slash

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
                            set_webhook_site = remove_lead_and_trail_slash(dt['webhook_site'])
                            set_webhook_path = remove_lead_and_trail_slash(dt['set_webhook_path'])
                            set_webhook_url = f"{set_webhook_site}/{set_webhook_path}/{bot.token}/"
                            logger.info(set_webhook_url)
                            r = httpx.post(set_webhook_url, data={})
                            if r.status_code == httpx.codes.OK:
                                logger.info(f"Success")
                            else:
                                logger.info("ERROR")
                    except Exception as e:
                        error = "Bot {} doesn't exist or is improperly configured.".format(bot_name)
                        logger.error(error)
                        logger.error(e)
            self.is_ready = True