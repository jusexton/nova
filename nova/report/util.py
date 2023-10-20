from nova.report.types import Report


def format_duration(duration: float) -> str:
    minutes, seconds = divmod(int(duration), 60)
    minute_desc = 'minutes' if minutes != 1 else 'minute'
    second_desc = 'seconds' if seconds != 1 else 'second'
    return f'**{minutes}** {minute_desc} and **{seconds}** {second_desc}'


def format_report(report: Report) -> str:
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