import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Dinámica Electoral Venado Tuerto 2019-2025",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    h1 {
        color: #2c3e50;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }

    h2 {
        color: #34495e;
        font-weight: 600;
        font-size: 1.6rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.2rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #007bff;
        color: white;
    }

    /* Forzar fondo blanco en toda la app */
    .stApp {
        background-color: #ffffff;
    }

    /* Forzar fondo blanco en contenedores */
    .main .block-container {
        background-color: #ffffff;
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

def normalizar_cargo(cargo):
    """Convierte nombres cortos de cargos a nombres completos"""
    return NOMBRES_CARGOS.get(cargo, cargo)

# Cargar datos
@st.cache_data
def cargar_datos():
    df_participacion = pd.read_csv("participacion_hist.csv")
    df_participacion_cuad = pd.read_csv("participacion_hist_cuad.csv")
    df_resultados = pd.read_csv("agrup_def.csv")

    # Limpiar columnas innecesarias
    df_resultados = df_resultados.drop(columns=["Unnamed: 20", "Unnamed: 21", "Unnamed: 22", "Unnamed: 23"], errors="ignore")

    # Convertir porcentajes
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

# Función para obtener color del partido
def get_color(partido):
    return COLORES_PARTIDOS.get(partido, "#95a5a6")

# Título principal
st.title("Dinámica Electoral en la Ciudad de Venado Tuerto durante el período comprendido entre los años 2019 y 2025")

# Crear pestañas principales
tab1, tab2 = st.tabs(["📊 Análisis de Resultados Electorales", "🔮 Simulador Electoral"])

with tab1:
    st.markdown("---")

    # Subtabs para local y provincial
    subtab_local, subtab_provincial = st.tabs(["🏛️ Cargos Locales", "🏢 Cargos Provinciales y Nacionales"])

    with subtab_local:
        st.header("Análisis Electoral - Cargos Locales")

        # Filtros
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cargos_locales = ["Intendente", "Concejales"]
            cargo_sel = st.selectbox("Cargo", cargos_locales, key="cargo_local")

        with col2:
            tipo_elec = st.selectbox("Tipo de Elección", ["Primarias", "Generales", "Ambas"], key="tipo_local")

        with col3:
            incluir_blancos = st.checkbox("Incluir Blancos y Anulados", value=False, key="blancos_local")

        with col4:
            vista_cuadrantes = st.selectbox("Vista", ["Total", "Por Cuadrante"], key="vista_local")

        # Filtrar datos
        df_cargo = df_res[df_res["Cargo"] == cargo_sel].copy()

        if tipo_elec != "Ambas":
            df_cargo = df_cargo[df_cargo["Elección"] == tipo_elec]

        if not incluir_blancos:
            df_cargo = df_cargo[~df_cargo["Partido"].isin(["BLANCOS", "ANULADOS"])]

        # Gráfico 1: Comparación por año y tipo de elección
        st.subheader(f"Evolución de votos - {normalizar_cargo(cargo_sel)}")

        if vista_cuadrantes == "Total":
            # Gráfico de barras agrupadas
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
                            y_values.append(df_temp["Cantidad de votos"].values[0])

                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=y_values,
                    marker_color=get_color(partido),
                    text=y_values,
                    textposition="outside",
                    texttemplate="%{text:,.0f}"
                ))

            fig.update_layout(
                barmode="group",
                height=500,
                xaxis_title="Año y Tipo de Elección",
                yaxis_title="Cantidad de Votos",
                legend_title="Fuerza Política",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            # Vista por cuadrantes
            cuadrante_sel = st.radio("Seleccionar Cuadrante", ["O", "N", "E", "S"], horizontal=True, key="cuad_local")

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
                            y_values.append(df_temp[cuadrante_sel].values[0])

                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=y_values,
                    marker_color=get_color(partido),
                    text=y_values,
                    textposition="outside",
                    texttemplate="%{text:,.0f}"
                ))

            fig.update_layout(
                barmode="group",
                title=f"Cuadrante {cuadrante_sel}",
                height=500,
                xaxis_title="Año y Tipo de Elección",
                yaxis_title="Cantidad de Votos",
                legend_title="Fuerza Política",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
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
            votos = [df_fuerza[df_fuerza["Año"] == año]["Cantidad de votos"].values[0] if año in df_fuerza["Año"].values else 0 for año in años]

            fig.add_trace(go.Scatter(
                x=años,
                y=votos,
                mode="lines+markers+text",
                name=fuerza_sel,
                line=dict(color=get_color(fuerza_sel), width=3),
                marker=dict(size=12),
                text=votos,
                textposition="top center",
                texttemplate="%{text:,.0f}"
            ))

            fig.update_layout(
                title=f"Evolución de {fuerza_sel} en Elecciones Generales - {normalizar_cargo(cargo_sel)}",
                height=400,
                xaxis_title="Año",
                yaxis_title="Cantidad de Votos",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        # Gráfico 3: Comparación porcentual (barras apiladas 100%)
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
            paper_bgcolor="#ffffff",
            font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
        )

        st.plotly_chart(fig, use_container_width=True)

        # Gráfico 4: Participación electoral
        st.subheader(f"Evolución de la participación electoral - {normalizar_cargo(cargo_sel)}")

        df_part_cargo = df_part[df_part["Cargo"] == cargo_sel]

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
            paper_bgcolor="#ffffff",
            font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0", range=[0, 100])
        )

        st.plotly_chart(fig, use_container_width=True)

    with subtab_provincial:
        st.header("Análisis Electoral - Cargos Provinciales y Nacionales")

        # Filtros
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cargos_prov = ["Gobernador", "Presidente", "Diputados N", "Senadores N", 
                          "Diputado P", "Senador P", "Convencionales D", "Convencionales DÚ"]
            cargo_sel_p = st.selectbox("Cargo", cargos_prov, key="cargo_prov")

        with col2:
            tipo_elec_p = st.selectbox("Tipo de Elección", ["Primarias", "Generales", "Ambas"], key="tipo_prov")

        with col3:
            incluir_blancos_p = st.checkbox("Incluir Blancos y Anulados", value=False, key="blancos_prov")

        with col4:
            vista_cuadrantes_p = st.selectbox("Vista", ["Total", "Por Cuadrante"], key="vista_prov")

        # Filtrar datos
        df_cargo_p = df_res[df_res["Cargo"] == cargo_sel_p].copy()

        if tipo_elec_p != "Ambas":
            df_cargo_p = df_cargo_p[df_cargo_p["Elección"] == tipo_elec_p]

        if not incluir_blancos_p:
            df_cargo_p = df_cargo_p[~df_cargo_p["Partido"].isin(["BLANCOS", "ANULADOS"])]

        # Gráficos similares a la sección local
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
                            y_values.append(df_temp["Cantidad de votos"].values[0])

                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=y_values,
                    marker_color=get_color(partido),
                    text=y_values,
                    textposition="outside",
                    texttemplate="%{text:,.0f}"
                ))

            fig.update_layout(
                barmode="group",
                height=500,
                xaxis_title="Año y Tipo de Elección",
                yaxis_title="Cantidad de Votos",
                legend_title="Fuerza Política",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            cuadrante_sel_p = st.radio("Seleccionar Cuadrante", ["O", "N", "E", "S"], horizontal=True, key="cuad_prov")

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
                            y_values.append(df_temp[cuadrante_sel_p].values[0])

                fig.add_trace(go.Bar(
                    name=partido,
                    x=x_labels,
                    y=y_values,
                    marker_color=get_color(partido),
                    text=y_values,
                    textposition="outside",
                    texttemplate="%{text:,.0f}"
                ))

            fig.update_layout(
                barmode="group",
                title=f"Cuadrante {cuadrante_sel_p}",
                height=500,
                xaxis_title="Año y Tipo de Elección",
                yaxis_title="Cantidad de Votos",
                legend_title="Fuerza Política",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        # Evolución por fuerza
        st.subheader("Evolución histórica por fuerza política")

        df_generales_p = df_cargo_p[df_cargo_p["Elección"] == "Generales"]
        partidos_disponibles_p = [p for p in df_generales_p["Partido"].unique() if p not in ["BLANCOS", "ANULADOS"]]

        if partidos_disponibles_p:
            fuerza_sel_p = st.selectbox("Seleccionar fuerza política", partidos_disponibles_p, key="fuerza_prov")

            df_fuerza_p = df_generales_p[df_generales_p["Partido"] == fuerza_sel_p]

            fig = go.Figure()

            años = sorted(df_fuerza_p["Año"].unique())
            votos = [df_fuerza_p[df_fuerza_p["Año"] == año]["Cantidad de votos"].values[0] if año in df_fuerza_p["Año"].values else 0 for año in años]

            fig.add_trace(go.Scatter(
                x=años,
                y=votos,
                mode="lines+markers+text",
                name=fuerza_sel_p,
                line=dict(color=get_color(fuerza_sel_p), width=3),
                marker=dict(size=12),
                text=votos,
                textposition="top center",
                texttemplate="%{text:,.0f}"
            ))

            fig.update_layout(
                title=f"Evolución de {fuerza_sel_p} en Elecciones Generales - {normalizar_cargo(cargo_sel_p)}",
                height=400,
                xaxis_title="Año",
                yaxis_title="Cantidad de Votos",
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

        # Comparación específica
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
                votos_2023 = df_gob_2023[df_gob_2023["Partido"] == partido]["Cantidad de votos"].values
                votos_2025 = df_dip_2025[df_dip_2025["Partido"] == partido]["Cantidad de votos"].values

                if len(votos_2023) > 0 and len(votos_2025) > 0:
                    fig.add_trace(go.Bar(
                        name=partido,
                        x=["Gobernador 2023", f"{normalizar_cargo('Diputados N')} 2025"],
                        y=[votos_2023[0], votos_2025[0]],
                        marker_color=get_color(partido),
                        text=[votos_2023[0], votos_2025[0]],
                        textposition="outside",
                        texttemplate="%{text:,.0f}"
                    ))

            fig.update_layout(
                barmode="group",
                height=450,
                xaxis_title="Elección",
                yaxis_title="Cantidad de Votos",
                legend_title="Fuerza Política",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
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
                votos_2023 = df_gob_2023[df_gob_2023["Partido"] == partido]["Cantidad de votos"].values
                votos_2025 = df_conv_2025[df_conv_2025["Partido"] == partido]["Cantidad de votos"].values

                if len(votos_2023) > 0 and len(votos_2025) > 0:
                    fig.add_trace(go.Bar(
                        name=partido,
                        x=["Gobernador 2023", f"{normalizar_cargo('Convencionales DÚ')} 2025"],
                        y=[votos_2023[0], votos_2025[0]],
                        marker_color=get_color(partido),
                        text=[votos_2023[0], votos_2025[0]],
                        textposition="outside",
                        texttemplate="%{text:,.0f}"
                    ))

            fig.update_layout(
                barmode="group",
                height=450,
                xaxis_title="Elección",
                yaxis_title="Cantidad de Votos",
                legend_title="Fuerza Política",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=11, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🔮 Simulador Electoral")
    st.markdown("Esta herramienta permite simular escenarios electorales variando el nivel de participación y la distribución de votos entre fuerzas políticas.")

    # Configuración del simulador
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

        participacion_sim = st.slider("Participación simulada (%)", 
                                       min_value=40.0, 
                                       max_value=90.0, 
                                       value=part_base,
                                       step=0.5,
                                       key="part_slider")

        votos_totales_sim = int(padron_estimado * participacion_sim / 100)
        st.markdown(f"**Votos totales simulados:** {votos_totales_sim:,}")

        st.markdown("---")
        st.markdown("**Distribución de votos (%)**")
        st.markdown("*Ajustar para que sume 100%*")

        porcentajes_sim = {}
        suma_actual = 0

        for partido in df_base["Partido"].unique():
            pct_base = df_base[df_base["Partido"] == partido]["% sobre votos emitidos válidos"].values[0]

            porcentajes_sim[partido] = st.slider(
                partido,
                min_value=0.0,
                max_value=100.0,
                value=float(pct_base),
                step=0.1,
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
                votos_sim = int(votos_totales_sim * pct / 100)
                votos_base = df_base[df_base["Partido"] == partido]["Cantidad de votos"].values[0]
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
                paper_bgcolor="#ffffff",
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
            df_display["% Cambio"] = df_display["% Cambio"].apply(lambda x: f"{x:+.1f}%")

            st.dataframe(df_display, use_container_width=True, hide_index=True)

            st.markdown("#### Cambio Porcentual por Fuerza")

            fig2 = go.Figure()

            colors_cambio = ["green" if x > 0 else "red" for x in df_sim["% Cambio"]]

            fig2.add_trace(go.Bar(
                x=df_sim["Partido"],
                y=df_sim["% Cambio"],
                marker_color=colors_cambio,
                text=df_sim["% Cambio"].apply(lambda x: f"{x:+.1f}%"),
                textposition="outside"
            ))

            fig2.update_layout(
                title="Cambio Porcentual Respecto al Escenario Base",
                height=400,
                xaxis_title="Fuerza Política",
                yaxis_title="% de Cambio",
                showlegend=False,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(family="Inter, sans-serif", size=12, color="#2c3e50"),
                xaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0"),
                yaxis=dict(showgrid=True, gridwidth=1, gridcolor="#e0e0e0")
            )

            fig2.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)

            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info("👈 Ajustar los porcentajes en el panel izquierdo para que sumen 100%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem; padding: 1rem;'>
    <p><strong>Dinámica Electoral en la Ciudad de Venado Tuerto (2019-2025)</strong></p>
    <p>Análisis de datos electorales | Municipalidad de Venado Tuerto</p>
</div>
""", unsafe_allow_html=True)
