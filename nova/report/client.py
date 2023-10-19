import aiohttp

from nova.report.types import Report


class ReportClient:
    """
    HTTP client used to interface with https://dps.report/api.
    """

    def __init__(self, anonymous: bool = False):
        """
        Instantiates a new client instance.

        :param anonymous: Denotes that the report should use anonymous player names.
        """
        self.anonymous = anonymous

    async def upload(self, name: str, content: bytes) -> Report:
        """
        Uploads file content to the dps.report API.

        :param name: The filename that will be attached to the uploaded content.
        :param content: File content that will be uploaded.
        :return: test
        """
        form = aiohttp.FormData()
        form.add_field('json', '1')
        form.add_field('anonymous', str(self.anonymous))
        form.add_field('file', filename=name, value=content)

        async with aiohttp.ClientSession() as session:
            async with session.post('https://dps.report/uploadContent', data=form) as response:
                data = await response.json()
                return Report(**data)
