from langchain_core.documents import Document


def create_university_document(university: dict) -> Document:
    study_types = []

    if university.get("is_mbbs"):
        study_types.append("MBBS")

    if university.get("is_study_abroad"):
        study_types.append("Study Abroad")

    study_type = ", ".join(study_types) or "Not specified"

    content = f"""
University Name: {university.get("name", "Not available")}

Country: {university.get("country", "Not available")}

Location: {university.get("location", "Not available")}

Educationopedia Highlight:
{university.get("highlight", "Not available")}

Study Type:
{study_type}

Fee Information:
{university.get("fees", "Not available")}

Minimum Fee:
{university.get("fees_min", "Not available")}

Maximum Fee:
{university.get("fees_max", "Not available")}

Total Estimated Fee:
{university.get("fees_total", "Not available")}

Fee Structure:
{university.get("fees_structure", "Not available")}
"""

    metadata = {
        "university_id": university.get("id"),
        "university_name": university.get("name"),
        "country": university.get("country"),
        "is_mbbs": university.get("is_mbbs", False),
        "is_study_abroad": university.get("is_study_abroad", False),
    }

    return Document(
        page_content=content.strip(),
        metadata=metadata,
    )