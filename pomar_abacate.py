import json
import sqlite3
from datetime import datetime

VARIEDADES = ("Fortuna", "Margarida", "Breda", "Quintal", "Geada")

CLASSIFICACOES = ("A", "B", "C")

talhoes = []
colheitas = []
proximo_id_talhao = 1
proximo_id_colheita = 1


def registrar_log(mensagem):
    with open("log_operacoes.txt", "a", encoding="utf-8") as arq:
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        arq.write(f"[{agora}] {mensagem}\n")


def inicializar_banco():
    conn = sqlite3.connect("pomar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colheitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            talhao_id INTEGER,
            data TEXT,
            qtd_kg REAL,
            classificacao TEXT,
            observacoes TEXT
        )
    """)
    conn.commit()
    conn.close()


def salvar_colheita_banco(colheita):
    conn = sqlite3.connect("pomar.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO colheitas (talhao_id, data, qtd_kg, classificacao, observacoes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        colheita["talhao_id"],
        colheita["data"],
        colheita["qtd_kg"],
        colheita["classificacao"],
        colheita["observacoes"]
    ))
    conn.commit()
    conn.close()


def ler_colheitas_banco():
    conn = sqlite3.connect("pomar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, talhao_id, data, qtd_kg, classificacao, observacoes FROM colheitas")
    linhas = cursor.fetchall()
    conn.close()
    return linhas


def validar_numero_positivo(texto, tipo=int):
    try:
        valor = tipo(texto)
        if valor <= 0:
            return None
        return valor
    except ValueError:
        return None


def validar_data(texto):
    try:
        datetime.strptime(texto, "%Y-%m-%d")
        return texto
    except ValueError:
        return None


def cadastrar_talhao(lista_talhoes):
    global proximo_id_talhao
    print("\n--- CADASTRO DE TALHAO ---")
    nome = input("Nome do talhao: ").strip()
    if not nome:
        print("Nome nao pode ser vazio.")
        return

    print("\nVariedades disponiveis:")
    for i, v in enumerate(VARIEDADES, 1):
        print(f"  {i}. {v}")
    escolha = input("Escolha o numero da variedade: ").strip()
    idx = validar_numero_positivo(escolha, int)
    if idx is None or idx > len(VARIEDADES):
        print("Variedade invalida.")
        return
    variedade = VARIEDADES[idx - 1]

    qtd_pes_texto = input("Quantidade de pes: ").strip()
    qtd_pes = validar_numero_positivo(qtd_pes_texto, int)
    if qtd_pes is None:
        print("Quantidade invalida.")
        return

    data_plantio = input("Data de plantio (AAAA-MM-DD): ").strip()
    if validar_data(data_plantio) is None:
        print("Data invalida. Use o formato AAAA-MM-DD.")
        return

    coordenadas = (-18.9188, -48.2767)

    talhao = {
        "id": proximo_id_talhao,
        "nome": nome,
        "variedade": variedade,
        "qtd_pes": qtd_pes,
        "data_plantio": data_plantio,
        "coordenadas": coordenadas
    }
    lista_talhoes.append(talhao)
    proximo_id_talhao += 1
    registrar_log(f"Talhao cadastrado: {nome} ({variedade}, {qtd_pes} pes)")
    print(f"\nTalhao '{nome}' cadastrado com sucesso! ID: {talhao['id']}")


def listar_talhoes(lista_talhoes):
    print("\n--- TALHOES CADASTRADOS ---")
    if not lista_talhoes:
        print("Nenhum talhao cadastrado ainda.")
        return
    for t in lista_talhoes:
        print(f"\nID: {t['id']}")
        print(f"  Nome........: {t['nome']}")
        print(f"  Variedade...: {t['variedade']}")
        print(f"  Qtd. pes....: {t['qtd_pes']}")
        print(f"  Plantio.....: {t['data_plantio']}")
        print(f"  Coordenadas.: {t['coordenadas']}")


def registrar_colheita(lista_talhoes, lista_colheitas):
    global proximo_id_colheita
    print("\n--- REGISTRO DE COLHEITA ---")
    if not lista_talhoes:
        print("Cadastre um talhao antes de registrar colheita.")
        return

    listar_talhoes(lista_talhoes)
    id_texto = input("\nID do talhao: ").strip()
    talhao_id = validar_numero_positivo(id_texto, int)
    if talhao_id is None:
        print("ID invalido.")
        return

    talhao = next((t for t in lista_talhoes if t["id"] == talhao_id), None)
    if talhao is None:
        print("Talhao nao encontrado.")
        return

    data = input("Data da colheita (AAAA-MM-DD): ").strip()
    if validar_data(data) is None:
        print("Data invalida.")
        return

    qtd_texto = input("Quantidade colhida (kg): ").strip()
    qtd_kg = validar_numero_positivo(qtd_texto, float)
    if qtd_kg is None:
        print("Quantidade invalida.")
        return

    print("\nClassificacoes: A (melhor), B (media), C (baixa)")
    classificacao = input("Classificacao: ").strip().upper()
    if classificacao not in CLASSIFICACOES:
        print("Classificacao invalida.")
        return

    observacoes = input("Observacoes (opcional): ").strip()

    colheita = {
        "id": proximo_id_colheita,
        "talhao_id": talhao_id,
        "data": data,
        "qtd_kg": qtd_kg,
        "classificacao": classificacao,
        "observacoes": observacoes
    }
    lista_colheitas.append(colheita)
    proximo_id_colheita += 1
    salvar_colheita_banco(colheita)
    registrar_log(f"Colheita registrada: talhao {talhao_id}, {qtd_kg} kg, classe {classificacao}")
    print(f"\nColheita registrada com sucesso! ID: {colheita['id']}")


def ver_historico_colheitas(lista_colheitas):
    print("\n--- HISTORICO DE COLHEITAS ---")
    linhas = ler_colheitas_banco()
    if not linhas:
        print("Nenhuma colheita registrada ainda.")
        return
    for l in linhas:
        print(f"\nID: {l[0]}")
        print(f"  Talhao......: {l[1]}")
        print(f"  Data........: {l[2]}")
        print(f"  Qtd. (kg)...: {l[3]}")
        print(f"  Classe......: {l[4]}")
        print(f"  Obs.........: {l[5] if l[5] else '-'}")


def relatorio_produtividade(lista_talhoes):
    print("\n--- RELATORIO DE PRODUTIVIDADE ---")
    if not lista_talhoes:
        print("Cadastre talhoes primeiro.")
        return

    linhas = ler_colheitas_banco()
    if not linhas:
        print("Nenhuma colheita para analisar.")
        return

    for talhao in lista_talhoes:
        colheitas_do_talhao = [l for l in linhas if l[1] == talhao["id"]]
        if not colheitas_do_talhao:
            continue

        total_kg = sum(l[3] for l in colheitas_do_talhao)
        kg_por_pe = total_kg / talhao["qtd_pes"]

        classes = [l[4] for l in colheitas_do_talhao]
        qtd_a = classes.count("A")
        qtd_b = classes.count("B")
        qtd_c = classes.count("C")

        print(f"\nTalhao: {talhao['nome']} ({talhao['variedade']})")
        print(f"  Total colhido....: {total_kg:.2f} kg")
        print(f"  Pes plantados....: {talhao['qtd_pes']}")
        print(f"  Produtividade....: {kg_por_pe:.2f} kg/pe")
        print(f"  Classificacoes...: A={qtd_a}, B={qtd_b}, C={qtd_c}")

        if kg_por_pe < 50:
            print("  ALERTA: Produtividade abaixo do esperado (< 50 kg/pe).")


def salvar_backup_json(lista_talhoes, lista_colheitas):
    print("\n--- BACKUP JSON ---")
    dados = {
        "talhoes": [
            {**t, "coordenadas": list(t["coordenadas"])}
            for t in lista_talhoes
        ],
        "colheitas": lista_colheitas,
        "data_backup": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("backup_pomar.json", "w", encoding="utf-8") as arq:
        json.dump(dados, arq, indent=4, ensure_ascii=False)
    registrar_log("Backup JSON gerado")
    print("Backup salvo em 'backup_pomar.json'")


def ver_log():
    print("\n--- LOG DE OPERACOES ---")
    try:
        with open("log_operacoes.txt", "r", encoding="utf-8") as arq:
            conteudo = arq.read()
            if conteudo.strip():
                print(conteudo)
            else:
                print("Log vazio.")
    except FileNotFoundError:
        print("Nenhum log gerado ainda.")


def menu():
    print("\n====================================")
    print("  GESTAO DE POMAR DE ABACATE")
    print("  Fazenda - Uberlandia/MG")
    print("====================================")
    print("1. Cadastrar talhao")
    print("2. Listar talhoes")
    print("3. Registrar colheita")
    print("4. Ver historico de colheitas")
    print("5. Relatorio de produtividade")
    print("6. Salvar backup (JSON)")
    print("7. Ver log de operacoes")
    print("0. Sair")
    print("====================================")
    return input("Escolha: ").strip()


def main():
    inicializar_banco()
    registrar_log("Sistema iniciado")

    while True:
        opcao = menu()

        if opcao == "1":
            cadastrar_talhao(talhoes)
        elif opcao == "2":
            listar_talhoes(talhoes)
        elif opcao == "3":
            registrar_colheita(talhoes, colheitas)
        elif opcao == "4":
            ver_historico_colheitas(colheitas)
        elif opcao == "5":
            relatorio_produtividade(talhoes)
        elif opcao == "6":
            salvar_backup_json(talhoes, colheitas)
        elif opcao == "7":
            ver_log()
        elif opcao == "0":
            registrar_log("Sistema encerrado")
            print("\nAte logo!")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
