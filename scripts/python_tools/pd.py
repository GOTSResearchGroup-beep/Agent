import numpy as np

def calcular_amenaza_pd(perturbacion, direcciones_inseguras, distancias):
    """
    Calcula la amenaza PD de una perturbación dada.
    - perturbacion: array de numpy, la perturbación delta
    - direcciones_inseguras: lista de arrays normalizados u_i
    - distancias: lista de floats g(x, u_i)

    Retorna el valor de amenaza d_PD.
    """
    amenazas = []
    for u, g in zip(direcciones_inseguras, distancias):
        proyeccion = np.dot(perturbacion, u)  # Proyección escalar de δ sobre u
        amenaza = proyeccion / g
        amenazas.append(amenaza)
    return max(amenazas)

# Simulemos datos
np.random.seed(42)  # Para reproducibilidad
imagen = np.random.rand(5)  # "Imagen" en 5D
perturbacion = np.array([0.1, -0.05, 0.0, 0.02, 0.03])  # Perturbación pequeña

# Direcciones inseguras simuladas (normalizadas, como en el paper)
direcciones_inseguras = [
    np.array([1, 0, 0, 0, 0]),
    np.array([0, 1, 0, 0, 0]),
    np.array([0, 0, 1, 0, 0]),
    np.array([0, 0, 0, 1, 0]),
    np.array([0, 0, 0, 0, 1])
]

# Distancias g(x,u) simuladas (cuán lejos está el cambio de clase)
distancias = [0.2, 0.1, 0.3, 0.15, 0.25]

# Calculamos la amenaza PD
amenaza = calcular_amenaza_pd(perturbacion, direcciones_inseguras, distancias)

print("Amenaza PD:", amenaza)
print("Interpretación: Si >1, puede cambiar la clase; si <1, es segura en este modelo.")
