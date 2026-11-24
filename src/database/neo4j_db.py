import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def get_neo4j_driver():
    if not all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
        raise ValueError("Neo4j credentials missing in .env")

    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )


def verify_connection():
    driver = get_neo4j_driver()
    try:
        driver.verify_connectivity()
        return True
    finally:
        driver.close()


def create_document_node(file_name):
    driver = get_neo4j_driver()

    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (d:Document {file_name: $file_name})
                RETURN d
                """,
                file_name=file_name
            )
        return True
    finally:
        driver.close()