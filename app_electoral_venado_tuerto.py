import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Dinámica Electoral Venado Tuerto 2019-2025",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado - FONDO GRIS SUAVE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    :root {
        color-scheme: light !important;
    }

    * {
        color-scheme: light !important;
    }

    html, body, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stApp"],
    [data-testid="stHeader"],
    .main, 
    .block-container,
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div {
        background-color: #f8f9fa !important;
        color: #2c3e50 !important;
    }

    html, body, [class*="css"], p, span, div, label, h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        color: #2c3e50 !important;
    }

    h1 {
        color: #2c3e50 !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
        margin-bottom: 1rem !important;
    }

    h2 {
        color: #34495e !important;
        font-weight: 600 !important;
        font-size: 1.6rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h3 {
        color: #4a5568 !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: #f8f9fa !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        color: #2c3e50 !important;
        border: 1px solid #dee2e6 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
        color: white !important;
        border: 1px solid #007bff !important;
    }

    .stSelectbox > div > div,
    .stSelectbox > div > div > div,
    [data-baseweb="select"],
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 4px !important;
    }

    [data-baseweb="select"] div[role="button"] {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }

    [role="option"] {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }

    [role="option"]:hover {
        background-color: #f3f4f6 !important;
    }

    .stMultiSelect > div > div,
    [data-baseweb="tag"] {
        background-color: #007bff !important;
        color: white !important;
    }

    .stCheckbox {
        padding-left: 0 !important;
        margin-left: 0 !important;
    }

    .stCheckbox > label {
        color: #2c3e50 !important;
    }

    .stNumberInput > div,
    .stNumberInput > div > div,
    .stNumberInput > div > div > div {
        background-color: #ffffff !important;
    }

    .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 4px !important;
        font-size: 14px !important;
        padding: 8px 12px !important;
    }

    .stNumberInput > div > div > input:focus {
        border-color: #007bff !important;
        box-shadow: 0 0 0 1px #007bff !important;
    }

    .stNumberInput label {
        color: #2c3e50 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    button[kind="stepUpButton"], 
    button[kind="stepDownButton"] {
        background-color: #f3f4f6 !important;
        border: 1px solid #d1d5db !important;
        color: #2c3e50 !important;
    }

    button[kind="stepUpButton"]:hover, 
    button[kind="stepDownButton"]:hover {
        background-color: #e5e7eb !important;
    }

    .stDataFrame,
    .stDataFrame > div,
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }

    .stDataFrame table {
        background-color: #ffffff !important;
    }

    .stDataFrame th {
        background-color: #e9ecef !important;
        color: #2c3e50 !important;
    }

    .stDataFrame td {
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown span,
    .stMarkdown div {
        color: #2c3e50 !important;
        background-color: transparent !important;
    }

    .stMarkdown strong {
        color: #2c3e50 !important;
    }

    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border: 1px solid #ffeaa7 !important;
    }
