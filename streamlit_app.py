
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="CALCULADORA MARTINEZ/ITALIANO", layout="centered")

st.image("logo_para_app.png", width=300)

st.title("CALCULADORA MARTINEZ/ITALIANO")

nombre = st.text_input("Nombre del caso:")
haber_base = st.number_input("Ingresar haber base ($):", min_value=0.0, step=100.0)
fecha_base = st.date_input("Fecha del haber base:", value=datetime.date(2020, 1, 1))

if haber_base and fecha_base:
    df_anses = pd.read_csv("movilidad_anses.csv")
    df_justicia = pd.read_csv("movilidad_justicia.csv")

    df_anses["fecha"] = pd.to_datetime(df_anses["fecha"])
    df_justicia["fecha"] = pd.to_datetime(df_justicia["fecha"])

    df_anses = df_anses[df_anses["fecha"] >= pd.to_datetime(fecha_base)]
    df_justicia = df_justicia[df_justicia["fecha"] >= pd.to_datetime(fecha_base)]

    # Agregar coeficiente automático para marzo 2020 ANSeS si falta
    fecha_marzo_2020 = pd.to_datetime("2020-03-01")
    if fecha_base <= fecha_marzo_2020 and fecha_marzo_2020 not in df_anses["fecha"].values:
        coef_marzo = round(1.023 + (1500 / haber_base), 6)
        nueva_fila = pd.DataFrame({"fecha": [fecha_marzo_2020], "coef_anses": [coef_marzo]})
        df_anses = pd.concat([df_anses, nueva_fila], ignore_index=True).sort_values("fecha")

    coef_total_anses = df_anses["coef_anses"].prod()
    coef_total_justicia = df_justicia["coef_justicia"].prod()

    haber_anses = haber_base * coef_total_anses
    haber_justicia = haber_base * coef_total_justicia
    diferencia = haber_justicia - haber_anses

    st.subheader(f"Resultado para: {nombre}")
    st.write(f"**Haber actualizado según ANSES:** ${haber_anses:,.2f}")
    st.write(f"**Haber actualizado según Justicia:** ${haber_justicia:,.2f}")
    st.write(f"**Diferencia potencial a reclamar:** ${diferencia:,.2f}")
