from fastapi import APIRouter

from app.api.v1.endpoints import users, tasks, auth
#from tests.test_api import tasks as test_Tasks, users as test_Users 
#TODO - ADD TESTS

api_router = APIRouter()

api_router.include_router(users.router, 
                          prefix="/users", 
                          tags=["users"])

api_router.include_router(tasks.router, 
                          prefix="/tasks", 
                          tags=["tasks"])

api_router.include_router(auth.router, 
                          prefix="/auth", 
                          tags=["authentication"])

#api_router.include_router(test_Tasks, 
#                          prefix="/test", 
#                          tags=["tasks",
#                                "test"])

#api_router.include_router(test_Users, 
#                          prefix="/test", 
#                          tags=["users",
#                                "test"])