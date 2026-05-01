import time
import asyncio
import os
from pyrogram import Client
from aiohttp import ClientSession
from typing import Union
from .. import client


async def download_coroutine(bot: Union[Client, None], session: ClientSession, url: str, file_name: str, chat_id: Union[str, int, None], message_id: Union[int, None], start: float, headers: dict):
    if bot:
        await bot.edit_message_text(
            chat_id,
            message_id,
            text="Initiating Download\nURL: {}".format(url)
        )

    # aria2c command
    cmd = [
        "aria2c",
        "--console-log-level=error",
        "-c",
        "-x", "16",
        "-s", "16",
        "-k", "1M",
        url,
        "-d", os.path.dirname(file_name),
        "-o", os.path.basename(file_name)
    ]

    if headers:
        for key, value in headers.items():
            cmd.append(f"--header={key}: {value}")

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # While aria2c doesn't provide easy progress via stdout without parsing,
    # we'll wait for it to finish.
    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        if bot:
            error = stderr.decode().strip()
            await bot.edit_message_text(
                chat_id,
                message_id,
                text=f"Download Error: {error}"
            )
        return False

    if bot:
        await bot.edit_message_text(
            chat_id,
            message_id,
            text=f"Download Completed."
        )
    return True
