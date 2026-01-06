import os
from dotenv import load_dotenv

from utils.db import init_db
from generators.team_memberships import generate_team_memberships
from generators.organizations import generate_organization
from generators.teams import generate_teams
from generators.users import generate_users
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.comments import generate_comments
from generators.custom_fields import generate_custom_fields
from generators.tags import generate_tags


def main():
    # Load environment variables
    load_dotenv()

    # Read config values
    db_path = os.getenv("DATABASE_PATH")

    num_teams = int(os.getenv("NUM_TEAMS", 10))
    num_users = int(os.getenv("NUM_USERS", 100))
    num_projects = int(os.getenv("NUM_PROJECTS", 50))

    # Initialize database
    conn = init_db(db_path)

    print("Starting Asana workspace simulation...")

    # Generate core entities
    organization = generate_organization(conn)
    teams = generate_teams(conn, organization, num_teams)
    users = generate_users(conn, organization, num_users)
    generate_team_memberships(conn, teams, users)
    



    # Generate relationships and work structure
    projects = generate_projects(conn, teams, num_projects)
    sections = generate_sections(conn, projects)

    tasks = generate_tasks(conn, projects, sections, users)

    comments = generate_comments(conn, tasks, users)

    generate_custom_fields(conn, tasks, projects)

    generate_tags(conn, tasks)


    conn.close()
    print("Asana simulation database generated successfully.")


if __name__ == "__main__":
    main()
