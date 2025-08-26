# security.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Clave secreta para firmar los tokens (en producción, guárdala en variables de entorno)
SECRET_KEY = "mi_clave_secreta_super_segura"
ALGORITHM = "HS256"

# Simulación de un esquema de autenticación por token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para verificar el token y extraer el usuario
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario = payload.get("sub")
        if usuario is None:
            raise credenciales_invalidas()
        return usuario
    except JWTError:
        raise credenciales_invalidas()

def credenciales_invalidas():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
