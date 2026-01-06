import random
from datetime import timedelta

from utils.dates import get_now
from utils.random_utils import random_subset


def generate_team_memberships(conn, teams, users):
    """
    Assigns users to teams and inserts team memberships.
    """
    cursor = conn.cursor()
    now = get_now()

    team_ids = [team["team_id"] for team in teams]

    for user in users:
        role = user["role"]

        # Decide how many teams a user belongs to
        if role == "IC":
            num_teams = 1
        elif role == "Manager":
            num_teams = random.randint(1, 3)
        else:  # Executive
            num_teams = random.randint(1, 2)

        assigned_team_ids = random_subset(team_ids, num_teams)

        # Ensure at least one team
        if not assigned_team_ids:
            assigned_team_ids = [random.choice(team_ids)]

        for team_id in assigned_team_ids:
            # Join date must be after user and team creation
            joined_at = max(
                user["created_at"],
                now - timedelta(days=random.randint(30, 365))
            )

            cursor.execute(
                """
                INSERT INTO team_memberships (team_id, user_id, joined_at)
                VALUES (?, ?, ?)
                """,
                (team_id, user["user_id"], joined_at)
            )

    conn.commit()
