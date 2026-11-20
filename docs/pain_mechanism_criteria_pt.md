# Critérios dos Mecanismos de Dor — Fundamentação Clínica

**Projeto:** pain-mechanism-classifier
**Autor:** Renato Murayama (Fisioterapeuta · Mestrando em Informática Médica)
**Versão:** 0.1 — novembro de 2026

> **Objetivo.** Este documento resume os critérios clínicos baseados em evidência usados para desenhar o dataset sintético e a lógica de apoio à decisão deste projeto. É uma referência educativa, **não um protocolo de diagnóstico**. A ferramenta apoia — e nunca substitui — o julgamento clínico de profissionais de saúde qualificados.

---

## 1. Definições (IASP)

- **Dor** — "Uma experiência sensorial e emocional desagradável associada, ou semelhante à associada, a uma lesão tecidual real ou potencial" (Raja et al., 2020). A dor é sempre uma experiência pessoal, influenciada por fatores biológicos, psicológicos e sociais.
- **Descritores mecanísticos** reconhecidos pela IASP:

| Descritor | Definição (resumo) | Referência principal |
|---|---|---|
| **Nociceptiva** | Dor resultante de lesão real ou potencial de tecido não neural, por ativação dos nociceptores | Terminologia IASP |
| **Neuropática** | Dor causada por lesão ou doença do sistema nervoso somatossensorial | Treede et al., 2008; Finnerup et al., 2016 |
| **Nociplástica** | Dor por alteração da nocicepção, sem evidência clara de lesão tecidual nem de doença/lesão do sistema somatossensorial | Kosek et al., 2016; Kosek et al., 2021 |
| **Mista** *(conceito clínico, não é descritor IASP)* | Sobreposição clinicamente relevante de dois ou mais mecanismos no mesmo doente | Freynhagen et al., 2019 |

---

## 2. Passo 0 — Portão de segurança (red flags)

Antes de qualquer classificação, é preciso **rastrear patologia grave**. Se houver red flags, a ferramenta **não classifica** e recomenda **encaminhamento médico**.

Exemplos (Finucane et al., 2020):
- História de cancro, perda de peso inexplicada → possível neoplasia
- Febre, infeção recente, imunossupressão, drogas injetáveis → possível infeção
- Anestesia em sela, alterações vesicais/intestinais, sinais neurológicos bilaterais → possível síndrome da cauda equina
- Trauma importante, osteoporose, corticoterapia prolongada → possível fratura
- Défice neurológico progressivo
- Sinais inflamatórios (ex.: rigidez matinal > 30 min, PCR/VS elevadas) → possível doença inflamatória/reumática
- **Achados graves nos exames de imagem** → ex.: fratura, lesão suspeita de malignidade, compressão medular/mielopatia, sinais de infeção ou de doença inflamatória sistémica

**As red flags podem surgir em qualquer momento da avaliação** — anamnese, exame físico, exames de imagem ou análises — e também mais tarde, durante o tratamento. Como os utilizadores previstos incluem profissionais que não fazem triagem médica (ex.: profissionais do exercício), a ferramenta **não** assume que o rastreio foi feito antes: o portão de segurança está integrado na ferramenta e é reaplicado sempre que surge informação nova.

> **Achados incidentais:** nem todo o achado de imagem é uma red flag. Achados incidentais comuns (ex.: degeneração discal, hemangioma vertebral, pequenos quistos benignos) são frequentes em pessoas sem dor e, por si só, não obrigam a exclusão. Só os achados graves, suspeitos ou que mudam a abordagem médica ativam o portão.

---

## 3. Indicadores clínicos por mecanismo

Baseado em Smart et al. (2012, partes 1–3), Shraim et al. (2022, consenso Delphi), Finnerup et al. (2016) e Kosek et al. (2021).

