import random

from utils.random_utils import generate_uuid, random_subset


TAG_VOCABULARY = [
    "bug",
    "urgent",
    "backend",
    "frontend",
    "design",
    "follow-up",
    "customer-request",
    "blocked",
    "performance",
    "campaign",
    "content",
    "compliance"
]


def generate_tags(conn, tasks):
    """
    Generates tags and assigns them to tasks.
    """
    cursor = conn.cursor()

    # -------------------------
    # Insert tags
    # -------------------------
    tag_id_map = {}

    for tag_name in TAG_VOCABULARY:
        tag_id = generate_uuid()
        tag_id_map[tag_name] = tag_id

        cursor.execute(
            """
            INSERT INTO tags (tag_id, name)
            VALUES (?, ?)
            """,
            (tag_id, tag_name)
        )

    # -------------------------
    # Assign tags to tasks
    # -------------------------
    for task in tasks:
        # ~30% of tasks receive tags
        if random.random() > 0.30:
            continue

        # Most tasks get 1 tag, few get multiple
        selected_tags = random_subset(list(tag_id_map.values()), max_items=3)

        for tag_id in selected_tags:
            cursor.execute(
                """
                INSERT INTO task_tags (task_id, tag_id)
                VALUES (?, ?)
                """,
                (task["task_id"], tag_id)
            )

    conn.commit()
