import abc

import aiohttp


class SessionContextManager(abc.ABC):
    """
    Class used to provide async context manager functionality along with a reference to an open aiohttp session.
    """

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()
