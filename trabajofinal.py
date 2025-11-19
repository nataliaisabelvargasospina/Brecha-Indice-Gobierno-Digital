import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import streamlit as st

#para abrir un archivo csv ("ruta de acceso")
base_datos = pd.read_csv("idg.csv", encoding="latin-1", sep=";")

base_datos.info()

base_datos.copy()

base_datos.columns = base_datos.columns.str.lower().str.replace(" ", "_", regex=False)
#base_datos

#base_datos.columns

#base_datos["código_sigep"]

base_datos["código_sigep"] = base_datos["código_sigep"].str.replace(",", "", regex=False)
base_datos["código_sigep"] = base_datos["código_sigep"].str.replace(".", "", regex=False)
#base_datos["código_sigep"]

#base_datos["entidad"]

base_datos["entidad"] = base_datos["entidad"].str.lower().str.capitalize()
#base_datos["entidad"]

#base_datos['entidad'].value_counts()

base_datos["orden"] = base_datos["orden"].str.lower().str.capitalize()
#base_datos["orden"]

#base_datos['orden'].value_counts()

base_datos["sector"] = base_datos["sector"].str.lower().str.capitalize()
#base_datos["sector"]

#base_datos['sector'].value_counts()

base_datos['naturaleza_jurídica'] = base_datos["naturaleza_jurídica"].str.lower().str.capitalize()
#base_datos["naturaleza_jurídica"]

#base_datos["naturaleza_jurídica"].value_counts()

base_datos["id_departamento"] = base_datos["id_departamento"].str.replace(",", "", regex=False)
#base_datos["id_departamento"]

#base_datos["id_departamento"].value_counts()

#base_datos["departamento"].value_counts()

base_datos["id_municipio"] = base_datos["id_municipio"].str.replace(",", "", regex=False)
base_datos["id_municipio"] = base_datos["id_municipio"].str.replace(".", "", regex=False)
#base_datos["id_municipio"]

#base_datos["id_departamento"].value_counts()

base_datos["municipio"] = base_datos["municipio"].str.lower().str.capitalize()
base_datos["municipio"] = base_datos["municipio"].str.replace("Bogotá, d. c.", "Bogotá, D. C.", regex=False)
#base_datos["municipio"]

#base_datos["municipio"].value_counts()

base_datos["vigencia"] = base_datos["vigencia"].str.replace(",", "", regex=False)
base_datos["vigencia"] = base_datos["vigencia"].str.replace(".", "", regex=False)
#base_datos["vigencia"]

#base_datos["vigencia"].value_counts()

#base_datos["id_índice"].value_counts()

#base_datos["índice"].value_counts()

base_datos['puntaje_entidad'] = base_datos["puntaje_entidad"].str.replace(",", ".", regex=False)
base_datos['puntaje_entidad'] = base_datos['puntaje_entidad'].astype(float).round(3)
#base_datos['puntaje_entidad']

base_datos['promedio_grupo_par'] = base_datos["promedio_grupo_par"].str.replace(",", ".", regex=False)
base_datos['promedio_grupo_par'] = base_datos['promedio_grupo_par'].astype(float).round(3)
#base_datos['promedio_grupo_par']

base_datos['máximo_grupo_par'] = base_datos["máximo_grupo_par"].str.replace(",", ".", regex=False)
base_datos['máximo_grupo_par'] = base_datos['máximo_grupo_par'].astype(float).round(3)
#base_datos['máximo_grupo_par']

base_datos['mínimo_grupo_par'] = base_datos["mínimo_grupo_par"].str.replace(",", ".", regex=False)
base_datos['mínimo_grupo_par'] = base_datos['mínimo_grupo_par'].astype(float).round(3)
#base_datos['mínimo_grupo_par']

base_datos['quintil_grupo_par'] = base_datos["quintil_grupo_par"].str.replace(",", "", regex=False).astype(int)
#base_datos['quintil_grupo_par']

#base_datos['quintil_grupo_par'].value_counts()

base_datos['percentil_grupo_par'] = base_datos["percentil_grupo_par"].str.replace(",", "", regex=False).astype(int)
#base_datos['percentil_grupo_par']

#base_datos['percentil_grupo_par'].value_counts()


pd.DataFrame.to_csv(base_datos, 'base_datos_limpios.csv')


