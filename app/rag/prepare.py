def prepare_university(university: dict) -> dict:
    fees = university.get("FeesInNumber") or {}

    return {
        "id": university.get("id"),
        "name": university.get("name"),
        "country": university.get("country"),
        "location": university.get("location"),
        "highlight": university.get("highlight"),
        "fees": university.get("Fees"),
        "fees_min": fees.get("min"),
        "fees_max": fees.get("max"),
        "fees_total": fees.get("total"),
        "fees_structure": university.get("FeesStructure"),
        "is_mbbs": university.get("isMBBS", False),
        "is_study_abroad": university.get("isStudyAbroad", False),
    }