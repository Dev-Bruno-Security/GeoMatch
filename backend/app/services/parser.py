import io
import re
import pandas as pd


def read_csv_addresses(content: bytes):
    df = pd.read_csv(io.BytesIO(content))
    col_candidates = ["address", "endereco", "logradouro", "rua"]
    col = next((c for c in col_candidates if c in df.columns), None)
    if not col:
        raise ValueError(f"Coluna de endereço não encontrada. Use uma das: {col_candidates}")
    return [str(v) for v in df[col].tolist()]


def parse_sql_addresses(sql_text: str):
    # Parser simples: localiza strings entre aspas dentro de VALUES (... 'address' ...)
    # Aceita aspas simples e duplas, mas prefere simples.
    # Exemplos de linhas suportadas:
    # INSERT INTO input_addresses(address) VALUES ('Avenida Paulista, 1000, São Paulo, SP');
    # Ou: INSERT INTO ... VALUES (1, 'Rua X 123', ...);
    addresses = []
    # Extrai texto entre aspas, evitando aspas escapadas
    # Também procura nomes de colunas comuns após INSERT INTO ... (address|endereco|logradouro|rua)
    # Se não houver estrutura, fallback para qualquer string entre aspas que se pareça com endereço.

    insert_regex = re.compile(r"INSERT\s+INTO\s+.*?VALUES\s*\((.*?)\)\s*;?", re.IGNORECASE | re.DOTALL)
    quoted_regex = re.compile(r"'(?:[^']|''|\\')+'|\"(?:[^\"]|\\\")+\"")

    for m in insert_regex.finditer(sql_text):
        inner = m.group(1)
        # Find all quoted values in the VALUES list
        qs = quoted_regex.findall(inner)
        for q in qs:
            # Remove aspas e faz unescape
            if q.startswith("'") and q.endswith("'"):
                val = q[1:-1].replace("''", "'")
            elif q.startswith('"') and q.endswith('"'):
                val = q[1:-1].replace('\"', '"')
            else:
                continue
            # Heurística: provavelmente é endereço se contém letras + dígitos ou separadores comuns
            if re.search(r"[a-zA-Z]", val) and re.search(r"\d", val):
                addresses.append(val)
                break  # assume que a primeira string adequada entre aspas é o endereço

    if not addresses:
        # Fallback: qualquer string entre aspas, linha por linha (ex: um endereço por linha)
        for q in quoted_regex.findall(sql_text):
            if q.startswith("'") and q.endswith("'"):
                val = q[1:-1].replace("''", "'")
            elif q.startswith('"') and q.endswith('"'):
                val = q[1:-1].replace('\"', '"')
            else:
                continue
            if re.search(r"[a-zA-Z]", val) and re.search(r"\d", val):
                addresses.append(val)

    if not addresses:
        raise ValueError("Não foi possível extrair endereços do SQL enviado.")

    return addresses