base_datos.isnull().sum().sum()

#STREAMLIT

#Titulo

st.set_page_config(
    page_title='Brecha Indice Gobierno Digital',
    layout='wide',
    page_icon='📊'
)

st.title('📊 Brecha Indice Gobierno Digital')

# Filtro 1: Departamento
all_departamentos = sorted(base_datos['departamento'].dropna().unique().tolist())
selected_depto = st.sidebar.multiselect(
    "1. Filtrar por Departamento:",
    options=all_departamentos,
    default=all_departamentos
)

# Filtro 2: Sector
all_sectores = sorted(base_datos['sector'].dropna().unique().tolist())
selected_sector = st.sidebar.multiselect(
    "2. Filtrar por Sector:",
    options=all_sectores,
    default=all_sectores
)

# Filtro 3: Naturaleza Jurídica
all_naturaleza = sorted(base_datos['naturaleza_jurídica'].dropna().unique().tolist())
selected_naturaleza = st.sidebar.multiselect(
    "3. Filtrar por Naturaleza Jurídica:",
    options=all_naturaleza,
    default=all_naturaleza
)

# Filtro 4: Orden (NUEVO)
all_orden = sorted(base_datos['orden'].dropna().unique().tolist())
selected_orden = st.sidebar.multiselect(
    "4. Filtrar por Orden:",
    options=all_orden,
    default=all_orden
)

# Filtro 5: Vigencia (NUEVO)
all_vigencia = sorted(base_datos['vigencia'].dropna().unique().tolist())
selected_vigencia = st.sidebar.multiselect(
    "5. Filtrar por Vigencia:",
    options=all_vigencia,
    default=all_vigencia
)

# 2. Filtros de Rango Numérico 

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros Numéricos (Puntajes)")


# Filtro 6: Puntaje Entidad (puntaje_entidad)
min_score = base_datos['puntaje_entidad'].min()
max_score = base_datos['puntaje_entidad'].max()
selected_puntaje = st.sidebar.slider(
    "6. Rango de Puntaje Entidad:",
    min_value=float(min_score),
    max_value=float(max_score),
    value=(float(min_score), float(max_score)),
    step=0.1 # Permite decimales
)

# Filtro 7: Máximo Grupo Par (máximo_grupo_par)
min_max_par = base_datos['máximo_grupo_par'].min()
max_max_par = base_datos['máximo_grupo_par'].max()
selected_max_par = st.sidebar.slider(
    "7. Rango Máx. Grupo Par:",
    min_value=float(min_max_par),
    max_value=float(max_max_par),
    value=(float(min_max_par), float(max_max_par)),
    step=0.1
)

# Filtro 8: Mínimo Grupo Par (mínimo_grupo_par)
min_min_par = base_datos['mínimo_grupo_par'].min()
max_min_par = base_datos['mínimo_grupo_par'].max()
selected_min_par = st.sidebar.slider(
    "8. Rango Mín. Grupo Par:",
    min_value=float(min_min_par),
    max_value=float(max_min_par),
    value=(float(min_min_par), float(max_min_par)),
    step=0.1
)

st.sidebar.markdown("---")

# 3. CREACIÓN DE LA BASE DE DATOS CONTROLADA: df_filtered

df_filtered = base_datos[
    # Filtros Multiselect
    base_datos['departamento'].isin(selected_depto) &
    base_datos['sector'].isin(selected_sector) &
    base_datos['naturaleza_jurídica'].isin(selected_naturaleza) &
    base_datos['orden'].isin(selected_orden) &
    base_datos['vigencia'].isin(selected_vigencia) &

    # Filtros de Rango (Sliders)
    (base_datos['puntaje_entidad'] >= selected_puntaje[0]) &
    (base_datos['puntaje_entidad'] <= selected_puntaje[1]) &

    (base_datos['máximo_grupo_par'] >= selected_max_par[0]) &
    (base_datos['máximo_grupo_par'] <= selected_max_par[1]) &

    (base_datos['mínimo_grupo_par'] >= selected_min_par[0]) &
    (base_datos['mínimo_grupo_par'] <= selected_min_par[1])

].copy()

# =========================================================
# --- BLOQUE DE MÉTRICAS (RESUMEN DEL RENDIMIENTO) ---
# =========================================================

