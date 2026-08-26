from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("QUANTUM SECRET SHARING - QISKIT")
print("=" * 60)

# Create a 3-qubit circuit
secret = QuantumCircuit(3, 3)

# Create a three-qubit GHZ state
secret.h(0)
secret.cx(0, 1)
secret.cx(0, 2)

print("\nGHZ-state circuit:")
print(secret)

# Measure all three qubits
secret.measure([0, 1, 2], [0, 1, 2])

# Run simulation
simulator = AerSimulator()

job = simulator.run(secret, shots=1000)
result = job.result()

counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

print("\nInterpretation:")
print("The GHZ state produces strongly correlated outcomes.")
print("The expected dominant outcomes are 000 and 111.")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("QUANTUM SECRET SHARING - QISKIT")
print("=" * 60)

# Create a 3-qubit circuit
secret = QuantumCircuit(3, 3)

# Create a three-qubit GHZ state
secret.h(0)
secret.cx(0, 1)
secret.cx(0, 2)

print("\nGHZ-state circuit:")
print(secret)

# Measure all three qubits
secret.measure([0, 1, 2], [0, 1, 2])

# Run simulation
simulator = AerSimulator()

job = simulator.run(secret, shots=1000)
result = job.result()

counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

print("\nInterpretation:")
print("The GHZ state produces strongly correlated outcomes.")
print("The expected dominant outcomes are 000 and 111.")