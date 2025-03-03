# tests/dummies.py

class DummyCursor:
    """
    Simula un cursor asíncrono para iterar sobre una lista de documentos.
    """
    def __init__(self, docs):
        self.docs = docs
        self.index = 0

    def skip(self, n: int):
        self.docs = self.docs[n:]
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.index >= len(self.docs):
            raise StopAsyncIteration
        doc = self.docs[self.index]
        self.index += 1
        return doc


class DummyCollection:
    """
    Simula una colección de MongoDB.
    Proporciona métodos básicos asíncronos para insertar y buscar documentos.
    """
    def __init__(self):
        self.docs = []

    async def insert_one(self, doc: dict):
        # Si no hay _id, asignarlo (por ejemplo, usando el número de documento)
        if "_id" not in doc:
            doc["_id"] = str(len(self.docs) + 1)
        self.docs.append(doc)
        class Result:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return Result(inserted_id=doc["_id"])

    def find(self, query: dict = None):
        if query:
            # Filtrado simple: comprobación de igualdad en cada campo
            filtered = []
            for doc in self.docs:
                match = True
                for key, value in query.items():
                    if doc.get(key) != value:
                        match = False
                        break
                if match:
                    filtered.append(doc)
        else:
            filtered = self.docs
        return DummyCursor(filtered)

    async def find_one(self, query: dict):
        for doc in self.docs:
            match = True
            for key, value in query.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                return doc
        return None
    
    async def update_one(self, query: dict, update: dict):
        # Implementación muy simple: buscar el primer doc que coincida y actualizarlo
        modified_count = 0
        for idx, doc in enumerate(self.docs):
            match = True
            for key, value in query.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                # Se asume que update es {"$set": { ... }}
                for k, v in update.get("$set", {}).items():
                    self.docs[idx][k] = v
                modified_count = 1
                break
        class Result:
            def __init__(self, modified_count):
                self.modified_count = modified_count
        return Result(modified_count)



class DummyDatabase:
    """
    Simula la base de datos MongoDB.
    Permite acceder a colecciones dummy mediante la sintaxis de subíndice o el método get_collection.
    """
    def __init__(self):
        self.collections = {}

    def __getitem__(self, collection_name: str):
        if collection_name not in self.collections:
            self.collections[collection_name] = DummyCollection()
        return self.collections[collection_name]

    def get_collection(self, collection_name: str):
        return self.__getitem__(collection_name)
