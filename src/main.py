from fastapi.staticfiles import StaticFiles
from auth.router import router as auth_router
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wallets.router import router as wallets_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(wallets_router)

app.include_router(router)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
