import json
import logging

from telegram import Update
from telegram.error import TelegramError

from django.http import Http404, JsonResponse
from django.views import View

from .apps import DjangoTelegramConfig

logger = logging.getLogger('django')


class BotSetWebhookView(View):
    async def post(self, request, *args, **kwargs):
        token = kwargs['token']
        bot = DjangoTelegramConfig.bot_registry.get_bot(token)

        if bot is not None:
            try:
                await bot.start_webhook()
                logger.info(f"Webhook for bot {bot.token} set successfully in view.")
                return JsonResponse({})
            except Exception as e:
                error = f"Error in setting up webhook for bot {bot.token}: {e}"
                logger.error(error)

                raise Http404
        else:
            error = f"Requested bot {token} not found."
            logger.error(error)
            raise Http404


class BotWebhookView(View):
    async def post(self, request, *args, **kwargs):
        token = kwargs['token']
        bot = DjangoTelegramConfig.bot_registry.get_bot(token)

        if bot is not None:
            try:
                data = json.loads(request.body.decode('utf-8'))
                logger.info(data)
            except Exception as e:
                error = f"Error in decoding update: {e}"
                logger.error(error)

                raise Http404

            try:
                update = Update.de_json(data, bot.telegram_bot)
                # await bot.application.process_update(update)
            except Exception as e:
                error = f"Error in processing update: {e}"
                logger.error(error)

            return JsonResponse({})
        else:
            raise Http404