if not df_filtered.empty: # Solo calcula si hay datos después de filtrar

    # 1. CÁLCULOS DE MÉTRICAS NUMÉRICAS BÁSICAS
    total_entidades = df_filtered.shape[0]
    promedio_entidad = df_filtered['puntaje_entidad'].mean().round(2)
    promedio_general_base = base_datos['puntaje_entidad'].mean().round(2)
    delta_promedio = promedio_entidad - promedio_general_base 
    
    # 2. CÁLCULO DE LA NUEVA MÉTRICA DE BRECHA DIGITAL
    df_filtered['brecha_digital'] = df_filtered['máximo_grupo_par'] - df_filtered['puntaje_entidad']
    promedio_brecha = df_filtered['brecha_digital'].mean().round(2)
    
    
    # 3. CÁLCULOS DE MÉTRICAS CATEGÓRICAS (ORDEN)
    
    # Distribución por Orden (Para reemplazar Gráfica 4)
    df_counts_orden = df_filtered['orden'].value_counts()
    count_territorial = df_counts_orden.get('Territorial', 0)
    count_nacional = df_counts_orden.get('Nacional', 0)
    total_filtrado = df_filtered.shape[0]
    pct_territorial = (count_territorial / total_filtrado) * 100 if total_filtrado > 0 else 0
    pct_nacional = (count_nacional / total_filtrado) * 100 if total_filtrado > 0 else 0
    
    # Promedio del IGD por Orden (Para reemplazar Gráfica 5)
    promedios_orden = df_filtered.groupby('orden')['puntaje_entidad'].mean().round(2)
    promedio_nacional = promedios_orden.get('Nacional', 0.00)
    promedio_territorial = promedios_orden.get('Territorial', 0.00)
    
    
    # --- VISUALIZACIÓN DE MÉTRICAS NUMÉRICAS (Promedio IGD, Máximo, Brecha, Conteo) ---
    st.subheader("📊 Resumen del Rendimiento (IGD) y Conteo")
    # Creamos 4 columnas
    col_a, col_b, col_c, col_d = st.columns(4) 
    
    with col_a:
        st.metric(
            label="Promedio IGD Filtrado",
            value=f"{promedio_entidad:.2f}",
            delta=f"{delta_promedio:.2f} vs. Promedio General",
            delta_color="normal" 
        )
    
    with col_b:
        st.metric(
            label="Máximo Puntaje de Entidad",
            value=f"{df_filtered['puntaje_entidad'].max().round(2):.2f}"
        )
        
    with col_c: 
        st.metric(
            label="Promedio de Brecha Digital",
            value=f"{promedio_brecha:.2f}",
            delta=f"{promedio_brecha:.2f} pts. por debajo del potencial", 
            delta_color="inverse" 
        )
    
    with col_d:
        st.metric(
            label="Entidades Analizadas",
            value=f"{total_entidades:,}",
        )
    
    st.markdown("---") 

    # --- VISUALIZACIÓN DE MÉTRICAS CATEGÓRICAS (ORDEN) ---
    st.subheader("🗺️ Distribución y Rendimiento por Orden de Entidad")
    
    # Columna 1 y 2: Distribución Porcentual (Gráfica 4 como métrica)
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown(f"**Conteo Territorial**")
        st.metric(
            label=f"{count_territorial:,} Entidades",
            value=f"{pct_territorial:.1f}%",
            delta="Proporción del Total",
            delta_color="off"
        )

    with col_f:
        st.markdown(f"**Conteo Nacional**")
        st.metric(
            label=f"{count_nacional:,} Entidades",
            value=f"{pct_nacional:.1f}%",
            delta="Proporción del Total",
            delta_color="off"
        )
        
    st.markdown("---") 
    
    # Columna 3 y 4: Promedio IGD por Orden (Gráfica 5 como métrica)
    st.subheader("📈 Promedio IGD por Orden")
    col_g, col_h = st.columns(2)
    
    with col_g:
        st.metric(
            label="Promedio IGD Nacional",
            value=f"{promedio_nacional:.2f}",
            delta=f"{promedio_nacional - promedio_territorial:.2f} pts. más que Territorial",
            delta_color="normal" 
        )

    with col_h:
        st.metric(
            label="Promedio IGD Territorial",
            value=f"{promedio_territorial:.2f}",
            delta=f"{promedio_territorial - promedio_nacional:.2f} pts. menos que Nacional",
            delta_color="inverse" 
        )
        
