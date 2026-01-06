from datetime import datetime, timedelta

from utils.random_utils import generate_uuid
from utils.dates import get_now


def generate_organization(conn):
    """
    Generates a single organization and inserts it into the database.
    """
    organization_id = generate_uuid()

    name = "Acme SaaS Inc"
    domain = "acmesaas.com"

    # Organization created several years ago
    created_at = get_now() - timedelta(days=5 * 365)

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO organizations (organization_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (organization_id, name, domain, created_at)
    )
    conn.commit()

    return {
        "organization_id": organization_id,
        "name": name,
        "domain": domain,
        "created_at": created_at,
    }