| Indicador | Nociceptiva | Neuropática | Nociplástica |
|---|---|---|---|
| **Duração** | Muitas vezes aguda/subaguda; pode ser crónica | Aguda ou crónica | Crónica (≥ 3 meses, por definição) |
| **Distribuição** | Localizada na zona da lesão/disfunção | Neuroanatomicamente plausível (dermátomo / território de nervo) | Regional, multifocal ou difusa; sem lógica anatómica |
| **Comportamento** | Fatores de agravamento e alívio mecânicos, claros e proporcionais | Associada à provocação neural (ex.: testes neurodinâmicos) | Desproporcionada, imprevisível; agravantes não mecânicos |
| **Qualidade** | Dor surda, intermitente, aguda com o movimento | Queimadura, choque, elétrica, formigueiro | Difusa, variável |
| **Sinais sensitivos** | Sensibilidade normal | Défice ou ganho sensitivo no território do nervo (hipostesia, alodinia) | Hipersensibilidade difusa (ex.: alodinia fora da área dolorosa) |
| **História** | Mecanismo de lesão claro | História ou evidência de lesão/compressão nervosa | Comorbilidades: alteração do sono, fadiga, problemas cognitivos, hipersensibilidade à luz/som/cheiros |
| **Instrumentos** | DN4/painDETECT e CSI baixos | **DN4 ≥ 4** · **painDETECT ≥ 19** | **CSI ≥ 40** |

### Sistemas de graduação (resumo)

- **Dor neuropática** (Finnerup et al., 2016): *possível* (história + distribuição plausível) → *provável* (+ sinais sensitivos no exame) → *definitiva* (+ exame complementar que confirma lesão/doença).
- **Dor nociplástica** (Kosek et al., 2021): *possível* (dor ≥ 3 meses, distribuição regional/multifocal/difusa, não totalmente explicada por mecanismo nociceptivo ou neuropático, mais sinais clínicos de hipersensibilidade) → *provável* (+ história de hipersensibilidade **e** comorbilidades como alteração do sono, fadiga ou problemas cognitivos).

---

## 4. Instrumentos de rastreio

| Instrumento | O que rastreia | Escala | Ponto de corte | Referência |
|---|---|---|---|---|
| **DN4** (Douleur Neuropathique 4) | Dor neuropática (entrevista + exame) | 0–10 | ≥ 4 | Bouhassira et al., 2005 |
| **painDETECT** | Componente neuropática | −1 a 38 | ≤ 12 improvável · 13–18 ambíguo · ≥ 19 provável | Freynhagen et al., 2006 |
| **CSI** (Central Sensitization Inventory), Parte A | Sintomas de sensibilização central | 0–100 (25 itens × 0–4) | ≥ 40; gravidade: 0–29 subclínico, 30–39 ligeiro, 40–49 moderado, 50–59 grave, 60–100 extremo | Mayer et al., 2012; Neblett et al., 2013, 2017 |

> **Cuidado:** o CSI também é influenciado pelo sofrimento psicológico. Nenhum instrumento classifica sozinho o mecanismo de dor.

---

## 5. Exames de imagem e análises

- Os achados de imagem **só têm significado quando concordantes com o quadro clínico**. Alterações degenerativas (ex.: degeneração discal, protrusões) são muito frequentes em pessoas **sem dor** e aumentam com a idade (Brinjikji et al., 2015).
- Neste projeto, imagem e análises são resumidas em:
  - *Achado de imagem concordante com os sintomas* (sim / não / não realizado) → reforça nociceptiva
  - *Compressão nervosa na imagem, concordante com os sintomas* (sim / não / não realizado) → reforça neuropática
  - *Marcadores inflamatórios elevados (PCR/VS)* → contribui para o **portão de red flags**
- A imagem de rotina **não é recomendada** na dor musculoesquelética inespecífica sem red flags (Lin et al., 2020).

---

## 6. Fatores psicossociais (abordagem biopsicossocial)

Os fatores psicossociais influenciam a experiência de dor, a incapacidade e o prognóstico **em todos os mecanismos** (Lin et al., 2020; Hill et al., 2008).

| Fator | Instrumento (exemplo) | Referência |
|---|---|---|
| Ansiedade e depressão | HADS | Zigmond & Snaith, 1983 |
| Catastrofização da dor | PCS | Sullivan et al., 1995 |
| Medo do movimento (cinesiofobia) | TSK | Miller et al., 1991 |
| Risco prognóstico (lombalgia) | STarT Back Tool | Hill et al., 2008 |
| Stress laboral, qualidade do sono | Entrevista clínica / escalas | — |

