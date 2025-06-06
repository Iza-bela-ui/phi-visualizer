
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from matplotlib.patches import Rectangle, Circle

st.set_page_config(layout="wide")
st.title("Wizualizacja odwzorowania Φ: ℝ² → ℝ²")

with st.expander("📝 Dokumentacja i ograniczenia"):
    st.markdown("""
    ### Ograniczenia aplikacji:
    1. **Odwzorowanie Φ**: funkcje u(x,y) i v(x,y) muszą być jawnie określone.
    2. **Zbiory B i C**: mogą być prostokątami lub kołami.
    3. **Instrukcja**: zdefiniuj Φ, ustaw parametry zbiorów, zobacz wizualizacje.
    """)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Definicja Φ(x,y) = (u(x,y), v(x,y))")
    u_expr = st.text_input("u(x, y) =", "x**2 - y**2")
    v_expr = st.text_input("v(x, y) =", "2*x*y")
    xmin, xmax = st.slider("Zakres x", -10.0, 10.0, (-3.0, 3.0))
    ymin, ymax = st.slider("Zakres y", -10.0, 10.0, (-3.0, 3.0))
    resolution = st.slider("Rozdzielczość siatki", 10, 200, 50)

with col2:
    st.subheader("Zbiór B (dla Φ⁻¹(B))")
    b_type = st.selectbox("Typ B", ["Prostokąt", "Koło"])
    if b_type == "Prostokąt":
        b_u1, b_u2 = st.slider("Zakres u", -20.0, 20.0, (-1.0, 1.0))
        b_v1, b_v2 = st.slider("Zakres v", -20.0, 20.0, (-1.0, 1.0))
    else:
        b_cu = st.number_input("Środek u", -20.0, 20.0, 0.0)
        b_cv = st.number_input("Środek v", -20.0, 20.0, 0.0)
        b_r = st.number_input("Promień", 0.1, 10.0, 1.0)

    st.subheader("Zbiór C (dla Φ(C))")
    c_type = st.selectbox("Typ C", ["Prostokąt", "Koło"])
    if c_type == "Prostokąt":
        c_x1, c_x2 = st.slider("Zakres x", -10.0, 10.0, (-1.0, 1.0))
        c_y1, c_y2 = st.slider("Zakres y", -10.0, 10.0, (-1.0, 1.0))
    else:
        c_cx = st.number_input("Środek x", -10.0, 10.0, 0.0)
        c_cy = st.number_input("Środek y", -10.0, 10.0, 0.0)
        c_r = st.number_input("Promień C", 0.1, 10.0, 1.0)

def create_mask(X, Y, U, V):
    if b_type == "Prostokąt":
        return (U >= b_u1) & (U <= b_u2) & (V >= b_v1) & (V <= b_v2)
    else:
        return ((U - b_cu)**2 + (V - b_cv)**2) <= b_r**2

def create_c_mask(X, Y):
    if c_type == "Prostokąt":
        return (X >= c_x1) & (X <= c_x2) & (Y >= c_y1) & (Y <= c_y2)
    else:
        return ((X - c_cx)**2 + (Y - c_cy)**2) <= c_r**2

try:
    x, y = sp.symbols('x y')
    u_func = sp.lambdify((x, y), sp.sympify(u_expr), "numpy")
    v_func = sp.lambdify((x, y), sp.sympify(v_expr), "numpy")
    X, Y = np.meshgrid(np.linspace(xmin, xmax, resolution),
                       np.linspace(ymin, ymax, resolution))
    U = u_func(X, Y)
    V = v_func(X, Y)
    B_mask = create_mask(X, Y, U, V)
    C_mask = create_c_mask(X, Y)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    ax1.set_title("Przeciwobraz Φ⁻¹(B)")
    ax1.scatter(X[B_mask], Y[B_mask], c='red', s=10, alpha=0.5)
    ax1.set_xlim(xmin, xmax)
    ax1.set_ylim(ymin, ymax)
    ax1.set_aspect('equal')
    ax1.grid(True)

    ax2.set_title("Obraz Φ(C)")
    ax2.scatter(U[C_mask], V[C_mask], c='blue', s=10, alpha=0.5)
    ax2.set_aspect('equal')
    ax2.grid(True)

    ax3.set_title("Transformacja Φ")
    ax3.quiver(X, Y, U-X, V-Y, angles='xy', scale_units='xy', scale=1,
               color="green", alpha=0.4, width=0.002)
    ax3.set_xlim(xmin, xmax)
    ax3.set_ylim(ymin, ymax)
    ax3.set_aspect('equal')
    ax3.grid(True)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Błąd: {str(e)}")
