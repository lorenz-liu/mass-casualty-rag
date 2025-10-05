import os
from typing import Dict, List, Optional

import chromadb
from chromadb.config import Settings

from toolkit.converter import MarkdownConverter


class VectorDatabase:
    def __init__(
        self,
        persist_directory: str = "./persistent_db",
        collection_name: str = "documents",
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory, settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def inject(
        self,
        *,
        documents: Optional[List[str]] = None,
        source_path: Optional[str] = None,
    ) -> None:
        """
        Inject documents into the database either directly or from a file converter.
        Skips documents with duplicate IDs.

        Args:
            documents: List of text documents to add directly
            source_path: Path to source file to convert (mutually exclusive with documents)
        """
        if documents is not None and source_path is not None:
            raise ValueError("Cannot specify both 'documents' and 'source_path'")

        if source_path is not None:
            doc_id = f"doc_{os.path.basename(source_path)}"

            # Check if document already exists
            existing = self.collection.get(ids=[doc_id])
            if existing["ids"]:
                return  # Skip if already exists

            converted_text = MarkdownConverter.convert(source_path)
            metadata = {
                "source": source_path,
                "filename": os.path.basename(source_path),
            }
            self.collection.add(
                documents=[converted_text], metadatas=[metadata], ids=[doc_id]
            )
        elif documents is not None:
            ids = [f"doc_{i}" for i in range(len(documents))]

            # Check existing IDs and filter out duplicates
            existing = self.collection.get(ids=ids)
            existing_ids = set(existing["ids"])

            new_docs = []
            new_ids = []
            for doc, doc_id in zip(documents, ids):
                if doc_id not in existing_ids:
                    new_docs.append(doc)
                    new_ids.append(doc_id)

            if new_docs:
                self.collection.add(documents=new_docs, ids=new_ids)
        else:
            raise ValueError("Must provide either 'documents' or 'source_path'")

    def query(
        self, query_texts: List[str], n_results: int = 3, where: Optional[Dict] = None
    ) -> Dict:
        return self.collection.query(
            query_texts=query_texts, n_results=n_results, where=where
        )

    def delete_collection(self) -> None:
        self.client.delete_collection(name=self.collection.name)

    def count(self) -> int:
        return self.collection.count()
