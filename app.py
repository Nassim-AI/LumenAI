import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import datetime as dt
import matplotlib.dates as mdates

# Configuration Streamlit
st.set_page_config(page_title="Analyse LumenAI", layout="wide")

# CSS pour un design professionnel et clean
st.markdown(
    """
<style>
    /* Variables CSS pour cohérence */
    :root {
        --primary-gradient: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4FC3F7 100%);
        --secondary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --accent-color: #FFB74D;
        --text-primary: #2c3e50;
        --text-secondary: #34495e;
        --background-white: rgba(255, 255, 255, 0.95);
        --shadow-soft: 0 10px 30px rgba(0, 0, 0, 0.1);
        --shadow-hover: 0 15px 40px rgba(0, 0, 0, 0.15);
        --border-radius: 16px;
        --border-radius-large: 20px;
    }

    /* Configuration générale et fond d'écran */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(79, 195, 247, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(41, 182, 246, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(255, 183, 77, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    .main .block-container {
        padding-top: 4rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius-large);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* En-tête principal amélioré */
    .header-container {
        background: var(--primary-gradient);
        padding: 3rem 2rem 2.5rem 2rem;
        border-radius: var(--border-radius-large);
        text-align: center !important;
        margin-bottom: 3rem;
        box-shadow: var(--shadow-soft);
        border: none;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M30 0L60 30L30 60L0 30z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        opacity: 0.3;
    }
    
    .header-container > * {
        position: relative;
        z-index: 1;
    }
    
    .header-icon {
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .header-title {
        color: white;
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .title-main {
        color: #ffffff;
    }
    
.title-accent {
    color: #FFB74D !important;
    text-shadow: 0 0 10px rgba(255, 183, 77, 0.5) !important;
    font-weight: 700 !important;
}
    
    .header-tags {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    
    .tag {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .tag:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
        line-height: 1.5;
        max-width: 600px;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;   
        display: block !important;       
    }
    
    .header-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .author-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.95rem;
    }
    
    .author-avatar {
        font-size: 1.2rem;
        background: rgba(255, 255, 255, 0.15);
        padding: 0.3rem;
        border-radius: 50%;
        backdrop-filter: blur(10px);
    }
    
    .header-stats {
        display: flex;
        gap: 2rem;
    }
    
    .stat-item {
        text-align: center;
        color: white;
    }
    
    .stat-number {
        display: block;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--accent-color);
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    .stat-label {
        display: block;
        font-size: 0.75rem;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
    }
    
    /* Boîte de contexte avec style moderne */
    .context-container {
        background: var(--background-white);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: var(--shadow-soft);
        margin: 2rem 0;
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .context-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }

    .context-container:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }
    
    .context-title {
        color: var(--text-primary);
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .context-text {
        color: var(--text-secondary);
        font-size: 16px;
        line-height: 1.7;
        margin-bottom: 1rem;
    }
    
    /* Mise en évidence du texte */
    .highlight {
        color: var(--text-primary);
        font-weight: 700;
        background: linear-gradient(120deg, var(--accent-color) 0%, transparent 100%);
        background-size: 100% 40%;
        background-repeat: no-repeat;
        background-position: 0 80%;
        padding: 0 0.2rem;
    }
    
    .company-highlight {
        color: var(--text-primary);
        font-weight: 700;
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Séparateurs élégants */
    .section-divider {
        height: 2px;
        background: var(--primary-gradient);
        margin: 4rem 0;
        border: none;
        border-radius: 1px;
        opacity: 0.3;
    }
    
    /* Titres de section avec gradient */
    .section-title {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ecf0f1;
        position: relative;
    }
    
    .subsection-title {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 1rem;
        padding: 0.8rem 1.2rem;
        background: var(--background-white);
        border-radius: var(--border-radius);
        border-left: 3px solid var(--accent-color);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Conteneurs de données modernisés */
    .data-container {
        background: var(--background-white);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .data-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--secondary-gradient);
    }

    .data-container:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-3px);
    }
    
    .data-header {
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 500;
        margin: 0 0 1rem 0;
        padding: 0 0 0.5rem 0.5rem;
        border-left: 3px solid var(--text-primary);
        border-bottom: 1px solid #ecf0f1;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Boîtes d'explication modernisées */
    .explanation-box {
        background: var(--background-white);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-size: 16px;
        line-height: 1.6;
        color: var(--text-primary);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow-soft);
        position: relative;
        transition: all 0.3s ease;
    }

    .explanation-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        width: 4px;
        background: var(--accent-color);
        border-radius: 0 4px 4px 0;
    }

    .explanation-box:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }
    
    /* Images avec style moderne */
    .image-container {
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow-soft);
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }

    .image-container:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-3px);
    }
    
    /* Titres centrés pour les DataFrames */
    .centered-title {
        text-align: center;
        color: var(--text-primary);
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 1rem;
        padding: 1rem;
        background: var(--background-white);
        border-radius: var(--border-radius);
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow-soft);
        border: 1px solid rgba(255, 255, 255, 0.3);
        background: var(--secondary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Alignement vertical pour les colonnes */
    .vertical-align {
        display: flex;
        align-items: center;
        height: 100%;
    }

    /* Style pour les DataFrames Streamlit */
    div[data-testid="stDataFrame"] {
        background: var(--background-white) !important;
        border-radius: var(--border-radius) !important;
        box-shadow: var(--shadow-soft) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(20px) !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataFrame"] > div {
        border-radius: var(--border-radius) !important;
    }

    /* Style pour les images Streamlit */
    div[data-testid="stImage"] {
        border-radius: var(--border-radius) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-soft) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stImage"]:hover {
        box-shadow: var(--shadow-hover) !important;
        transform: translateY(-2px) !important;
    }

    /* Style pour la flèche entre le texte et l'image */
    .arrow-bridge {
        position: relative;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0.5rem 0;
    }

    .curved-arrow {
        position: relative;
        width: 100%;
        height: 100%;
    }

    .curved-arrow svg {
        width: 100%;
        height: 100%;
    }

    .arrow-path {
        fill: none;
        stroke: #4FC3F7;
        stroke-width: 2;
        stroke-dasharray: 5,5;
        animation: dash 3s linear infinite;
    }

    .arrow-marker {
        fill: #4FC3F7;
    }

    @keyframes dash {
        to {
            stroke-dashoffset: -20;
        }
    }

    /* Container pour la section avec flèche */
    .section-with-arrow {
        position: relative;
    }

    /* Style pour les graphiques et analyses */
    .analysis-section {
        background: var(--background-white);
        padding: 2rem;
        border-radius: var(--border-radius);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: var(--shadow-soft);
        margin: 2rem 0;
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .analysis-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--secondary-gradient);
    }

    .analysis-section:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
    }

    .analysis-text {
        color: var(--text-secondary);
        font-size: 16px;
        line-height: 1.7;
        margin: 1rem 0;
    }

    .analysis-highlight {
        background: linear-gradient(120deg, rgba(79, 195, 247, 0.3) 0%, transparent 100%);
        background-size: 100% 40%;
        background-repeat: no-repeat;
        background-position: 0 80%;
        font-weight: 600;
        color: var(--text-primary);
        padding: 0 0.2rem;
    }

    /* Styles pour les listes numérotées */
    .numbered-list {
        margin: 1.5rem 0;
        padding-left: 0;
    }

    .numbered-item {
        margin: 1rem 0;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: var(--border-radius);
        border-left: 4px solid var(--accent-color);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        position: relative;
    }

    .numbered-item::before {
        content: counter(list-counter);
        counter-increment: list-counter;
        position: absolute;
        left: -15px;
        top: 15px;
        background: var(--accent-color);
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        box-shadow: var(--shadow-soft);
    }

    .numbered-list {
        counter-reset: list-counter;
    }

    /* Animations globales */
    @keyframes slideInFromBottom {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .context-container,
    .data-container,
    .explanation-box,
    .analysis-section {
        animation: slideInFromBottom 0.6s ease-out;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-8px);
        }
        60% {
            transform: translateY(-4px);
        }
    }
    
    @media (max-width: 768px) {
        .header-container {
            padding: 2rem 1.5rem;
        }
        
        .header-title {
            font-size: 2.2rem;
        }
        
        .header-footer {
            flex-direction: column;
            text-align: center;
            gap: 1.5rem;
        }
        
        .header-stats {
            gap: 1.5rem;
        }
        
        .header-tags {
            gap: 0.5rem;
        }
        
        .tag {
            font-size: 0.8rem;
            padding: 0.3rem 0.8rem;
        }

        .context-container,
        .data-container,
        .explanation-box,
        .analysis-section {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .section-title {
            font-size: 1.6rem;
            margin: 2rem 0 1.5rem 0;
        }
        
        .subsection-title {
            font-size: 1.2rem;
            padding: 0.6rem 1rem;
        }

        .arrow-bridge {
            height: 20px;
        }

        .numbered-item {
            padding: 1rem;
            margin-left: 20px;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Style et avertissements
sns.set_style("darkgrid")
warnings.filterwarnings("ignore")

# En-tête principal avec design moderne et coloré
st.markdown(
    """
<div class="header-container">
    <div class="header-icon">
        <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="45" fill="url(#gradient1)" stroke="#ffffff" stroke-width="2"/>
            <path d="M30 35 L50 25 L70 35 L70 65 L50 75 L30 65 Z" fill="#ffffff" opacity="0.9"/>
            <circle cx="50" cy="50" r="8" fill="#FFB74D"/>
            <defs>
                <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#4FC3F7;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#29B6F6;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>
    </div>
    <h1 class="header-title">
        <span class="title-main">Lumen</span><span class="title-accent">AI</span> Analytics
    </h1>
    <div class="header-tags">
        <span class="tag">Machine Learning</span>
        <span class="tag">Énergies Renouvelables</span>
        <span class="tag">Analyse de données</span>
    </div>
    <p class="header-subtitle">Analyse des performances de parcs solaires photovoltaïques</p>
    <div class="header-footer">
        <div class="author-info">
            <span class="author-text">Réalisé par <strong>ISSAD Nassim</strong></span>
        </div>
        <div class="header-stats">
            <div class="stat-item">
                <span class="stat-number">AI</span>
                <span class="stat-label">Powered</span>
            </div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# Chargement des données
@st.cache_data
def load_data():
    plant1_gen = pd.read_csv("Dataset_LumenAI/Plant_1_Generation_Data.csv")
    plant2_gen = pd.read_csv("Dataset_LumenAI/Plant_2_Generation_Data.csv")
    plant1_weather = pd.read_csv("Dataset_LumenAI/Plant_1_Weather_Sensor_Data.csv")
    plant2_weather = pd.read_csv("Dataset_LumenAI/Plant_2_Weather_Sensor_Data.csv")
    return plant1_gen, plant2_gen, plant1_weather, plant2_weather


plant1_gen, plant2_gen, plant1_weather, plant2_weather = load_data()
plant1_gen["DATE_TIME"] = pd.to_datetime(
    plant1_gen["DATE_TIME"], format="%d-%m-%Y %H:%M"
)
plant1_weather["DATE_TIME"] = pd.to_datetime(
    plant1_weather["DATE_TIME"], format="%Y-%m-%d %H:%M:%S"
)

# Contexte du projet avec design amélioré
st.markdown(
    """
<div class="context-container">
    <h4 class="context-title">
         Contexte du projet
    </h4>
    <p class="context-text">
        En septembre 2020, <span class="company-highlight">LumenAI</span> a été contactée par <span class="highlight">Éric Dussolier</span>, 
        gestionnaire d'actifs chez <em>SolarEdge Management</em>, pour étudier les performances 
        d'un parc solaire situé dans le sud de la France.
    </p>
    <p class="context-text">
        Ce gestionnaire souhaite détecter les <span class="highlight">sous-performances invisibles à l'œil nu</span>, 
        afin d'anticiper les baisses de rendement. Il souhaite également obtenir une 
        <span class="highlight">estimation des productions futures</span> afin de pouvoir communiquer les résultats 
        à son client, qui souhaite estimer la <span class="highlight">rentabilité de son financement</span>. 
        Voici les données des 2 fichiers CSV qu'il nous fournit.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Crée deux colonnes
col1, col2 = st.columns(2)

# Tableau 1 : Données de génération
with col1:
    st.markdown(
        '<div class="centered-title">Données de production d\'énergie – Fichier 1</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(plant1_gen.head(100))

# Tableau 2 : Données météo
with col2:
    st.markdown(
        '<div class="centered-title">Données météorologiques – Fichier 2</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(plant1_weather.head(100))

# Titre d'analyse
st.markdown(
    '<h2 class="section-title">Analysons les données de production d\'énergie</h2>',
    unsafe_allow_html=True,
)

# Deux colonnes : image + texte
col1, col2 = st.columns([1, 2])

with col1:
    st.image("capture_csv1.png", use_container_width=True)

with col2:
    st.markdown(
        """
    <div class="explanation-box">
        <strong>Identifiant de centrale</strong><br>
        La colonne PLANT_ID représente l'identifiant unique de la centrale qu'il nous demande d'analyser.
    </div>
    """,
        unsafe_allow_html=True,
    )

# Section avec flèche entre le texte et l'image
st.markdown('<div class="section-with-arrow">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="vertical-align">', unsafe_allow_html=True)
    st.image("capture_csv2.png", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(
        """
    <div class="explanation-box">
        <strong>Fonctionnement des onduleurs</strong><br>
        Toutes les 15 minutes, 22 onduleurs transmettent des mesures précises sur leur état de fonctionnement. Ces équipements sont essentiels dans une centrale solaire : ils transforment l'électricité produite en courant continu (DC) par les panneaux photovoltaïques en courant alternatif (AC), directement injectable sur le réseau.
        Ainsi chaque ligne de données correspond à une fenêtre temporelle de 15 minutes pour un onduleur donné (SOURCE_KEY). Les colonnes DAILY_YIELD et TOTAL_YIELD représentent donc respectivement les courants alternatifs cumulés depuis le début de la journée et depuis l'activation des onduleurs.
    </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)

# Flèche pointant vers le schéma en bas
st.markdown(
    """
<div style="text-align: center; margin: 0.5rem 0; padding-left: 30%;">
    <div style="display: inline-flex; flex-direction: column; align-items: center; gap: 0.5rem;">
        <span style="color: var(--text-primary); font-size: 1rem; font-weight: 500; 
                     background: var(--secondary-gradient); -webkit-background-clip: text; 
                     -webkit-text-fill-color: transparent; background-clip: text;">
            Voir le schéma explicatif
        </span>
        <svg width="30" height="60" viewBox="0 0 30 60" xmlns="http://www.w3.org/2000/svg" 
             style="animation: bounce 2s infinite;">
            <defs>
                <linearGradient id="arrowGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#4FC3F7;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#29B6F6;stop-opacity:1" />
                </linearGradient>
            </defs>
            <!-- Ligne principale -->
            <line x1="15" y1="10" x2="15" y2="40" stroke="url(#arrowGradient)" 
                  stroke-width="3" stroke-linecap="round" opacity="0.8"/>
            <!-- Pointe de la flèche -->
            <polygon points="15,50 8,35 22,35" fill="url(#arrowGradient)" opacity="0.9"/>
        </svg>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("")  # Colonne vide pour pousser l'image vers la droite

with col2:
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    st.image("capture_csv3.png")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# NOUVELLE SECTION : COURBES DC_POWER + DAILY_YIELD
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown(
    """


        On commence par visualiser l'évolution de la production journalière d'énergie ainsi que de la puissance instantanée produite par tous les onduleurs en courant continu (DC).
""",
    unsafe_allow_html=True,
)

# Code de traitement des données
temp1_gen = plant1_gen.copy()
temp1_gen["day"] = temp1_gen["DATE_TIME"].dt.date
temp1_gen["time"] = temp1_gen["DATE_TIME"].dt.time

# ✅ Correction ici : pas besoin de fig/ax manuels
ax_list = (
    temp1_gen.groupby(["time", "day"])["DC_POWER"]
    .mean()
    .unstack()
    .plot(sharex=True, subplots=True, layout=(17, 2), figsize=(20, 30))
)

temp1_gen.groupby(["time", "day"])["DAILY_YIELD"].mean().unstack().plot(
    sharex=True, subplots=True, layout=(17, 2), figsize=(20, 30), style="-.", ax=ax_list
)

# Titres
i = 0
for a in range(len(ax_list)):
    for b in range(len(ax_list[a])):
        ax_list[a, b].set_title(temp1_gen["day"].unique()[i], size=15)
        ax_list[a, b].legend(["DC_POWER", "DAILY_YIELD"])
        i += 1

plt.tight_layout()
st.pyplot(plt)

# Analyse des observations
st.markdown(
    """
Nous pouvons déjà faire plusieurs observations :

**1.** On constate que la puissance instantanée de chaque onduleur commence à dépasser zéro aux alentours de 5h40 et redescend à zéro vers 18h00. 
Cela correspond globalement à la période comprise entre le lever du soleil et le coucher du soleil.

**2.** Nous disposons de 34 jours de données, ce qui peut parfois être trop peu pour analyser des tendances, des anomalies, ou faire de l'IA de manière efficace. 

**3.** Les **19 et 20 mai**, une anomalie semble affecter les mesures de certains onduleurs. 
Toutefois, comme il y a un saut dans la production journalière qui augmente de manière significative juste après ce dysfonctionnement, cela suggère que le dysfonctionnement provient probablement des **données enregistrées**, et non d'un défaut réel des capteurs.
"""
)

# Section image avec texte
col1, col2 = st.columns([2, 1])

with col1:
    st.image("capture_csv4.png")

with col2:
    st.markdown("")

# Transition vers l'analyse individuelle
st.markdown(
    """
 Maintenant que nous avons analysé les courbes globales de l'ensemble des onduleurs pour détecter d'éventuels défauts généraux, passons à une étude plus fine, en examinant <span class="analysis-highlight">chaque onduleur individuellement</span>.

""",
    unsafe_allow_html=True,
)

# Nouvelle section d'analyse par onduleur

# Étape 1 : Préparation
temp1_gen = plant1_gen.copy()
temp1_gen["time"] = temp1_gen["DATE_TIME"].dt.time
temp1_gen["day"] = temp1_gen["DATE_TIME"].dt.date

# Étape 2 : Agrégation - moyenne DC_POWER par heure et par onduleur
dc_gen = temp1_gen.groupby(["time", "SOURCE_KEY"])["DC_POWER"].mean().unstack()

# Étape 3 : Palette personnalisée
highlight_red = "bvBOhCH3iADSZry"  # Onduleur à mettre en rouge
highlight_blue = "1BY6WEcLGh8j5v7"  # Onduleur à mettre en bleu

all_sources = dc_gen.columns.tolist()
colors = []

for col in all_sources:
    if col == highlight_red:
        colors.append("red")  # 🔴 capteur 1
    elif col == highlight_blue:
        colors.append("blue")  # 🔵 capteur 2
    else:
        colors.append("lightgray")  # Autres capteurs = gris clair

# Étape 4 : Affichage du graphique dans Streamlit
fig, ax = plt.subplots(figsize=(20, 6), dpi=100)
dc_gen.plot(ax=ax, color=colors, linewidth=2)

ax.set_title(
    "Puissance DC moyenne par heure – 2 onduleurs mis en évidence", fontsize=16
)
ax.set_xlabel("Heure", fontsize=13)
ax.set_ylabel("DC POWER (kW)", fontsize=13)
ax.legend(title="Onduleur", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
ax.grid(True)

st.pyplot(fig)

# Conclusion de l'analyse
st.markdown(
    """
        Deux onduleurs semblent clairement sous-performer par rapport aux autres : <span class="analysis-highlight">1BY6WEcLGh8j5v7</span> et <span class="analysis-highlight">bvBOhCH3iADSZry</span>. 
        Analysons désormais leurs performances de manière séparée.

""",
    unsafe_allow_html=True,
)

# DÉBUT DE L'AJOUT DE VOTRE CODE
st.markdown(
    """
On va donc cette fois-ci visualiser l'évolution de la production journalière d'énergie ainsi que de la puissance instantanée produite en courant continu (DC) par l’onduleur <span class="analysis-highlight">bvBOhCH3iADSZry</span>.
""",
    unsafe_allow_html=True,
)

# Étape 1 : Filtrer le capteur
worst_source = plant1_gen[plant1_gen["SOURCE_KEY"] == "bvBOhCH3iADSZry"].copy()

# Étape 2 : Extraction des champs temporels
worst_source["time"] = worst_source["DATE_TIME"].dt.time
worst_source["day"] = worst_source["DATE_TIME"].dt.date

# Étape 3 : Tracé des courbes DC_POWER et DAILY_YIELD
ax = (
    worst_source.groupby(["time", "day"])["DC_POWER"]
    .mean()
    .unstack()
    .plot(sharex=True, subplots=True, layout=(17, 2), figsize=(20, 30), color="red")
)

worst_source.groupby(["time", "day"])["DAILY_YIELD"].mean().unstack().plot(
    sharex=True, subplots=True, layout=(17, 2), figsize=(20, 30), style="-.", ax=ax
)

# Étape 4 : Titres et légendes
i = 0
cols = worst_source["day"].unique().tolist()

for a in range(len(ax)):
    for b in range(len(ax[a])):
        if i < len(cols):
            ax[a, b].set_title(str(cols[i]), fontsize=13)
            ax[a, b].legend(["DC_POWER", "DAILY_YIELD"])
            i += 1

plt.tight_layout()
st.pyplot(plt)

st.markdown(
    """

    Nous observons un dysfonctionnement total pour ces deux onduleurs les **7 juin** et **14 juin**.  
    """
)


col1, col2 = st.columns(
    [2, 1]
)  # Inverser les proportions pour agrandir la colonne de l'image

with col1:
    st.image("capture_csv5.png")  # définir une largeur fixe

with col2:
    st.markdown(
        """
        """,
        unsafe_allow_html=True,
    )


col1, col2 = st.columns(
    [2, 1]
)  # Inverser les proportions pour agrandir la colonne de l'image

with col1:
    st.image("capture_csv6.png")  # définir une largeur fixe

with col2:
    st.markdown(
        """
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Cependant, une question subsiste : 
        <strong>les anomalies détectées sont-elles dues à un dysfonctionnement interne des onduleurs</strong>, 
        ou bien à des <strong>facteurs extérieurs</strong> comme la météo ?
        </p>
        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Pour y répondre, intéressons-nous au second jeu de données, 
        qui contient des mesures de température du module, 
        de température ambiante et d’irradiation.
        Cela nous permettra d’examiner s’il existe un lien entre les dysfonctionnements observés
        et certaines conditions climatiques particulières.
        </p>
    """,
    unsafe_allow_html=True,
)


# Étape 1 : Préparation des données météo
temp1_sens = plant1_weather.copy()
temp1_sens["time"] = temp1_sens["DATE_TIME"].dt.time
temp1_sens["day"] = temp1_sens["DATE_TIME"].dt.date

# Étape 2 : Tracer les courbes de température et irradiation
fig, ax = plt.subplots(figsize=(20, 30))

ax_list = (
    temp1_sens.groupby(["time", "day"])["MODULE_TEMPERATURE"]
    .mean()
    .unstack()
    .plot(subplots=True, layout=(17, 2), figsize=(20, 30), color="orange", ax=ax)
)

temp1_sens.groupby(["time", "day"])["AMBIENT_TEMPERATURE"].mean().unstack().plot(
    subplots=True,
    layout=(17, 2),
    figsize=(20, 30),
    style="-.",
    ax=ax_list,
    color="skyblue",
)

temp1_sens.groupby(["time", "day"])["IRRADIATION"].mean().unstack().plot(
    subplots=True,
    layout=(17, 2),
    figsize=(20, 30),
    style="--",
    ax=ax_list,
    color="green",
)

# Étape 3 : Mise en forme
i = 0
jours = temp1_sens["day"].unique()

for a in range(len(ax_list)):
    for b in range(len(ax_list[a])):
        if i < len(jours):
            ax_list[a, b].set_title(str(jours[i]), fontsize=13)
            ax_list[a, b].legend(
                ["Temp Module (°C)", "Temp Ambiante (°C)", "Irradiation (W/m²)"],
                loc="upper right",
                fontsize=8,
            )
            ax_list[a, b].axhline(50, color="red", linestyle=":", linewidth=1.2)
            i += 1

plt.tight_layout()
st.pyplot(plt)

st.markdown(
    """
        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Aucune anomalie particulière n’a été constatée au niveau des températures 
        (ni du module, ni ambiante) lors des journées concernées par les dysfonctionnements — en l’occurrence, les <strong>7 juin</strong> et <strong>14 juin</strong>.
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Nous pouvons donc en conclure que ces interruptions complètes de production sont très probablement liées 
        à une <strong>défaillance technique ou matérielle</strong>, et non à des conditions climatiques exceptionnelles.
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        <strong>Mais alors, comment détecter ce type d’anomalies à l’avenir ?</strong><br>
        C’est là tout le problème : <em>les jours de défaillance ne présentent pas une baisse évidente 
        de la production journalière</em>. Les moyennes semblent normales, ce qui empêche tout soupçon à première vue.
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Une solution manuelle consisterait à examiner chaque jour les courbes de chaque capteur.
        Mais cette méthode est chronophage, et inadaptée aux attentes de 
        <em>SolarEdge Management</em>, qui recherche une solution simple, automatisée et efficace.
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50; margin-top:20px;">
        Explorons donc maintenant les corrélations entre les variables, 
        afin d’identifier des indicateurs utiles pour une détection automatisée des anomalies.
        </p>
    """,
    unsafe_allow_html=True,
)
col1, col2 = st.columns(
    [2, 1]
)  # Inverser les proportions pour agrandir la colonne de l'image

with col1:
    st.image("capture_csv7.png")  # définir une largeur fixe

with col2:
    st.markdown(
        """
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    "Nous remarquons que l'AC/DC power ont la plus forte corrélation avec l'irradiation, nous allons donc représenter le dc power du capteur bvBOhCH3iADSZry ainsi que l'irradiation moyenne en fonction du temps afin d'observer s'il n'y a pas d'anomalies visibles."
)

col1, col2 = st.columns(
    [2, 1]
)  # Inverser les proportions pour agrandir la colonne de l'image

with col1:
    st.image("capture_csv8.png")  # définir une largeur fixe

with col2:
    st.image("capture_csv9.png")


st.markdown(
    """
        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        En observant le ratio puissance DC produite / irradiation, on remarque que les journées du 
        14 juin, 7 juin et 21 mai présentent des valeurs anormalement faibles 
        par rapport aux autres jours.
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Toutefois, le 21 mai, cette baisse concerne l’ensemble des capteurs, 
        ce qui suggère un <em>phénomène global</em> non identifié (ex. : couverture nuageuse, erreur de mesure…).
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        En revanche, les 7 et 14 juin, seuls les deux capteurs soupçonnés comme défaillants 
        affichent ce comportement inhabituel. Cela renforce donc l’hypothèse d’un dysfonctionnement localisé.
        </p>
        
        <hr style="margin: 20px 0;">

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Pour aller plus loin, nous allons tenter de détecter automatiquement les anomalies à l’aide d’un algorithme 
        d’<em>Isolation Forest</em>.  
        </p>

        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">
        Mais avant cela, un peu de feature engineering s’impose : nous allons commencer par 
        fusionner les deux jeux de données fournis par SolarEdge Management.
        </p>
    """,
    unsafe_allow_html=True,
)


# 🔁 Étape 1 : Fusionner les données sur la colonne 'DATE_TIME'
p1 = pd.merge(plant1_gen, plant1_weather, on="DATE_TIME", how="inner")

# 🧹 Étape 2 : Supprimer les colonnes redondantes
p1 = p1.drop(columns=["PLANT_ID_x", "PLANT_ID_y", "SOURCE_KEY_y"])

# ⏰ Étape 3 : Extraire l'heure pour pouvoir filtrer plus facilement
p1["HEURE"] = p1["DATE_TIME"].dt.time


# 🔍 Étape 5 : Afficher les données mesurées à 12h00
from datetime import time

donnees_12h = p1[p1["HEURE"] == time(12, 0)]


# 🧹 1. Nettoyage des données fusionnées
df_merged_clean = p1.dropna(subset=["DC_POWER", "IRRADIATION", "SOURCE_KEY_x"]).copy()
df_merged_clean = df_merged_clean[df_merged_clean["IRRADIATION"] > 0]

df_merged_clean["DC_per_IRRADIATION"] = (
    df_merged_clean["DC_POWER"] / df_merged_clean["IRRADIATION"]
) / 1e6

df_merged_clean["DATE"] = df_merged_clean["DATE_TIME"].dt.date

df_journalier = (
    df_merged_clean.groupby(["SOURCE_KEY_x", "DATE"])["DC_per_IRRADIATION"]
    .mean()
    .reset_index()
)

df_journalier.rename(
    columns={
        "SOURCE_KEY_x": "SOURCE_KEY",
        "DC_per_IRRADIATION": "mean_DC_per_IRRADIATION",
    },
    inplace=True,
)


col1, col2, col3 = st.columns([1.2, 0.2, 0.8])

# Tableau 1 : Données de génération
with col1:
    st.markdown(
        '<div class="centered-title">Données fusionnées</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(donnees_12h)

# Flèche au milieu (plus jolie, de gauche vers droite)
with col2:
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; height: 400px;">
            <svg width="100" height="60" viewBox="0 0 100 60" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="arrowGradientRL" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:#4FC3F7;stop-opacity:1" />
                        <stop offset="50%" style="stop-color:#29B6F6;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#FFB74D;stop-opacity:1" />
                    </linearGradient>
                    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="rgba(0,0,0,0.2)"/>
                    </filter>
                </defs>
                <!-- Corps de la flèche avec courbe légère -->
                <path d="M 15 30 Q 50 25 75 30" stroke="url(#arrowGradientRL)" 
                      stroke-width="4" fill="none" stroke-linecap="round" 
                      filter="url(#shadow)" opacity="0.9"/>
                <!-- Pointe de la flèche -->
                <polygon points="85,30 70,22 70,26 75,30 70,34 70,38" 
                         fill="url(#arrowGradientRL)" filter="url(#shadow)" opacity="0.9"/>
                <!-- Petit cercle de départ -->
                <circle cx="15" cy="30" r="3" fill="url(#arrowGradientRL)" 
                        filter="url(#shadow)" opacity="0.8"/>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Tableau 2 : Données météo
with col3:
    st.markdown(
        '<div class="centered-title">Rajout du ratio DC_POWER / IRRADIATION</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(df_journalier.head(100))


st.markdown(
    """
    Ce tableau présente, pour chaque onduleur  et chaque date, la **moyenne du ratio DC_POWER / IRRADIATION**. Cela permet de comparer objectivement les performances des onduleurs uniquement en fonction de ce ratio et de détecter les anomalies. Ainsi en entrainant un algorithme d'isolation forest, on a pu identifier les anomalies.
    """
)


col1, col2 = st.columns(2)

with col1:
    st.image("capture_csv11.png")

with col2:
    st.image("capture_csv12.png")


st.markdown(
    """

        <hr style="margin: 20px 0;">


        <p style="font-size:16px; line-height:1.6em; color:#2c3e50;">

    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    Une question légitime se pose : **peut-on prédire précisément la production solaire des prochains jours ?**

    C’est en effet le souhait de SolarEdge Management, qui aimerait pouvoir communiquer à ses clients des estimations fiables de la production à venir.

    En réalité, prédire précisément la production d’un système photovoltaïque est une tâche complexe.  Et les données dont on dispose actuellement sont insuffisantes pour entraîner un modèle robuste de ML/DL. Pour améliorer la précision, il serait nécessaire de collecter davantage de variables externes, en voici une liste non-exhaustive :

    1- La couverture nuageuse : les nuages réduisent directement l’irradiation solaire.  
    2- La vitesse du vent : influence le refroidissement des panneaux et donc le rendement.  
    3- L'humidité : peut affecter l’efficacité des modules.  
    4- Les précipitations : moins de soleil les jours de pluie.  
    5- L'âge des panneaux : l’usure diminue la performance au fil du temps.  
    6- Les défauts signalés par les onduleurs** : ceci afin d'intégrer les erreurs matérielles connues.  
    7- Tension et courant mesurés** : permettent des calculs fins de rendement.   

    Tant que de telles variables ne sont pas disponibles, toute tentative de prévision restera très approximative. Toutefois, il existe des approches statistiques puissantes qui permettent d’identifier des tendances générales dans les séries temporelles.

    Parmi elles, l’algorithme Prophet, développé par Meta, est particulièrement adapté.  Prophet est capable de modéliser les tendances, les effets saisonniers (quotidiens, hebdomadaires, annuels), et de générer des prédictions avec une estimation d’incertitude.  

    Essayons-le.
    """
)
# Section image avec texte
col1, col2 = st.columns([2, 1])

with col1:
    st.image("capture_csv13.png")

with col2:
    st.markdown("")

st.markdown(
    """
    Pourquoi les prévisions Prophet sont-elles peu fiables ici ?  

    Le modèle Prophet repose sur la décomposition des séries temporelles en tendance, saisonnalité et bruit résiduel. Il est très performant lorsque la donnée suit une structure stable et récurrente dans le temps (comme les ventes mensuelles, ou le trafic web).

    Cependant, dans notre cas, la production d’énergie dépend de facteurs externes fortement variables, qui ne sont pas tous fournis et qui changent de manière non-linéaire donc Prophet ne peut donc pas les anticiper. Au final pour améliorer les prévisions, il serait indispensable d'avoir des données plus enrichies.
    """
)
