from fastapi import FastAPI


app = FastAPI()


@app.get("/get-friends/{profile_id}")
async def get_friends(profile_id: int) -> list[dict]:
    return []
