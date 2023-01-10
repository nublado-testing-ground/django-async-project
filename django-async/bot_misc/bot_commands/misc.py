import random
import logging

from telegram import Update
from telegram.ext import ContextTypes

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from django_telegram.functions.functions import (
    parse_command_last_arg_text
)
from django_telegram.functions.group import (
    get_random_group_member
)

logger = logging.getLogger('django')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message and prompt a reply on start."""
    user = update.effective_user
    bot_name = context.bot.first_name
    message = "Hello, {}. {} has started.".format(
        user.mention_markdown(),
        bot_name
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the current time."""
    weekday = timezone.now().weekday()
    message = _("It's {weekday}, {time} {timezone}.").format(
        weekday=_(settings.WEEKDAYS[weekday]),
        time=timezone.now().strftime('%H:%M'),
        timezone=settings.TIME_ZONE
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


# def reverse_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Reverse the text provided as an argument and display it."""
#     if len(context.args) >= 1:
#         message = parse_command_last_arg_text(
#             update.effective_message,
#             maxsplit=1
#         )
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=message[::-1]
#         )
#     else:
#         message = _("The command requires some text to be reversed.")
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=message
#         )


# def hello(
#     update: Update,
#     context: ContextTypes.DEFAULT_TYPE,
#     group_id: int = None
# ) -> None:
#     if group_id:
#         member = get_random_group_member(group_id)
#         if member:
#             try:
#                 user = update.effective_user
#                 chat_member = context.bot.get_chat_member(group_id, member.user_id)
#                 message = _("Hey {}.\n{} says hello.").format(
#                     chat_member.user.mention_markdown(),
#                     user.mention_markdown()
#                 )
#                 context.bot.send_message(
#                     chat_id=group_id,
#                     text=message
#                 )
#             except:
#                 pass


# def echo(
#     update: Update,
#     context: ContextTypes.DEFAULT_TYPE,
#     group_id: int = None
# ) -> None:
#     """Echo a message to the group."""
#     if group_id:
#         if len(context.args) >= 1:
#             message = parse_command_last_arg_text(
#                 update.effective_message,
#                 maxsplit=1
#             )
#             context.bot.send_message(
#                 chat_id=group_id,
#                 text=message
#             )


# def roll_dice_c(
#     update: Update,
#     context: ContextTypes.DEFAULT_TYPE,
#     min_dice=1,
#     max_dice=10,
#     dice_min_val=1,
#     dice_max_val=6,
#     dice_sum=False
# ):
#     if len(context.args) >= 1:
#         int_arg = int(context.args[0])
#         if int_arg >= min_dice and int_arg <= max_dice:
#             num_dice = int_arg
#             results = []
#             user = update.effective_user
#             for x in range(num_dice):
#                 result = random.randint(dice_min_val, dice_max_val)
#                 results.append(result)
#             if dice_sum:
#                 total = sum(results)
#                 message = _("{} has rolled {}.\n\n Sum: {}").format(
#                     user.mention_markdown(),
#                     results,
#                     total
#                 )
#             else:
#                 message = _("{} has rolled {}.").format(
#                     user.mention_markdown(),
#                     results
#                 )
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id,
#                 text=message 
#             )
#     else:
#         message = _("Please specify the number of dice to be rolled ({} - {}).").format(
#             min_dice,
#             max_dice
#         )
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text=message
#         )

# def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Roll specified number of dice and show results as text."""
#     roll_dice_c(update, context, dice_sum=False)


# def roll_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Roll specified number of dice and show results as text."""
#     roll_dice_c(update, context, dice_sum=True)
