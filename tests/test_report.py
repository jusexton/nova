import pytest

from nova.report import format_report, format_duration
from nova.report.types import Encounter, Report, Player


@pytest.mark.parametrize('duration,expected', [
    (100, '**1** minute and **40** seconds'),
    (100.54, '**1** minute and **40** seconds'),
    (240, '**4** minutes and **0** seconds'),
    (241, '**4** minutes and **1** second')
])
def test_format_duration(duration: float, expected: str):
    actual = format_duration(duration)
    assert actual == expected


def test_format_report():
    report = Report(
        id='test-id',
        permalink='test-permalink',
        encounter=Encounter(
            success=True,
            duration=100.56,
            boss='test-boss',
            isCm=False
        ),
        players={
            'player-one': Player(
                profession=2,
                elite_spec=68,
                display_name='test-player'
            ),
            'player-two': Player(
                profession=2,
                elite_spec=56,
                display_name='another-test-player'
            )
        }
    )

    actual_message = format_report(report)
    expected_message = (
        '## Report\n'
        'The full published report can be found here test-permalink.\n'
        '### Encounter\n'
        'Name: test-boss\n'
        'Status: :white_check_mark:\n'
        'Duration: **1** minute and **40** seconds\n'
        '### Players\n'
        ':crossed_swords: test-player\n'
        ':crossed_swords: another-test-player'
    )

    assert actual_message == expected_message
