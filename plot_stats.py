import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# Load CSV file with no index column
df = pd.read_csv("risposte_questionario_5.csv", index_col=False)

# Reset the index just in case
df = df.reset_index(drop=True)

# Seleziona le colonne di interesse (1, 2, 3, 4)
selected_questions = ["1", "2", "3", "4"]

# Assicurati che le colonne selezionate siano trattate come dati
df_selected = df[selected_questions]

# Converti tutte le colonne in stringa per evitare problemi con i dati non numerici
df_selected = df_selected.astype(str)

# Determina i valori univoci per ogni domanda
unique_values_per_question = [sorted(df_selected[question].unique()) for question in selected_questions]

# Crea un DataFrame per memorizzare i conteggi
all_unique_values = pd.Index([val for sublist in unique_values_per_question for val in sublist], name='Values').unique()
counts_df = pd.DataFrame(index=all_unique_values, columns=selected_questions).fillna(0)

# Popola counts_df con i conteggi per ciascun valore
for question in selected_questions:
    counts = df_selected[question].value_counts()
    counts_df.loc[counts.index, question] = counts

# Normalizza i conteggi per ogni domanda (a 19, dato che abbiamo 19 risposte in totale)
counts_df = counts_df.div(counts_df.sum(axis=0), axis=1) * 19

# Definisci i colori per i valori unici
color_map = {
    'Female': '#003049',
    'Male': '#d62828',
    'Prof.': '#003049',
    'Research Fellow': '#d62828',
    'Ph.D. Student': '#f77f00',
    'Student': '#fcbf49',
    'High': '#003049',
    'Medium': '#d62828',
    'Low': '#f77f00',
    'None': '#fcbf49'
}

# Definisci l'ordine dei segmenti per ogni domanda
order_map = {
    "1": ["Female", "Male"],
    "2": ["Prof.", "Research Fellow", "Ph.D. Student", "Student"],
    "3": ["High", "Medium", "Low", "None"],
    "4": ["High", "Medium", "Low", "None"],
}

# Crea il grafico a barre impilate orizzontali
fig, ax = plt.subplots(figsize=(12, len(selected_questions) * 0.5))

# Inizializza la posizione inferiore per impilare le barre (inizia a 0 per tutte le domande)
bottom = np.zeros(len(selected_questions))

# Plotta ogni valore unico con barre impilate
for j, question in enumerate(selected_questions):
    # Ottieni l'ordine specificato per la domanda corrente
    ordered_values = order_map.get(question, counts_df.index)

    for value in ordered_values:
        if value in counts_df.index:
            width = counts_df.loc[value, question]
            if width > 0:
                bar = ax.barh(
                    y=f'Q{int(j)+1}',  # Etichetta ogni barra con il nome della domanda
                    width=width,
                    left=bottom[j],
                    color=color_map.get(value, '#cccccc'),  # Colore specificato per ogni valore unico, con default se non trovato
                    edgecolor='black',  # Bordi neri
                    height=0.6,  # Altezza della barra
                )
                # Aggiungi il valore assunto al centro della barra
                ax.text(bottom[j] + width / 2, f'Q{int(j)+1}', value, va='center', ha='center', color='white', fontsize=7, fontweight='bold')

                # Aggiorna la posizione inferiore per impilare la prossima barra
                bottom[j] += width

# Imposta i limiti dell'asse x per evitare spazi bianchi dopo il 100%
ax.set_xlim(0, 19)

# Imposta i tick dell'asse x a valori interi
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# Riduci la dimensione dei tick delle y e delle x
ax.tick_params(axis='y', labelsize=8)
ax.tick_params(axis='x', labelsize=8)

# Aggiungi griglia e sottogriglia
ax.grid(True, which='major', axis='x', linestyle='--', color='grey', alpha=0.7)  # Griglia principale
ax.grid(True, which='minor', axis='x', linestyle=':', color='lightgrey', alpha=0.7)  # Sottogriglia

# Attiva i minor ticks solo sull'asse x
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))  # Numero di minor ticks

# Imposta le etichette dell'asse y
ax.set_yticks([f'Q{int(j)+1}' for j in range(len(selected_questions))])
ax.set_yticklabels([f'Q{int(j)+1}' for j in range(len(selected_questions))])

# Aggiungi etichette e titolo
ax.set_xlabel('Number of Responses', fontsize=8)  # Etichetta asse x
ax.set_ylabel('Question ID', fontsize=8)  # Etichetta asse y

plt.tight_layout()
plt.savefig("stacked_barchart_final.pdf", bbox_inches='tight')

# Mostra il grafico
plt.show()
