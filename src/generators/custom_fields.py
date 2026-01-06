import random

from utils.random_utils import generate_uuid, random_bool


CUSTOM_FIELDS = [
    {"name": "Priority", "type": "Enum", "values": ["High", "Medium", "Low"], "projects": ["Sprint", "Bug Tracking", "Campaign"]},
    {"name": "Effort", "type": "Number", "values": [1, 2, 3, 4, 5], "projects": ["Sprint"]},
    {"name": "Status", "type": "Enum", "values": ["Blocked", "On Track", "At Risk"], "projects": ["Sprint", "Process"]},
    {"name": "Story Points", "type": "Number", "values": [1, 2, 3, 5, 8], "projects": ["Sprint"]},
    {"name": "Notes", "type": "Text", "values": None, "projects": ["Campaign", "Process"]},
]


def generate_custom_fields(conn, tasks, projects):
    """
    Generates custom field definitions and assigns values to tasks.
    """
    cursor = conn.cursor()

    # -------------------------
    # Insert field definitions
    # -------------------------
    field_id_map = {}

    for field in CUSTOM_FIELDS:
        field_id = generate_uuid()
        field_id_map[field["name"]] = field_id

        cursor.execute(
            """
            INSERT INTO custom_field_definitions
            (field_id, name, field_type, applicable_project_type)
            VALUES (?, ?, ?, ?)
            """,
            (
                field_id,
                field["name"],
                field["type"],
                ",".join(field["projects"])
            )
        )

    # -------------------------
    # Assign values to tasks
    # -------------------------
    project_type_map = {
        project["project_id"]: project["project_type"]
        for project in projects
    }

    for task in tasks:
        # ~50% of tasks get custom fields
        if not random_bool(0.5):
            continue

        project_type = project_type_map.get(task["project_id"])

        for field in CUSTOM_FIELDS:
            if project_type not in field["projects"]:
                continue

            # Not every applicable field is assigned
            if not random_bool(0.7):
                continue

            field_id = field_id_map[field["name"]]

            if field["type"] == "Enum":
                value = random.choice(field["values"])
            elif field["type"] == "Number":
                value = str(random.choice(field["values"]))
            else:  # Text
                value = "Requires follow-up"

            cursor.execute(
                """
                INSERT INTO custom_field_values (task_id, field_id, value)
                VALUES (?, ?, ?)
                """,
                (
                    task["task_id"],
                    field_id,
                    value
                )
            )

    conn.commit()
