RAG_FIELDS = [
    "id",
    "name",
    "country",
    "location",
    "highlight",
    "Fees",
    "FeesInNumber",
    "FeesStructure",
    "isMBBS",
    "isStudyAbroad",
]


def has_rag_relevant_changes(
    before: dict,
    after: dict,
) -> bool:
    for field in RAG_FIELDS:
        before_value = before.get(field)
        after_value = after.get(field)

        if before_value != after_value:
            return True

    return False