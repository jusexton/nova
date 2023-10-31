import aiohttp

from nova.util import SessionContextManager
from nova.extensions.gw2.types import Report

UploadResult = Report | str


class ReportClient(SessionContextManager):
    """
    HTTP client used to interface with https://dps.report/api.
    """

    async def upload(self, name: str, content: bytes, anonymous: bool = False) -> UploadResult:
        """
        Uploads file content to the dps.report API.

        :param name: The filename that will be attached to the uploaded content.
        :param content: File content that will be uploaded.
        :param anonymous: Whether the report should be generated with anonymous player names.
        :return: The created report
        """

        form = aiohttp.FormData()
        form.add_field('json', '1')
        form.add_field('anonymous', str(anonymous))
        form.add_field('file', filename=name, value=content)

        async with self._session.post('https://dps.report/uploadContent', data=form) as response:
            data = await response.json()
            return data['error'] if data['error'] else Report(**data)