else:
    # Mensaje si el filtro resulta en cero datos
    st.warning("⚠️ No hay datos para los filtros seleccionados. Por favor, ajusta los criterios.")

st.markdown("---")

#graficas 1 y 2
st.subheader("Distribución de Puntajes del Índice de Gobierno Digital (IGD)")

# Creamos dos columnas de igual tamaño [5, 5]
col1, col2 = st.columns(2) 

# =========================================================
# COLUMNA IZQUIERDA: GRÁFICA 1 (Distribución General)
# =========================================================
with col1:
    st.markdown("##### 1. Distribución del Puntaje Entidad")
    sns.set_style("whitegrid")

    # CLAVE: Ajustamos el tamaño a (5, 3.5) para que coincida con la Gráfica 2
    fig, ax = plt.subplots(figsize=(5, 3.5))

    sns.histplot(
        data=df_filtered, 
        x='puntaje_entidad', 
        kde=True,
        bins=30,
        color='blue',
        ax=ax 
    )

    # Fuentes
    ax.set_title('Distribución General', fontsize=10, fontweight='bold')
    ax.set_xlabel('Puntaje Entidad', fontsize=8)
    ax.set_ylabel('Frecuencia', fontsize=8)
    ax.tick_params(axis='both', labelsize=7) 

    plt.tight_layout() 
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# =========================================================
# COLUMNA DERECHA: GRÁFICA 2 (Distribución Segmentada por Orden)
# =========================================================
with col2:
    st.markdown("##### 2. Distribución Segmentada por Orden de Entidad")

    # Tamaño ligeramente aumentado (5, 3.5)
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))

    # Definimos la paleta de colores: Territorial (verde claro) y Nacional (rojo)
    custom_palette = {'Territorial': '#90EE90', 'Nacional': 'red'} 

    sns.histplot(
        data=df_filtered, 
        x='puntaje_entidad',
        hue='orden', 
        kde=True,
        palette=custom_palette, 
        alpha=0.6,
        ax=ax2,
        legend=False # <--- CLAVE 1: Deshabilitamos la leyenda de Seaborn
    )

    # Reducimos los tamaños de fuente
    ax2.set_title('Distribución Segmentada por Orden', fontsize=9, fontweight='bold')
    ax2.set_xlabel('Puntaje Entidad (0-100)', fontsize=8)
    ax2.set_ylabel('Frecuencia', fontsize=8)
    ax2.set_xlim(0, 100)
    ax2.tick_params(axis='both', labelsize=7)
    
    # CLAVE 2: Creamos y dibujamos la leyenda manualmente en una posición segura (dentro del área de datos)
    ax2.legend(
        handles=[
            plt.Rectangle((0, 0), 1, 1, fc='#90EE90'), # Territorial
            plt.Rectangle((0, 0), 1, 1, fc='red')      # Nacional
        ], 
        labels=['Territorial', 'Nacional'], 
        title='Orden', 
        fontsize=7, 
        title_fontsize=8, 
        loc='upper right', # Ubicación segura dentro del gráfico
        framealpha=0.8 # Fondo semitransparente
    )

    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

st.markdown("---")


# --- COLUMNAS PARA GRÁFICAS 6 Y 7 EN LA MISMA FILA ---
st.subheader("Comparación del Promedio del IGD: Por Departamento vs. Por Sector")

# Mantenemos las proporciones [3, 2] pero ajustaremos los figsizes para control total
col_izq, col_der = st.columns([5.5, 4.5])


