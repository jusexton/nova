import re
import shelve
import uuid

import discord
from discord import Interaction
from discord.ui import Select, Button

from nova.extensions.gw2.types import Team, EventType, TeamMember


def format_team(team: Team) -> str:
    team_members = '\n'.join(f'{index + 1}. {member.name}' for index, member in enumerate(team.members))
    slots = '\n'.join(f'{index}.' for index in range(len(team.members) + 1, team.count + 1))
    return (
        f'Team ID: {team.id}\n'
        f'A team for {team.event_type} is being formed!\n'
        f'{team_members}\n'
        f'{slots}'
    )


class TeamLimitError(Exception):
    def __init__(self, limit: int):
        self.limit = limit


class DuplicateTeamMemberError(Exception):
    pass


class TeamService:
    db_loc = 'teams'

    def get_team(self, _id: str) -> Team | None:
        with shelve.open(self.db_loc) as db:
            return db.get(_id)

    def create_team(self, event_type: EventType, role_selection: bool) -> Team:
        _id = str(uuid.uuid4())[:8]
        team = Team(id=_id, event_type=event_type, role_selection=role_selection)
        with shelve.open(self.db_loc) as db:
            db[_id] = team

        return team

    def update_team(self, interaction: Interaction) -> Team:
        _id = self._extract_team_id(interaction.message.content)
        team = self.get_team(_id)

        member_name = self._validate_new_member(interaction, team)
        team_member = TeamMember(name=member_name)
        team.members.append(team_member)
        with shelve.open(self.db_loc) as db:
            db[_id] = team

        return team

    @staticmethod
    def _extract_team_id(content: str) -> str:
        return re.match(r'^Team ID: ([a-zA-Z0-9]+)', content)[1]

    @staticmethod
    def _validate_new_member(interaction: Interaction, team: Team) -> str | None:
        if len(team.members) == team.event_type.member_limit():
            raise TeamLimitError()

        member_name = interaction.user.display_name
        if team.contains(member_name):
            raise DuplicateTeamMemberError()

        return member_name


class SimpleTeamView(discord.ui.View):
    def __init__(self, team: Team, team_service: TeamService):
        super().__init__(timeout=None)
        self.team = team
        self.team_service = team_service

    @discord.ui.button(label='Im in!')
    async def on_click(self, _: Button, interaction: Interaction):
        await interaction.response.defer()
        updated_team = self.team_service.update_team(interaction)
        content = format_team(updated_team)
        view = SimpleTeamView(updated_team, self.team_service)
        await interaction.edit_original_response(content=content, view=view)


class RoleSelectTeamView(discord.ui.View):
    def __init__(self, team: Team, team_service: TeamService):
        super().__init__(timeout=None)
        self.team = team
        self.team_service = team_service

    @discord.ui.select(
        placeholder='Role',
        options=[
            discord.SelectOption(label="DPS"),
            discord.SelectOption(label='Q-DPS'),
            discord.SelectOption(label='A-DPS'),
            discord.SelectOption(label='Q-Heal'),
            discord.SelectOption(label='A-Heal'),
            discord.SelectOption(label="Any")
        ]
    )
    async def on_select(self, _: Select, interaction: Interaction):
        await interaction.response.defer()
        updated_team = self.team_service.update_team(interaction)
        content = format_team(updated_team)
        view = RoleSelectTeamView(updated_team, self.team_service)
        await interaction.edit_original_response(content=content, view=view)
