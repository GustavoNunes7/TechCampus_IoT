def retirar_unidade(connection, material_id):
    cursor=connection.execute(
        "UPDATE materiais SET quantidade=quantidade-1 WHERE id=? AND quantidade>0",
        (material_id,),
    )
    return cursor.rowcount==1
