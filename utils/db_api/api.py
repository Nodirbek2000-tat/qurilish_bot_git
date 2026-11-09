"""Sayt backendi (Django) bilan aloqa.

Bot o'zida hech qanday ro'yxat saqlamaydi: kimga ruxsat borligini faqat katta baza hal qiladi.
"""

import asyncio
import logging

import aiohttp

from data.config import API_URL, BOT_API_KEY


class ApiError(Exception):
    def __init__(self, status: int, message: str = ""):
        super().__init__(message or f"HTTP {status}")
        self.status = status
        self.message = message


_session = None


async def call(path: str, data: dict) -> dict:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))
    try:
        async with _session.post(f"{API_URL}/api/bot/{path}/", json=data, headers={"X-Bot-Key": BOT_API_KEY}) as resp:
            body = await resp.json(content_type=None)
            status = resp.status
    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as err:
        logging.warning("Sayt API bilan aloqa yo'q: %s", err)
        raise ApiError(0, "Server bilan aloqa yo'q") from err
    if status >= 400:
        raise ApiError(status, (body or {}).get("error", ""))
    return body


async def close():
    if _session is not None and not _session.closed:
        await _session.close()
