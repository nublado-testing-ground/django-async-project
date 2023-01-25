import logging

from asgiref.sync import sync_to_async

from telegram import Update
from telegram.ext import (
    ContextTypes, MessageHandler, filters
)

from django.conf import settings
from django.utils.translation import gettext as _

from django_telegram.models import GroupMember
from django_telegram.functions.user import get_username_or_name

logger = logging.getLogger('django')

ADD_POINTS_TRIGGER = '+'
ADD_POINTS_REGEX = '^[' + ADD_POINTS_TRIGGER + '][\s\S]*$'
REMOVE_POINTS_TRIGGER = '-'
REMOVE_POINTS_REGEX = '^[' + REMOVE_POINTS_TRIGGER + '][\s\S]*$'
POINT_NAME = _("raindrop")
POINTS_NAME = _("raindrops")
TOP_POINTS_LIMIT = 10

# Translated bot messages
BOT_MESSAGES = {
    'no_give_bot': _("You can't give {points_name} to a bot."),
    'no_take_bot': _("You can't take {points_name} from a bot."),
    'no_give_self': _("You can't give {points_name} to yourself."),
    'no_take_self': _("You can't take {points_name} from yourself."),
    'give_point': _(
        "*{sender_name} ({member_sender})* has given a " + \
        "{points_name} to *{receiver_name} ({receiver_points})*."
    ),
    'give_points': (
        "*{sender_name} ({member_sender})* has given some " + \
        "{points_name} to *{receiver_name} ({receiver_points})*."
    ),
    'take_point': _(
        "*{sender_name} ({member_sender})* has taken a " + \
        "{points_name} from *{receiver_name} ({receiver_points})*."
    ),
    'take_points': _(
        "*{sender_name} ({member_sender})* has taken some " + \
        "{points_name} from *{receiver_name} ({receiver_points})*."
    ),
}

@sync_to_async
def get_group_member(user_id, group_id):
    """Get user's total points in group."""
    group_member, group_member_created = GroupMember.objects.get_or_create(
        group_id=group_id,
        user_id=user_id
    )

    return group_member


# def group_top_points(update: Update, context: ContextTypes.DEFAULT_TYPE, group_id: int = None) -> None:
#     if group_id:
#         member_points = GroupMemberPoints.objects.get_group_top_points(
#             group_id, TOP_POINTS_LIMIT
#         )

#         if member_points:
#             top_points = []

#             for member in member_points:
#                 points = member.points
#                 user_id = member.group_member.user_id
#                 chat_member = get_chat_member(context, user_id, GROUP_ID)

#                 if chat_member:
#                     user = chat_member.user
#                     logger.info(user)
#                     name = get_username_or_name(user)
#                     name_points = "*{points}: {name}*".format(
#                         name=name,
#                         points=points
#                     )
#                     top_points.append(name_points)

#             message = _("*Top {point_name} rankings*\n{rankings_list}").format(
#                 point_name=_(POINT_NAME),
#                 rankings_list="\n".join(top_points)
#             )
#             await context.bot.send_message(
#                 chat_id=group_id,
#                 text=message
#             )


async def add_points(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None,
) -> None:
    if group_id:
        # Check if the message is a reply to another message.
        if update.message.reply_to_message:
            sender = update.effective_user
            sender_name = get_username_or_name(sender)
            receiver = update.message.reply_to_message.from_user
            receiver_name = get_username_or_name(receiver)

            # Check if the reply is to another member and not a bot or oneself.
            if not receiver.is_bot and sender != receiver:
                member_sender = await get_group_member(sender.id, group_id)
                member_receiver = await get_group_member(receiver.id, group_id)
                member_receiver.points += member_sender.point_increment
                await sync_to_async(member_receiver.save)()

                if member_sender.point_increment > 1:
                    message = _(BOT_MESSAGES['give_points']).format(
                        sender_name=sender_name,
                        member_sender=member_sender.points,
                        points_name=_(POINTS_NAME),
                        receiver_name=receiver_name,
                        receiver_points=member_receiver.points
                    )
                else:
                    message = _(BOT_MESSAGES['give_point']).format(
                        sender_name=sender_name,
                        member_sender=member_sender.points,
                        points_name=_(POINT_NAME),
                        receiver_name=receiver_name,
                        receiver_points=member_receiver.points
                    )
            elif receiver.is_bot:
                message = _(BOT_MESSAGES['no_give_bot']).format(
                    points_name=_(POINTS_NAME)
                )
            elif receiver == sender:
                message = _(BOT_MESSAGES['no_give_self']).format(
                    points_name=_(POINTS_NAME)
                )

            await context.bot.send_message(
                chat_id=group_id,
                text=message
            )


async def remove_points(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None
) -> None:
    if group_id:
        if update.message.reply_to_message:
            sender = update.effective_user
            sender_name = get_username_or_name(sender)
            receiver = update.message.reply_to_message.from_user
            receiver_name = get_username_or_name(receiver)

            if not receiver.is_bot and sender != receiver:
                member_sender = await get_group_member(sender.id, group_id)
                member_receiver = await get_group_member(receiver.id, group_id)
                points = member_receiver.points - member_sender.point_increment
                member_receiver.points = points if points >= 0 else 0
                await sync_to_async(member_receiver.save)()

                if member_sender.point_increment > 1:
                    message = _(BOT_MESSAGES['take_points']).format(
                        sender_name=sender_name,
                        member_sender=member_sender.points,
                        points_name=_(POINTS_NAME),
                        receiver_name=receiver_name,
                        receiver_points=member_receiver.points
                    )
                else:
                    message = _(BOT_MESSAGES['take_point']).format(
                        sender_name=sender_name,
                        member_sender=member_sender.points,
                        points_name=_(POINT_NAME),
                        receiver_name=receiver_name,
                        receiver_points=member_receiver.points
                    )
            elif receiver.is_bot:
                message = _(BOT_MESSAGES['no_take_bot']).format(
                    points_name=_(POINTS_NAME)
                )
            elif receiver == sender:
                message = _(BOT_MESSAGES['no_take_self']).format(
                    points_name=_(POINTS_NAME)
                )        
            await context.bot.send_message(
                chat_id=group_id,
                text=message
            )


# Message handlers to listen for triggers to add or remove points.
add_points_handler = MessageHandler(
    (filters.Regex(ADD_POINTS_REGEX) & filters.REPLY),
    add_points
)


remove_points_handler = MessageHandler(
    (filters.Regex(REMOVE_POINTS_REGEX) & filters.REPLY),
    remove_points
)