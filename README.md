# Análise de Times de Hóquei

Este projeto realiza a extração automatizada (web scraping) de dados de performance de times de hóquei, seguido por uma análise estatística e aplicação de técnicas de aprendizado não supervisionado (K-Means) para agrupar equipes com características de jogo semelhantes.

## Estrutura do Projeto

O fluxo de execução do projeto está estruturado nas seguintes etapas:

1. **Scraping de Dados :** Coleta automatizada de dados reais de performance das páginas de resultados esportivos do site *Scrape This Site*.
2. **Engenharia de Recursos :** Cálculo de métricas por jogo (como média de gols pró e contra) e normalização dos dados para otimizar o algoritmo K-Means.
3. **K-means Agrupada :** Agrupamento das franquias históricas com base em sua média global de performance.
4. **K-means Individual :** Análise de cada temporada de forma independente para identificar picos específicos de performance e consistência.

## Tecnologias e Dependências

Este projeto foi desenvolvido em Python utilizando as seguintes bibliotecas listadas:
- `requests` & `beautifulsoup4` (Coleta de dados)
- `pandas` & `numpy` (Manipulação e estruturação de dados)
- `scikit-learn` (Algoritmos de Machine Learning e Normalização)
- `matplotlib` & `seaborn` (Visualização de dados)

## Como Executar

1. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script de scraping para gerar o conjunto de dados em formato CSV:
   ```bash
   # O scraper irá gerar o arquivo: 'times_hockey.csv'
   ```
3. Rode os códigos de modelagem para gerar as visualizações dos clusters.

## Conclusões e Insights Obtidos

Através da aplicação do algoritmo K-Means (parametrizado com 4 clusters), identificamos padrões claros de comportamento esportivo:
- **Equipes de Alta Performance:** Caracterizadas por alto percentual de vitórias, alta média de gols marcados e defesas sólidas (baixos gols sofridos).
- **Equipes Equilibradas:** Times medianos que mantém uma razão equilibrada entre ataque e defesa.
- **Equipes Defensivas vs. Ofensivas:** Distinção de estratégias de jogo onde alguns times focam em jogos com poucos gols (foco na defesa) e outros que, apesar de sofrerem muitos gols, compensam no setor de ataque.
- **Equipes Inconsistentes / Retrancadas:** Times com baixo aproveitamento que necessitam de reestruturação técnica em ambos os setores do jogo.
