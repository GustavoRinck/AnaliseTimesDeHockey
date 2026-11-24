import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import os

if not os.path.exists('times_hockey.csv'):
    print("Erro: O arquivo 'times_hockey.csv' não foi encontrado. Execute 'coleta_dados.py' primeiro.")
    exit()

df = pd.read_csv('times_hockey.csv')

# Engenharia de Recursos
df['total_jogos'] = df['vitorias'] + df['derrotas'] + df['derrotas_prorroga']
df = df[df['total_jogos'] > 0].copy()
df['media_gols_pro_jogo'] = df['gols_pro'] / df['total_jogos']
df['media_gols_contra_jogo'] = df['gols_contra'] / df['total_jogos']

# Análise K-Means Individual (Sem Agrupar por Time)
print("Executando K-Means Individual por Temporada...")
features = ['media_gols_pro_jogo', 'media_gols_contra_jogo', 'percentual_vitorias']
X_ind = df[features]

scaler_ind = StandardScaler()
X_scaled_ind = scaler_ind.fit_transform(X_ind)

kmeans_ind = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster'] = kmeans_ind.fit_predict(X_scaled_ind)

# Geração do Gráfico
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.scatterplot(
    data=df,
    x='media_gols_pro_jogo',
    y='media_gols_contra_jogo',
    hue='cluster',
    palette='viridis',
    s=60,
    alpha=0.7,
    edgecolor='none',
    ax=axes[0]
)
axes[0].set_title('Gols Pró vs Gols Contra (Individual)')
axes[0].set_xlabel('Média de Gols Pró por Jogo')
axes[0].set_ylabel('Média de Gols Sofridos por Jogo')
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.scatterplot(
    data=df,
    x='media_gols_pro_jogo',
    y='percentual_vitorias',
    hue='cluster',
    palette='viridis',
    s=60,
    alpha=0.7,
    edgecolor='none',
    ax=axes[1]
)
axes[1].set_title('Percentual de Vitórias vs Gols Pró (Individual)')
axes[1].set_xlabel('Média de Gols Pró por Jogo')
axes[1].set_ylabel('Percentual de Vitórias')
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.suptitle('Análise K-Means Sem Agrupar por Time (Por Temporada)', fontsize=16)
plt.tight_layout()
plt.show()
