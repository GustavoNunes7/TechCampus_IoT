# TechCampus IoT

Servidor Python responsável pela camada IoT do TechCampus.

## Função

- gerar tokens temporários;
- validar tokens;
- controlar estoque;
- controlar máquinas;
- registrar retiradas;
- integrar o sistema TechCampus com ESP8266 por HTTP/JSON.

## Fluxo

TechCampus (Node.js) -> TechCampus IoT (Flask + SQLite) -> ESP8266

## Instalação

python -m venv venv

Windows:
venv\Scripts\activate

pip install -r requirements.txt

Copie .env.example para .env e configure as chaves.

Execute:

python run.py

Servidor:
http://localhost:5000

## Endpoints

GET /api/health
POST /api/solicitacoes
GET /api/tokens/<token>
GET /api/estoque
GET /api/estoque/<material_id>
GET /api/maquinas
GET /api/maquinas/<maquina_id>
POST /api/iot/validar-token
POST /api/iot/retirada

As duas rotas /api/iot/* exigem o cabeçalho X-IoT-Key.

O banco SQLite é criado automaticamente e não deve ser enviado ao GitHub.
