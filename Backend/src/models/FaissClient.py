import os
from pathlib import Path
from typing import Any, Dict, List, Union

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document


class FaissClient:
    """
    Helper class for managing local FAISS vector store with Google Gemini embeddings.

    This class handles:
        - Connecting to a persisted FAISS index
        - Adding single or multiple documents
        - Automatic persistence after insertion
        - Lazy initialization of the vector store
    """

    def __init__(self, logger: Any, config: Dict[str, Any], index_path: str = "finbot_index") -> None:
        """
        Initialize FaissClient with logger, configuration, and optional index path.

        Args:
            logger: Logger instance for logging operations.
            config: Configuration dictionary containing model API key and name.
            index_path: Path to store/load FAISS index locally.
        """
        self.__config = config
        self.__logger = logger
        self.index_path = index_path

        # Set API key for Gemini embeddings
        os.environ["GOOGLE_API_KEY"] = self.__config['model']['gemini']['api_key']

        # Initialize embedding model
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=f"models/{self.__config['model']['gemini']['name']}"
        )

        self.vector_store: Union[FAISS, None] = None

    def connect(self) -> None:
        """
        Connect to the FAISS index or create a new one if it does not exist.

        Raises:
            Exception: If FAISS index cannot be loaded or created.
        """
        if self.vector_store is not None:
            self.__logger.info("FAISS index already connected.")
            return

        try:
            if Path(self.index_path).exists():
                self.vector_store = FAISS.load_local(
                    self.index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self.__logger.info(f"Loaded FAISS index from '{self.index_path}' successfully.")
            else:
                # Create empty index
                self.vector_store = FAISS.from_texts([], embedding=self.embeddings)
                self.vector_store.save_local(self.index_path)
                self.__logger.info(f"No existing index found. Created new FAISS index at '{self.index_path}'.")
        except Exception as e:
            self.__logger.exception("Failed to connect or create FAISS index.")
            raise e

    def insert_texts(self, data_list: List[Dict[str, Any]]) -> bool:
        """
        Insert multiple text documents into the FAISS index with metadata.

        Args:
            data_list: List of dictionaries, each containing:
                - 'text': str, the content to embed
                - 'metadata': Optional[dict], metadata associated with the document

        Returns:
            bool: True if insertion succeeds, False otherwise.
        """
        self.connect()

        documents = [
            Document(
                page_content=item['text'],
                metadata=item.get('metadata', {"type": "generic"})
            )
            for item in data_list
        ]

        try:
            result = self.vector_store.add_documents(documents=documents)
            self.vector_store.save_local(self.index_path)
            self.__logger.info(f"Inserted {len(documents)} document(s) into FAISS. IDs: {result}")
            return bool(result)
        except Exception as e:
            self.__logger.exception("Failed to insert documents into FAISS index.")
            self.__logger.error(str(e))
            return False

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """
        Perform a similarity search on the FAISS index.

        Args:
            query: The query string to search for similar documents.
            k: Number of top results to retrieve.

        Returns:
            List[Document]: List of top-k most similar documents.
        """
        self.connect()
        try:
            results = self.vector_store.similarity_search(query, k=k)
            self.__logger.info(f"Retrieved {len(results)} similar document(s) for query: '{query}'")
            source_and_context = {i.id:i.page_content for i in results}
            return source_and_context
        except Exception as e:
            self.__logger.exception("Failed to perform similarity search on FAISS index.")
            self.__logger.error(str(e))
            return []

    def clear_index(self) -> None:
        """Delete all vectors and metadata from FAISS index."""
        try:
            self.vector_store = FAISS.from_texts([], embedding=self.embeddings)
            self.vector_store.save_local(self.index_path)
            self.__logger.info("FAISS index cleared successfully.")
        except Exception as e:
            self.__logger.exception("Failed to clear FAISS index.")
            self.__logger.error(str(e))

