import streamlit as st
import pandas as pd
import plotly.express as px

# === Import Data ===
df = pd.read_csv("sdm_clean.csv")
# Konversi kolom 'kendaraan' menjadi numerik
df['kendaraan'] = pd.to_numeric(df['kendaraan'], errors='coerce')

# PAGE CONFIG
st.set_page_config(page_title="KELOMPOK 5", layout="wide")

st.title("KETIMPANGAN & KUALITAS SUMBER DAYA MANUSIA")

# === TAB ===
tab_capaian, tab_ipm, tab_sosial,tab_lingkungan_geospasial, tab_infrastruktur, tab_airpangan, tab_gizi = st.tabs([
                                                                                        "Capaian Pendidikan", 
                                                                                        "IPM & Akses Pendidikan", 
                                                                                        "Sosial Ekonomi Rumah Tangga",
                                                                                        "Lingkungan dan GeoSpacial",
                                                                                        "Infrastruktur",
                                                                                        "Kerawanan Pangan dan Air Minum Layak",
                                                                                        "Konsumsi Gizi"
                                                                                        ])

with tab_capaian:
    st.header("Tren Capaian Pendidikan 5 Tahun Terakhir")

    st.write("""
    Analisis ini menampilkan perkembangan penyelesaian pendidikan jenjang **SD, SMP, dan SMA** 
    selama lima tahun terakhir, baik di tingkat **nasional** maupun **provinsi**.
    """)

    # --- Tambahkan total jenjang untuk setiap tahun 2020–2024 ---
    for tahun in range(2020, 2025):
        df[f"penyelesaian_pendidikanTotal{tahun}"] = (
            df[f"penyelesaian_pendidikanSD{tahun}"] +
            df[f"penyelesaian_pendidikanSMP{tahun}"] +
            df[f"penyelesaian_pendidikanSMA{tahun}"]
        )

    # DEFINISI KOLOM PENYELESAIAN PENDIDIKAN 2020–2024
    pend_cols = {
        "SD":  [f"penyelesaian_pendidikanSD{tahun}"  for tahun in range(2020, 2025)],
        "SMP": [f"penyelesaian_pendidikanSMP{tahun}" for tahun in range(2020, 2025)],
        "SMA": [f"penyelesaian_pendidikanSMA{tahun}" for tahun in range(2020, 2025)],
    }

    # memastikan semua kolom numerik
    for cols in pend_cols.values():
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # TREN NASIONAL
    st.subheader("Tren Nasional")

    with st.expander("Tekan untuk melakukan analisis"):
        selected_jenjang_nasional = st.selectbox(
            "Pilih Jenjang Nasional:",
            ["SD", "SMP", "SMA", "Seluruh Jenjang"],
            key="jenjang_nasional"
        )

        df_nas = df[df["provinsi"].str.lower() == "indonesia"].copy()

        if selected_jenjang_nasional == "Seluruh Jenjang":
            cols_total = [f"penyelesaian_pendidikanTotal{tahun}" for tahun in range(2020, 2025)]
            df_nasional_long = pd.DataFrame({
                "tahun": list(range(2020, 2025)),
                "nilai": [df_nas[col].values[0] for col in cols_total]
            })
        else:
            df_nasional_long = pd.DataFrame({
                "tahun": list(range(2020, 2025)),
                "nilai": [df_nas[col].values[0] for col in pend_cols[selected_jenjang_nasional]]
            })

        fig_nasional = px.line(
            df_nasional_long,
            x="tahun",
            y="nilai",
            markers=True,
            title=f"Tren Nasional Penyelesaian Pendidikan – {selected_jenjang_nasional}",
            labels={"nilai": "Persentase (%)"}
        )

        fig_nasional.update_traces(mode="lines+markers")
        fig_nasional.update_traces(hovertemplate='%{y}<extra></extra>')
        fig_nasional.update_xaxes(type="category")
        fig_nasional.update_layout(height=450)

        st.plotly_chart(fig_nasional, use_container_width=True)

    # TREND PER PROVINSI 
    st.subheader("Tren Berdasarkan Provinsi")

    # --- Tambahkan total jenjang untuk setiap tahun 2020–2024 ---
    for tahun in range(2020, 2025):
        df[f"penyelesaian_pendidikanTotal{tahun}"] = (
            df[f"penyelesaian_pendidikanSD{tahun}"] +
            df[f"penyelesaian_pendidikanSMP{tahun}"] +
            df[f"penyelesaian_pendidikanSMA{tahun}"]
        )

    with st.expander("Tekan untuk melakukan analisis"):
        col1, col2 = st.columns(2)

        with col1:
            selected_prov = st.selectbox(
                "Pilih Provinsi:",
                sorted(df[df["provinsi"].str.lower() != "indonesia"]["provinsi"].unique()),
                key="prov_tren"
            )

        with col2:
            selected_jenjang_prov = st.selectbox(
                "Pilih Jenjang Provinsi:",
                ["SD", "SMP", "SMA", "Seluruh Jenjang"],
                key="jenjang_prov"
            )

        df_prov = df[df["provinsi"] == selected_prov].copy()

        if selected_jenjang_prov == "Seluruh Jenjang":
            cols_total = [f"penyelesaian_pendidikanTotal{tahun}" for tahun in range(2020, 2025)]
            df_prov_long = pd.DataFrame({
                "tahun": list(range(2020, 2025)),
                "nilai": [df_prov[col].values[0] for col in cols_total]
            })
        else:
            df_prov_long = pd.DataFrame({
                "tahun": list(range(2020, 2025)),
                "nilai": [df_prov[col].values[0] for col in pend_cols[selected_jenjang_prov]]
            })

        fig_prov = px.line(
            df_prov_long,
            x="tahun",
            y="nilai",
            markers=True,
            title=f"Tren Penyelesaian Pendidikan – {selected_prov} ({selected_jenjang_prov})",
            labels={"nilai": "Persentase (%)"}
        )

        fig_prov.update_traces(mode="lines+markers")
        fig_prov.update_traces(hovertemplate='%{y}<extra></extra>')
        fig_prov.update_xaxes(type="category")
        fig_prov.update_layout(height=450)

        st.plotly_chart(fig_prov, use_container_width=True)

    # === BARCHART PER PROVINSI: PILIH JENJANG & TAHUN ===
    st.subheader("Perbandingan Penyelesaian Pendidikan Antar Provinsi")

    with st.expander("Tekan untuk menampilkan bar chart per provinsi"):

        # Dropdown jenjang
        selected_jenjang = st.selectbox(
            "Pilih Jenjang Pendidikan:",
            ["SD", "SMP", "SMA"],
            key="jenjang_barchart"
        )

        # Dropdown tahun
        selected_tahun = st.selectbox(
            "Pilih Tahun:",
            [2020, 2021, 2022, 2023, 2024],
            key="tahun_barchart"
        )

        # Ambil nama kolom berdasarkan jenjang + tahun
        col_map = {
            "SD":  f"penyelesaian_pendidikanSD{selected_tahun}",
            "SMP": f"penyelesaian_pendidikanSMP{selected_tahun}",
            "SMA": f"penyelesaian_pendidikanSMA{selected_tahun}",
        }

        selected_col = col_map[selected_jenjang]

        # Filter hanya provinsi (hilangkan Indonesia)
        df_plot = df[df["provinsi"].str.lower() != "indonesia"].copy()

        # Pastikan kolom numerik
        df_plot[selected_col] = pd.to_numeric(df_plot[selected_col], errors="coerce")

        # Siapkan dataframe untuk plot
        df_bar = pd.DataFrame({
            "provinsi": df_plot["provinsi"],
            "nilai": df_plot[selected_col]
        })

        # Plot Bar Chart
        fig_bar = px.bar(
            df_bar,
            x="provinsi",
            y="nilai",
            color="provinsi",
            title=f"Penyelesaian Pendidikan {selected_jenjang} Tahun {selected_tahun}",
            labels={"nilai": "Persentase (%)", "provinsi": "Provinsi"}
        )

        fig_bar.update_layout(
            xaxis_tickangle=45,
            height=550,
            showlegend=False  
        )

        st.plotly_chart(fig_bar, use_container_width=True)

