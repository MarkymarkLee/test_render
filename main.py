from fastapi import FastAPI, HTTPException
from typing import List
import uuid
from queue import Queue

app = FastAPI()

# Global queue to store waiting users
waiting_users: Queue = Queue()

# Dictionary to store paired users and their chat IDs
paired_users = {}


@app.get("/pairUser/{user_id}")
async def pair_user(user_id: str):
    if user_id in paired_users:
        return {"chatId": paired_users[user_id]}

    if not waiting_users.empty():
        paired_user = waiting_users.get()
        chat_id = str(uuid.uuid4())
        paired_users[user_id] = chat_id
        paired_users[paired_user] = chat_id
        return {"chatId": chat_id}
    else:
        waiting_users.put(user_id)
        return {"message": "Waiting for a partner"}


@app.get("/status")
async def get_status():
    return {
        "waiting_users": list(waiting_users.queue),
        "paired_users": paired_users
    }
