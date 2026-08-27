from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("QUANTUM BIT COMMITMENT - QISKIT")
print("=" * 60)

# Alice chooses a secret bit
secret_bit = 1

# Create one qubit
circuit = QuantumCircuit(1, 1)

# Encode the bit
if secret_bit == 1:
    circuit.x(0)

# Hide the state using Hadamard
circuit.h(0)

print("\nCommitment circuit:")
print(circuit)

# Reveal phase
circuit.h(0)

# Measure
circuit.measure(0, 0)

# Simulate
simulator = AerSimulator()

job = simulator.run(circuit, shots=1000)
result = job.result()

counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

print("\nSecret bit committed by Alice:", secret_bit)

print("\nInterpretation:")
print("Alice encodes a bit and applies a quantum transformation.")
print("The state is later transformed back and measured.")
print("This is an educational demonstration, not a secure")
print("cryptographic bit-commitment protocol.")