</style>
""", unsafe_allow_html=True)

# Paleta de colores
COLORES_PARTIDOS = {
    "UNIDOS": "#ff7f0e",
    "PJ (K)": "#0088ff",
    "PJ NO K": "#2510a3",
    "PRO": "#ffde21",
    "FRENTE AMPLIO PROGRESISTA (SOC)": "#9467bd",
    "LLA": "#4c2882",
    "CIUDAD FUTURA": "#ff0000",
    "IZQUIERDA": "#e74c3c",
    "OTROS": "#008f39",
    "BLANCOS": "#CCCCCC",
    "ANULADOS": "#666666",
    "NUEVO HORIZONTE": "#17a2b8",
    "VENADO RENACE": "#20c997",
    "GEN": "#6c757d",
    "SOMOS VIDA Y LIBERTAD": "#fd7e14"
}

# Diccionario para normalizar nombres de cargos
NOMBRES_CARGOS = {
    "Diputados N": "Diputados Nacionales",
    "Senadores N": "Senadores Nacionales",
    "Diputado P": "Diputado Provincial",
    "Senador P": "Senador Provincial",
    "Convencionales D": "Convencionales Departamentales",
    "Convencionales DÚ": "Convencionales del Distrito Único"
}

# Mapeo de cuadrantes
CUADRANTES = {
    "O": "Oeste",
    "N": "Norte",
    "E": "Este",
    "S": "Sur"
}

def normalizar_cargo(cargo):
    """Convierte nombres cortos de cargos a nombres completos"""
    return NOMBRES_CARGOS.get(cargo, cargo)

# Cargar datos
@st.cache_data
def cargar_datos():
    df_participacion = pd.read_csv("participacion_hist.csv")
    df_participacion_cuad = pd.read_csv("participacion_hist_cuad.csv")
    df_resultados = pd.read_csv("agrup_def.csv")

    df_resultados = df_resultados.drop(columns=["Unnamed: 20", "Unnamed: 21", "Unnamed: 22", "Unnamed: 23"], errors="ignore")

    for col in df_participacion.columns:
        if "Participación" in col or "%" in col:
            if df_participacion[col].dtype == "object":
                df_participacion[col] = df_participacion[col].str.replace("%", "").str.replace(",", ".").astype(float)

    for col in df_participacion_cuad.columns:
        if col in ["O", "N", "E", "S"] or "Participación" in col:
            if df_participacion_cuad[col].dtype == "object":
                df_participacion_cuad[col] = df_participacion_cuad[col].str.replace("%", "").str.replace(",", ".").astype(float)

    for col in df_resultados.columns:
        if "%" in col:
            if df_resultados[col].dtype == "object":
                df_resultados[col] = df_resultados[col].str.replace("%", "").str.replace(",", ".").astype(float)

    return df_participacion, df_participacion_cuad, df_resultados

df_part, df_part_cuad, df_res = cargar_datos()

def get_color(partido):
    return COLORES_PARTIDOS.get(partido, "#95a5a6")

# Título principal con emoji
st.title("🗳️ Dinámica Electoral en la Ciudad de Venado Tuerto (2019 - 2025)")

# Crear pestañas principales
tab1, tab2 = st.tabs(["📊 Análisis de Resultados Electorales", "🔮 Simulador Electoral"])

with tab1:
    st.markdown("---")

    # Subtabs para local y provincial
    subtab_local, subtab_provincial = st.tabs(["🏛️ Cargos Locales", "🏢 Cargos Provinciales y Nacionales"])

    with subtab_local:
        st.header("Análisis Electoral - Cargos Locales")

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            cargos_locales = ["Intendente", "Concejales"]
            cargo_sel = st.selectbox("Cargo", cargos_locales, key="cargo_local")

        with col2:
            tipo_elec = st.selectbox("Tipo de Elección", ["Primarias", "Generales", "Ambas"], key="tipo_local")

        with col3:
            vista_cuadrantes = st.selectbox("Vista", ["Total", "Por Cuadrante"], key="vista_local")

        # Filtro de años
        años_disponibles = sorted(df_res[df_res["Cargo"] == cargo_sel]["Año"].unique())
        años_sel = st.multiselect(
            "Seleccionar años a mostrar",
            options=años_disponibles,
            default=años_disponibles,
            key="años_local"
        )

        incluir_blancos = st.checkbox("Incluir Blancos y Anulados", value=False, key="blancos_local")

        # Filtrar datos
        df_cargo = df_res[df_res["Cargo"] == cargo_sel].copy()

        if años_sel:
            df_cargo = df_cargo[df_cargo["Año"].isin(años_sel)]

        if tipo_elec != "Ambas":
            df_cargo = df_cargo[df_cargo["Elección"] == tipo_elec]

        if not incluir_blancos:
            df_cargo = df_cargo[~df_cargo["Partido"].isin(["BLANCOS", "ANULADOS"])]

        # Gráfico 1: Comparación por año y tipo de elección
        st.subheader(f"Evolución de votos - {normalizar_cargo(cargo_sel)}")

        if vista_cuadrantes == "Total":
            años = sorted(df_cargo["Año"].unique())

            fig = go.Figure()

            for partido in df_cargo["Partido"].unique():
                df_partido = df_cargo[df_cargo["Partido"] == partido]

                x_labels = []
                y_values = []

                for año in años:
                    for tipo in df_partido[df_partido["Año"] == año]["Elección"].unique():
                        df_temp = df_partido[(df_partido["Año"] == año) & (df_partido["Elección"] == tipo)]
                        if not df_temp.empty:
                            x_labels.append(f"{año}<br>{tipo}")
                            y_values.append(df_temp["% sobre votos emitidos válidos"].values[0])

                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=y_values,
                    marker_color=get_color(partido),
                    text=[f"{v:.1f}%" for v in y_values],
                    textposition="outside",
                    width=0.6
                ))

            fig.update_layout(
                barmode="group",
                height=500,
                xaxis_title="Año y Tipo de Elección",
                yaxis_title="Porcentaje de Votos (%)",
                legend_title="Fuerza Política",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                bargap=0.3,
                bargroupgap=0.1
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            # SUBPLOTS: Un panel por cuadrante CON BARRAS MÁS FINITAS
            cuadrantes_sel = st.multiselect(
                "Seleccionar cuadrantes para comparar",
                options=["Oeste", "Norte", "Este", "Sur"],
                default=["Oeste"],
                key="cuad_local"
            )

            if cuadrantes_sel:
                años = sorted(df_cargo["Año"].unique())
                cuad_map_inv = {v: k for k, v in CUADRANTES.items()}

                n_cuadrantes = len(cuadrantes_sel)

                rows = (n_cuadrantes + 1) // 2
                cols = 2 if n_cuadrantes > 1 else 1

                fig = make_subplots(
                    rows=rows,
                    cols=cols,
                    subplot_titles=cuadrantes_sel,
                    vertical_spacing=0.12,
                    horizontal_spacing=0.1
                )

                for idx, cuadrante_nombre in enumerate(cuadrantes_sel):
                    row = (idx // 2) + 1
                    col = (idx % 2) + 1

                    cuadrante_codigo = cuad_map_inv[cuadrante_nombre]

                    for partido in df_cargo["Partido"].unique():
                        df_partido = df_cargo[df_cargo["Partido"] == partido]

                        x_labels = []
                        y_values = []

                        for año in años:
                            for tipo in df_partido[df_partido["Año"] == año]["Elección"].unique():
                                df_temp_all = df_cargo[(df_cargo["Año"] == año) & (df_cargo["Elección"] == tipo)]
                                total_cuadrante = df_temp_all[cuadrante_codigo].sum()

                                df_temp = df_partido[(df_partido["Año"] == año) & (df_partido["Elección"] == tipo)]
                                if not df_temp.empty:
                                    x_labels.append(f"{año}<br>{tipo}")
                                    votos_partido = df_temp[cuadrante_codigo].values[0]
                                    porcentaje = (votos_partido / total_cuadrante * 100) if total_cuadrante > 0 else 0
                                    y_values.append(porcentaje)

                        showlegend = (idx == 0)

                        fig.add_trace(
                            go.Bar(
                                name=partido,
                                x=x_labels,
                                y=y_values,
                                marker_color=get_color(partido),
                                text=[f"{v:.1f}%" for v in y_values],
                                textposition="outside",
                                width=0.35,  # ← BARRAS MÁS FINITAS
                                legendgroup=partido,
                                showlegend=showlegend
                            ),
                            row=row,
                            col=col
                        )

                fig.update_xaxes(title_text="Año y Tipo", showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
                fig.update_yaxes(title_text="% Votos", showgrid=True, gridwidth=1, gridcolor="#e0e0e0")

                height = 400 * rows

                fig.update_layout(
                    height=height,
                    title_text=f"Comparación por Cuadrante: {normalizar_cargo(cargo_sel)}",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5
                    ),
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#f8f9fa",
                    font=dict(family="Inter, sans-serif", size=11, color="#2c3e50"),
                    barmode="group",
                    bargap=0.35,  # ← MÁS ESPACIO ENTRE GRUPOS
                    bargroupgap=0.15  # ← MÁS ESPACIO DENTRO DE GRUPOS
                )

                st.plotly_chart(fig, use_container_width=True)

        # Gráfico 2: Evolución de una fuerza específica en Generales
        st.subheader("Evolución histórica por fuerza política")

        df_generales = df_cargo[df_cargo["Elección"] == "Generales"]
        partidos_disponibles = [p for p in df_generales["Partido"].unique() if p not in ["BLANCOS", "ANULADOS"]]

        if partidos_disponibles:
            fuerza_sel = st.selectbox("Seleccionar fuerza política", partidos_disponibles, key="fuerza_local")

            df_fuerza = df_generales[df_generales["Partido"] == fuerza_sel]

            fig = go.Figure()

            años = sorted(df_fuerza["Año"].unique())
            porcentajes = [df_fuerza[df_fuerza["Año"] == año]["% sobre votos emitidos válidos"].values[0] if año in df_fuerza["Año"].values else 0 for año in años]

            fig.add_trace(go.Scatter(
                x=años,
                y=porcentajes,
                mode="lines+markers+text",
                name=fuerza_sel,
                line=dict(color=get_color(fuerza_sel), width=3),
                marker=dict(size=12),
                text=[f"{p:.1f}%" for p in porcentajes],
                textposition="top center"
            ))

            fig.update_layout(
                title=f"Evolución de {fuerza_sel} en Elecciones Generales - {normalizar_cargo(cargo_sel)}",
                height=400,
                xaxis_title="Año",
                yaxis_title="Porcentaje de Votos (%)",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        # Gráfico 3: Comparación porcentual
        st.subheader("Distribución porcentual del voto")

        año_comp = st.selectbox("Seleccionar año", sorted(df_cargo["Año"].unique(), reverse=True), key="año_comp_local")

        df_año = df_cargo[df_cargo["Año"] == año_comp]

        fig = go.Figure()

        tipos = df_año["Elección"].unique()

        for partido in df_año["Partido"].unique():
            df_partido = df_año[df_año["Partido"] == partido]

            porcentajes = []
            x_labels = []

            for tipo in ["Primarias", "Generales"]:
                if tipo in tipos:
                    df_temp = df_partido[df_partido["Elección"] == tipo]
                    if not df_temp.empty:
                        porcentajes.append(df_temp["% sobre votos emitidos válidos"].values[0])
                        x_labels.append(tipo)

            if porcentajes:
                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=porcentajes,
                    marker_color=get_color(partido),
                    text=[f"{p:.1f}%" for p in porcentajes],
                    textposition="inside"
                ))

        fig.update_layout(
            barmode="stack",
            title=f"Distribución porcentual - {normalizar_cargo(cargo_sel)} {año_comp}",
            height=450,
            xaxis_title="Tipo de Elección",
            yaxis_title="Porcentaje de Votos (%)",
            legend_title="Fuerza Política",
            hovermode="x unified",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#f8f9fa",
            font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
        )

        st.plotly_chart(fig, use_container_width=True)

        # Gráfico 4: Participación electoral
        st.subheader(f"Evolución de la participación electoral - {normalizar_cargo(cargo_sel)}")

        df_part_cargo = df_part[df_part["Cargo"] == cargo_sel]

        if años_sel:
            df_part_cargo = df_part_cargo[df_part_cargo["Año"].isin(años_sel)]

        fig = go.Figure()

        for tipo in df_part_cargo["Tipo elección"].unique():
            df_tipo = df_part_cargo[df_part_cargo["Tipo elección"] == tipo]

            fig.add_trace(go.Scatter(
                x=df_tipo["Año"],
                y=df_tipo["Participación"],
                mode="lines+markers+text",
                name=tipo,
                line=dict(width=3),
                marker=dict(size=10),
                text=[f"{p:.1f}%" for p in df_tipo["Participación"]],
                textposition="top center"
            ))

        fig.update_layout(
            title="Porcentaje de Participación sobre el Padrón Electoral",
            height=400,
            xaxis_title="Año",
            yaxis_title="Participación (%)",
            hovermode="x unified",
            plot_bgcolor="#ffffff",
            paper_bgcolor="#f8f9fa",
            font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0", range=[0, 100])
        )

        st.plotly_chart(fig, use_container_width=True)

    with subtab_provincial:
        st.header("Análisis Electoral - Cargos Provinciales y Nacionales")

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            cargos_prov = ["Gobernador", "Presidente", "Diputados N", "Senadores N", 
                          "Diputado P", "Senador P", "Convencionales D", "Convencionales DÚ"]
            cargo_sel_p = st.selectbox("Cargo", cargos_prov, key="cargo_prov")

        with col2:
            tipo_elec_p = st.selectbox("Tipo de Elección", ["Primarias", "Generales", "Ambas"], key="tipo_prov")

        with col3:
            vista_cuadrantes_p = st.selectbox("Vista", ["Total", "Por Cuadrante"], key="vista_prov")

        # Filtro de años
        años_disponibles_p = sorted(df_res[df_res["Cargo"] == cargo_sel_p]["Año"].unique())
        años_sel_p = st.multiselect(
            "Seleccionar años a mostrar",
            options=años_disponibles_p,
            default=años_disponibles_p,
            key="años_prov"
        )

        incluir_blancos_p = st.checkbox("Incluir Blancos y Anulados", value=False, key="blancos_prov")

        df_cargo_p = df_res[df_res["Cargo"] == cargo_sel_p].copy()

        if años_sel_p:
            df_cargo_p = df_cargo_p[df_cargo_p["Año"].isin(años_sel_p)]

        if tipo_elec_p != "Ambas":
            df_cargo_p = df_cargo_p[df_cargo_p["Elección"] == tipo_elec_p]

        if not incluir_blancos_p:
            df_cargo_p = df_cargo_p[~df_cargo_p["Partido"].isin(["BLANCOS", "ANULADOS"])]

        st.subheader(f"Evolución de votos - {normalizar_cargo(cargo_sel_p)}")

        if vista_cuadrantes_p == "Total":
            años = sorted(df_cargo_p["Año"].unique())

            fig = go.Figure()

            for partido in df_cargo_p["Partido"].unique():
                df_partido = df_cargo_p[df_cargo_p["Partido"] == partido]

                x_labels = []
                y_values = []

                for año in años:
                    for tipo in df_partido[df_partido["Año"] == año]["Elección"].unique():
                        df_temp = df_partido[(df_partido["Año"] == año) & (df_partido["Elección"] == tipo)]
                        if not df_temp.empty:
                            x_labels.append(f"{año}<br>{tipo}")
                            y_values.append(df_temp["% sobre votos emitidos válidos"].values[0])

                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=y_values,
                    marker_color=get_color(partido),
                    text=[f"{v:.1f}%" for v in y_values],
                    textposition="outside",
                    width=0.6
                ))

            fig.update_layout(
                barmode="group",
                height=500,
                xaxis_title="Año y Tipo de Elección",
                yaxis_title="Porcentaje de Votos (%)",
                legend_title="Fuerza Política",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                bargap=0.3,
                bargroupgap=0.1
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            # SUBPLOTS CON BARRAS MÁS FINITAS
            cuadrantes_sel_p = st.multiselect(
                "Seleccionar cuadrantes para comparar",
                options=["Oeste", "Norte", "Este", "Sur"],
                default=["Oeste"],
                key="cuad_prov"
            )

            if cuadrantes_sel_p:
                años = sorted(df_cargo_p["Año"].unique())
                cuad_map_inv = {v: k for k, v in CUADRANTES.items()}

                n_cuadrantes = len(cuadrantes_sel_p)

                rows = (n_cuadrantes + 1) // 2
                cols = 2 if n_cuadrantes > 1 else 1

                fig = make_subplots(
                    rows=rows,
                    cols=cols,
                    subplot_titles=cuadrantes_sel_p,
                    vertical_spacing=0.12,
                    horizontal_spacing=0.1
                )

                for idx, cuadrante_nombre in enumerate(cuadrantes_sel_p):
                    row = (idx // 2) + 1
                    col = (idx % 2) + 1

                    cuadrante_codigo = cuad_map_inv[cuadrante_nombre]

                    for partido in df_cargo_p["Partido"].unique():
                        df_partido = df_cargo_p[df_cargo_p["Partido"] == partido]

                        x_labels = []
                        y_values = []

                        for año in años:
                            for tipo in df_partido[df_partido["Año"] == año]["Elección"].unique():
                                df_temp_all = df_cargo_p[(df_cargo_p["Año"] == año) & (df_cargo_p["Elección"] == tipo)]
                                total_cuadrante = df_temp_all[cuadrante_codigo].sum()

                                df_temp = df_partido[(df_partido["Año"] == año) & (df_partido["Elección"] == tipo)]
                                if not df_temp.empty:
                                    x_labels.append(f"{año}<br>{tipo}")
                                    votos_partido = df_temp[cuadrante_codigo].values[0]
                                    porcentaje = (votos_partido / total_cuadrante * 100) if total_cuadrante > 0 else 0
                                    y_values.append(porcentaje)

                        showlegend = (idx == 0)

                        fig.add_trace(
                            go.Bar(
                                name=partido,
                                x=x_labels,
                                y=y_values,
                                marker_color=get_color(partido),
                                text=[f"{v:.1f}%" for v in y_values],
                                textposition="outside",
                                width=0.35,  # ← BARRAS MÁS FINITAS
                                legendgroup=partido,
                                showlegend=showlegend
                            ),
                            row=row,
                            col=col
                        )

                fig.update_xaxes(title_text="Año y Tipo", showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
                fig.update_yaxes(title_text="% Votos", showgrid=True, gridwidth=1, gridcolor="#e0e0e0")

                height = 400 * rows

                fig.update_layout(
                    height=height,
                    title_text=f"Comparación por Cuadrante: {normalizar_cargo(cargo_sel_p)}",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5
                    ),
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#f8f9fa",
                    font=dict(family="Inter, sans-serif", size=11, color="#2c3e50"),
                    barmode="group",
                    bargap=0.35,
                    bargroupgap=0.15
                )

                st.plotly_chart(fig, use_container_width=True)

        st.subheader("Evolución histórica por fuerza política")

        df_generales_p = df_cargo_p[df_cargo_p["Elección"] == "Generales"]
        partidos_disponibles_p = [p for p in df_generales_p["Partido"].unique() if p not in ["BLANCOS", "ANULADOS"]]

        if partidos_disponibles_p:
            fuerza_sel_p = st.selectbox("Seleccionar fuerza política", partidos_disponibles_p, key="fuerza_prov")

            df_fuerza_p = df_generales_p[df_generales_p["Partido"] == fuerza_sel_p]

            fig = go.Figure()

            años = sorted(df_fuerza_p["Año"].unique())
            porcentajes = [df_fuerza_p[df_fuerza_p["Año"] == año]["% sobre votos emitidos válidos"].values[0] if año in df_fuerza_p["Año"].values else 0 for año in años]

            fig.add_trace(go.Scatter(
                x=años,
                y=porcentajes,
                mode="lines+markers+text",
                name=fuerza_sel_p,
                line=dict(color=get_color(fuerza_sel_p), width=3),
                marker=dict(size=12),
                text=[f"{p:.1f}%" for p in porcentajes],
                textposition="top center"
            ))

            fig.update_layout(
                title=f"Evolución de {fuerza_sel_p} en Elecciones Generales - {normalizar_cargo(cargo_sel_p)}",
                height=400,
                xaxis_title="Año",
                yaxis_title="Porcentaje de Votos (%)",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Comparaciones Específicas 2023-2025")

        col_comp1, col_comp2 = st.columns(2)

        with col_comp1:
            st.markdown(f"#### Gobernador 2023 (Generales) vs {normalizar_cargo('Diputados N')} 2025 (Generales)")

            df_gob_2023 = df_res[(df_res["Cargo"] == "Gobernador") & 
                                  (df_res["Año"] == 2023) & 
                                  (df_res["Elección"] == "Generales") &
                                  (~df_res["Partido"].isin(["BLANCOS", "ANULADOS"]))].copy()

            df_dip_2025 = df_res[(df_res["Cargo"] == "Diputados N") & 
                                  (df_res["Año"] == 2025) & 
                                  (df_res["Elección"] == "Generales") &
                                  (~df_res["Partido"].isin(["BLANCOS", "ANULADOS"]))].copy()

            partidos_comunes = set(df_gob_2023["Partido"].unique()) & set(df_dip_2025["Partido"].unique())

            fig = go.Figure()

            for partido in partidos_comunes:
                pct_2023 = df_gob_2023[df_gob_2023["Partido"] == partido]["% sobre votos emitidos válidos"].values
                pct_2025 = df_dip_2025[df_dip_2025["Partido"] == partido]["% sobre votos emitidos válidos"].values

                if len(pct_2023) > 0 and len(pct_2025) > 0:
                    fig.add_trace(go.Bar(
                        name=partido,
                        x=["Gobernador 2023", f"{normalizar_cargo('Diputados N')} 2025"],
                        y=[pct_2023[0], pct_2025[0]],
                        marker_color=get_color(partido),
                        text=[f"{pct_2023[0]:.1f}%", f"{pct_2025[0]:.1f}%"],
                        textposition="outside"
                    ))

            fig.update_layout(
                barmode="group",
                height=450,
                xaxis_title="Elección",
                yaxis_title="Porcentaje de Votos (%)",
                legend_title="Fuerza Política",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=11, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        with col_comp2:
            st.markdown(f"#### Gobernador 2023 (Generales) vs {normalizar_cargo('Convencionales DÚ')} 2025 (Primarias)")

            df_conv_2025 = df_res[(df_res["Cargo"] == "Convencionales DÚ") & 
                                   (df_res["Año"] == 2025) & 
                                   (df_res["Elección"] == "Primarias") &
                                   (~df_res["Partido"].isin(["BLANCOS", "ANULADOS"]))].copy()

            partidos_comunes2 = set(df_gob_2023["Partido"].unique()) & set(df_conv_2025["Partido"].unique())

            fig = go.Figure()

            for partido in partidos_comunes2:
                pct_2023 = df_gob_2023[df_gob_2023["Partido"] == partido]["% sobre votos emitidos válidos"].values
                pct_2025 = df_conv_2025[df_conv_2025["Partido"] == partido]["% sobre votos emitidos válidos"].values

                if len(pct_2023) > 0 and len(pct_2025) > 0:
                    fig.add_trace(go.Bar(
                        name=partido,
                        x=["Gobernador 2023", f"{normalizar_cargo('Convencionales DÚ')} 2025"],
                        y=[pct_2023[0], pct_2025[0]],
                        marker_color=get_color(partido),
                        text=[f"{pct_2023[0]:.1f}%", f"{pct_2025[0]:.1f}%"],
                        textposition="outside"
                    ))

            fig.update_layout(
                barmode="group",
                height=450,
                xaxis_title="Elección",
                yaxis_title="Porcentaje de Votos (%)",
                legend_title="Fuerza Política",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=11, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🔮 Simulador Electoral")
    st.markdown("Esta herramienta permite simular escenarios electorales variando el nivel de participación y la distribución de votos entre fuerzas políticas.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Configuración")

        cargo_sim = st.selectbox("Cargo a simular", 
                                 ["Intendente", "Concejales", "Gobernador", "Presidente", "Diputados N"],
                                 key="cargo_sim")

        años_disponibles = sorted(df_res[df_res["Cargo"] == cargo_sim]["Año"].unique(), reverse=True)
        año_base = st.selectbox("Año base", años_disponibles, key="año_sim")

        tipo_base = st.selectbox("Tipo de elección base", ["Generales", "Primarias"], key="tipo_sim")

        df_base = df_res[(df_res["Cargo"] == cargo_sim) & 
                         (df_res["Año"] == año_base) & 
                         (df_res["Elección"] == tipo_base) &
                         (~df_res["Partido"].isin(["BLANCOS", "ANULADOS"]))].copy()

        total_votos_base = df_base["Cantidad de votos"].sum()

        df_part_base = df_part[(df_part["Cargo"] == cargo_sim) & 
                               (df_part["Año"] == año_base) & 
                               (df_part["Tipo elección"] == tipo_base)]

        if not df_part_base.empty:
            part_base = df_part_base["Participación"].values[0]
            padron_estimado = int(total_votos_base / (part_base / 100))
        else:
            padron_estimado = int(total_votos_base / 0.7)
            part_base = 70.0

        st.markdown(f"**Padrón estimado:** {padron_estimado:,}")
        st.markdown(f"**Participación base:** {part_base:.1f}%")
        st.markdown(f"**Votos emitidos base:** {total_votos_base:,}")

        st.markdown("---")

        participacion_sim = st.number_input(
            "Participación simulada (%)",
            min_value=40.0,
            max_value=90.0,
            value=part_base,
            step=0.5,
            format="%.1f",
            key="part_slider"
        )

        votos_totales_sim = int(padron_estimado * participacion_sim / 100)
        st.markdown(f"**Votos totales simulados:** {votos_totales_sim:,}")

        st.markdown("---")

        agregar_adicionales = st.checkbox("Agregar partidos adicionales (LLA, Izquierda, Otros)", value=False, key="add_parties")

        st.markdown("**Distribución de votos (%)**")
        st.markdown("*Ajustar para que sume 100%*")

        porcentajes_sim = {}
        suma_actual = 0

        for partido in df_base["Partido"].unique():
            pct_base = df_base[df_base["Partido"] == partido]["% sobre votos emitidos válidos"].values[0]

            porcentajes_sim[partido] = st.number_input(
                partido,
                min_value=0.0,
                max_value=100.0,
                value=float(pct_base),
                step=0.1,
                format="%.1f",
                key=f"pct_{partido}"
            )
            suma_actual += porcentajes_sim[partido]

        if agregar_adicionales:
            partidos_adicionales = ["LLA", "IZQUIERDA", "OTROS"]
            for partido in partidos_adicionales:
                if partido not in porcentajes_sim:
                    porcentajes_sim[partido] = st.number_input(
                        partido,
                        min_value=0.0,
                        max_value=100.0,
                        value=0.0,
                        step=0.1,
                        format="%.1f",
                        key=f"pct_{partido}"
                    )
                    suma_actual += porcentajes_sim[partido]

        color_suma = "green" if abs(suma_actual - 100) < 0.5 else "red"
        st.markdown(f"**Suma actual:** :{color_suma}[{suma_actual:.1f}%]")

        if abs(suma_actual - 100) > 0.5:
            st.warning("⚠️ La suma debe ser 100% para simular correctamente")

    with col2:
        st.subheader("Resultados de la Simulación")

        if abs(suma_actual - 100) < 0.5:
            resultados_sim = []

            for partido, pct in porcentajes_sim.items():
                if pct > 0:
                    votos_sim = int(votos_totales_sim * pct / 100)

                    if partido in df_base["Partido"].values:
                        votos_base = df_base[df_base["Partido"] == partido]["Cantidad de votos"].values[0]
                    else:
                        votos_base = 0

                    diferencia = votos_sim - votos_base
                    pct_cambio = (diferencia / votos_base * 100) if votos_base > 0 else 0

                    resultados_sim.append({
                        "Partido": partido,
                        "Votos Base": votos_base,
                        "Votos Simulados": votos_sim,
                        "Diferencia": diferencia,
                        "% Cambio": pct_cambio
                    })

            df_sim = pd.DataFrame(resultados_sim)

            fig = go.Figure()

            fig.add_trace(go.Bar(
                name="Resultado Base",
                x=df_sim["Partido"],
                y=df_sim["Votos Base"],
                marker_color="lightgray",
                text=df_sim["Votos Base"],
                textposition="outside",
                texttemplate="%{text:,.0f}"
            ))

            fig.add_trace(go.Bar(
                name="Simulación",
                x=df_sim["Partido"],
                y=df_sim["Votos Simulados"],
                marker_color=[get_color(p) for p in df_sim["Partido"]],
                text=df_sim["Votos Simulados"],
                textposition="outside",
                texttemplate="%{text:,.0f}"
            ))

            fig.update_layout(
                title=f"Comparación: {normalizar_cargo(cargo_sim)} {año_base} {tipo_base}",
                barmode="group",
                height=500,
                xaxis_title="Fuerza Política",
                yaxis_title="Cantidad de Votos",
                legend_title="Escenario",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#f8f9fa",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Tabla de Resultados Detallada")

            df_display = df_sim.copy()
            df_display["Votos Base"] = df_display["Votos Base"].apply(lambda x: f"{x:,}")
            df_display["Votos Simulados"] = df_display["Votos Simulados"].apply(lambda x: f"{x:,}")
            df_display["Diferencia"] = df_display["Diferencia"].apply(lambda x: f"{x:+,}")
            df_display["% Cambio"] = df_display["% Cambio"].apply(lambda x: f"{x:+.1f}%" if x != 0 else "N/A")

            st.dataframe(df_display, use_container_width=True, hide_index=True)

            st.markdown("#### Cambio Porcentual por Fuerza")

            df_sim_con_base = df_sim[df_sim["Votos Base"] > 0]

            if not df_sim_con_base.empty:
                fig2 = go.Figure()

                colors_cambio = [get_color(p) for p in df_sim_con_base["Partido"]]

                fig2.add_trace(go.Bar(
                    x=df_sim_con_base["Partido"],
                    y=df_sim_con_base["% Cambio"],
                    marker_color=colors_cambio,
                    text=df_sim_con_base["% Cambio"].apply(lambda x: f"{x:+.1f}%"),
                    textposition="outside"
                ))

                fig2.update_layout(
                    title="Cambio Porcentual Respecto al Escenario Base",
                    height=400,
                    xaxis_title="Fuerza Política",
                    yaxis_title="% de Cambio",
                    showlegend=False,
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#f8f9fa",
                    font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                    xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                    yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
                )

                fig2.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)

                st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("👈 Ajustar los porcentajes en el panel izquierdo para que sumen 100%")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem; padding: 1rem;'>
    <p><strong>Dinámica Electoral en la Ciudad de Venado Tuerto (2019-2025)</strong></p>
    <p>Análisis de datos electorales | Municipalidad de Venado Tuerto</p>
</div>
""", unsafe_allow_html=True)
