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

# Agrupamento K-Means por Time (Média Histórica)
print("Executando K-Means Agrupado por Time...")
df_agrupado = df.groupby('time_nome')[['media_gols_pro_jogo', 'media_gols_contra_jogo', 'percentual_vitorias']].mean().reset_index()
features = ['media_gols_pro_jogo', 'media_gols_contra_jogo', 'percentual_vitorias']
X = df_agrupado[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_agrupado['cluster'] = kmeans.fit_predict(X_scaled)

# Geração do Gráfico
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.scatterplot(
    data=df_agrupado,
    x='media_gols_pro_jogo',
    y='media_gols_contra_jogo',
    hue='cluster',
    palette='viridis',
    s=100,
    edgecolor='black',
    ax=axes[0]
)
axes[0].set_title('Cluster: Gols Pró vs Gols Contra (Agrupado)')
axes[0].set_xlabel('Média de Gols Pró por Jogo')
axes[0].set_ylabel('Média de Gols Sofridos por Jogo')
axes[0].grid(True, linestyle='--', alpha=0.5)

sns.scatterplot(
    data=df_agrupado,
    x='media_gols_pro_jogo',
    y='percentual_vitorias',
    hue='cluster',
    palette='viridis',
    s=100,
    edgecolor='black',
    ax=axes[1]
)
axes[1].set_title('Cluster: Percentual de Vitórias vs Gols Pró (Agrupado)')
axes[1].set_xlabel('Média de Gols Pró por Jogo')
axes[1].set_ylabel('Percentual Médio de Vitórias')
axes[1].grid(True, linestyle='--', alpha=0.5)

plt.suptitle('Análise K-Means de Times de Hóquei (Média Histórica)', fontsize=16)
plt.tight_layout()
plt.show()
