import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


shots = 2000

simulator = AerSimulator()


# Measure a Bell pair using a specific angle
def run_measurement(alice_angle, bob_angle):

    qc = QuantumCircuit(2, 2)

    # Create Bell state
    qc.h(0)
    qc.cx(0, 1)

    # Alice's measurement rotation
    qc.ry(-2 * alice_angle, 0)

    # Bob's measurement rotation
    qc.ry(-2 * bob_angle, 1)

    # Measure
    qc.measure(0, 0)
    qc.measure(1, 1)

    result = simulator.run(
        qc,
        shots=shots
    ).result()

    return result.get_counts()


# Calculate correlation
def correlation(counts):

    total = sum(counts.values())

    same = 0
    different = 0

    for state, count in counts.items():

        if state[0] == state[1]:
            same += count
        else:
            different += count

    return (same - different) / total


# Measurement angles
A0 = 0
A1 = math.pi / 4

B0 = math.pi / 8
B1 = -math.pi / 8


# Calculate correlations
E_A0B0 = correlation(run_measurement(A0, B0))
E_A0B1 = correlation(run_measurement(A0, B1))
E_A1B0 = correlation(run_measurement(A1, B0))
E_A1B1 = correlation(run_measurement(A1, B1))


print("E(A0,B0) =", E_A0B0)
print("E(A0,B1) =", E_A0B1)
print("E(A1,B0) =", E_A1B0)
print("E(A1,B1) =", E_A1B1)


# CHSH calculation
S = abs(
    E_A0B0
    + E_A0B1
    + E_A1B0
    - E_A1B1
)


print()
print("CHSH value =", S)

print()
print("Classical limit =", 2)
print("Quantum maximum =", 2 * math.sqrt(2))


if S > 2:
    print("Bell inequality violated!")
    print("E91 quantum correlation verified.")
else:
    print("No Bell inequality violation.") 