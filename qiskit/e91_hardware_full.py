import math

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


# ============================================================
# IBM QUANTUM CONNECTION
# ============================================================

service = QiskitRuntimeService()

backend = service.backend("ibm_fez")

print("Using IBM Quantum backend:", backend.name)


# ============================================================
# RUN ONE E91 MEASUREMENT
# ============================================================

def run_measurement(alice_angle, bob_angle, shots=1024):

    qc = QuantumCircuit(2)

    # Create Bell state
    qc.h(0)
    qc.cx(0, 1)

    # Alice measurement basis
    qc.ry(-2 * alice_angle, 0)

    # Bob measurement basis
    qc.ry(-2 * bob_angle, 1)

    # Measurement
    qc.measure_all()

    # Compile for real IBM hardware
    compiled = transpile(
        qc,
        backend=backend,
        optimization_level=1
    )

    # Run
    sampler = Sampler(backend)

    job = sampler.run(
        [compiled],
        shots=shots
    )

    print()
    print("Job submitted")
    print("Job ID:", job.job_id())

    result = job.result()

    # Extract BitArray
    bit_array = result[0].data.meas

    # Convert to counts
    counts = bit_array.get_counts()

    return counts


# ============================================================
# CALCULATE CORRELATION
# ============================================================

def calculate_correlation(counts):

    total = sum(counts.values())

    correlation = (
        counts.get("00", 0)
        + counts.get("11", 0)
        - counts.get("01", 0)
        - counts.get("10", 0)
    ) / total

    return correlation


# ============================================================
# E91 SETTINGS
# ============================================================

A0 = 0
A1 = math.pi / 4

B0 = math.pi / 8
B1 = -math.pi / 8


# ============================================================
# RUN FOUR MEASUREMENTS
# ============================================================

print()
print("=" * 60)
print("E91 REAL IBM HARDWARE EXPERIMENT")
print("=" * 60)


print()
print("Running E(A0,B0)...")

counts_A0_B0 = run_measurement(A0, B0)

E_A0_B0 = calculate_correlation(counts_A0_B0)

print("Counts:", counts_A0_B0)
print("E(A0,B0) =", round(E_A0_B0, 4))


print()
print("Running E(A0,B1)...")

counts_A0_B1 = run_measurement(A0, B1)

E_A0_B1 = calculate_correlation(counts_A0_B1)

print("Counts:", counts_A0_B1)
print("E(A0,B1) =", round(E_A0_B1, 4))


print()
print("Running E(A1,B0)...")

counts_A1_B0 = run_measurement(A1, B0)

E_A1_B0 = calculate_correlation(counts_A1_B0)

print("Counts:", counts_A1_B0)
print("E(A1,B0) =", round(E_A1_B0, 4))


print()
print("Running E(A1,B1)...")

counts_A1_B1 = run_measurement(A1, B1)

E_A1_B1 = calculate_correlation(counts_A1_B1)

print("Counts:", counts_A1_B1)
print("E(A1,B1) =", round(E_A1_B1, 4))


# ============================================================
# CHSH
# ============================================================

S = abs(
    E_A0_B0
    + E_A0_B1
    + E_A1_B0
    - E_A1_B1
)


print()
print("=" * 60)
print("E91 CHSH RESULT — REAL IBM HARDWARE")
print("=" * 60)

print("E(A0,B0) =", round(E_A0_B0, 4))
print("E(A0,B1) =", round(E_A0_B1, 4))
print("E(A1,B0) =", round(E_A1_B0, 4))
print("E(A1,B1) =", round(E_A1_B1, 4))

print()
print("CHSH value =", round(S, 4))

print("Classical limit =", 2)
print("Quantum maximum =", round(2 * math.sqrt(2), 4))

if S > 2:
    print()
    print("Bell inequality violated!")
    print("E91 quantum correlation observed on IBM hardware.")
else:
    print()
    print("No Bell inequality violation.")
    print("Hardware noise may have prevented the violation.")