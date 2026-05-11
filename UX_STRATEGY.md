# 🎨 UX/UI STRATEGY: PowerShoring Analytics
**Filosofia Visual:** Cyber-Dark Operations HUD
**Abordagem:** Mobile-First Responsiva com Foco em Alta Densidade de Dados

---

## 👁️ 1. Direção Visual & Identidade (Look & Feel)

Migramos de uma interface corporativa tradicional para um sistema imersivo, inspirado em centros de comando aeroespaciais e monitoramento de rede (SCADA High-Tech).

### A Paleta de Cores Operacional (Brand Matrix)
*   **Fundo Espacial (Deep Space):** `#030712` (Base escura para alto contraste e economia cognitiva).
*   **Acento Operacional (Cyber Cyan):** `#00F0FF` (Utilizado para métricas ativas, botões de call-to-action e dados positivos).
*   **Energia Dinâmica (Neon Green):** `#00FF88` (Métricas de descarbonização, energia eólica e renovável).
*   **Atenção Exigida (Action Orange):** `#FF5F1F` (Alertas de gargalos de transmissão, e pontos críticos).

---

## 🌌 2. Princípios de Interface (Arquitetura de Informação)

### A Estratégia de Camadas (Layers)
Ao invés de forçar o usuário a navegar entre "páginas" separadas, implementamos uma arquitetura de **Visualização Contínua**:
1.  **Base Layer:** O mapa 3D do Brasil está SEMPRE rodando ao fundo. Ele fornece o contexto espacial universal.
2.  **Backdrop Glass Layer:** Quando o dashboard é ativado, aplica-se um `backdrop-blur` que suaviza o mapa sem removê-lo da visão periférica.
3.  **Analytics Float Layer:** Os gráficos (Radar, Barras verticais, KPIs) flutuam em cards translúcidos com brilho de borda em néon.

Essa estratégia mantém o usuário **espacialmente orientado** a cada segundo da interação.

---

## 🛠️ 3. Tokens e Componentes de Design

### Glassmorphism 2.0
Utilizamos a utilidade CSS `.glass` que combina:
*   `background: rgba(3, 7, 18, 0.75);`
*   `backdrop-filter: blur(20px) saturate(180%);`
*   Isso garante que o texto seja lido perfeitamente mesmo se houver um polígono complexo e colorido atrás dele no mapa.

### Micro-Interações (Framer Motion)
*   **Transitions:** Menus laterais entram com efeito de "molas" (`damping: 25, stiffness: 120`) transmitindo uma sensação de peso e qualidade tátil.
*   **Shimmer Loading:** Quando os dados estão carregando, utilizamos esqueletos pulsantes com brilho sutil no lugar de spinners de rotação clássicos, reduzindo o estresse visual.

---

## ♿ 4. Acessibilidade (WCAG Alignment)
*   **Razão de Contraste:** Todos os textos primários operam com taxa de contraste superior a 7:1 contra o fundo escuro.
*   **Visualização Híbrida:** Os gráficos utilizam cores mas também possuem Labels numéricos explícitos, garantindo compreensão por usuários daltônicos (Protanopia/Deuteranopia).
