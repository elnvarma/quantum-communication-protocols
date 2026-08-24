from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler


# ==========================================
# CONNECT TO IBM QUANTUM
# ==========================================

service = QiskitRuntimeService()

backend = service.backend("ibm_fez")

print("Using backend:", backend.name)


# ==========================================
# CREATE E91 BELL STATE
# ==========================================

qc = QuantumCircuit(2)

qc.h(0)
qc.cx(0, 1)

qc.measure_all()

print()
print("E91 hardware test circuit:")
print(qc)


# ==========================================
# TRANSPILE
# ==========================================

compiled = transpile(
    qc,
    backend=backend,
    optimization_level=1
)


# ==========================================
# RUN ON REAL HARDWARE
# ==========================================

sampler = Sampler(backend)

job = sampler.run(
    [compiled],
    shots=1024
)

print()
print("Job submitted successfully.")
print("Job ID:", job.job_id())


# ==========================================
# GET HARDWARE RESULT
# ==========================================

result = job.result()

pub_result = result[0]

# Extract measurement data
bit_array = pub_result.data.meas

# Convert to counts
counts = bit_array.get_counts()

print()
print("Hardware counts:")
print(counts)


# ==========================================
# CHECK TOTAL SHOTS
# ==========================================

total = sum(counts.values())

print()
print("Total shots:", total)