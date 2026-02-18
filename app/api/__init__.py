from app.api.auth.login_api import auth_router
from app.api.user.user_api import user_router
from app.api.song.song_api import song_router
__all__ = ["auth_router", "user_router", "song_router"]
