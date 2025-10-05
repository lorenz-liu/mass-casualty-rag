from system.db import VectorDatabase

if __name__ == "__main__":
    db = VectorDatabase()
    db.inject(
        documents=[
            "The person's name is Zhaoxun.",
            "The person's age is 30.",
            "The person's occupation is software engineer.",
        ]
    )
    print(db.query(["job"], n_results=2))