# =========================================================
# COLUMNA IZQUIERDA: GRÁFICA 6 (Promedio por Departamento)
# =========================================================
with col_izq:
    st.markdown("##### 3. Promedio del Índice de Gobierno Digital por Departamento")

    # Cálculos de la Gráfica 6 (Se mantienen)
    promedio_territorial = df_filtered[df_filtered['orden'] == 'Territorial']['puntaje_entidad'].mean()
    df_departamentos = df_filtered.groupby('departamento')['puntaje_entidad'].mean().reset_index()
    df_departamentos = df_departamentos.sort_values(by='puntaje_entidad', ascending=False)

    # TAMAÑO ÓPTIMO para muchos ítems: Más ancho que alto, con altura controlada
    fig6, ax6 = plt.subplots(figsize=(7, 7)) 

    sns.barplot(
        x='puntaje_entidad',
        y='departamento',
        data=df_departamentos,
        palette='viridis',
        ax=ax6
    )

    # AJUSTE DE TAMAÑOS DE FUENTE MÁS COMPACTOS
    ax6.set_title('IGD Promedio por Departamento', fontsize=9, fontweight='bold')
    ax6.set_xlabel('Puntaje Promedio (0-100)', fontsize=7)
    ax6.set_ylabel('Departamento', fontsize=7)
    ax6.tick_params(axis='both', labelsize=6) # Reducimos el tamaño de los nombres y números
    
    ax6.set_xlim(0, 100)
    ax6.axvline(promedio_territorial, color='red', linestyle='--', linewidth=1.0,
                label=f'Promedio Territorial: {promedio_territorial:.1f}')
    ax6.legend(loc='lower right', fontsize=6)

    plt.tight_layout() # Asegura que todos los textos quepan
    st.pyplot(fig6, use_container_width=True) # Usamos True para que llene el ancho asignado (3)
    plt.close(fig6)


# =========================================================
# COLUMNA DERECHA: GRÁFICA 7 (Promedio por Sector)
# =========================================================
with col_der:
    st.markdown("##### 4. Promedio del Índice de Gobierno Digital por Sector")

    # Cálculos de la Gráfica 7 (Se mantienen)
    promedio_general = df_filtered['puntaje_entidad'].mean()
    df_sectores = df_filtered.groupby('sector')['puntaje_entidad'].mean().reset_index()
    df_sectores = df_sectores.sort_values(by='puntaje_entidad', ascending=False)

    # CLAVE: Altura fijada a 7 para ser igual a la Gráfica 6
    fig7, ax7 = plt.subplots(figsize=(7, 7)) 

    # Barras horizontales
    sns.barplot(
        y='sector', 
        x='puntaje_entidad',
        data=df_sectores,
        palette='coolwarm',
        ax=ax7
    )

    # Ajuste de tamaños de fuente
    ax7.set_title('IGD Promedio por Sector', fontsize=9, fontweight='bold')
    ax7.set_xlabel('Promedio del Puntaje (0-100)', fontsize=7)
    ax7.set_ylabel('Sector', fontsize=7)
    
    ax7.tick_params(axis='y', labelsize=6) 
    ax7.tick_params(axis='x', labelsize=7)
    
    ax7.set_xlim(0, 100)
    ax7.axvline(promedio_general, color='red', linestyle='--', linewidth=1.0,
                label=f'Promedio General: {promedio_general:.1f}')
    ax7.legend(loc='lower right', fontsize=6)
    
    plt.tight_layout()
    st.pyplot(fig7, use_container_width=True) 
    plt.close(fig7)

st.markdown("---")

#grafico 8

st.subheader("Gráfica 5: Brecha Digital Individual: Puntaje Entidad vs. Máximo Grupo Par")

df_dispersion = df_filtered[['puntaje_entidad', 'máximo_grupo_par', 'orden']].copy()

fig8, ax8 = plt.subplots(figsize=(5, 3)) 

ax = sns.scatterplot(
    x='máximo_grupo_par',
    y='puntaje_entidad',
    data=df_dispersion,
    hue='orden',
    style='orden',
    s=10, 
    alpha=0.5,
    ax=ax8
)

max_val = df_dispersion[['máximo_grupo_par', 'puntaje_entidad']].values.max()

ax8.plot([0, max_val], [0, max_val],
          color='red',
          linestyle='--',
          label='Línea de No Brecha',
          linewidth=0.8) 

ax8.set_title('Brecha Digital Individual: Puntaje vs. Máximo Grupo Par', fontsize=8, fontweight='bold')
ax8.set_xlabel('Máximo Puntaje del Grupo Par (Potencial Ideal)', fontsize=6)
ax8.set_ylabel('Puntaje Entidad (Rendimiento Real)', fontsize=6)
ax8.set_xlim(0, 100)
ax8.set_ylim(0, 100)
ax8.legend(title='Orden', fontsize=5, title_fontsize=6, loc='lower right')
ax8.grid(True, linestyle=':', alpha=0.6, linewidth=0.5)
ax8.tick_params(axis='both', labelsize=6)

