from database.connection import get_connection


def salvar_aulas(escola_id, aulas, turma_id=None):
    """Salva uma lista de aulas no banco. Cada aula é um dict com turma_id, professor_id, disciplina_id, dia, periodo."""
    conn = get_connection()
    if turma_id:
        conn.execute("DELETE FROM aulas WHERE escola_id = %s AND turma_id = %s", (escola_id, turma_id))
    else:
        conn.execute("DELETE FROM aulas WHERE escola_id = %s", (escola_id,))
    for a in aulas:
        conn.execute(
            """INSERT INTO aulas (escola_id, turma_id, professor_id, disciplina_id, dia, periodo)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (escola_id, a['turma_id'], a['professor_id'], a['disciplina_id'], a['dia'], a['periodo'])
        )
    conn.commit()
    conn.close()


def listar_aulas(escola_id):
    conn = get_connection()
    rows = conn.execute(
        """SELECT a.*, t.nome AS turma_nome, p.nome AS professor_nome,
                  d.nome AS disciplina_nome, d.cor AS disciplina_cor
           FROM aulas a
           JOIN turmas t ON a.turma_id = t.id
           JOIN professores p ON a.professor_id = p.id
           JOIN disciplinas d ON a.disciplina_id = d.id
           WHERE a.escola_id = %s
           ORDER BY a.turma_id, a.dia, a.periodo""",
        (escola_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mover_aula(aula_id, novo_dia, novo_periodo):
    """Move uma aula para outro dia/período (drag and drop)."""
    conn = get_connection()
    conn.execute(
        "UPDATE aulas SET dia = %s, periodo = %s WHERE id = %s",
        (novo_dia, novo_periodo, aula_id)
    )
    conn.commit()
    conn.close()


def deletar_aulas_escola(escola_id):
    conn = get_connection()
    conn.execute("DELETE FROM aulas WHERE escola_id = %s", (escola_id,))
    conn.commit()
    conn.close()