> **Nota ética:** fatores psicossociais **não** são sinónimo de dor nociplástica. Nos dados sintéticos estão presentes em todas as classes, com apenas um aumento moderado no grupo nociplástico, para não codificar o estigma de que a dor "está na cabeça".

---

## 7. Dor mista

A dor mista descreve uma sobreposição clinicamente relevante de mecanismos (ex.: nociceptiva + neuropática na lombalgia radicular, ou nociceptiva + nociplástica na osteoartrose crónica). É muito comum na dor musculoesquelética crónica (Freynhagen et al., 2019) e deverá ser a **classe mais difícil** de distinguir para o modelo.

---

## 8. Boas práticas (o que a ferramenta pode mostrar após a classificação)

Onze recomendações consistentes das diretrizes de alta qualidade (Lin et al., 2020), incluindo: cuidado centrado no doente; rastreio de patologia grave; avaliação de fatores psicossociais; desencorajar a imagem de rotina; exame físico; monitorização da evolução; educação e tranquilização; promover a atividade física e o exercício; terapia manual só como complemento; oferecer cuidados não cirúrgicos baseados em evidência antes da cirurgia; e facilitar o regresso ao trabalho.

Outras diretrizes: NICE NG59 (lombalgia e ciática) e NICE NG193 (dor crónica primária).

---

## 9. Pressupostos de prevalência das classes

Nenhum estudo reporta a prevalência das quatro classes em conjunto, por isso a distribuição do dataset sintético combina várias fontes:

- **Nociplástica / sensibilização central:** ~22% dos doentes com lombalgia (± dor na perna) cumpriam critérios clínicos de sensibilização central (Smart et al., 2012).
- **Componente neuropática:** ~37% dos doentes com lombalgia crónica tinham uma componente neuropática provável (Freynhagen et al., 2006); uma meta-análise reportou uma prevalência agregada de ~47% (Gudala et al., 2017). Este valor **inclui casos mistos**, por isso é dividido entre neuropática "pura" e dor mista.
- **Nociceptiva:** a proporção restante, coerente com a elevada fração de quadros agudos/subagudos nos cuidados primários.

| Cenário | Nociceptiva | Neuropática | Nociplástica | Mista | Uso no projeto |
|---|---|---|---|---|---|
| **A — Baseado na evidência (cuidados primários)** | 40% | 15% | 20% | 25% | Dataset principal para treino e teste |
| **B — Contexto especializado de dor crónica** (estimativa da casuística clínica do autor) | 20% | 10% | 40% | 30% | Teste de robustez (dataset shift) |

> **Fundamentação:** a prevalência depende do contexto clínico. Em clínicas especializadas ou de fisioterapia privada, os doentes são muitas vezes crónicos e encaminhados após tratamentos anteriores, pelo que os quadros nociplásticos e mistos são mais frequentes. O cenário B testa se o modelo generaliza para uma casuística diferente — um conceito-chave da avaliação de IA (generalização e dataset shift).

---

## 10. Como estes critérios são usados no projeto

1. **Portão de red flags** → regras fixas (sem machine learning).
2. **Geração de dados sintéticos** → cada classe é gerada com padrões **probabilísticos** (não determinísticos) derivados dos indicadores acima, incluindo ruído, valores em falta, desequilíbrio entre classes e casos mistos ambíguos.
3. **Modelo de machine learning** → prevê o **mecanismo predominante**.
4. **Conteúdo das diretrizes** → recomendações educativas fixas, específicas de cada mecanismo.

---

## 11. Limitações

- O dataset é **sintético**: o modelo aprende as regras codificadas a partir deste documento. Os resultados demonstram o **processo completo**, não a validade clínica.
- Para uso real seriam necessários dados clínicos, validação externa e avaliação regulatória (ex.: avaliação clínica IMDRF, MDR / AI Act da UE).
- Os critérios estão simplificados para fins educativos e devem ser aplicados com julgamento clínico.

---

## Referências

A lista completa de referências (formato Vancouver) está na versão inglesa: `pain_mechanism_criteria.md`.
