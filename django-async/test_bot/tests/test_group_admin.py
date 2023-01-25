import logging

import pytest
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import get_display_name

from django.conf import settings
from django.utils.translation import gettext as _

from group_admin.bot_commands.group_admin import (
    BOT_MESSAGES
)

from .helpers import (
    get_button_with_text, is_group_member
)
from .conftest import (
    TEST_GROUP_ID, TEST_BOT_ID, TIMEOUT, MAX_MSGS
)

TEST_GROUP_INVITATION = "elL0E4yk9vs3ZGZh"

logger = logging.getLogger('django')

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
            # Get the welcome message with the "I agree" button.
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=TEST_BOT_ID)
            )
            logger.info(response.message.message)
            assert "I agree" in response.raw_text
            button = get_button_with_text(response.message, "I agree.")
            assert button is not None
            await button.click()
            # # Get the welcome message after the user has clicked the "I agree" button.
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=TEST_BOT_ID)
            )
            assert "voice message" in response.raw_text
            # # Permissions after clicking the "I agree" button.
