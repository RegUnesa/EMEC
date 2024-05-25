import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sqlite3

# Configuração do banco de dados usando SQLAlchemy
bd = r'C:\Program Files (x86)\sqlite3\BD_REGIONAL.db'
engine = create_engine(f'sqlite:///{bd}')

# Função para carregar dados do banco de dados
def load_data():
    query = text("SELECT * FROM TB_MODALIDADE")
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df

# Título do dashboard
st.title("Dashboard de Monitoramento da Extração")

# Carregar os dados
df = load_data()

# Mostrar a tabela completa
st.header("Dados Extraídos")
st.dataframe(df)

# Mostrar o progresso total
total_rows = len(df)
completed_rows = df[df['STATUS_RUN'] == 1].shape[0]
error_rows = df[df['STATUS_RUN'] == 0].shape[0]

st.header("Progresso da Extração")
st.write(f"Total de Linhas: {total_rows}")
st.write(f"Linhas Concluídas: {completed_rows}")
st.write(f"Linhas com Erro: {error_rows}")

# Barra de progresso
progress = completed_rows / total_rows if total_rows > 0 else 0
st.progress(progress)

# Mostrar os últimos registros processados
st.header("Últimos Registros Processados")
df_sorted = df.sort_values(by='DT_RUN', ascending=False)
st.dataframe(df_sorted.head(10))

# Mostrar registros com erro
st.header("Registros com Erro")
st.dataframe(df[df['STATUS_RUN'] == 0])

# Atualizar os dados
if st.button('Atualizar Dados'):
    df = load_data()
    st.experimental_rerun()
