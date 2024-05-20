from fastapi import FastAPI

from app.tasks.handlers import router as tasks_router
from app.users.user.handlers import router as users_router
from app.users.auth.handlers import router as auth_router


app = FastAPI()



app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(auth_router)
