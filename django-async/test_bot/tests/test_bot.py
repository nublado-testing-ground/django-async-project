import logging

import pytest
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import get_display_name

from django.conf import settings
from django.utils.translation import gettext as _

from bot_misc.bot_commands.misc import (
    MIN_DICE, MAX_DICE,
    BOT_MESSAGES as BOT_MISC_MESSAGES
)

from .helpers import (
    is_from_test_bot, get_button_with_text,
    is_group_member, get_num_list_from_str
)
from .conftest import (
    TEST_GROUP_ID, TEST_BOT_ID, TIMEOUT, MAX_MSGS
)

TEST_GROUP_INVITATION = "elL0E4yk9vs3ZGZh"

logger = logging.getLogger('django')
logger_debug = logging.getLogger('django-debug')

# Note: Suspend the external webhook web service and run the bot
# locally with polling when running these tests.
# python manage.py runbot testbot --settings=config.settings.test


class TestGroupAdminCommands:
    @pytest.mark.asyncio
    async def test_member_join_group(self, tg_client):
        if await is_group_member(tg_client, TEST_GROUP_ID):
            await tg_client.delete_dialog(TEST_GROUP_ID)

        updates = await tg_client(ImportChatInviteRequest(TEST_GROUP_INVITATION))
        async with tg_client.conversation(
            TEST_GROUP_ID,
            timeout=TIMEOUT,
            max_messages=MAX_MSGS
        ) as conv:
            # User default permissions when joining
            me = await tg_client.get_me()
            await conv.send_message("testing")
            # Get the welcome message with the "I agree" button.
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=TEST_BOT_ID)
            )
            assert "I agree" in response.raw_text
            button = get_button_with_text(response.message, "I agree.")
            assert button is not None
            await button.click()
            # Get the welcome message after the user has clicked the "I agree" button.
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=TEST_BOT_ID)
            )
            assert "voice message" in response.raw_text
            # Permissions after clicking the "I agree" button.


class TestMiscBotCommands:
    @pytest.mark.asyncio
    async def test_group_get_time(self, group_conv):
        cmd = "/get_time"
        await group_conv.send_message(cmd)
        resp = await group_conv.get_response()
        assert is_from_test_bot(resp, TEST_BOT_ID)
        assert "UTC" in resp.raw_text

    @pytest.mark.asyncio
    async def test_group_reverse(self, group_conv):
        cmd = "/reverse"
        await group_conv.send_message(f"{cmd} I like pizza.")
        resp = await group_conv.get_response()
        assert is_from_test_bot(resp, TEST_BOT_ID)
        assert resp.raw_text == ".azzip ekil I"

    @pytest.mark.asyncio
    async def test_group_roll(self, tg_client):
        cmd = "/roll"
        async with tg_client.conversation(
            TEST_GROUP_ID,
            timeout=TIMEOUT,
            max_messages=MAX_MSGS
        ) as conv:
            await conv.send_message(f"{cmd} 5")
            resp = await conv.get_response()
            logger.info(resp.raw_text)
            # Extract the "dice" from the response string as a list.
            nums = get_num_list_from_str(resp.raw_text)
            display_name = get_display_name(await tg_client.get_me())
            assert display_name != ''
            assert is_from_test_bot(resp, TEST_BOT_ID)
            assert resp.raw_text == f"{display_name} has rolled {nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}, {nums[4]}."
            
            await conv.send_message(f"{cmd} 4")
            resp = await conv.get_response()
            nums = get_num_list_from_str(resp.raw_text)
            assert resp.raw_text == f"{display_name} has rolled {nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}."
           
            await conv.send_message(f"{cmd} 2")
            resp = await conv.get_response()
            nums = get_num_list_from_str(resp.raw_text)
            assert resp.raw_text == f"{display_name} has rolled {nums[0]}, {nums[1]}."
           
            await conv.send_message(f"{cmd} 1")
            resp = await conv.get_response()
            nums = get_num_list_from_str(resp.raw_text)
            assert resp.raw_text == f"{display_name} has rolled {nums[0]}."

            # Attempt roll with no argument.
            error_msg = _(BOT_MISC_MESSAGES['dice_specify_num']).format(
                min_dice=MIN_DICE,
                max_dice=MAX_DICE
            )   
            await conv.send_message(f"{cmd}")
            resp = await conv.get_response()
            assert resp.raw_text == error_msg

            # Attempt roll wit more the the maximum number of dice.
            await conv.send_message(f"{cmd} {MAX_DICE + 1}")
            resp = await conv.get_response()
            assert resp.raw_text == error_msg

            # Attempt roll with less than the minimum number of dice.
            await conv.send_message(f"{cmd} {MIN_DICE - 1}")
            resp = await conv.get_response()
            assert resp.raw_text == error_msg