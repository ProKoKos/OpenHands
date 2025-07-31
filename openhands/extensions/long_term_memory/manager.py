import chromadb
from openhands.core.logger import openhands_logger as logger

class LongTermMemoryManager:
    def __init__(self, session_id: str):
        logger.info("Initializing LongTermMemoryManager...")
        self.collection_name = f"session_{session_id.replace('-', '_')}"

        try:
            # Простое подключение к клиенту
            self.client = chromadb.HttpClient(host='chroma', port=8000)

            # Проверка связи с сервером
            self.client.heartbeat()
            logger.info("Successfully connected to ChromaDB.")

            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            logger.info(f"Got or created collection '{self.collection_name}'.")

        except Exception as e:
            logger.error(f"Failed to connect to ChromaDB: {e}")
            raise

    def add_memory(self, content: str, metadata: dict):
        try:
            doc_id = str(self.collection.count())
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
        except Exception as e:
            logger.error(f"Failed to add memory to ChromaDB: {e}")

    def search_memory(self, query: str, n_results: int = 5) -> list:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results.get('documents', [[]])[0]
        except Exception as e:
            logger.error(f"Failed to search memory in ChromaDB: {e}")
            return []
