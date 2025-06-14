
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from matplotlib.patches import Rectangle, Circle

st.set_page_config(layout="wide")
st.title("Wizualizacja odwzorowania Φ: ℝ² → ℝ²")

with st.expander("📄 Dokumentacja i ograniczenia"):
    st.markdown("""
    ## 📘 Instrukcja obsługi aplikacji

    Aplikacja służy do wizualizacji działania odwzorowania **Φ: ℝ² → ℝ²** (czyli funkcji, która przekształca punkty płaszczyzny w inne punkty płaszczyzny). Umożliwia:

    - Obliczenie **przeciwobrazu zbioru B**, czyli pokazanie, które punkty (x, y) zostaną przekształcone przez Φ do wnętrza zbioru B.
    - Obliczenie **obrazu zbioru C**, czyli pokazanie, gdzie trafi zbiór C po przekształceniu Φ.

    ### 🔧 Krok po kroku

    1. **Zdefiniuj funkcję Φ(x, y)**:
        - Wpisz wyrażenia dla:
            - `u(x, y)` – współrzędnej x obrazu
            - `v(x, y)` – współrzędnej y obrazu
        - Przykład: `u = x**2 - y**2`, `v = 2*x*y` (czyli przekształcenie do współrzędnych biegunowych)

    2. **Określ zbiór B** *(obszar docelowy w przestrzeni obrazu)*:
        - Do wyboru masz: prostokąt lub koło.
        - Dla prostokąta podajesz zakresy `u` i `v`
        - Dla koła: środek i promień

    3. **Określ zbiór C** *(obszar w przestrzeni wejściowej przed przekształceniem)*:
        - Tak samo: prostokąt lub koło

    4. **Ustaw parametry siatki**:
        - Zakresy osi x i y oraz rozdzielczość
        - Im wyższa rozdzielczość, tym dokładniejsze wyniki (ale może być wolniejsze)

    5. **Zobacz wyniki**:
        - Wykres 1: Przeciwobraz Φ⁻¹(B) – punkty w (x, y), które po Φ trafiają do B
        - Wykres 2: Obraz Φ(C) – punkty (u, v) po przekształceniu C
        - Wykres 3: Wektory przekształcenia Φ w całym obszarze

    ## ⚠️ Ograniczenia techniczne

    - **Typ funkcji Φ**:
        - Musi być podana w postaci jawnej, jako dwie wyrażenia w zmiennych `x` i `y`
        - Dozwolone są tylko funkcje obsługiwane przez bibliotekę `SymPy` (np. `sin(x)`, `cos(x)`, `x**2`)
        - Funkcja powinna być ciągła i najlepiej różniczkowalna

    - **Rodzaje zbiorów**:
        - Obsługiwane są tylko:
            - prostokąty (określone zakresem)
            - koła (określone środkiem i promieniem)
        - Na razie nie można wprowadzać zbiorów ogólnych ani wielokątów ręcznie

    - **Wydajność**:
        - Im większa rozdzielczość siatki, tym lepsza jakość, ale wolniejsze działanie
        - Dla złożonych funkcji zaleca się ograniczyć zakres do np. [-3, 3] i rozdzielczość 50–100

    - **Wyniki przybliżone**:
        - Obliczenia bazują na punktach z siatki – to **metoda przybliżona**
        - Dokładność zależy od rozdzielczości siatki i zakresu

    ## 🧪 Przykłady do testowania

    ### 1. Transformacja liniowa
    Φ(x, y) = (2x + y, −x + 3y)

    - Zbiór B: Koło (0, 0), promień 2
    - Zbiór C: Prostokąt [−1, 1] × [−1, 1]

    ### 2. Transformacja nieliniowa (do układu biegunowego)
    Φ(x, y) = (x² − y², 2xy)

    - Zbiór B: Prostokąt [0, 4] × [−2, 2]
    - Zbiór C: Koło o środku (1, 0), promień 1
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

    ax3.set_title("Pole wektorowe Φ")
    ax3.quiver(X, Y, U-X, V-Y, angles='xy', scale_units='xy', scale=1,
               color="green", alpha=0.4, width=0.002)
    ax3.set_xlim(xmin, xmax)
    ax3.set_ylim(ymin, ymax)
    ax3.set_aspect('equal')
    ax3.grid(True)

    st.pyplot(fig)

except Exception as e:
    st.error(f"Błąd: {str(e)}")
