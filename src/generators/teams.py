import random
from datetime import timedelta

from utils.random_utils import generate_uuid, weighted_choice
from utils.dates import get_now


TEAM_NAME_PREFIXES = [
    "Payments",
    "Billing",
    "Platform",
    "Infrastructure",
    "Growth",
    "Analytics",
    "Marketing",
    "Content",
    "Sales",
    "Customer Support",
    "Operations",
    "Finance",
    "Security",
    "Mobile",
    "Web"
]

TEAM_FUNCTIONS = [
    "Engineering",
    "Marketing",
    "Operations",
    "Product",
    "Sales"
]

TEAM_FUNCTION_WEIGHTS = [0.45, 0.20, 0.15, 0.10, 0.10]


def generate_teams(conn, organization, num_teams):
    """
    Generates teams for the organization.
    """
    teams = []
    cursor = conn.cursor()
    now = get_now()

    for _ in range(num_teams):
        team_id = generate_uuid()

        function = weighted_choice(TEAM_FUNCTIONS, TEAM_FUNCTION_WEIGHTS)
        prefix = random.choice(TEAM_NAME_PREFIXES)
        name = f"{prefix} {function}"

        # Teams created over the past several years
        created_at = now - timedelta(days=random.randint(180, 4 * 365))

        cursor.execute(
            """
            INSERT INTO teams (team_id, organization_id, name, function, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                team_id,
                organization["organization_id"],
                name,
                function,
                created_at
            )
        )

        teams.append({
            "team_id": team_id,
            "organization_id": organization["organization_id"],
            "name": name,
            "function": function,
            "created_at": created_at
        })

    conn.commit()
    return teams
