CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL DEFAULT 'aluno',
    ativo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS materiais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    quantidade INTEGER NOT NULL DEFAULT 0,
    ativo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    local TEXT,
    status TEXT NOT NULL DEFAULT 'online'
);

CREATE TABLE IF NOT EXISTS tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT NOT NULL UNIQUE,
    usuario_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    maquina_id INTEGER,
    criado_em TEXT NOT NULL,
    expira_em TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'disponivel',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (material_id) REFERENCES materiais(id),
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
);

CREATE TABLE IF NOT EXISTS retiradas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id INTEGER NOT NULL UNIQUE,
    usuario_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    maquina_id INTEGER NOT NULL,
    data_hora TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'concluida',
    FOREIGN KEY (token_id) REFERENCES tokens(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (material_id) REFERENCES materiais(id),
    FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
);
