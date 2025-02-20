"""Module for handling Neo4j database connections and queries"""

import json
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DB


class Neo4jConnection:
    """Class for handling Neo4j database connections and queries"""

    def __init__(self, uri, user, password):
        """Initialize Neo4j connection with credentials

        Args:
            uri (str): Neo4j database URI
            user (str): Username for authentication
            password (str): Password for authentication
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the Neo4j driver connection if it exists"""
        if self.driver is not None:
            self.driver.close()

    # Метод, который передает запрос в БД
    def query(self, query, db=None):
        """Execute a Cypher query against the Neo4j database

        Args:
            query (str): Cypher query to execute
            db (str, optional): Database name to query. Defaults to None.

        Returns:
            list: Results of the query execution
        """
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = (
                self.driver.session(database=db)
                if db is not None
                else self.driver.session()
            )
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


connection = Neo4jConnection(uri=NEO4J_URI, user=NEO4J_USER, password=NEO4J_PASSWORD)

try:
    print(f"Trying to connect to Neo4j ({NEO4J_URI})")
    connection.driver.verify_connectivity()
    print("Connected to Neo4j")
except:
    print("Cannot connect to Neo4J")


def get_path_between_nodes(sourceNode_elementID: str, destNode_elementID: str):
    """Find the shortest path between two nodes

    Args:
        sourceNode_elementID (str): Element ID of the source node
        destNode_elementID (str): Element ID of the destination node

    Returns:
        list: List of nodes on the shortest path from source to destination
    """
    query_string = f"""
    MATCH (source:landmark),(target:landmark)
    WHERE elementId(source) = '{sourceNode_elementID}' AND elementId(target) = '{destNode_elementID}'
    MATCH p = shortestPath((source)-[*]-(target))
    return p;
    """
    response = connection.query(query_string, db=NEO4J_DB)
    return response[0]["p"].nodes