plt.tight_layout() 

st.pyplot(fig8, use_container_width=False) 
plt.close(fig8)
st.markdown("---")

#graficas 9 y 10

st.subheader("Mapas de Calor: Rendimiento y Potencial Digital (Comparación)")

# Aumentamos ligeramente la proporción de la columna izquierda a 5.5
col_izq, col_der = st.columns([4.5, 5]) 

# =========================================================
# COLUMNA IZQUIERDA: GRÁFICA 9 (Mapa de Calor por Departamento)
# =========================================================
with col_izq:
    st.markdown("##### 6. Mapa de Calor por Departamento")

    # Cálculos de la Gráfica 9 (Se mantienen)
    df_rendimiento_depto = df_filtered.groupby('departamento').agg(
        Promedio_IGD=('puntaje_entidad', 'mean'),
        Maximo_Par=('máximo_grupo_par', 'mean'),
        Minimo_Par=('mínimo_grupo_par', 'mean')
    ).reset_index()

    df_heatmap_depto = df_rendimiento_depto.set_index('departamento')
    df_heatmap_depto = df_heatmap_depto.sort_values(by='Promedio_IGD', ascending=False)

    # CLAVE: Reducimos la altura del figsize a 6.5 (Mínimo viable con tantos ítems)
    fig9, ax9 = plt.subplots(figsize=(6, 6.5)) 

    sns.heatmap(
        df_heatmap_depto,
        annot=True,
        fmt=".1f",
        cmap='coolwarm',
        linewidths=.5,
        cbar_kws={'label': 'Puntaje'}, 
        ax=ax9,
        annot_kws={"fontsize": 5} # Fuente de los números extremadamente pequeña
    )

    # Reducimos al máximo las fuentes de títulos y etiquetas
    ax9.set_title('Rendimiento y Potencial por Departamento', fontsize=8, fontweight='bold')
    ax9.tick_params(axis='y', rotation=0, labelsize=5) # Nombres de departamentos muy pequeños
    ax9.tick_params(axis='x', labelsize=6) 

    plt.tight_layout() 
    st.pyplot(fig9, use_container_width=True)
    plt.close(fig9)

# =========================================================
# COLUMNA DERECHA: GRÁFICA 10 (Mapa de Calor por Sector)
# =========================================================
with col_der:
    st.markdown("##### 7. Mapa de Calor por Sector")

    # Cálculos de la Gráfica 10 (Se mantienen)
    df_rendimiento_sector = df_filtered.groupby('sector').agg(
        Promedio_IGD=('puntaje_entidad', 'mean'),
        Maximo_Par=('máximo_grupo_par', 'mean'),
        Minimo_Par=('mínimo_grupo_par', 'mean')
    ).reset_index()

    df_heatmap_sector = df_rendimiento_sector.set_index('sector')
    df_heatmap_sector = df_heatmap_sector.sort_values(by='Promedio_IGD', ascending=False)

    # TAMAÑO: 6 de ancho, 6.0 de alto
    fig10, ax10 = plt.subplots(figsize=(6, 6)) 

    sns.heatmap(
        df_heatmap_sector,
        annot=True,
        fmt=".1f",
        cmap='coolwarm',
        linewidths=.5,
        cbar_kws={'label': 'Puntaje'},
        ax=ax10,
        annot_kws={"fontsize": 5} 
    )

    # AJUSTES DE FUENTE: Reducimos el tamaño del título y los nombres de los sectores
    ax10.set_title('Rendimiento y Potencial por Sector', fontsize=7, fontweight='bold') # Título más pequeño
    ax10.tick_params(axis='y', rotation=0, labelsize=6) # Nombres de sectores (etiquetas Y) más pequeños
    ax10.tick_params(axis='x', labelsize=6) # Números de puntaje (etiquetas X) más pequeños
    
    plt.tight_layout() # Esto asegurará que el área del gráfico se amplíe
    st.pyplot(fig10, use_container_width=True) 
    plt.close(fig10)

st.markdown("---")

#grafico 11

st.subheader("Gráfica 8: Distribución de Instituciones por Departamento")

# *** YA NO USAMOS st.columns para que ocupe más ancho. ***
# col_g11_small, col_g11_spacer = st.columns([1.0, 1.0]) 

