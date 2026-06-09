ANALYSIS_PROMPT = """
Domanda:

{query}

Risultati web:

{web_results}

Analizza i risultati.

Produci:

- sintesi
- fattori principali
- cause
- conseguenze
- dati rilevanti
- contesto

Massimo 300 parole.

Non suggerire nuove ricerche.
"""


NEXT_RESEARCH_PROMPT = """
Domanda originale:

{original_query}

Informazioni raccolte:

{running_summary}

Identifica l'aspetto meno approfondito.

Genera UNA SOLA query di ricerca.

REGOLE OBBLIGATORIE:

- massimo 15 parole
- nessuna spiegazione
- nessun elenco
- nessun commento
- nessuna introduzione
- nessuna conclusione
- restituisci esclusivamente la query

Esempi validi:

Impatto ETF Bitcoin sul prezzo nel 2026

Politiche monetarie USA e crescita Bitcoin

Adozione istituzionale Bitcoin negli ultimi 12 mesi

Se non servono ulteriori approfondimenti rispondi esclusivamente con:

STOP
"""


FINAL_SUMMARY_PROMPT = """
Domanda originale:

{original_query}

Informazioni raccolte:

{running_summary}

Genera una risposta finale professionale.

La risposta deve:

- essere completa
- eliminare duplicazioni
- integrare tutte le fonti
- avere una conclusione finale
- essere scritta come un articolo professionale

Non parlare dei cicli.
Non parlare dell'agente.
Non parlare del processo di ricerca.
"""