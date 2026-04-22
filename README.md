# FIAP - Fase 2 - CAP 6

Sistema de gestão de pomar de abacate desenvolvido em Python.

Aluno: Caio Felix Carrijo - RM 570459

## Contexto

Meu pai produz abacate em Uberlândia/MG, plantando as variedades Fortuna, Margarida, Breda, Quintal e Geada. A partir da realidade dele, montei um sistema simples de gestão de pomar pra cadastrar talhões, registrar colheitas e acompanhar a produtividade.

## O que o sistema faz

Menu em linha de comando com 7 opções:

1. Cadastrar talhão (nome, variedade, qtd de pés, data de plantio)
2. Listar talhões cadastrados
3. Registrar colheita (data, kg, classificação A/B/C)
4. Ver histórico de colheitas (lido do banco SQLite)
5. Relatório de produtividade (kg por pé, com alerta se < 50 kg/pé)
6. Salvar backup em JSON
7. Ver log de operações

## Requisitos cobertos

- Funções com passagem de parâmetros (`cadastrar_talhao(lista)`, `registrar_colheita(talhoes, colheitas)` etc)
- Estruturas: listas (talhões e colheitas), tupla (coordenadas, variedades), dicionário (cada registro)
- Arquivo texto: `log_operacoes.txt`
- Arquivo JSON: `backup_pomar.json`
- Banco de dados: SQLite (`pomar.db`)

## Observação sobre o banco

Usei SQLite em vez de Oracle por conta de problemas com as credenciais de acesso ao servidor Oracle da FIAP. A estrutura do código é a mesma — só muda a string de conexão, então a migração pra Oracle no futuro seria direta.

## Como rodar