# with col_g11_small: # Quitamos el 'with' de la columna
sns.set_style("white")

# *** AUMENTAMOS EL FIGSIZE A (12, 6) PARA MÁS RESOLUCIÓN Y TAMAÑO ***
fig11, ax11 = plt.subplots(figsize=(12, 6)) 

sns.countplot(
    data=df_filtered, 
    x='departamento',
    color='skyblue',
    edgecolor='black',
    order=df_filtered['departamento'].value_counts().index, 
    ax=ax11
)

# Aumentamos el tamaño de fuente para que sea legible
ax11.tick_params(axis='x', rotation=90, labelsize=9) 
ax11.set_title('Distribución de Instituciones por Departamento', fontsize=14) 
ax11.set_xlabel('Departamento', fontsize=10)
ax11.set_ylabel('Número de Instituciones', fontsize=10)
ax11.tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig11) # Usamos st.pyplot normal
plt.close(fig11)
    
st.markdown("---")

#grafico 12

st.subheader("Gráfica 9: Distribución de Naturaleza Jurídica por Departamento")

# *** YA NO USAMOS st.columns PARA LA G12. Que ocupe el ancho disponible. ***
# col_g12_small, col_g12_spacer = st.columns([1.0, 1.0]) 

# with col_g12_small: # Quitamos el 'with' de la columna

# *** AUMENTAMOS EL FIGSIZE PARA MÁS RESOLUCIÓN: (12, 6) ***
fig12, ax12 = plt.subplots(figsize=(12, 6)) 

contingency_table = pd.crosstab(df_filtered['departamento'], df_filtered['naturaleza_jurídica'])

sns.heatmap(
    contingency_table,
    cmap='YlGnBu',
    annot=True,
    fmt='d',
    linewidths=.5,
    ax=ax12,
    # *** AUMENTAMOS LA FUENTE INTERNA A 4 PARA LEGIBILIDAD ***
    annot_kws={"fontsize": 4}, 
    # Barra de color más grande
    cbar_kws={'shrink': 0.8} 
)

# Título y etiquetas de ejes con fuentes legibles
ax12.set_title('Distribución de Naturaleza Jurídica por Departamento', fontsize=10) 
ax12.set_xlabel('Naturaleza Jurídica', fontsize=8)
ax12.set_ylabel('Departamento', fontsize=8)

# Marcas de los ejes con letras legibles (para que quepan)
ax12.tick_params(axis='x', rotation=90, labelsize=7) # Etiquetas de las columnas (Naturaleza)
ax12.tick_params(axis='y', rotation=0, labelsize=7) # Etiquetas de las filas (Departamento)

# Controlamos el tamaño de la barra de color (leyenda)
cbar = ax12.collections[0].colorbar
cbar.ax.tick_params(labelsize=8)
cbar.set_label('Conteo (Entidades)', fontsize=9)

# Usamos tight_layout para mantener la estabilidad
plt.tight_layout() 

# *** Usamos st.pyplot normal para que ocupe el ancho disponible de Streamlit ***
st.pyplot(fig12)
plt.close(fig12)

st.markdown("---")

#GRAFICA 13 Y 14

# Crea dos columnas para colocar las gráficas una al lado de la otra
col_g13, col_g14 = st.columns(2)

# =========================================================
# --- GRÁFICA 13: Departamentos Rezagados (Boxplot) ---
# =========================================================
with col_g13:
    st.subheader("Gráfica 10: Variabilidad del Puntaje IGD en los Departamentos más Rezagados")

    # Cálculos
    departamentos_rezagados = df_filtered.groupby('departamento')['puntaje_entidad'].mean().nsmallest(5).index.tolist()
    df_rezagados = df_filtered[df_filtered['departamento'].isin(departamentos_rezagados)].copy()
    orden_rezagados = df_rezagados.groupby('departamento')['puntaje_entidad'].mean().sort_values(ascending=True).index

    # Figura (Tamaño ajustado a la columna)
    fig13, ax13 = plt.subplots(figsize=(6, 4))

    sns.boxplot(
        x='puntaje_entidad',
        y='departamento',
        data=df_rezagados,
        order=orden_rezagados,
        palette='Reds',
        fliersize=5,
        ax=ax13
    )

    ax13.set_title(f'IGD en {len(departamentos_rezagados)} Departamentos más Rezagados',
                  fontsize=10,
                  fontweight='bold')
    ax13.set_xlabel('Puntaje Entidad (0-100)', fontsize=8)
    ax13.set_ylabel('Departamento', fontsize=8)
    ax13.tick_params(axis='x', labelsize=7)
    ax13.tick_params(axis='y', labelsize=7)
    ax13.set_xlim(0, 100)

    # *** SOLUCIÓN: Añadir tight_layout para ajuste y estabilidad ***
    plt.tight_layout()
    st.pyplot(fig13)
    plt.close(fig13)


