import streamlit as st
import pandas as pd
import plotly.express as px

# === Import Data ===
df = pd.read_csv("sdm_clean.csv")

# PAGE CONFIG
st.set_page_config(page_title="KELOMPOK 5", layout="wide")

st.title("KETIMPANGAN & KUALITAS SUMBER DAYA MANUSIA")

# === IPM DAN AKSES PENDIDIKAN ===
tab_ipm, tab_sosial = st.tabs(["IPM & Akses Pendidikan", "Sosial Ekonomi Rumah Tangga"])

with tab_ipm:
    # === IPM VS APS ===
    df_aps = df[["provinsi", 
                 "ipm_2024", 
                 "aps_7_12", 
                 "aps_13_15", 
                 "aps_16_18", 
                 "aps_19_23"]]

    st.header("IPM vs APS per Kelompok Umur")

    st.write("""
    Visualisasi ini menunjukkan hubungan antara **IPM** dan **Angka Partisipasi Sekolah (APS)**.
    Tujuannya untuk melihat apakah provinsi dengan IPM rendah cenderung memiliki APS yang stagnan atau lebih rendah.
    """)

    aps_cols = {
        "APS Usia 7–12 (SD)": "aps_7_12",
        "APS Usia 13–15 (SMP)": "aps_13_15",
        "APS Usia 16–18 (SMA)": "aps_16_18",
        "APS Usia 19–23 (PT)": "aps_19_23"
    }

    selected_label = st.selectbox(
        "Pilih Kelompok Umur APS:",
        list(aps_cols.keys()),
        key="aps_selectbox"
    )
    selected_col = aps_cols[selected_label]

    show_grid_aps = st.checkbox(
        "Tampilkan grid 4-plot (semua tingkat sekaligus)",
        value=True,
        key="aps_grid_checkbox"
    )

    # --- Single Scatter ---
    fig = px.scatter(
        df,
        x="ipm_2024",
        y=selected_col,
        trendline="ols",
        hover_name="provinsi",
        title=f"IPM vs {selected_label}",
        labels={"ipm_2024": "IPM 2024", selected_col: selected_label}
    )
    fig.update_traces(marker=dict(size=12, opacity=0.8))
    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True, key=f"single_aps_{selected_col}")

    # --- Grid APS ---
    if show_grid_aps:
        st.subheader("Visualisasi Semua Kelompok Usia (Grid)")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        positions = [col1, col2, col3, col4]

        for (label, colname), container in zip(aps_cols.items(), positions):
            with container:
                fig_g = px.scatter(
                    df,
                    x="ipm_2024",
                    y=colname,
                    trendline="ols",
                    hover_name="provinsi",
                    title=label,
                    labels={"ipm_2024": "IPM 2024", colname: label},
                )
                fig_g.update_traces(marker=dict(size=10, opacity=0.8))
                fig_g.update_layout(height=350)
                st.plotly_chart(fig_g, use_container_width=True, key=f"grid_aps_{colname}")

    # === IPM VS PUTUS SEKOLAH ===
    df_putus = df[["provinsi", 
                   "ipm_2024", 
                   "putus_sd", 
                   "putus_smp", 
                   "putus_sma", 
                   "putus_smk"]]

    st.header("IPM vs Angka Putus Sekolah")

    st.markdown("""
    Scatter plot ini mengecek apakah provinsi dengan **IPM rendah** juga memiliki **angka putus sekolah tinggi**.
    Pilih jenjang pendidikan untuk melihat korelasinya.
    """)

    putus_map = {
        "Putus SD": "putus_sd",
        "Putus SMP": "putus_smp",
        "Putus SMA": "putus_sma",
        "Putus SMK": "putus_smk"
    }

    selected_putus_label = st.selectbox(
        "Pilih Jenis Putus Sekolah:",
        list(putus_map.keys()),
        key="putus_selectbox"
    )
    selected_putus_col = putus_map[selected_putus_label]

    show_grid_putus = st.checkbox(
        "Tampilkan grid 4-plot (semua tingkat sekaligus)",
        value=True,
        key="putus_grid_checkbox"
    )

    # --- Function Plot ---
    def plot_ipm_vs_putus(df, y_col, title_suffix=""):
        fig = px.scatter(
            df,
            x="ipm_2024",
            y=y_col,
            trendline="ols",
            hover_name="provinsi",
            title=f"IPM vs {title_suffix}",
            labels={"ipm_2024": "IPM 2024", y_col: title_suffix},
        )
        fig.update_traces(marker=dict(size=10, opacity=0.85))
        fig.update_layout(height=500)
        return fig

    # --- Single Putus Plot ---
    fig_main = plot_ipm_vs_putus(df_putus, selected_putus_col, selected_putus_label)
    st.plotly_chart(fig_main, use_container_width=True, key=f"single_putus_{selected_putus_col}")

    # --- Grid Putus ---
    if show_grid_putus:
        st.subheader("Semua Tingkat Putus Sekolah (Grid)")
        colA, colB = st.columns(2)
        positions = [colA, colB] * 2  # menghasilkan urutan 4 kolom

        for (label, colname), container in zip(putus_map.items(), positions):
            with container:
                fig_g = plot_ipm_vs_putus(df_putus, colname, label)
                st.plotly_chart(fig_g, use_container_width=True, key=f"grid_putus_{colname}")

    # --- Statistik ---
    st.markdown("### Statistik Ringkas")
    st.write(df_putus[["ipm_2024","putus_sd","putus_smp","putus_sma","putus_smk"]].describe())

    st.markdown("""
    ### Catatan Interpretasi Cepat
    - **Kiri-atas** → IPM rendah tapi putus rendah (perlu dicek apakah datanya kecil atau under-report)
    - **Kiri-bawah** → IPM rendah & putus tinggi → red flag (akses & retensi pendidikan lemah)
    """)