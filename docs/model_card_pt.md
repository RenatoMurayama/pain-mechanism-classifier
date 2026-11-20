# Model Card — Classificador de Mecanismos de Dor

**Autor:** Renato Murayama (Fisioterapeuta · Mestrando em Informática Médica, Universidade do Minho)
**Versão:** 1.0 — novembro de 2026
**Estado:** Projeto educativo de portfólio. **Não é um dispositivo médico. Não foi validado em doentes reais. Não se destina a uso clínico.**

---

## 1. Detalhes do modelo

| Item | Descrição |
|---|---|
| Tarefa | Classificação multiclasse do **mecanismo de dor musculoesquelética predominante** |
| Classes | Nociceptiva · Neuropática · Nociplástica · Mista (descritores mecanísticos da IASP + dor mista) |
| Algoritmo | Regressão logística multinomial (scikit-learn), `class_weight="balanced"` |
| Pré-processamento | Imputação pela mediana + padronização (numéricas); one-hot (categóricas); ajustados só nos dados de treino |
| Comparador | Random forest (300 árvores) — desempenho semelhante; escolheu-se a regressão logística pela simplicidade e interpretabilidade |
| Portão de segurança | Rastreio de red flags por regras **antes** do modelo (não é machine learning) |

## 2. Uso previsto (definition statement ao estilo IMDRF)

- **Finalidade médica:** **informar a gestão clínica**, sugerindo o mecanismo de dor predominante e mostrando conteúdo educativo baseado em diretrizes para esse mecanismo. A ferramenta não diagnostica, não trata e não substitui o julgamento clínico.
- **Situação clínica:** dor musculoesquelética **sem red flags**. A classificação é suspensa sempre que existe alguma red flag.
- **População prevista:** adultos com dor musculoesquelética avaliados em cuidados primários, fisioterapia ou contexto de exercício.
- **Utilizadores previstos:** profissionais de saúde e do movimento (médicos, fisioterapeutas, enfermeiros, fisiologistas do exercício, educadores físicos e personal trainers, terapeutas manuais como massoterapeutas). Os utilizadores sem competência diagnóstica usam o resultado só para educação e encaminhamento.
- **Categoria de risco hipotética:** Categoria II do IMDRF (informa a gestão clínica numa situação não crítica). Segundo a Regra 11 do MDR da UE, um software comparável seria provavelmente Classe IIa e, segundo o AI Act da UE, um sistema de IA de alto risco.

**Fora do âmbito:** doentes com red flags; crianças; uso pelos próprios doentes; uso como base única para decisões de diagnóstico, tratamento, medicação ou exames de imagem.

## 3. Dados

- **Dataset sintético** de 2000 doentes, gerado em Python a partir de critérios clínicos publicados (IASP; Kosek et al., 2021; Finnerup et al., 2016; Smart et al., 2012; Shraim et al., 2022). Ver `docs/pain_mechanism_criteria_pt.md`.
- **Variáveis (13 entradas do modelo):** duração da dor, distribuição da dor, DN4, painDETECT, CSI, qualidade do sono, imagem (achado tecidual concordante, compressão nervosa concordante), HADS ansiedade, HADS depressão, PCS, TSK, stress laboral.
- **Prevalência das classes (cenário A, baseado na evidência):** nociceptiva 40%, mista 25%, nociplástica 20%, neuropática 15%.
- **Realismo:** padrões probabilísticos (não determinísticos) por classe, variáveis correlacionadas (CSI–sono; sofrimento psicológico latente), dados em falta clinicamente informados (MCAR, MAR, MNAR) e o "exame não realizado" como categoria informativa.
- **Red flags:** 190 doentes (9,5%) com ≥ 1 red flag (incluindo achados graves de imagem) foram excluídos da modelação, ficando 1810 doentes elegíveis.
- **Divisão:** estratificada 80/20 → 1448 doentes de treino / 362 de teste (uma linha por doente, logo sem sobreposição de doentes).

## 4. Desempenho

### Validação cruzada (treino, 5-fold estratificado)

| Modelo | Balanced accuracy | F1 macro | AUROC (OvR) |
|---|---|---|---|
| **Regressão logística (escolhida)** | **0,796** | **0,783** | **0,953** |
| Random forest | 0,802 | 0,795 | 0,949 |

Acrescentar indicadores de valores em falta não melhorou o desempenho.

### Conjunto de teste (n = 362, aberto uma só vez)

**Balanced accuracy 0,805 · Accuracy 0,826 · AUROC 0,96**

| Mecanismo | Precisão | Recall (sensibilidade) | n |
|---|---|---|---|
| Nociceptiva | 0,953 | 0,986 | 143 |
| Neuropática | 0,762 | 0,873 | 55 |
| Mista | 0,694 | 0,621 | 95 |
| Nociplástica | 0,773 | 0,739 | 69 |