# =========================================================
# --- GRÁFICA 14: Sectores Rezagados (Boxplot) ---
# =========================================================
with col_g14:
    st.subheader("Gráfica 11: Variabilidad del Puntaje IGD en los Sectores más Rezagados")

    # Cálculos
    sectores_rezagados = df_filtered.groupby('sector')['puntaje_entidad'].mean().nsmallest(5).index.tolist()
    
    # Lógica para forzar el salto de línea en etiquetas largas
    def format_sector_label(label):
        if len(label) > 25:
            return label.replace(' y de ', ' y de\n', 1).replace(', la ', ',\nla ', 1).replace(' la ', '\nla ', 1)
        return label
    
    df_rezagados_sector = df_filtered[df_filtered['sector'].isin(sectores_rezagados)].copy()
    df_rezagados_sector['sector_short'] = df_rezagados_sector['sector'].apply(format_sector_label)
    orden_rezagados_sector = df_rezagados_sector.groupby('sector_short')['puntaje_entidad'].mean().sort_values(ascending=True).index

    # *** AJUSTE CLAVE: FIGSIZE A (7, 4) PARA HACERLO MÁS ANCHO Y AMPLIO ***
    fig14, ax14 = plt.subplots(figsize=(7, 4)) 

    sns.boxplot(
        x='puntaje_entidad',
        y='sector_short', 
        data=df_rezagados_sector,
        order=orden_rezagados_sector,
        palette='Purples',
        fliersize=5,
        ax=ax14
    )

    # AJUSTES DE TEXTO PEQUEÑO
    ax14.set_title(f'IGD en {len(sectores_rezagados)} Sectores más Rezagados',
                  fontsize=8, 
                  fontweight='bold')
    ax14.set_xlabel('Puntaje Entidad (0-100)', fontsize=6) 
    ax14.set_ylabel('Sector', fontsize=6) 
    ax14.tick_params(axis='x', labelsize=6) 
    # *** LABELS DE LOS SECTORES A 6 PARA MÁS ESPACIO ***
    ax14.tick_params(axis='y', labelsize=6) 
    ax14.set_xlim(0, 100)

    plt.tight_layout()
    st.pyplot(fig14)
    plt.close(fig14)

#grafica 15

st.subheader("Gráfica 12: Evolución del Rendimiento del IGD: Nacional vs. Territorial")

df_tendencia = df_filtered.groupby(['vigencia', 'orden'])['puntaje_entidad'].mean().reset_index(name='Promedio_IGD')

fig_linea = px.line(
    df_tendencia,
    x='vigencia',
    y='Promedio_IGD',
    color='orden',
    line_dash='orden',
    markers=True,
    title='Evolución del Rendimiento del IGD: Nacional vs. Territorial',
    labels={'Promedio_IGD': 'Puntaje Promedio IGD', 'vigencia': 'Año de Medición', 'orden': 'Orden de la Entidad'}
)

fig_linea.update_layout(
    xaxis_title='Vigencia (Año)',
    yaxis_title='Puntaje Promedio IGD',
    yaxis=dict(range=[40, 90]),
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig_linea, use_container_width=True)
st.markdown("---")


#python3 -m streamlit run trabajofinal.py

#cd "Trabajo Final"
#streamlit run trabajofinal.py

# Tabla resumen
#st.subheader('🏙️ Resumen por ciudad actual')
#tabla_ciudad = df_filtrado['ciudad_actual_'].value_counts().reset_index()
#tabla_ciudad.columns = ['Ciudad actual', 'Número de personas']
#st.dataframe(tabla_ciudad, use_container_width=True)

#st.markdown('---')
#st.caption('Dashboard de datos personales')