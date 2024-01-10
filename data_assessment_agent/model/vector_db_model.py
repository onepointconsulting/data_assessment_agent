from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import EmbeddingFunctionRegistry

registry = EmbeddingFunctionRegistry.get_instance()
func = registry.get("openai").create()


class Questions(LanceModel):
    question: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
