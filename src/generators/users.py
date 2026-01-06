import random
from datetime import timedelta

from faker import Faker

from utils.random_utils import generate_uuid, weighted_choice, random_bool
from utils.dates import get_now

fake = Faker()

ROLES = ["IC", "Manager", "Executive"]
ROLE_WEIGHTS = [0.75, 0.20, 0.05]


def generate_users(conn, organization, num_users):
    """
    Generates users (employees) for the organization.
    """
    users = []
    cursor = conn.cursor()
    now = get_now()

    for _ in range(num_users):
        user_id = generate_uuid()

        full_name = fake.name()
        base_email = (
            full_name.lower()
            .replace(" ", ".")
            .replace("'", "")
        )

        # Add randomness to ensure uniqueness
        email = f"{base_email}.{user_id[:6]}@{organization['domain']}"



        role = weighted_choice(ROLES, ROLE_WEIGHTS)

        # Users joined over the past several years
        created_at = now - timedelta(days=random.randint(30, 5 * 365))

        # ~90% users are active
        is_active = 1 if random_bool(0.90) else 0

        cursor.execute(
            """
            INSERT INTO users (user_id, full_name, email, role, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                full_name,
                email,
                role,
                created_at,
                is_active
            )
        )

        users.append({
            "user_id": user_id,
            "full_name": full_name,
            "email": email,
            "role": role,
            "created_at": created_at,
            "is_active": is_active
        })

    conn.commit()
    return users