with tab_ipm:
    # === IPM VS APS ===

    # === Buat kolom APS Total ===
    df["aps_total"] = df[["aps_7_12", "aps_13_15", "aps_16_18", "aps_19_23"]].sum(axis=1)

    df_aps = df[df["provinsi"] != "Indonesia"][[
                "provinsi", 
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

    with st.expander("Tekan untuk melakukan analisis"):
        aps_cols = {
            "APS Usia 7–12 (SD)": "aps_7_12",
            "APS Usia 13–15 (SMP)": "aps_13_15",
            "APS Usia 16–18 (SMA)": "aps_16_18",
            "APS Usia 19–23 (PT)": "aps_19_23",
            "APS Total": "aps_total"
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

    # --- Interpretasi ---
        st.info(
            "💡 *Interpretasi:* Pola titik yang naik dari kiri ke kanan menunjukkan bahwa "
            "provinsi dengan IPM lebih tinggi umumnya memiliki APS lebih tinggi pada semua kelompok usia. "
            "Jika titik cenderung horizontal atau turun di IPM rendah, hal ini menandakan akses pendidikan yang terbatas."
        )

    # === IPM VS PUTUS SEKOLAH ===

    # === Buat kolom angka putus sekolah Total ===
    df["putus_total"] = df[["putus_sd", "putus_smp", "putus_sma", "putus_smk"]].sum(axis=1)

    df_putus = df[df["provinsi"] != "Indonesia"][[
                    "provinsi", 
                    "ipm_2024", 
                    "putus_sd", 
                    "putus_smp", 
                    "putus_sma", 
                    "putus_smk",
                    "putus_total"]]

    st.header("IPM vs Angka Putus Sekolah")

    st.markdown("""
    Scatter plot ini mengecek apakah provinsi dengan **IPM rendah** juga memiliki **angka putus sekolah tinggi**.
    Pilih jenjang pendidikan untuk melihat korelasinya.
    """)

    with st.expander("Tekan untuk melakukan analisis"):
        putus_map = {
            "Putus SD": "putus_sd",
            "Putus SMP": "putus_smp",
            "Putus SMA": "putus_sma",
            "Putus SMK": "putus_smk",
            "Putus Total": "putus_total"
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

        st.info(
            "💡 *Interpretasi:* jika titik-titik cenderung naik ke atas saat IPM menurun, "
            "artinya provinsi dengan IPM lebih rendah kemungkinan memiliki angka putus sekolah lebih tinggi. "
            "Sebaliknya, jika titik-titik cenderung tetap rendah saat IPM meningkat, "
            "provinsi dengan IPM lebih tinggi kemungkinan mampu mempertahankan murid di sekolah lebih baik."
        )

        # --- Statistik ---
        st.markdown("### Statistik Ringkas")
        st.write(df_putus[["ipm_2024","putus_sd","putus_smp","putus_sma","putus_smk"]].describe())


with tab_sosial:
        # === 2. Scatter Plot IPM vs Penduduk Miskin ===
    st.header("IPM vs Penduduk Miskin")
    st.write(""" Scatter plot ini digunakan untuk melihat keterkaitan antara tingkat IPM dan jumlah penduduk miskin. 
                Dengan visualisasi ini, kita bisa mengetahui apakah peningkatan IPM berkaitan dengan penurunan jumlah penduduk miskin, 
                serta menemukan provinsi yang menyimpang dari pola umum tersebut
        """)
    with st.expander("Tekan untuk melakukan analisis"):

        fig_ipm_miskin = px.scatter(
            df,
            x="ipm_2024",
            y="penduduk_miskin",
            trendline="ols",
            hover_name="provinsi",
            labels={
                "ipm_2024": "IPM 2024",
                "penduduk_miskin": "Penduduk Miskin (%)"
            },
        )

        fig_ipm_miskin.update_traces(marker=dict(size=11, opacity=0.8))
        fig_ipm_miskin.update_layout(height=500)

        st.plotly_chart(fig_ipm_miskin, use_container_width=True)

        # Korelasi IPM dan Penduduk Miskin
        corr_ipm = df["ipm_2024"].corr(df["penduduk_miskin"])

        st.metric(
            label="Korelasi IPM → Penduduk Miskin",
            value=f"{corr_ipm:.3f}",
            delta=(
                "artinya ketika IPM meningkat, jumlah penduduk miskin cenderung menurun."
                if corr_ipm < 0
                else "artinya ketika IPM meningkat, jumlah penduduk miskin justru cenderung meningkat."
            )
        )


# === Radar Chart Profil Sosial Ekonomi Provinsi ===
    st.header("Profil Sosial Ekonomi Provinsi (Radar Chart)")

    st.write("""
    Radar chart ini memperlihatkan perbandingan beberapa indikator sosial ekonomi pada tiap provinsi. 
    Grafik ini membantu melihat sektor mana yang paling kuat dan sektor mana yang relatif rendah sehingga memudahkan analisis kekuatan dan kelemahan sosial ekonomi daerah tersebut
    """)
    with st.expander("Tekan untuk melihat radar"):
        selected_prov = st.selectbox(
            "Pilih Provinsi:",
            df["provinsi"].unique()
        )

        radar_cols = [
            "penduduk_miskin",
            "pendapatan_industri", "pendapatan_pertanian", "pendapatan_jasa"
        ]

        df_radar = df[df["provinsi"] == selected_prov][radar_cols].T.reset_index()
        df_radar.columns = ["variabel", "nilai"]

        fig_radar = px.line_polar(
            df_radar,
            r="nilai",
            theta="variabel",
            line_close=True,
            title=f"Radar Chart Sosial Ekonomi — {selected_prov}"
        )

        fig_radar.update_traces(fill="toself")
        fig_radar.update_layout(height=550)

        st.plotly_chart(fig_radar, use_container_width=True)


#== pengaruh kemiskinan terhadap angka partisipasi sekolah
    st.header("Pengaruh Kemiskinan terhadap APS")
    st.write("""
        Visualisasi ini menunjukkan hubungan antara **Kemiskinan** dan **Angka Partisipasi Sekolah (APS)**.
        Tujuannya untuk melihat apakah kemiskinan adalah faktor yang berpengaruh terhadap rendahnya angka partisipasi sekolah.
        """)
    with st.expander("Tekan Untuk Melakukan Analisis"):
    
        # ================================
        # 1️⃣ BUAT TOTAL APS
        # ================================
        df["aps_total"] = (
            df["aps_7_12"] +
            df["aps_13_15"] +
            df["aps_16_18"] +
            df["aps_19_23"]
        )

        # ================================
        # 2️⃣ DROPDOWN APS (DENGAN APS TOTAL)
        # ================================
        aps_cols = [
            "aps_7_12",
            "aps_13_15",
            "aps_16_18",
            "aps_19_23",
            "aps_total"     # ← Tambahan baru
        ]

        selected_aps = st.selectbox(
            "Pilih Angka Partisipasi Sekolah (APS):",
            aps_cols
        )

        # ================================
        # 3️⃣ SCATTER PLOT
        # ================================
        fig = px.scatter(
            df,
            x="penduduk_miskin",
            y=selected_aps,
            trendline="ols",
            hover_name="provinsi",             
            hover_data={
                "penduduk_miskin": True,
                selected_aps: True,
                "provinsi": True
            },
            title=f"Kemiskinan vs {selected_aps.upper()}",
            labels={
                "penduduk_miskin": "Penduduk Miskin (%)",
                selected_aps: selected_aps.upper()
            }
        )

        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)

        # ================================
        # 4️⃣ KORELASI PENDUDUK MISKIN ↔ APS TERPILIH
        # ================================
        corr_value_pendudukmiskin_vs_aps = df["penduduk_miskin"].corr(df[selected_aps])

        st.metric(
            label=f"Korelasi Kemiskinan → {selected_aps.upper()}",
            value=f"{corr_value_pendudukmiskin_vs_aps:.3f}",
            delta=(
                f"Korelasi negatif: saat kemiskinan meningkat, {selected_aps.upper()} cenderung menurun."
                if corr_value_pendudukmiskin_vs_aps < 0
                else f"Korelasi positif: saat kemiskinan meningkat, {selected_aps.upper()} cenderung meningkat."
            )
        )


# === Rata-rata Pendapatan per Provinsi Berdasarkan Sektor ===
    st.header("Rata-rata Pendapatan Berdasarkan Sektor")
    st.write("""
        Visualisasi ini menunjukkan perbandingan rata-rata pendapatan berdasarkan sektor pada tiap provinsi. 
        Tujuannya untuk melihat provinsi mana yang memiliki pendapatan tertinggi dan terendah pada sektor tersebut, 
        serta mengidentifikasi pola ketimpangan pendapatan antar wilayah.
        """)
    with st.expander("Tekan untuk melihat visualisasi"):
        # --- Dropdown memilih sektor + total ---
        pilihan_sektor = st.selectbox(
            "Pilih Sektor Pendapatan:",
            {
                "Pertanian": "pendapatan_pertanian",
                "Industri": "pendapatan_industri",
                "Jasa": "pendapatan_jasa",
                "Total Pendapatan (Pertanian + Industri + Jasa)": "total_pendapatan"
            }
        )

        # --- Proses kolom berdasarkan pilihan user ---
        if pilihan_sektor == "Total Pendapatan (Pertanian + Industri + Jasa)":
            df["total_pendapatan"] = (
                df["pendapatan_pertanian"] +
                df["pendapatan_industri"] +
                df["pendapatan_jasa"]
            )
            kolom_pendapatan = "total_pendapatan"
        else:
            kolom_pendapatan = {
                "Pertanian": "pendapatan_pertanian",
                "Industri": "pendapatan_industri",
                "Jasa": "pendapatan_jasa",
                "Total Pendapatan (Pertanian + Industri + Jasa)": "total_pendapatan"
            }[pilihan_sektor]

        # --- Siapkan Data ---
        df_plot = df[["provinsi", kolom_pendapatan]].copy()
        df_plot_group = df_plot.groupby("provinsi").mean().reset_index()
        df_plot_group.columns = ["Provinsi", "Pendapatan"]

        # --- Plot ---
        fig = px.area(
            df_plot_group,
            x="Provinsi",
            y="Pendapatan",
            markers=True,
            title=f"Pendapatan Rumah Tangga: {pilihan_sektor}",
        )

        fig.update_traces(opacity=0.5, line=dict(width=3))
        fig.update_layout(height=450)

        st.plotly_chart(fig, use_container_width=True)

        # Urutkan berdasarkan Pendapatan
        df_sorted = df_plot_group.sort_values(by="Pendapatan")

        provinsi_terendah = df_sorted.iloc[0]["Provinsi"]
        pendapatan_terendah = df_sorted.iloc[0]["Pendapatan"]

        provinsi_tertinggi = df_sorted.iloc[-1]["Provinsi"]
        pendapatan_tertinggi = df_sorted.iloc[-1]["Pendapatan"]

        # Provinsi tengah-tengah (median)
        median_index = len(df_sorted) // 2
        provinsi_tengah = df_sorted.iloc[median_index]["Provinsi"]
        pendapatan_tengah = df_sorted.iloc[median_index]["Pendapatan"]

        st.markdown(f"""
        **Kesimpulan Pendapatan per Provinsi untuk sektor {pilihan_sektor}:**

        - Provinsi dengan pendapatan **terendah**: {provinsi_terendah} ({pendapatan_terendah:,.0f})
        - Provinsi dengan pendapatan **tertinggi**: {provinsi_tertinggi} ({pendapatan_tertinggi:,.0f})
        - Provinsi dengan pendapatan **tengah-tengah**: {provinsi_tengah} ({pendapatan_tengah:,.0f})
        """)


# ======== Rata-rata Nasional Pendapatan Rumah Tangga per Sektor Ekonomi
    st.header("Rata-rata Pendapatan Rumah Tangga per Sektor Ekonomi")
    with st.expander("Tekan untuk melihat visualisasi"):
        # --- 1. Hitung rata-rata nasional per sektor ---
        pendapatan_cols = ["pendapatan_pertanian", "pendapatan_industri", "pendapatan_jasa"]

        pendapatan_mean = (
            df[pendapatan_cols]
            .mean()
            .reset_index()
        )

        pendapatan_mean.columns = ["Sektor", "Pendapatan"]

        # Rename agar lebih rapi
        rename_pendapatan = {
            "pendapatan_pertanian": "Sektor Pertanian",
            "pendapatan_industri": "Sektor Industri",
            "pendapatan_jasa": "Sektor Jasa"
        }

        pendapatan_mean["Sektor"] = pendapatan_mean["Sektor"].map(rename_pendapatan)

        # --- 2. Buat grafik gaya APS (area + markers) ---
        fig_pendapatan = px.area(
            pendapatan_mean,
            x="Sektor",
            y="Pendapatan",
            markers=True,
        )

        fig_pendapatan.update_traces(opacity=0.5, line=dict(width=3))
        fig_pendapatan.update_layout(
            height=450,
            xaxis_title="Sektor Ekonomi",
            yaxis_title="Pendapatan (Rata-rata Nasional)",
        )

        st.plotly_chart(fig_pendapatan, use_container_width=True)

#======= Pengaruh Bencana terhadap Variabel Sosial Ekonomi
    st.header("Pengaruh Bencana terhadap Kemiskinan")
    st.write("""
    Visualisasi ini menampilkan hubungan antara intensitas bencana dengan kondisi sosial ekonomi seperti jumlah penduduk miskin. 
    Tujuannya adalah untuk melihat apakah wilayah yang lebih sering mengalami bencana juga memiliki tingkat kemiskinan yang lebih tinggi.
    """)
    with st.expander("Tekan untuk melihat visualisasi"):
        # Dropdown untuk memilih jenis bencana
        selected_disaster = st.selectbox(
            "Pilih Jenis Bencana:",
            ["banjir", "gempa_bumi", "tanah_longsor"]
        )

        # Dropdown untuk memilih variabel sosial ekonomi
        selected_variable = st.selectbox(
            "Pilih Variabel Sosial Ekonomi:",
            ["penduduk_miskin", "keluarga_penerima"]
        )

        # Membuat dataframe hanya untuk kolom yang dipilih
        df_scatter = df[["provinsi", selected_disaster, selected_variable]].copy()
        df_scatter[selected_disaster] = pd.to_numeric(df_scatter[selected_disaster], errors="coerce")
        df_scatter[selected_variable] = pd.to_numeric(df_scatter[selected_variable], errors="coerce")

        # drop NA hasil konversi
        df_scatter = df_scatter.dropna(subset=[selected_disaster, selected_variable])

        # Membuat scatter plot menggunakan Plotly
        fig_scatter = px.scatter(
            df_scatter,
            x=selected_variable,
            y=selected_disaster,
            hover_name="provinsi",
            trendline="ols",
            title=f"Scatter Plot: {selected_variable.replace('_',' ').title()} vs {selected_disaster.title()}"
        )

        fig_scatter.update_traces(marker=dict(size=12, opacity=0.7))
        fig_scatter.update_layout(height=550)

        # Tampilkan plot
        st.plotly_chart(fig_scatter, use_container_width=True)

        # ================================
        # 1️⃣ Hitung korelasi
        # ================================
        corr_disaster_pengaruh_bencana_kemiskinan = df_scatter[selected_disaster].corr(df_scatter[selected_variable])

        st.metric(
            label=f"Korelasi {selected_disaster.title()} → {selected_variable.replace('_',' ').title()}",
            value=f"{corr_disaster_pengaruh_bencana_kemiskinan:.3f}",
            delta=(
                f"Korelasi positif: saat {selected_disaster} meningkat, {selected_variable.replace('_',' ')} cenderung meningkat."
                if corr_disaster_pengaruh_bencana_kemiskinan > 0
                else f"Korelasi negatif: saat {selected_disaster} meningkat, {selected_variable.replace('_',' ')} cenderung menurun."
            )
        )

# =======   
    st.header("Penduduk Miskin dan Keluarga Penerima Bansos per Provinsi")
    with st.expander("Tekan untuk melihat visualisasi"):
        # Pastikan kolom numerik
        df['keluarga_penerima'] = df['keluarga_penerima'].astype(str).str.replace(',', '').str.strip()
        df['keluarga_penerima'] = pd.to_numeric(df['keluarga_penerima'], errors='coerce')

        # Agregasi per provinsi
        df_plot = df.groupby("provinsi")[['penduduk_miskin', 'keluarga_penerima']].sum().reset_index()

        # Melt supaya jadi format panjang untuk Plotly
        df_melt = df_plot.melt(id_vars='provinsi', value_vars=['penduduk_miskin', 'keluarga_penerima'],
                            var_name='Variabel', value_name='Jumlah')

        # Rename agar lebih rapi
        rename_vars = {
            'penduduk_miskin': 'Penduduk Miskin',
            'keluarga_penerima': 'Keluarga Penerima Bansos'
        }
        df_melt['Variabel'] = df_melt['Variabel'].map(rename_vars)

        # Area chart
        fig = px.area(
            df_melt,
            x='provinsi',
            y='Jumlah',
            color='Variabel',
            markers=True,
            title="Penduduk Miskin dan Keluarga Penerima Bansos per Provinsi"
        )

        fig.update_traces(opacity=0.5, line=dict(width=3))
        fig.update_layout(height=450)

        st.plotly_chart(fig, use_container_width=True)

        # Hitung korelasi
        corr_bansos_pendudukmiskin = df_plot['penduduk_miskin'].corr(df_plot['keluarga_penerima'])

        st.metric(
            label="Korelasi Penduduk Miskin vs Keluarga Penerima Bansos",
            value=f"{corr_bansos_pendudukmiskin:.3f}",
            delta=(
                f"Korelasi positif: provinsi dengan penduduk miskin lebih banyak cenderung menerima bantuan sosial lebih banyak."
                if corr_bansos_pendudukmiskin > 0
                else f"Korelasi negatif: provinsi dengan penduduk miskin lebih banyak cenderung menerima bantuan sosial lebih sedikit."
            )
        )

# ================================
    st.header("Apakah Penerima Bantuan Sosial Memiliki APS Tinggi?")
    st.write("""Visualisasi ini menunjukkan hubungan antara jumlah penerima bantuan sosial dan tingkat APS (Angka Partisipasi Sekolah).
             Scatter plot ini digunakan untuk melihat apakah bantuan sosial dapat meningkatkan angka partisipasi sekolah""")

    with st.expander("Tekan untuk melihat visualisasi"):
        # =======================
        # 1. Tambahkan Total APS
        # =======================

        aps_map = {
            "APS 7–12 Tahun": "aps_7_12",
            "APS 13–15 Tahun": "aps_13_15",
            "APS 16–18 Tahun": "aps_16_18",
            "APS 19–23 Tahun": "aps_19_23",
            "TOTAL APS (Rata-rata)": "aps_total"
        }
        # =======================
        # 2. Dropdown APS
        # =======================

        selected_aps_label = st.selectbox(
            "Pilih Jenjang APS:",
            list(aps_map.keys())
        )

        aps_col = aps_map[selected_aps_label]

        # =======================
        # 3. Scatter Plot
        # =======================

        fig = px.scatter(
            df,
            x="keluarga_penerima",
            y=aps_col,
            hover_name="provinsi",
            trendline="ols",
            title=f"Hubungan Penerima Bantuan dan {selected_aps_label}",
            labels={
                "keluarga_penerima": "Jumlah Penerima Bantuan Sosial",
                aps_col: selected_aps_label
            }
        )

        fig.update_traces(marker=dict(size=14, opacity=0.75))
        fig.update_layout(height=520)

        st.plotly_chart(fig, use_container_width=True)

        # =======================
        # 4. Korelasi
        # =======================

        corr_value_bansos_aps = df["keluarga_penerima"].corr(df[aps_col])
        st.metric(
            label="Korelasi Penerima Bantuan vs Total APS",
            value=f"{corr_value_bansos_aps:.3f}",
            delta=(
                "Positif → kesimpulannya adalah ketika angka penerima bantuan sosial lebih tinggi, justru APS cenderung lebih tinggi"
                if corr_value_bansos_aps > 0 else
                "Negatif → kesimpulannya adalah ketika angka penerima bantuan sosial lebih tinggi, justru APS cenderung lebih rendah"
            )
        )

#================== 
    st.header("Pengaruh Sektor Ekonomi terhadap Putus Sekolah")
    st.write("""Visualisasi ini menunjukkan hubungan antara angka putus sekolah dengan sektor pendapatan. 
             Scatter plot ini digunakan untuk melihat apakah sektor ekonomi berpengaruh pada terjadinya putus sekolah""")
    with st.expander("Tekan untuk melihat visualisasi"):

        # --- Hitung Total Putus Sekolah ---
        df["total_putus_sekolah"] = (
            df["putus_sd"] +
            df["putus_smp"] +
            df["putus_sma"] +
            df["putus_smk"]
        )

        # --- Dropdown sektor ekonomi ---
        sector = st.selectbox(
            "Pilih Sektor Pendapatan:",
            ["pendapatan_pertanian", "pendapatan_industri", "pendapatan_jasa"]
        )

        # --- Dropdown jenis putus sekolah termasuk TOTAL ---
        drop_col = st.selectbox(
            "Pilih Jenjang Putus Sekolah:",
            [
                "putus_sd",
                "putus_smp",
                "putus_sma",
                "putus_smk",
                "total_putus_sekolah"   # tambahan baru
            ]
        )

        # --- Scatter Plot ---
        fig = px.scatter(
            df,
            x=sector,
            y=drop_col,
            hover_name="provinsi",
            trendline="ols",
            title=f"{drop_col.replace('_',' ').title()} vs {sector.replace('_',' ').title()}",
            labels={
                sector: sector.replace("_", " ").title(),
                drop_col: drop_col.replace("_", " ").title()
            }
        )

        fig.update_traces(marker=dict(size=12, opacity=0.7))
        fig.update_layout(height=520)

        st.plotly_chart(fig, use_container_width=True)

        # --- Korelasi otomatis ---
        corr_ekonomi_ptssklh = df[sector].corr(df[drop_col])

        st.metric(
            label="Korelasi",
            value=f"{corr_ekonomi_ptssklh:.3f}",
            delta=(
                "Positif → ketika pedapatan sektor naik, angka putus sekolah meningkat"
                if corr_ekonomi_ptssklh > 0 else
                "Negatif → ketika pendapatan sektor naik, angka putus sekolah menurun"
            )
        )

#===============================
    st.header("Hubungan Pengeluaran Pangan dan Non-Pangan terhadap APS")
    st.write("""Visualisasi ini menunjukkan hubungan antara angka partisipasi sekolah dengan pengeluaran pangan dan non-pangan. 
             Scatter plot ini digunakan untuk melihat bagaimanakah hubungan pangan dan non-pangan terhadap angka partisipasi sekolah di indonesia""")
    with st.expander("Tekan untuk melihat visualisasi"):

        # === Buat kolom APS Total ===
        df["aps_total"] = df[["aps_7_12", "aps_13_15", "aps_16_18", "aps_19_23"]].sum(axis=1)

        # === Pilihan APS ===
        aps_map = {
            "APS 7–12 Tahun": "aps_7_12",
            "APS 13–15 Tahun": "aps_13_15",
            "APS 16–18 Tahun": "aps_16_18",
            "APS 19–23 Tahun": "aps_19_23",
            "APS Total": "aps_total"
        }

        selected_aps = st.selectbox("Pilih Jenjang APS:", list(aps_map.keys()))
        aps_col = aps_map[selected_aps]

        pengeluaran_var = "pengeluaran_pangan_dan_nonpangan"

        # Filter data (jika mau hilangkan baris 'Indonesia')
        df_plot = df[df["provinsi"] != "Indonesia"].copy()

        # Scatter plot
        fig = px.scatter(
            df_plot,
            x=pengeluaran_var,
            y=aps_col,
            hover_name="provinsi",
            trendline="ols",
            title=f"Pengeluaran {pengeluaran_var.replace('_',' ').title()} vs {selected_aps}"
        )

        fig.update_traces(marker=dict(size=12, opacity=0.75))
        fig.update_layout(
            xaxis_title="Pengeluaran Pangan & Non-Pangan",
            yaxis_title=selected_aps,
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Korelasi
        corr = df_plot[pengeluaran_var].corr(df_plot[aps_col])
        st.metric(
            label=f"Korelasi {pengeluaran_var.replace('_',' ').title()} → {selected_aps}",
            value=f"{corr:.3f}",
            delta="positif artinya APS meningkat seiring pengeluaran meningkat" if corr > 0 else "negatif artinya APS menurun seiring pengeluaran meningkat"
        )

    #========================
    st.header("Hubungan Penduduk Miskin dengan Jumlah Guru")

    st.write("""
    Visualisasi ini menunjukkan hubungan antara **jumlah penduduk miskin** dengan **jumlah guru** di tiap jenjang sekolah per provinsi.
    Tujuannya untuk melihat apakah provinsi dengan tingkat kemiskinan tinggi memiliki jumlah guru yang memadai.
    """)
    with st.expander("Tekan untuk melihat visualisasi"):

        # Mapping kolom guru per jenjang
        jenjang_guru = {
            "SD": "jml_gr_sd",
            "SMP": "jml_gr_smp",
            "SMA": "jml_gr_sma",
            "SMK": "jml_gr_smk",
            "Total Guru" : "jml_guru_all"
        }
        df['jml_guru_all'] = df[['jml_gr_sd', 'jml_gr_smp', 'jml_gr_sma', 'jml_gr_smk']].sum(axis=1)

        # Dropdown untuk memilih jenjang
        selected_jenjang = st.selectbox("Pilih Jenjang Guru:", list(jenjang_guru.keys()))
        kolom_guru = jenjang_guru[selected_jenjang]

        # Pastikan kolom numerik
        df['penduduk_miskin'] = pd.to_numeric(df['penduduk_miskin'], errors='coerce')
        df[kolom_guru] = pd.to_numeric(df[kolom_guru], errors='coerce')

        # Drop NA
        df_plot = df.dropna(subset=['penduduk_miskin', kolom_guru])

        # Scatter plot dengan trendline
        fig = px.scatter(
            df_plot,
            x='penduduk_miskin',
            y=kolom_guru,
            hover_name='provinsi',
            trendline='ols',
            title=f"Penduduk Miskin vs Jumlah Guru ({selected_jenjang})",
            labels={
                'penduduk_miskin': 'Penduduk Miskin (%)',
                kolom_guru: f"Jumlah Guru {selected_jenjang}"
            }
        )
        fig.update_traces(marker=dict(size=12, opacity=0.7))
        fig.update_layout(height=550)
        st.plotly_chart(fig, use_container_width=True)
        
        # Hitung korelasi
        corr_value_gr_miskin = df_plot['penduduk_miskin'].corr(df_plot[kolom_guru])

        # Tampilkan metric dengan kalimat informatif
        st.metric(
        label=f"Korelasi Penduduk Miskin ↔ Jumlah Guru ({selected_jenjang})",
        value=f"{corr_value_gr_miskin:.3f}",
        delta=(
            f"Korelasi positif: provinsi dengan penduduk miskin lebih banyak cenderung punya lebih banyak guru. Bisa dibayangkan, guru-guru ini ‘berjuang di wilayah miskin’!" 
            if corr_value_gr_miskin > 0 
            else f"Korelasi negatif: provinsi dengan penduduk miskin lebih banyak justru punya lebih sedikit guru, menandakan guru ‘kurang tersebar di wilayah miskin’."
        )
    )
with tab_lingkungan_geospasial:
   # --- Header & Penjelasan ---
    st.header("Putus Sekolah vs Tingkat Rawan Bencana")

    st.write("""
    Scatter plot ini digunakan untuk melihat keterkaitan antara **jumlah putus sekolah** dan **tingkat rawan bencana** di tiap provinsi.Dengan visualisasi ini, kita bisa mengetahui apakah putus sekolah lebih tinggi terjadi di wilayah yang rawan terkena bencana.
    """)

    with st.expander("Tekan untuk melakukan analisis"):

        # Mapping jenjang putus sekolah
        jenjang_putus = {
            "SD": "putus_sd",
            "SMP": "putus_smp",
            "SMA": "putus_sma",
            "SMK": "putus_smk",
            "Total Putus Sekolah": "total_putus_sekolah"
        }

        # Dropdown pilih jenjang
        pilihan_jenjang = st.selectbox("Pilih Jenjang Putus Sekolah", list(jenjang_putus.keys()))
        kolom_putus = jenjang_putus[pilihan_jenjang]

        # Hitung total bencana
        bencana_cols = ["banjir", "gempa_bumi", "tanah_longsor"]
        df['total_bencana'] = df[bencana_cols].sum(axis=1)

        # Dropdown pilih bencana
        pilihan_bencana = st.selectbox("Pilih Jenis Bencana", bencana_cols + ["Total Bencana"])
        kolom_bencana = 'total_bencana' if pilihan_bencana == "Total Bencana" else pilihan_bencana

        # --- Scatter Plot ---
        fig_scatter = px.scatter(
            df,
            x=kolom_bencana,
            y=kolom_putus,
            trendline="ols",
            hover_name="provinsi",
            labels={
                kolom_bencana: pilihan_bencana.replace("_", " ").capitalize(),
                kolom_putus: f"Putus Sekolah {pilihan_jenjang}"
            },
        )

        fig_scatter.update_traces(marker=dict(size=11, opacity=0.8))
        fig_scatter.update_layout(height=500)

        st.plotly_chart(fig_scatter, use_container_width=True)

        # --- Korelasi ---
        corr_value = df[kolom_bencana].corr(df[kolom_putus])
        st.metric(
            label=f"Korelasi {pilihan_bencana} → Putus Sekolah {pilihan_jenjang}",
            value=f"{corr_value:.3f}",
            delta=(
                "artinya ketika tingkat bencana meningkat, putus sekolah cenderung meningkat."
                if corr_value > 0
                else "artinya ketika tingkat bencana meningkat, putus sekolah justru cenderung menurun."
            )
        )
    #=======================
        # --- Header & Penjelasan ---
    st.header("Area Chart Putus Sekolah")
    st.write("""
    Visualisasi ini menampilkan **angka putus sekolah** per provinsi. Hover atau klik provinsi untuk melihat **jumlah bencana** dan total bencana.  
    """)

    with st.expander("Tekan untuk melihat visualisasi"):

        # Dropdown pilih jenjang putus sekolah
        pilihan_jenjang = st.selectbox(
            "Pilih Jenjang Putus Sekolah", 
            ["SD","SMP","SMA","SMK","Total Putus Sekolah"],
            key="area_jenjang"
        )

        if pilihan_jenjang == "Total Putus Sekolah":
            kolom_putus = "total_putus"
        else:
            kolom_putus = f"putus_{pilihan_jenjang.lower()}"

        # --- Area Chart Interaktif ---
        fig_area = px.area(
            df.sort_values('provinsi'),
            x='provinsi',
            y=kolom_putus,
            hover_data={
                'provinsi': True,
                kolom_putus: True,
                'banjir': True,
                'gempa_bumi': True,
                'tanah_longsor': True,
                'total_bencana': True
            },
            labels={
                'provinsi':'Provinsi',
                kolom_putus:f'Putus Sekolah {pilihan_jenjang}',
                'banjir':'Jumlah Banjir',
                'gempa_bumi':'Jumlah Gempa Bumi',
                'tanah_longsor':'Jumlah Tanah Longsor',
                'total_bencana':'Total Bencana'
            },
            title=f"Putus Sekolah {pilihan_jenjang} per Provinsi dengan Detail Bencana"
        )

        fig_area.update_layout(height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig_area, use_container_width=True)

        # --- Interpretasi Otomatis ---
        prov_high = df.loc[df[kolom_putus].idxmax()]
        prov_low  = df.loc[df[kolom_putus].idxmin()]

        st.subheader("Interpretasi Otomatis")
        st.write(f"- Provinsi dengan **putus sekolah tertinggi**: **{prov_high['provinsi']}** ({prov_high[kolom_putus]} siswa), total bencana: {prov_high['total_bencana']} (banjir: {prov_high['banjir']}, gempa: {prov_high['gempa_bumi']}, longsor: {prov_high['tanah_longsor']})")
        st.write(f"- Provinsi dengan **putus sekolah terendah**: **{prov_low['provinsi']}** ({prov_low[kolom_putus]} siswa), total bencana: {prov_low['total_bencana']} (banjir: {prov_low['banjir']}, gempa: {prov_low['gempa_bumi']}, longsor: {prov_low['tanah_longsor']})")

#=====================
    st.header("Pengaruh Akses Internet terhadap IPM")
    st.write("""
    Scatter plot ini digunakan untuk melihat apakah provinsi dengan **akses internet** yang tinggi cenderung memiliki **IPM yang lebih tinggi**. Dan juga untuk memastikan apakah daerah dengan akses internet rendah memiliki capaian pendidikan yang lebih buruk.
    """)

    with st.expander("Tekan untuk melakukan analisis"):

        # Dropdown pilih indikator akses internet
        pilihan_internet = st.selectbox(
            "Pilih Indikator Akses Internet", 
            ["internet_kota","internet_desa","internet_kotadesa"],
            key="ipm_internet"
        )

        # Scatter plot
        fig = px.scatter(
            df,
            x=pilihan_internet,
            y='ipm_2024',
            trendline="ols",
            hover_name="provinsi",
            labels={
                pilihan_internet: pilihan_internet.replace("_"," ").capitalize(),
                'ipm_2024': 'IPM 2024'
            },
            title=f"{pilihan_internet.replace('_',' ').capitalize()} vs IPM 2024"
        )

        fig.update_traces(marker=dict(size=11, opacity=0.8))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Korelasi otomatis
        corr_value = df[pilihan_internet].corr(df['ipm_2024'])
        st.metric(
            label=f"Korelasi {pilihan_internet.replace('_',' ').capitalize()} → IPM 2024",
            value=f"{corr_value:.3f}",
            delta=(
                "artinya akses internet yang lebih tinggi berkaitan dengan IPM lebih tinggi → capaian pendidikan, kesehatan, dan standar hidup lebih baik."
                if corr_value > 0
                else "artinya akses internet yang lebih rendah berkaitan dengan IPM lebih rendah → capaian pendidikan, kesehatan, dan standar hidup kemungkinan lebih buruk."
            )
        )

#======
    st.header("Pengaruh Akses Internet terhadap Angka Partisipasi Sekolah (APS)")
    st.write("""Scatter plot ini menunjukkan hubungan antara **akses internet** di provinsi dengan **Angka Partisipasi Sekolah (APS)**.  
             Tujuannya untuk melihat apakah provinsi dengan akses internet yang lebih rendah cenderung memiliki partisipasi sekolah yang lebih rendah, 
             Visualisasi ini membantu mengidentifikasi provinsi yang mungkin membutuhkan peningkatan infrastruktur digital untuk mendukung pendidikan.""")

    with st.expander("Tekan untuk melakukan analisis"):

        # Dropdown pilih indikator APS (termasuk Total APS)
        pilihan_aps = st.selectbox(
            "Pilih Indikator APS",
            ["aps_7_12","aps_13_15","aps_16_18","aps_19_23","Total APS"],
            key="aps_internet"
        )

        if pilihan_aps == "Total APS":
            kolom_aps = "aps_total"
        else:
            kolom_aps = pilihan_aps

        # Dropdown pilih indikator akses internet
        pilihan_internet = st.selectbox(
            "Pilih Indikator Akses Internet", 
            ["internet_kota","internet_desa","internet_kotadesa"],
            key="aps_internet_access"
        )

        # Scatter plot
        fig = px.scatter(
            df,
            x=pilihan_internet,
            y=kolom_aps,
            trendline="ols",
            hover_name="provinsi",
            labels={
                pilihan_internet: pilihan_internet.replace("_"," ").capitalize(),
                kolom_aps: kolom_aps.replace("_"," ").capitalize()
            },
            title=f"{pilihan_internet.replace('_',' ').capitalize()} vs {kolom_aps.replace('_',' ').capitalize()}"
        )

        fig.update_traces(marker=dict(size=11, opacity=0.8))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Korelasi otomatis
        corr_value = df[pilihan_internet].corr(df[kolom_aps])
        st.metric(
            label=f"Korelasi {pilihan_internet.replace('_',' ').capitalize()} → {kolom_aps.replace('_',' ').capitalize()}",
            value=f"{corr_value:.3f}",
            delta=(
                "artinya akses internet yang lebih tinggi berkaitan dengan APS lebih tinggi → partisipasi pendidikan lebih baik."
                if corr_value > 0
                else "artinya akses internet yang lebih rendah berkaitan dengan APS lebih rendah → partisipasi pendidikan kemungkinan lebih buruk."
            )
        )

    #==========================
    st.header("Pengaruh Jumlah Kendaraan terhadap Partisipasi Sekolah (APS)")
    st.write("""
    Scatter plot ini digunakan untuk melihat apakah **jumlah kendaraan** mempengaruhi **Angka Partisipasi Sekolah**. Jumlah kendaraan bisa menjadi proxy akses transportasi menuju sekolah""")

    with st.expander("Tekan untuk melakukan analisis"):

        # Dropdown pilih APS
        pilihan_aps = st.selectbox(
            "Pilih Indikator APS",
            ["aps_7_12","aps_13_15","aps_16_18","aps_19_23","aps_total"],
            key="aps_kendaraan"
        )

        # Scatter plot
        fig = px.scatter(
            df,
            x='kendaraan',
            y=pilihan_aps,
            trendline="ols",
            hover_name="provinsi",
            labels={
                'kendaraan': 'Jumlah Kendaraan',
                pilihan_aps: pilihan_aps.replace("_"," ").capitalize()
            },
            title=f"Jumlah Kendaraan vs {pilihan_aps.replace('_',' ').capitalize()}"
        )

        fig.update_traces(marker=dict(size=11, opacity=0.8))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Korelasi otomatis
        corr_value = df['kendaraan'].corr(df[pilihan_aps])
        st.metric(
            label=f"Korelasi Kendaraan → {pilihan_aps.replace('_',' ').capitalize()}",
            value=f"{corr_value:.3f}",
            delta=(
                "artinya semakin banyak kendaraan, APS cenderung lebih tinggi → akses ke sekolah lebih mudah."
                if corr_value > 0
                else "artinya semakin sedikit kendaraan, APS cenderung lebih rendah → akses ke sekolah lebih sulit."
            )
        )

#===

# --- Header & Penjelasan ---
    st.header("Pengaruh Lokasi Bencana Alam terhadap IPM Provinsi")
    st.write("""
    Scatter plot ini digunakan untuk melihat apakah provinsi dengan **frekuensi bencana alam tinggi** cenderung memiliki **IPM lebih rendah**.  
    IPM mencerminkan capaian pendidikan, kesehatan, dan standar hidup.
    """)

    with st.expander("Tekan untuk melakukan analisis"):

        # Dropdown pilih jenis bencana
        pilihan_bencana = st.selectbox(
            "Pilih Jenis Bencana",
            ["banjir","gempa_bumi","tanah_longsor","total_bencana"],
            key="bencana_ipm"
        )

        # Scatter plot
        fig = px.scatter(
            df,
            x=pilihan_bencana,
            y='ipm_2024',
            trendline="ols",
            hover_name="provinsi",
            labels={
                pilihan_bencana: pilihan_bencana.replace("_"," ").capitalize(),
                'ipm_2024': 'IPM 2024'
            },
            title=f"{pilihan_bencana.replace('_',' ').capitalize()} vs IPM 2024"
        )

        fig.update_traces(marker=dict(size=11, opacity=0.8))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Korelasi otomatis
        corr_value = df[pilihan_bencana].corr(df['ipm_2024'])
        st.metric(
            label=f"Korelasi {pilihan_bencana.replace('_',' ').capitalize()} → IPM 2024",
            value=f"{corr_value:.3f}",
            delta=(
                "artinya semakin banyak bencana alam, IPM cenderung lebih rendah"
                if corr_value < 0
                else "artinya semakin banyak bencana alam, IPM cenderung lebih tinggi"
            )
        )

# ====================
    # --- Header & Penjelasan ---
    st.header("Pengaruh Bencana Alam terhadap Angka Partisipasi Sekolah (APS)")
    st.write("""
    Scatter plot ini digunakan untuk melihat apakah provinsi dengan **frekuensi bencana alam tinggi** cenderung memiliki **APS lebih rendah**.  
    APS mencerminkan partisipasi pendidikan anak-anak dan remaja.
    """)

    with st.expander("Tekan untuk melakukan analisis"):

        # Dropdown pilih jenis APS
        pilihan_aps = st.selectbox(
            "Pilih Indikator APS",
            ["aps_7_12","aps_13_15","aps_16_18","aps_19_23","aps_total"],
            key="aps_bencana"
        )

        # Dropdown pilih jenis bencana
        pilihan_bencana = st.selectbox(
            "Pilih Jenis Bencana",
            ["banjir","gempa_bumi","tanah_longsor","total_bencana"],
            key="bencana_aps"
        )

        # Scatter plot
        fig = px.scatter(
            df,
            x=pilihan_bencana,
            y=pilihan_aps,
            trendline="ols",
            hover_name="provinsi",
            labels={
                pilihan_bencana: pilihan_bencana.replace("_"," ").capitalize(),
                pilihan_aps: pilihan_aps.replace("_"," ").capitalize()
            },
            title=f"{pilihan_bencana.replace('_',' ').capitalize()} vs {pilihan_aps.replace('_',' ').capitalize()}"
        )

        fig.update_traces(marker=dict(size=11, opacity=0.8))
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Korelasi otomatis
        corr_value = df[pilihan_bencana].corr(df[pilihan_aps])
        st.metric(
            label=f"Korelasi {pilihan_bencana.replace('_',' ').capitalize()} → {pilihan_aps.replace('_',' ').capitalize()}",
            value=f"{corr_value:.3f}",
            delta=(
                "artinya semakin banyak bencana alam, APS cenderung lebih rendah"
                if corr_value < 0
                else "artinya semakin banyak bencana alam, APS cenderung lebih tinggi"
            )
        )

# === INFRASTRUKTUR ===

# hitung rasio murid-guru
df["rasio_sd"] = df["murid_sd"] / df["jml_gr_sd"]
df["rasio_smp"] = df["murid_smp"] / df["jml_gr_smp"]
df["rasio_sma"] = df["murid_sma"] / df["jml_gr_sma"]

with tab_infrastruktur:

    # === RASIO MURID-GURU TERHADAP KUALITAS PENDIDIKAN ===
    st.subheader("Rasio Murid–Guru Terhadap Kualitas Pendidikan")
    st.write(
        "Visualisasi ini digunakan untuk mengidentifikasi hubungan antara rasio murid–guru "
        "dan kualitas pendidikan di setiap provinsi. Rasio yang semakin tinggi menunjukkan "
        "bahwa seorang guru menangani lebih banyak murid, sehingga potensi penurunan efektivitas "
        "proses pembelajaran menjadi lebih besar. Melalui grafik ini, hubungan antara beban kerja "
        "guru dan capaian pendidikan dapat diamati secara lebih objektif."
    )

    with st.expander("Tekan untuk melakukan analisis"):
    
        # === HILANGKAN BARIS 'Indonesia' ===
        df_plot = df[df["provinsi"] != "Indonesia"]

        # === Dropdown Jenjang Pendidikan ===
        jenjang = st.selectbox(
            "Pilih Jenjang Pendidikan",
            ["SD", "SMP", "SMA"]
        )

        # === Tentukan kolom kualitas ===
        if jenjang == "SD":
            col_rasio = "rasio_sd"
            col_kualitas = "penyelesaian_pendidikanSD2024"
        elif jenjang == "SMP":
            col_rasio = "rasio_smp"
            col_kualitas = "penyelesaian_pendidikanSMP2024"
        elif jenjang == "SMA":
            col_rasio = "rasio_sma"
            col_kualitas = "penyelesaian_pendidikanSMA2024"

        # check kolom
        if col_kualitas not in df_plot.columns:
            st.error(f"Kolom indikator kualitas {col_kualitas} tidak ditemukan di data.")
        else:
            # === Bubble Chart ===
            fig = px.scatter(
                df_plot,
                x=col_rasio,
                y=col_kualitas,
                size="total_murid",
                color="provinsi",
                hover_name="provinsi",
                title=f"Bubble Chart – Pengaruh Rasio Murid–Guru Terhadap Kualitas Pendidikan ({jenjang})",
                size_max=60
            )

            fig.update_layout(
                xaxis_title="Rasio Murid–Guru",
                yaxis_title="Indikator Kualitas Pendidikan",
                legend_title="Provinsi",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.info(
            "💡 *Interpretasi:* Pada grafik, posisi bubble menunjukkan hubungan antara beban guru dan capaian pendidikan. "
            "Jika bubble lebih tinggi saat rasio murid–guru rendah, hal ini menandakan guru dapat memberikan perhatian lebih kepada setiap siswa sehingga kualitas pembelajaran lebih baik. "
            "Sebaliknya, jika bubble lebih rendah saat rasio tinggi, artinya beban guru lebih besar dan efektivitas pembelajaran berpotensi menurun."
        )

    # === KETERSEDIAAN SEKOLAH TERHADAP ANGKA PUTUS SEKOLAH
    st.subheader("Ketersediaan Sekolah vs Angka Putus Sekolah (Grouped Bar Chart)")

    st.write("""
    Visualisasi ini menunjukkan hubungan antara jumlah sekolah yang tersedia 
    dengan angka putus sekolah pada setiap jenjang pendidikan. Pemilihan jenjang 
    memungkinkan analisis yang lebih terfokus terhadap kondisi pada masing-masing tingkat pendidikan.
    """)

    with st.expander("Tekan untuk melakukan analisis"):
        # === PILIH JENJANG ===
        jenjang = st.selectbox(
            "Pilih Jenjang Pendidikan:",
            ["SD", "SMP", "SMA", "SMK"]
        )

        # === Mapping kolom berdasarkan jenjang ===
        mapping = {
            "SD": {"sekolah": "jml_sklh_sd", "putus": "putus_sd"},
            "SMP": {"sekolah": "jml_sklh_smp", "putus": "putus_smp"},
            "SMA": {"sekolah": "jml_sklh_sma", "putus": "putus_sma"},
            "SMK": {"sekolah": "jml_sklh_smk", "putus": "putus_smk"}
        }

        # Ambil nama kolom sesuai jenjang
        col_sekolah = mapping[jenjang]["sekolah"]
        col_putus = mapping[jenjang]["putus"]

        # === HILANGKAN BARIS 'INDONESIA' ===
        df_clean = df[df["provinsi"] != "Indonesia"].copy()

        # === Siapkan data khusus jenjang terpilih ===
        df_filtered = pd.DataFrame({
            "Provinsi": df_clean["provinsi"],
            f"Jumlah Sekolah {jenjang}": df_clean[col_sekolah],
            f"Putus Sekolah {jenjang}": df_clean[col_putus],
        })

        # === Melt untuk bentuk long (biar bisa grouped bar) ===
        df_melt = df_filtered.melt(
            id_vars="Provinsi",
            var_name="Kategori",
            value_name="Nilai"
        )

        # === Chart ===
        fig = px.bar(
            df_melt,
            x="Provinsi",
            y="Nilai",
            color="Kategori",
            barmode="group",
            title=f"Ketersediaan Sekolah dan Angka Putus Sekolah – Jenjang {jenjang}"
        )

        fig.update_layout(
            xaxis_title="Provinsi",
            yaxis_title="Jumlah",
            legend_title="Kategori",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

# === KETAHANAN PANGAN DAN AIR ===
with tab_airpangan:

    st.subheader("Pengaruh Ketahanan Pangan dan Akses Air Layak terhadap Kualitas SDM")
    st.write(
        "Bagian ini menampilkan hubungan antara kondisi pangan dan air dengan kualitas "
        "sumber daya manusia. Semakin baik ketahanan pangan dan akses air minum layak, "
        "diharapkan semakin tinggi pula kualitas SDM suatu wilayah."
    )

    # === HILANGKAN BARIS 'Indonesia' ===
    df_plot = df[df["provinsi"] != "Indonesia"]

    # ==========================================================
    # 1. PLOT KETAHANAN PANGAN vs IPM
    # ==========================================================
    st.subheader("Ketahanan Pangan dan Kualitas SDM")

    with st.expander("Tekan untuk melakukan analisis"):

        if ("ketahanan_pangan" not in df_plot.columns) or ("ipm_2024" not in df_plot.columns):
            st.error("Kolom 'ketahanan_pangan' atau 'ipm_2024' tidak ditemukan pada dataset.")
        else:
            fig1 = px.scatter(
                df_plot,
                x="ketahanan_pangan",
                y="ipm_2024",
                color="provinsi",
                hover_name="provinsi",
                title="Scatter Plot – Ketahanan Pangan vs Indeks Pembangunan Manusia (IPM) 2024",
                size_max=50,
            )

            fig1.update_layout(
                xaxis_title="Indeks Ketahanan Pangan",
                yaxis_title="IPM 2024",
                legend_title="Provinsi",
                template="plotly_white"
            )

            st.plotly_chart(fig1, use_container_width=True)

        st.info(
            "💡 *Interpretasi:* Titik yang cenderung naik menunjukkan bahwa semakin baik ketahanan pangan, "
            "semakin tinggi kualitas SDM."
        )

    # ==========================================================
    # 2. PLOT AIR MINUM LAYAK vs IPM
    # ==========================================================
    st.subheader("Akses Air Minum Layak dan Kualitas SDM")

    with st.expander("Tekan untuk melakukan analisis"):

        if ("airminum_layak" not in df_plot.columns) or ("ipm_2024" not in df_plot.columns):
            st.error("Kolom 'airminum_layak' atau 'ipm_2024' tidak ditemukan pada dataset.")
        else:
            fig2 = px.scatter(
                df_plot,
                x="airminum_layak",
                y="ipm_2024",
                color="provinsi",
                hover_name="provinsi",
                title="Scatter Plot – Akses Air Minum Layak vs Indeks Pembangunan Manusia (IPM) 2024",
                size_max=50,
            )

            fig2.update_layout(
                xaxis_title="Akses Air Minum Layak (%)",
                yaxis_title="IPM 2024",
                legend_title="Provinsi",
                template="plotly_white"
            )

            st.plotly_chart(fig2, use_container_width=True)

        st.info(
            "💡 *Interpretasi:* Semakin tinggi akses air minum layak, umumnya kualitas SDM juga lebih tinggi."
        )

# === KONSUMSI GIZI ===

with tab_gizi:
    st.subheader("Pengaruh Konsumsi Gizi (Protein) terhadap Kualitas SDM")
    st.write(
        "Bagian ini menunjukkan hubungan antara konsumsi protein dan Indeks Pembangunan "
        "Manusia (IPM). Peningkatan asupan gizi yang lebih baik diharapkan berkontribusi "
        "positif terhadap kualitas SDM di setiap provinsi."
    )

    df_plot = df[df["provinsi"] != "Indonesia"].copy()

    # Pastikan kolom numerik
    df_plot["protein"] = pd.to_numeric(df_plot["protein"], errors="coerce")
    df_plot["ipm_2024"] = pd.to_numeric(df_plot["ipm_2024"], errors="coerce")

    df_plot = df_plot.dropna(subset=["protein", "ipm_2024"])

    st.subheader("Konsumsi Protein dan Kualitas SDM")

    with st.expander("Tekan untuk melakukan analisis"):

        if ("protein" not in df_plot.columns) or ("ipm_2024" not in df_plot.columns):
            st.error("Kolom 'protein' atau 'ipm_2024' tidak ditemukan pada dataset.")
        else:
            fig = px.scatter(
                df_plot,
                x="protein",
                y="ipm_2024",
                color="provinsi",
                hover_name="provinsi",
                trendline="ols",
                title="Scatter Plot – Konsumsi Protein vs Indeks Pembangunan Manusia (IPM) 2024"
            )

            fig.update_layout(
                xaxis_title="Konsumsi Protein (kapita)",
                yaxis_title="IPM 2024",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.info(
            "*Interpretasi:* Jika titik-titik membentuk pola naik, maka provinsi dengan "
        "konsumsi protein lebih tinggi cenderung memiliki IPM lebih baik."
        )
