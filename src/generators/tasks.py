import random
from datetime import timedelta

from faker import Faker

from utils.random_utils import generate_uuid, random_bool
from utils.dates import (
    random_past_datetime,
    random_due_date,
    completion_datetime
)

fake = Faker()


def generate_tasks(conn, projects, sections, users, avg_tasks_per_project=250, subtask_ratio=0.25):
    """
    Generates tasks and subtasks for each project.
    """
    cursor = conn.cursor()
    tasks = []

    # Map project_id -> sections
    sections_by_project = {}
    for section in sections:
        sections_by_project.setdefault(section["project_id"], []).append(section)

    # Map team_id -> users
    users_by_team = {}
    for user in users:
        users_by_team.setdefault(user.get("team_id", None), []).append(user)

    for project in projects:
        project_sections = sections_by_project.get(project["project_id"], [])
        if not project_sections:
            continue

        num_tasks = random.randint(
            int(avg_tasks_per_project * 0.8),
            int(avg_tasks_per_project * 1.2)
        )

        project_tasks = []

        for _ in range(num_tasks):
            task_id = generate_uuid()
            section = random.choice(project_sections)

            created_at = random_past_datetime(months_back=6)

            # Assignee logic (~15% unassigned)
            assignee_id = None
            if random_bool(0.85):
                assignee = random.choice(users)
                assignee_id = assignee["user_id"]

            due_date = random_due_date(created_at)

            # Completion logic
            completed = random_bool(0.65)
            completed_at = completion_datetime(created_at) if completed else None

            name = fake.sentence(nb_words=5).rstrip(".")
            description = (
                fake.paragraph(nb_sentences=3)
                if random_bool(0.8)
                else None
            )

            cursor.execute(
                """
                INSERT INTO tasks (
                    task_id, project_id, section_id, parent_task_id,
                    name, description, assignee_id, due_date,
                    completed, created_at, completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    project["project_id"],
                    section["section_id"],
                    None,
                    name,
                    description,
                    assignee_id,
                    due_date,
                    int(completed),
                    created_at,
                    completed_at
                )
            )

            task_record = {
                "task_id": task_id,
                "project_id": project["project_id"],
                "section_id": section["section_id"],
                "created_at": created_at
            }

            project_tasks.append(task_record)
            tasks.append(task_record)

        # Subtasks (~25%)
        num_subtasks = int(len(project_tasks) * subtask_ratio)

        for _ in range(num_subtasks):
            parent_task = random.choice(project_tasks)

            subtask_id = generate_uuid()
            created_at = parent_task["created_at"] + timedelta(days=random.randint(0, 3))

            name = fake.sentence(nb_words=4).rstrip(".")
            description = fake.sentence(nb_words=10)

            completed = random_bool(0.75)
            completed_at = completion_datetime(created_at) if completed else None

            cursor.execute(
                """
                INSERT INTO tasks (
                    task_id, project_id, section_id, parent_task_id,
                    name, description, assignee_id, due_date,
                    completed, created_at, completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    subtask_id,
                    parent_task["project_id"],
                    parent_task["section_id"],
                    parent_task["task_id"],
                    name,
                    description,
                    None,
                    None,
                    int(completed),
                    created_at,
                    completed_at
                )
            )

            tasks.append({
                "task_id": subtask_id,
                "project_id": parent_task["project_id"],
                "section_id": parent_task["section_id"],
                "created_at": created_at
            })

    conn.commit()
    return tasks
