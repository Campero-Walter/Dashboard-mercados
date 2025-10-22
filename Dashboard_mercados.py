# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 14:29:36 2025
                                     Risk Management
                                    By Campero Walter
                                Portfolio Manger | Qaunt Analyst

@author: walte
"""
#========================================================================================================================
#                                           DASHBOARD MERCADOS FINANCIEROS
#========================================================================================================================

import streamlit as st
import yfinance as yf
import seaborn as sns
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap

# ===============================
# CONFIGURACIÓN DE PÁGINA
# ===============================
st.set_page_config(page_title="Tablero Financiero - MERVAL & S&P 500", layout="wide")
st.title("📊 Tablero de Mercados Financieros")
st.markdown("Visualización interactiva del **MERVAL en USD CCL** y del **S&P 500** — datos actualizados desde Yahoo Finance.")

# ===============================
# ESTILO Y COLOR MAP
# ===============================
cmap_jp = LinearSegmentedColormap.from_list("Custom", ("red", "black", "green"), N=256)
plt.style.use("dark_background")

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("⚙️ Opciones del Tablero")
seccion = st.sidebar.radio("Seleccioná el mercado a visualizar:", ["MERVAL (USD CCL)", "S&P 500"])
st.sidebar.markdown("---")
st.sidebar.info("Fuente de datos: Yahoo Finance")

# ===============================
# MERVAL
# ===============================
if seccion == "MERVAL (USD CCL)":
    st.subheader("🇦🇷 MERVAL en dólares CCL")
    with st.spinner("Descargando datos..."):
        ticker = "^MERV"
        data = yf.download(ticker, auto_adjust=False, progress=False)
        df = data[['Close']].copy()
        df.columns = ['Close']
        
        ypfd = yf.download('YPFD.BA', auto_adjust=False)['Close']
        ypf = yf.download('YPF', auto_adjust=False)['Close']
        
        df_ccl = pd.concat([ypfd, ypf], axis=1)
        df_ccl.columns = ["YPFD.BA", "YPF"]
        ccl = (df_ccl['YPFD.BA'] / df_ccl['YPF']).dropna()
        
        df = df.to_frame(name="Close")
        df = df.reindex(ccl.index, method='ffill')  # rellena fechas faltantes
        df["USD_CCL"] = ccl
        df["Close_USD"] = df["Close"] / df["USD_CCL"]
        df = df.dropna(subset=["Close_USD"])

        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df["Close"] = df["Close_USD"]
        df = df.loc[df.index.year > 1999].copy()

        df["Year"] = df.index.year
        df["Month"] = df.index.month
        df = df.resample("M").last()
        df["variación"] = df['Close'].pct_change()

        tabla = df.pivot_table(index="Year", columns="Month", values="variación")
        meses = [x[:3] for x in list(calendar.month_name[1:])]
        tabla.columns = meses

    # --- HEATMAP ---
    fig1 = plt.figure(figsize=(18, 10))
    gs = GridSpec(nrows=3, ncols=2, figure=fig1, width_ratios=[2.5, 1], hspace=0.2, wspace=0.1, top=.9)
    ax_1 = fig1.add_subplot(gs[:, 0])
    ax_r = [fig1.add_subplot(gs[i, 1]) for i in range(3)]

    sc = lambda y: (y - y.min()) / (y.max() - y.min())
    ax_r[0].bar(meses, tabla.mean(), color=cmap_jp(sc(tabla.mean())), label="Media Returns", edgecolor="gray")
    ax_r[1].bar(meses, tabla.median(), color=cmap_jp(sc(tabla.median())), label="Mediana Returns", edgecolor="gray")
    ax_r[2].bar(meses, tabla.kurt(), color=cmap_jp(sc(tabla.kurt())), label="Kurtosis", edgecolor="gray")

    for i in range(3):
        ax_r[i].legend(fontsize=11)
        ax_r[i].grid(alpha=0.5)

    sns.heatmap(tabla, annot=True, ax=ax_1, cmap=cmap_jp, fmt=".2%", vmax=0.00, vmin=0.00, cbar_kws={"shrink": 0.6})
    ax_1.set_title("MERVAL: Rendimientos Mensuales en USD CCL (2000–2025)", fontsize=14)
    ax_1.grid(False)

    st.pyplot(fig1)

    # --- HISTOGRAMA DE RENDIMIENTOS ANUALES ---
    ytd = df.groupby("Year")["Close"].agg(["first", "last"])
    ytd["varytd"] = ytd["last"]/ytd["first"] - 1
    rendimientos = ytd["varytd"]

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.histplot(rendimientos, bins=15, kde=True, color='white', edgecolor="black", ax=ax2)
    ax2.axvline(rendimientos.mean(), color='gold', linestyle='--', label=f"Media: {rendimientos.mean():.2%}")
    ax2.axvline(rendimientos.median(), color='cyan', linestyle='--', label=f"Mediana: {rendimientos.median():.2%}")
    if 2025 in rendimientos.index:
        ax2.axvline(rendimientos[2025], color='red', linewidth=2, label=f"2025: {rendimientos[2025]:.2%}")
    ax2.legend()
    ax2.set_title("Distribución de Rendimientos Anuales del MERVAL (USD CCL)")
    st.pyplot(fig2)

    # --- BARRAS POR AÑO ---
    fig3, ax3 = plt.subplots(figsize=(16, 6))
    sc = lambda y: (y - y.min()) / (y.max() - y.min())
    bars = ax3.bar(rendimientos.index, rendimientos, color=cmap_jp(sc(rendimientos)), edgecolor="gray")
    for bar in bars:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.2%}", ha='center', va='bottom', fontsize=9, color='white')
    ax3.axhline(0, color="white")
    ax3.axhline(rendimientos.mean(), color='gold', linestyle='--', label=f"Media: {rendimientos.mean():.2%}")
    ax3.axhline(rendimientos.median(), color='cyan', linestyle='--', label=f"Mediana: {rendimientos.median():.2%}")
    ax3.legend()
    ax3.set_title("Rendimiento Anual del MERVAL en USD CCL")
    st.pyplot(fig3)

# ===============================
# S&P 500
# ===============================
else:
    st.subheader("🇺🇸 S&P 500")
    with st.spinner("Descargando datos..."):
        df = yf.download('^GSPC', auto_adjust=True, progress=False)['Close']
        df.rename(columns={"^GSPC":"Close"}, inplace = True)
        df = df.loc[df.index.year > 1980].copy()
        df["Year"] = df.index.year
        df["Month"] = df.index.month
        df = df.resample("M").last()
        df["variación"] = df.Close.pct_change()
        tabla = df.pivot_table(index="Year", columns="Month", values="variación")
        meses = [x[:3] for x in list(calendar.month_name[1:])]
        tabla.columns = meses

    fig4 = plt.figure(figsize=(18, 10))
    gs = GridSpec(nrows=3, ncols=2, figure=fig4, width_ratios=[2.5, 1], hspace=0.2, wspace=0.1, top=.9)
    ax_1 = fig4.add_subplot(gs[:, 0])
    ax_r = [fig4.add_subplot(gs[i, 1]) for i in range(3)]

    sc = lambda y: (y - y.min()) / (y.max() - y.min())
    ax_r[0].bar(meses, tabla.mean(), color=cmap_jp(sc(tabla.mean())), label="Media", edgecolor="gray")
    ax_r[1].bar(meses, tabla.median(), color=cmap_jp(sc(tabla.median())), label="Mediana", edgecolor="gray")
    ax_r[2].bar(meses, tabla.kurt(), color=cmap_jp(sc(tabla.kurt())), label="Kurtosis", edgecolor="gray")

    for i in range(3):
        ax_r[i].legend(fontsize=11)
        ax_r[i].grid(alpha=0.5)

    sns.heatmap(tabla, annot=True, ax=ax_1, cmap=cmap_jp, fmt=".2%", vmax=0.00, vmin=0.00, cbar_kws={"shrink": 0.6})
    ax_1.set_title("S&P 500: Rendimientos Mensuales (1981–2025)", fontsize=14)
    ax_1.grid(False)
    st.pyplot(fig4)

    st.dataframe(tabla.round(4), use_container_width=True)

st.markdown("---")
st.caption("By Walter Campero")
st.caption("Portfolio Manager | Quant Analyst")
st.caption("Fuente: Yahoo Finance")



