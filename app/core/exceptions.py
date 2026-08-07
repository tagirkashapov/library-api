class EntityNotFound(Exception):
    def __init__(self, entity: str, id: int):
        self.entity = entity
        self.id = id
        super().__init__(f"{entity} with id {id} not found")


class NoFieldsToUpdate(Exception):
    def __init__(self, entity: str):
        self.entity = entity
        super().__init__(f"No fields provided to update {entity}")
