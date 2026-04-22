import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Rentas Pro", layout="centered")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Usaremos st.connection para leer y escribir
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏨 Gestión de Rentas")

opcion = st.sidebar.radio("MENÚ:", ["📝 Reservar", "👤 Ver por Trabajador", "📊 Historial"])

# URL de tu Google Sheet (Asegúrate de cambiarla por la tuya)
url = "https://docs.google.com/spreadsheets/d/1OQFeiDtvhV2wPMvt3YZNTpdaej_54h-R3TYgbfELNeA/edit?usp=sharing"

if opcion == "📝 Reservar":
    st.header("Nueva Reservación")
    with st.form("form"):
        dueño = st.selectbox("Asignar a:", ["Jaky", "Miriam", "Pepillo"])
        cliente = st.text_input("Nombre del Huésped")
        depa = st.text_input("Departamento / Casa")
        precio = st.number_input("Precio por noche ($)", min_value=0)
        col1, col2 = st.columns(2)
        llegada = col1.date_input("Entrada")
        salida = col2.date_input("Salida")
        transporte = st.checkbox("Transporte Internacional (+$100)")
        
        noches = (salida - llegada).days
        total = (noches * precio) + (100 if transporte else 0)
        
        if submit := st.form_submit_button("GUARDAR EN LA NUBE"):
            if cliente and depa and noches > 0:
                # Leer datos actuales
                df_actual = conn.read(spreadsheet=url)
                # Crear nueva fila
                nueva_fila = pd.DataFrame([{
                    "Dueño": dueño, "Huésped": cliente, "Propiedad": depa,
                    "Llegada": str(llegada), "Salida": str(salida), "Total": total
                }])
                # Concatenar y actualizar
                df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
                conn.update(spreadsheet=url, data=df_final)
                st.success("✅ ¡Guardado y sincronizado!")
                st.balloons()

elif opcion == "👤 Ver por Trabajador" or opcion == "📊 Historial":
    df = conn.read(spreadsheet=url)
    if opcion == "👤 Ver por Trabajador":
        t = st.selectbox("Selecciona:", ["Jaky", "Miriam", "Pepillo"])
        st.table(df[df["Dueño"] == t])
    else:
        st.dataframe(df, use_container_width=True)
