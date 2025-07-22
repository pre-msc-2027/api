from fastapi import APIRouter, Request, Response, status
from fastapi.responses import RedirectResponse
import httpx
import os
import dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.get("/github")
async def github_oauth(request: Request):
    state = os.uradom(8).hex()
    request.session['oauth_state'] = state
    scope = "repo"
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={os.getenv('CLIENT_ID')}"
        f"&redirect_uri={os.getenv('REDIRECT_URI')}"
        f"&scope={scope}"
        f"&state={state}"
    )
    return RedirectResponse(url=github_auth_url)

@router.get("/callback")
async def github_callback(request: Request, code: str = None,):
    if not code:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Missing code parameter")
    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": os.getenv("CLIENT_ID"),
                    "client_secret": os.getenv("CLIENT_SECRET"),
                    "code": code,
                    "redirect_uri": os.getenv("REDIRECT_URI"),
                    "state": state,
                },
                headers={"Accept": "application/json"},
            )
            token_data = token_response.json()
            if "error" in token_data:
                return Response(status_code=status.HTTP_400_BAD_REQUEST, content=token_data["error_description"])
            access_token = token_data["access_token"]
            return {"access_token": access_token}
    except Exception as e:
        return Response(content=f"Erreur serveur: {str(e)}", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)