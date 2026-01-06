from utils.random_utils import generate_uuid


SECTIONS_BY_PROJECT_TYPE = {
    "Sprint": ["Backlog", "In Progress", "Review", "Done"],
    "Bug Tracking": ["To Do", "In Progress", "Blocked", "Done"],
    "Campaign": ["Planning", "Drafting", "Review", "Launched"],
    "Content": ["Ideas", "Writing", "Editing", "Published"],
    "Process": ["To Do", "In Progress", "Done"],
    "Compliance": ["Open", "Under Review", "Completed"],
    "Roadmap": ["Planned", "In Progress", "Completed"],
    "Discovery": ["Research", "Validation", "Completed"],
    "Pipeline": ["Leads", "Contacted", "Closed"],
    "Customer Expansion": ["Opportunities", "Negotiation", "Closed"],
    "General": ["To Do", "In Progress", "Done"],
}


def generate_sections(conn, projects):
    """
    Generates sections for each project.
    """
    sections = []
    cursor = conn.cursor()

    for project in projects:
        project_type = project["project_type"]
        section_names = SECTIONS_BY_PROJECT_TYPE.get(
            project_type,
            SECTIONS_BY_PROJECT_TYPE["General"]
        )

        for index, name in enumerate(section_names):
            section_id = generate_uuid()

            cursor.execute(
                """
                INSERT INTO sections (section_id, project_id, name, order_index)
                VALUES (?, ?, ?, ?)
                """,
                (
                    section_id,
                    project["project_id"],
                    name,
                    index
                )
            )

            sections.append({
                "section_id": section_id,
                "project_id": project["project_id"],
                "name": name,
                "order_index": index
            })

    conn.commit()
    return sections
