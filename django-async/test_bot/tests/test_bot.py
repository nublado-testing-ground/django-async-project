import re
import logging

import pytest
from telethon.tl.custom.message import Message
from telethon.tl.types import PeerUser
from telethon.utils import get_display_name

from django.conf import settings

from bot_misc.bot_commands.misc import (
    MIN_DICE, MAX_DICE
)

from .conftest import (
    TEST_GROUP_ID, TEST_BOT_ID, TIMEOUT, MAX_MSGS
)

logger = logging.getLogger('django')


# Note: Suspend the external webhook web service and run the bot
# locally with polling when running these tests.
# python manage.py runbot testbot --settings=config.settings.test


# Helper functions
def is_from_test_bot(message: Message, test_bot_id: int) -> bool:
    return (isinstance(message.from_id, PeerUser) and
            message.from_id.user_id == test_bot_id)


def get_num_list_from_str(txt):
    """Return a list of comma-separated numbers in string."""
    num_list = re.findall("\d+(?:,\d+)?", txt)
    return num_list


class TestBotCommands:
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
        group = await tg_client.get_entity(TEST_GROUP_ID)
        async with tg_client.conversation(
            group,
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
            error_msg = f"Please specify the number of dice ({MIN_DICE} - {MAX_DICE})."
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