import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def load_opsd_data(filepath='../Datensätze/renewable_power_plants_DE.csv'):
    """Lädt die fertige OPSD-CSV Datei"""
    if not os.path.exists(filepath):
        print(f"Fehler: Datei {filepath} nicht gefunden.")
        return pd.DataFrame()
        
    print(f"Lade Daten aus {filepath}...")
    df = pd.read_csv(filepath, low_memory=False)
    
    # OPSD hat englische Spalten, wir mappen sie für unseren weiteren Code
    # 'energy_source_level_2' enthält Solar, Wind etc.
    # 'voltage_level' enthält die Netzebene
    # 'electrical_capacity' enthält die Leistung in MW (Achtung: nicht kW!)
    
    df_mapped = pd.DataFrame()
    df_mapped['Energieträger'] = df['energy_source_level_2']
    df_mapped['Netzebene'] = df['voltage_level']
    # Umrechnung von MW in kW (entsprechend der Vorlage)
    df_mapped['Bruttoleistung'] = df['electrical_capacity'] * 1000 
    
    # Bereinigung fehlender Werte
    df_mapped = df_mapped.dropna(subset=['Energieträger', 'Netzebene', 'Bruttoleistung'])
    
    # Mapping der Energieträger auf unsere deutschen Bezeichnungen
    et_mapping = {
        'Solar': 'Solarstrom',
        'Wind': 'Windkraft',
        'Bioenergy': 'Biomasse',
        'Hydro': 'Wasserkraft'
    }
    df_mapped['Energieträger'] = df_mapped['Energieträger'].map(et_mapping).fillna(df_mapped['Energieträger'])
    
    # Mapping der Spannungsebenen (OPSD verwendet teils englische Nummern/Strings)
    # Beipiel: "low voltage" -> "(NS)", "medium voltage" -> "(MS)"
    ebenen_mapping = {
        'low voltage': '(NS)',
        'medium voltage': '(MS)',
        'high voltage': '(HS)',
        'extra high voltage': '(HÖS)'
    }
    df_mapped['Netzebene'] = df_mapped['Netzebene'].map(ebenen_mapping).fillna(df_mapped['Netzebene'])
    
    return df_mapped

def process_and_plot(df):
    """Verarbeitet den DataFrame und erstellt die zwei Grafiken."""
    if df.empty:
        return

    netzebenen_order = ['(NS)', '(MS/NS)', '(MS)', '(HS/MS)', '(HS)', '(HÖS/HS)', '(HÖS)']
    # Gültige Netzebenen filtern
    df = df[df['Netzebene'].isin(netzebenen_order)]

    colors = {
        'Solarstrom': '#ffff33', # Gelb
        'Windkraft': '#8da0cb',  # Blau
        'Biomasse': '#66c2a5',   # Grün
        'Wasserkraft': '#8cd2e8' # Hellblau
    }

    df_leistung = df.groupby(['Netzebene', 'Energieträger'])['Bruttoleistung'].sum().unstack(fill_value=0)
    df_leistung = df_leistung.reindex(netzebenen_order).fillna(0)

    df_anzahl = df.groupby(['Netzebene', 'Energieträger']).size().unstack(fill_value=0)
    df_anzahl = df_anzahl.reindex(netzebenen_order).fillna(0)
    
    plot_columns = [col for col in colors.keys() if col in df_leistung.columns]
    plot_colors = [colors[col] for col in plot_columns]

    formatter = FuncFormatter(lambda x, pos: f"{int(x):,}".replace(',', '.'))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 14))

    # NENNLEISTUNG
    df_leistung[plot_columns].plot(kind='barh', stacked=True, color=plot_colors, ax=ax1, width=0.6)
    ax1.set_title("ERNEUERBARE ENERGIEN\n", fontsize=16, fontweight='bold', color='gray')
    ax1.set_xlabel('NENNLEISTUNG [kW]', fontsize=10, color='gray')
    ax1.set_ylabel('NETZEBENE', fontsize=10, color='gray')
    ax1.xaxis.set_major_formatter(formatter)
    ax1.grid(axis='x', linestyle='-', alpha=0.3)
    ax1.set_axisbelow(True)
    ax1.legend().set_visible(False)

    # ANLAGENANZAHL
    df_anzahl[plot_columns].plot(kind='barh', stacked=True, color=plot_colors, ax=ax2, width=0.6)
    ax2.set_title("ERNEUERBARE ENERGIEN\n", fontsize=16, fontweight='bold', color='gray')
    ax2.set_xlabel('ANLAGEN [STK]', fontsize=10, color='gray')
    ax2.set_ylabel('NETZEBENE', fontsize=10, color='gray')
    ax2.xaxis.set_major_formatter(formatter)
    ax2.grid(axis='x', linestyle='-', alpha=0.3)
    ax2.set_axisbelow(True)

    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.02), ncol=4, frameon=False)
    ax2.legend().set_visible(False)

    # Fügt Abstand ZWISCHEN den Plots ein (hspace) und passt die Außenränder an
    plt.subplots_adjust(hspace=0.4, bottom=0.15)

    # DIESE ZEILE LOESCHEN ODER AUSKOMMENTIEREN:
    # plt.tight_layout(rect=[0, 0.05, 1, 1]) 
    
    plt.show()

if __name__ == "__main__":
    df_raw = load_opsd_data('../Datensätze/renewable_power_plants_DE.csv')
    process_and_plot(df_raw)