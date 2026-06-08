ANALYSIS_PROMPT = """
Analizza in profondità il seguente argomento.
Massimo 250 parole.

ARGOMENTO:
{query}

Produci un testo chiaro e diretto con queste sezioni:
- spiegazione dettagliata
- fattori principali
- cause
- conseguenze
- dati rilevanti
- parole chiave utili per approfondire
- contesto economico e geopolitico

Evita meta-analisi, suggerimenti operativi o ricerche future.
Rispondi con contenuto utile e concreto.
"""

NEXT_RESEARCH_PROMPT = """
Domanda iniziale:
{original_query}

Conoscenza raccolta:
{running_summary}

Identifica l'aspetto meno approfondito e formula una sola nuova domanda di ricerca specifica.
Se non ci sono ulteriori approfondimenti utili rispondi ESCLUSIVAMENTE con:
STOP
"""

FINAL_SUMMARY_PROMPT = """
Domanda originale:
{original_query}

Tutte le informazioni raccolte:
{running_summary}

Genera una risposta finale professionale e completa.
La risposta deve:
- eliminare duplicazioni
- unificare le informazioni
- essere completa
- essere leggibile
- avere una conclusione finale
- includere consigli pratici o indicazioni concrete quando possibile

Non parlare dei cicli di ricerca.
Non parlare dell'agente.
"""