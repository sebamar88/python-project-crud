import os
import ssl
from urllib.parse import urlparse
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL no definido en el entorno")

# --- 🔧 Limpiar la URL eliminando todo lo que viene después del '?' ---
parsed = urlparse(db_url)
clean_db_url = f"{parsed.scheme}://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port or 5432}{parsed.path}"

# --- 🔄 Cambiar el driver a asyncpg ---
engine_url = clean_db_url.replace("postgresql://", "postgresql+asyncpg://")

# --- 🔐 Configurar SSL (requerido por Neon/Supabase) ---
ssl_context = ssl.create_default_context()

engine = create_async_engine(
    engine_url,
    echo=True,
    connect_args={"ssl": ssl_context},
)

# --- 🧠 Session factory ---
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
