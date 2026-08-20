from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Quantum Teleportation
qc = QuantumCircuit(3, 3)

# Prepare the state to teleport: |1>
qc.x(0)

# Create Bell pair between q1 and q2
qc.h(1)
qc.cx(1, 2)

# Bell measurement
qc.cx(0, 1)
qc.h(0)

# Measure Alice's two qubits
qc.measure(0, 0)
qc.measure(1, 1)

# Classical corrections on Bob's qubit
with qc.if_test((qc.clbits[1], True)):
    qc.x(2)

with qc.if_test((qc.clbits[0], True)):
    qc.z(2)

# Measure Bob's qubit
qc.measure(2, 2)

print(qc)

# Simulate
simulator = AerSimulator()
result = simulator.run(qc, shots=1024).result()

print("\nTeleportation results:")
print(result.get_counts())