**Análise de erros:** os erros concentram-se na classe **mista**, clinicamente ambígua (ex.: 25% dos nociplásticos e 13% dos neuropáticos previstos como mistos). As confusões mais prejudiciais são raras: neuropática → nociceptiva 0%; nociplástica → nociceptiva 1% (1 em 69).

### Testes de robustez

| Teste | Resultado |
|---|---|
| **Mudança de prevalência** (cenário B: clínica de dor crónica — nociceptiva 20%, neuropática 10%, mista 30%, nociplástica 40%) | Balanced accuracy 0,811 (estável); accuracy 0,769. Recall por classe estável; a precisão mudou com a prevalência (nociplástica 0,77 → 0,87; neuropática 0,76 → 0,65), como prevê o teorema de Bayes |
| **Ablação sem imagem** (modelo retreinado) | Balanced accuracy 0,780; recall da neuropática 0,80 |
| **Mudança de fluxo: sem exames disponíveis** (modelo final) | Balanced accuracy 0,779; recall da neuropática 0,76; erros nociplástica → nociceptiva 2 em 69 |

A imagem contribui sobretudo através de achados clinicamente significativos (compressão nervosa concordante), com dependência mínima do padrão "não realizado".

## 5. Interpretabilidade

- **Global:** os coeficientes são coerentes com os critérios publicados — a duração, a distribuição difusa e o CSI levam a previsões nociplásticas; a distribuição em dermátomo, o painDETECT, o DN4 e a compressão nervosa concordante levam a previsões neuropáticas; a duração curta e a dor localizada levam a previsões nociceptivas. As variáveis psicossociais têm pesos próximos de zero.
- **Local:** os gráficos waterfall do SHAP explicam cada previsão individual. Quando as duas probabilidades mais altas são próximas, a ferramenta deve comunicar a incerteza (ex.: "perfil entre misto e nociplástico").

## 6. Equidade e viés (MINIMAR)

| Elemento MINIMAR | Neste projeto |
|---|---|
| População e contexto do estudo | Adultos sintéticos com dor musculoesquelética; casuística de cuidados primários (cenário A) e de clínica de dor crónica (cenário B) |
| Dados demográficos | **Não disponíveis** — os dados sintéticos não têm idade, sexo, etnia nem variáveis socioeconómicas |
| Arquitetura do modelo | Regressão logística multinomial com portão de red flags por regras |
| Avaliação do modelo | Validação cruzada 5-fold estratificada, conjunto de teste, testes de mudança de prevalência e de atalho da imagem |

- **Não foi possível avaliar a equidade por subgrupos**, por não existirem variáveis demográficas. Com dados reais, o desempenho tem de ser reportado por sexo, grupo etário, etnia e nível socioeconómico.
- **Riscos de viés conhecidos com dados reais:** viés de medição (validade dos questionários entre línguas e culturas), viés de representação (quem chega à consulta especializada) e viés de acesso (exames pedidos de forma desigual).
- **Escolha ética de desenho:** os fatores psicossociais foram gerados em todas as classes, com apenas um aumento moderado na dor nociplástica, para não codificar o estigma de que a dor nociplástica é "psicológica".

## 7. Limitações

1. **Dados sintéticos:** o modelo aprende as regras codificadas no processo de geração. Os resultados demonstram o método completo, **não a validade clínica**.
2. **Quadro clínico simplificado:** a avaliação real inclui achados do exame físico que não foram modelados, como os testes neurodinâmicos, os testes sensitivos quantitativos, a **avaliação da marcha** (para a coluna lombar e os membros inferiores) e a **avaliação dos movimentos funcionais dos braços** (para a coluna cervical e os membros superiores), que revelam padrões de movimento e comportamento motor relevantes para o mecanismo de dor.
3. **A dor mista** é definida de forma inconsistente na literatura e é a classe menos fiável.
4. **Relações simplificadas:** ex.: o sono foi modelado como consequência da sensibilização central, embora a relação seja bidirecional.
5. **Sem validação externa, temporal nem geográfica.**

## 8. Recomendações antes de qualquer uso real

1. Treinar e validar com dados clínicos reais, com aprovação ética e rótulos decididos por especialistas.
2. Validação externa em contextos diferentes, com análise de equidade por subgrupos.
3. Validação local em **silent mode** antes da entrada em funcionamento, com feedback dos clínicos.
4. Monitorização após a implementação (deriva dos dados, desempenho, eventos de segurança) e um processo definido para atualizar o modelo.
5. Avaliação regulatória (MDR e AI Act da UE) e de proteção de dados (RGPD).

## Referências

Ver `docs/pain_mechanism_criteria_pt.md` para as referências clínicas. O relato do modelo segue Mitchell M, et al. Model Cards for Model Reporting. *FAT\* '19*, 2019; e Hernandez-Boussard T, et al. MINIMAR (MINimum Information for Medical AI Reporting). *J Am Med Inform Assoc*. 2020;27(12):2011-2015.
