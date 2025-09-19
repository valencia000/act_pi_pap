from src.database import Base, engine
from src.models import User, PQRS  # Importar todos los modelos

def create_tables():
    print("🔄 Creando tablas en la base de datos...")
    try:
        Base.metadata.drop_all(bind=engine)  # Eliminar tablas existentes
        Base.metadata.create_all(bind=engine)  # Crear nuevas tablas
        print("✅ Tablas creadas exitosamente!")
        print("📋 Tablas disponibles:")
        print("   - users (autenticación)")
        print("   - pqrs (sistema PQRS)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_tables()