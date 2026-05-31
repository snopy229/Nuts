from ninja import Schema


class Select2Option(Schema):
    id: int | str
    text: str


class Select2Response(Schema):
    results: list[dict]
    pagination: dict = {"more": False}
