class EntityNotFound(Exception):
    def __init__(self, entity: str, id: int | set[int]):
        self.entity = entity
        self.id = id
        super().__init__(f"{entity}(s) with id(s)={id} not found")


class NoFieldsToUpdate(Exception):
    def __init__(self, entity: str):
        self.entity = entity
        super().__init__(f"No fields provided for {entity} update")
