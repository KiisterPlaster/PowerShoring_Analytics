# 📊 PRODUCT SPECIFICATION (PRD): PowerShoring Analytics
**Versão:** 1.0 | **Status:** Finalizado / Entrega de Hackathon

---

## 📋 1. Resumo Executivo
O **PowerShoring Analytics** é um SaaS de inteligência geográfica focado em destravar o investimento em neoindustrialização verde no Brasil. Ele fornece a governos, empresas e investidores uma visão cross-data única sobre disponibilidade de energia renovável, proximidade logística e segurança socioambiental.

---

## 👥 2. Público-Alvo (Personas)

### Persona A: O Investidor Estratégico (Empresas Eletrointensivas)
*   **Desejo:** Identificar locais com maior disponibilidade de energia limpa e menor custo logístico de exportação.
*   **Dor:** Demora meses para cruzar dados de órgãos diferentes (ANEEL, EPE, Antaq).

### Persona B: Analista Governamental / Formulador de Políticas
*   **Desejo:** Monitorar e promover clusters industriais vocacionados à transição energética.
*   **Dor:** Dificuldade em visualizar gargalos de infraestrutura (ex: ferrovias incompletas) sobrepostos a potenciais energéticos.

---

## 🎯 3. Escopo de Funcionalidades

### 3.1 Motor de Visualização Geográfica (MVP 1.0)
*   **Camadas Energéticas:** Exibição de Geração Eólica, Solar e Biomassa (Existente/Planejada).
*   **Infraestrutura de Transportes:** Rodovias federais, Hidrovias e Malha Ferroviária.
*   **Recursos e Meio Ambiente:** Áreas prioritárias de Terras Raras e buffers de proteção ambiental (Terras Indígenas/UCs).

### 3.2 Painel de Análise Cruzada (Módulo Inovador)
*   **Métricas Decarbonização:** Gráficos comparativos exibindo o Potencial de Descarbonização de cada Cluster.
*   **Gráfico Radar:** Cruzamento multidimensional para tomada de decisão rápida e visual.
*   **Tabela de Salvaguardas:** Indicadores "Semáforo" (Verde, Amarelo, Vermelho) para proximidade de conflitos ambientais.

### 3.3 Matchmaker AI
*   Processamento analítico para cruzamento de intenção de perfil industrial vs. vocação regional.

---

## ✅ 4. Critérios de Aceitação (Definition of Done)

1.  **Carregamento de Camadas:** Camadas com >5.000 objetos (ex: Estradas) devem ser exibidas sem travar a interface do usuário (Uso de Cache PostGIS).
2.  **Alta Disponibilidade de Dados:** Caso a API do ArcGIS fique instável, a plataforma deve servir os dados armazenados localmente (Offline/Cache-first).
3.  **Consistência Visual:** Todo o sistema deve operar em paleta Dark (Cyber Neon) mantendo contraste para legibilidade de texto em dashboards.

---

## 📈 5. Roadmap de Futuro
*   **V2.0:** Integração em tempo real com preços de energia (PLD/CCEE).
*   **V2.1:** Simulação financeira de CAPEX/OPEX para interconexão à rede elétrica baseado na distância Euclidiana até a subestação mais próxima.
