import random
from datetime import timedelta

from utils.random_utils import generate_uuid, weighted_choice
from utils.dates import get_now


PROJECT_TYPES_BY_FUNCTION = {
    "Engineering": (["Sprint", "Bug Tracking"], [0.7, 0.3]),
    "Marketing": (["Campaign", "Content"], [0.7, 0.3]),
    "Operations": (["Process", "Compliance"], [0.6, 0.4]),
    "Product": (["Roadmap", "Discovery"], [0.6, 0.4]),
    "Sales": (["Pipeline", "Customer Expansion"], [0.6, 0.4]),
}

PROJECT_STATUSES = ["Active", "Completed", "Archived"]
PROJECT_STATUS_WEIGHTS = [0.6, 0.25, 0.15]


def generate_projects(conn, teams, num_projects):
    """
    Generates projects and assigns them to teams.
    """
    projects = []
    cursor = conn.cursor()
    now = get_now()

    for _ in range(num_projects):
        project_id = generate_uuid()

        team = random.choice(teams)
        function = team["function"]

        project_types, weights = PROJECT_TYPES_BY_FUNCTION.get(
            function,
            (["General"], [1.0])
        )

        project_type = weighted_choice(project_types, weights)

        name = f"{project_type} Project"

        created_at = now - timedelta(days=random.randint(0, 180))

        # Older projects more likely archived
        status = weighted_choice(
            PROJECT_STATUSES,
            PROJECT_STATUS_WEIGHTS
        )

        cursor.execute(
            """
            INSERT INTO projects (
                project_id, team_id, name,
                project_type, status, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                team["team_id"],
                name,
                project_type,
                status,
                created_at
            )
        )

        projects.append({
            "project_id": project_id,
            "team_id": team["team_id"],
            "project_type": project_type,
            "status": status,
            "created_at": created_at
        })

    conn.commit()
    return projects
