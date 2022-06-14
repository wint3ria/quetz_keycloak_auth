from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/api/keycloak_auth"
)
def get_keycloak_auth():

    return {"message": "Hello world!"}
