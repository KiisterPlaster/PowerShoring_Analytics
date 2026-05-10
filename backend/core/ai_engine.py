"""
PowerShoring Analytics — AI Matchmaker Engine
Uses OpenAI GPT-4o with System Prompt Injection containing Atlas do Futuro Industrial 2025 data.
"""
import json
from openai import AsyncOpenAI
from core.config import settings
from core.clusters_data import CLUSTERS_DATA

_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    """Lazy-init the OpenAI client so the app boots without a key."""
    global _client
    if _client is None:
        _client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


SYSTEM_PROMPT = """Você é o PowerShoring Analytics AI, um sistema especialista em neoindustrialização verde do Brasil.

Seu papel é recomendar o melhor Cluster Industrial Verde para investidores que desejam instalar plantas industriais no Brasil, baseado no Atlas do Futuro Industrial do Brasil 2025.

## CLUSTERS INDUSTRIAIS DISPONÍVEIS (Dados Reais do Atlas 2025)
{clusters_json}

## REGRAS DE RECOMENDAÇÃO
1. SEMPRE recomende o cluster que melhor se alinha à intenção do investidor.
2. Justifique a recomendação com dados REAIS: energia disponível, minerais, logística portuária.
3. Inclua impacto socioeconômico: empregos projetados, PIB per capita, transição justa.
4. Mencione o conceito de POWERSHORING: atrair elos intensivos em energia para onde a energia é limpa e barata.
5. Combata a "inclusão adversa": o Brasil não deve exportar matéria-prima bruta, mas sim produtos de alto valor agregado.
6. Sempre mencione o Consenso de Belém quando falar de justiça na transição.
7. Se o investidor perguntar sobre hidrogênio, priorize Pecém (CE) e Camaçari (BA).
8. Se perguntar sobre minerais/lítio/polissilício, priorize Minas Gerais.
9. Se perguntar sobre biocombustíveis/SAF/biometano, priorize Centro-Oeste ou São Paulo.

## FORMATO DA RESPOSTA
Responda SEMPRE em JSON válido com exatamente estas chaves:
{{
  "cluster_recommended": "Nome completo do cluster",
  "cluster_id": "ID do cluster (ex: nordeste-pecem)",
  "location": "Cidade/Estado",
  "justification": "Justificativa detalhada (3-5 parágrafos)",
  "energy_profile": "Perfil energético da região",
  "logistics": "Infraestrutura logística (portos, ferrovias, rodovias)",
  "socioeconomic_impact": "Impacto socioeconômico projetado",
  "transition_justa": "Como essa instalação promove a Transição Justa"
}}
"""


async def run_matchmaker(user_query: str) -> dict:
    """Execute the AI Matchmaker with the investor's query."""
    clusters_json = json.dumps(CLUSTERS_DATA, ensure_ascii=False, indent=2)
    system = SYSTEM_PROMPT.format(clusters_json=clusters_json)

    response = await _get_client().chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_query},
        ],
        temperature=0.7,
        max_tokens=2000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {
            "cluster_recommended": "Erro ao processar",
            "cluster_id": "",
            "location": "",
            "justification": content,
            "energy_profile": "",
            "logistics": "",
            "socioeconomic_impact": "",
            "transition_justa": "",
        }

    result["raw_model"] = settings.OPENAI_MODEL
    return result
