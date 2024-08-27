from fastapi import FastAPI
from pydantic import BaseModel

from db import driver


app = FastAPI()


class ShortestConnection(BaseModel):
    from_id: int
    to_id: int


@app.get("/get-friends/{profile_id}")
async def get_friends(profile_id: int) -> list[int]:
    result = driver.execute_query(
        """
        MATCH (profile:Profile {id: $id})-[:FRIEND]-(friend)
        RETURN friend
        """, id=profile_id
    )
    try:
        friend_ids = list(set(map(lambda rec: rec[0]._properties['id'], result.records)))
    except Exception as e:
        print(f'An error occurred while mapping friend ids: \n {e}')
        return []

    return friend_ids


@app.post("/find-shortest-connection")
async def get_shortest_connection(connection: ShortestConnection) -> list[int]:
    result = driver.execute_query(
        """
        MATCH (start:Profile {id: $from_id}), (end:Profile {id: $to_id}), 
        p = shortestPath((start)-[:FRIEND*]-(end)) 
        RETURN p
        """, from_id=connection.from_id, to_id=connection.to_id
    )
    try:
        friend_ids = list(map(lambda node: node._properties['id'], result.records[0][0]._nodes))
    except Exception as e:
        print(f'An error occurred while mapping friend ids: \n {e}')
        return []

    return friend_ids
