from app import create_app
from app.database.database import get_db

app = create_app()

with app.app_context():
    db = get_db()

    db.execute(
        """
        INSERT OR IGNORE INTO usuarios (id, nome, matricula, tipo, ativo)
        VALUES (1, 'Gustavo Nunes', '2026001', 'aluno', 1)
        """
    )

    db.execute(
        """
        INSERT OR IGNORE INTO materiais (id, nome, descricao, quantidade, ativo)
        VALUES (1, 'Kit Arduino', 'Kit para atividades de IoT', 10, 1)
        """
    )

    db.execute(
        """
        INSERT OR IGNORE INTO maquinas (id, codigo, nome, local, status)
        VALUES (1, 'MAQ-01', 'Dispenser IoT 01', 'Laboratório de IoT', 'online')
        """
    )

    db.commit()
    db.close()

    print("Dados de demonstração cadastrados com sucesso.")
    print("Aluno: ID 1 - Gustavo Nunes")
    print("Material: ID 1 - Kit Arduino - Estoque: 10")
    print("Máquina: ID 1 - MAQ-01")
