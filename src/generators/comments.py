import random
from datetime import timedelta

from faker import Faker

from utils.random_utils import generate_uuid
from utils.dates import get_now

fake = Faker()


def generate_comments(conn, tasks, users):
    """
    Generates comments for a subset of tasks.
    """
    cursor = conn.cursor()
    comments = []
    now = get_now()

    for task in tasks:
        # ~35% of tasks receive comments
        if random.random() > 0.35:
            continue

        num_comments = random.choice([1, 1, 2, 2, 3])

        for _ in range(num_comments):
            comment_id = generate_uuid()
            author = random.choice(users)

            # Comment must be after task creation
            created_at = task["created_at"] + timedelta(
                days=random.randint(0, 7),
                seconds=random.randint(0, 3600)
            )

            content = fake.sentence(nb_words=random.randint(6, 14))

            cursor.execute(
                """
                INSERT INTO comments (comment_id, task_id, author_id, content, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    comment_id,
                    task["task_id"],
                    author["user_id"],
                    content,
                    created_at
                )
            )

            comments.append({
                "comment_id": comment_id,
                "task_id": task["task_id"],
                "author_id": author["user_id"],
                "created_at": created_at
            })

    conn.commit()
    return comments
