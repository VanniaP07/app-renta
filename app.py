import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración para que se vea bien en celular
st.set_page_config(page_title="Rentas Pro", layout="centered")

# --- TÍTULO ---
st.title("🏨 Gestión de Rentas")

# --- MENÚ DE NAVEGACIÓN ---
opcion = st.sidebar.radio("IR A:", ["📝 Reservar", "👤 Ver por Trabajador", "📊 Historial Completo"])

# Simulamos datos (Aquí es donde conectaremos tu Google Sheet después)
if 'db' not in st.session_state:
    st.session_state.db = []

if opcion == "📝 Reservar":
    st.header("Nueva Reserva")
    
    with st.form("form_registro", clear_on_submit=True):
        dueño = st.selectbox("Asignar a:", ["Jaky", "Miriam", "Pepillo"])
        cliente = st.text_input("Nombre del Huésped")
        depa = st.text_input("Departamento / Casa")
        precio = st.number_input("Precio por noche ($)", min_value=0)
        
        col1, col2 = st.columns(2)
        llegada = col1.date_input("Llegada")
        salida = col2.date_input("Salida")
        
        transporte = st.checkbox("Transporte Internacional (+$100)")
        
        # Cálculo automático
        noches = (salida - llegada).days
        total = (noches * precio) + (100 if transporte else 0)
        
        if noches > 0:
            st.info(f"🌙 Noches: {noches} | 💰 TOTAL: ${total}")
        
        btn_guardar = st.form_submit_button("GUARDAR RESERVA")
        
        if btn_guardar:
            nueva_reserva = {
                "Dueño": dueño, "Huésped": cliente, "Propiedad": depa,
                "Llegada": llegada, "Salida": salida, "Total": f"${total}"
            }
            st.session_state.db.append(nueva_reserva)
            st.success(f"✅ Guardado para {dueño}")

elif opcion == "👤 Ver por Trabajador":
    trabajador = st.selectbox("Selecciona trabajador:", ["Jaky", "Miriam", "Pepillo"])
    st.subheader(f"Huéspedes de {trabajador}")
    
    df = pd.DataFrame(st.session_state.db)
    if not df.empty:
        filtrado = df[df["Dueño"] == trabajador]
        st.table(filtrado)
    else:
        st.write("No hay reservas aún.")

elif opcion == "📊 Historial Completo":
    st.header("Todas las Reservas")
    df = pd.DataFrame(st.session_state.db)
    if not df.empty:
        # Ordenar por fecha de llegada
        df = df.sort_values(by="Llegada")
        st.dataframe(df, use_container_width=True)
