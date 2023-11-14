import aiohttp

from nova.extensions.gw2.types import Report
from nova.util import SessionContextManager

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


def format_report(report: Report):
    encounter = report.encounter
    duration = format_duration(encounter.duration)
    status = ':white_check_mark:' if encounter.success else ':x:'
    players = '\n'.join(
        f':crossed_swords: {player.display_name}'
        for player in report.players.values()
    )

    return (
        f'## Report\n'
        f'The full published report can be found here {report.permalink}.\n'
        '### Encounter\n'
        f'Name: {encounter.boss}\n'
        f'Status: {status}\n'
        f'Duration: {duration}\n'
        '### Players\n'
        f'{players}'
    )


def format_duration(duration: float) -> str:
    minutes, seconds = divmod(int(duration), 60)
    minute_desc = 'minutes' if minutes != 1 else 'minute'
    second_desc = 'seconds' if seconds != 1 else 'second'
    return f'**{minutes}** {minute_desc} and **{seconds}** {second_desc}'
