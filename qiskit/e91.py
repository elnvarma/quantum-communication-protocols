from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import math


# ============================================================
# E91 PHYSICAL QUANTUM CIRCUIT
# ============================================================

def run_measurement(alice_angle, bob_angle, shots=2000):
    """
    Create an entangled Bell pair and measure Alice and Bob
    using the requested measurement angles.
    """

    qc = QuantumCircuit(2, 2)

    # --------------------------------------------------------
    # Create Bell state
    # |Phi+> = (|00> + |11>) / sqrt(2)
    # --------------------------------------------------------

    qc.h(0)
    qc.cx(0, 1)

    # --------------------------------------------------------
    # Rotate measurement basis
    # Ry(-theta) changes the measurement basis
    # --------------------------------------------------------

    qc.ry(-2 * alice_angle, 0)
    qc.ry(-2 * bob_angle, 1)

    # --------------------------------------------------------
    # Measure
    # --------------------------------------------------------

    qc.measure(0, 0)
    qc.measure(1, 1)

    # --------------------------------------------------------
    # Run simulator
    # --------------------------------------------------------

    simulator = AerSimulator()

    compiled = transpile(qc, simulator)

    result = simulator.run(
        compiled,
        shots=shots
    ).result()

    counts = result.get_counts()

    return counts


# ============================================================
# CALCULATE CORRELATION
# ============================================================

def calculate_correlation(counts):
    """
    E = P(00) + P(11) - P(01) - P(10)
    """

    total = sum(counts.values())

    correlation = 0

    for state, count in counts.items():

        probability = count / total

        if state in ["00", "11"]:
            correlation += probability

        elif state in ["01", "10"]:
            correlation -= probability

    return correlation


# ============================================================
# RUN ONE E91 MEASUREMENT
# ============================================================

def run_e91_measurement(name, alice_angle, bob_angle):

    counts = run_measurement(
        alice_angle,
        bob_angle
    )

    correlation = calculate_correlation(counts)

    print()
    print(name)
    print("Alice angle:", alice_angle)
    print("Bob angle:  ", bob_angle)
    print("Counts:     ", counts)
    print("Correlation:", round(correlation, 4))

    return correlation


# ============================================================
# E91 MEASUREMENT SETTINGS
# ============================================================

# Alice settings
A0 = 0
A1 = math.pi / 4

# Bob settings
B0 = math.pi / 8
B1 = -math.pi / 8


# ============================================================
# FOUR CORRELATION MEASUREMENTS
# ============================================================

E_A0_B0 = run_e91_measurement(
    "E(A0,B0)",
    A0,
    B0
)

E_A0_B1 = run_e91_measurement(
    "E(A0,B1)",
    A0,
    B1
)

E_A1_B0 = run_e91_measurement(
    "E(A1,B0)",
    A1,
    B0
)

E_A1_B1 = run_e91_measurement(
    "E(A1,B1)",
    A1,
    B1
)


# ============================================================
# CHSH CALCULATION
# ============================================================

S = abs(
    E_A0_B0
    + E_A0_B1
    + E_A1_B0
    - E_A1_B1
)


print()
print("=" * 50)
print("E91 CHSH RESULT")
print("=" * 50)

print("E(A0,B0) =", round(E_A0_B0, 4))
print("E(A0,B1) =", round(E_A0_B1, 4))
print("E(A1,B0) =", round(E_A1_B0, 4))
print("E(A1,B1) =", round(E_A1_B1, 4))

print()
print("CHSH value =", round(S, 4))

print()
print("Classical limit =", 2)
print("Quantum maximum =", 2 * math.sqrt(2))

if S > 2:
    print("Bell inequality violated!")
    print("E91 quantum correlation verified.")
else:
    print("No Bell inequality violation.")