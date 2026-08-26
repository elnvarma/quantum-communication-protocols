from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("QUANTUM COIN TOSSING - QISKIT")
print("=" * 60)

# Create a one-qubit circuit
coin = QuantumCircuit(1, 1)

# Hadamard gate creates an equal superposition
coin.h(0)

# Measure the quantum coin
coin.measure(0, 0)

print("\nQuantum coin circuit:")
print(coin)

# Run simulation
simulator = AerSimulator()

job = simulator.run(coin, shots=1000)
result = job.result()

counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

# Calculate percentages
total = sum(counts.values())

print("\nProbabilities:")
for bit, count in sorted(counts.items()):
    percentage = count / total * 100
    print(f"{bit}: {percentage:.2f}%")

print("\nInterpretation:")
print("The Hadamard gate creates an equal superposition.")
print("Measurement produces approximately 50% 0 and 50% 1.")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("QUANTUM COIN TOSSING - QISKIT")
print("=" * 60)

# Create a one-qubit circuit
coin = QuantumCircuit(1, 1)

# Hadamard gate creates an equal superposition
coin.h(0)

# Measure the quantum coin
coin.measure(0, 0)

print("\nQuantum coin circuit:")
print(coin)

# Run simulation
simulator = AerSimulator()

job = simulator.run(coin, shots=1000)
result = job.result()

counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

# Calculate percentages
total = sum(counts.values())

print("\nProbabilities:")
for bit, count in sorted(counts.items()):
    percentage = count / total * 100
    print(f"{bit}: {percentage:.2f}%")

print("\nInterpretation:")
print("The Hadamard gate creates an equal superposition.")
print("Measurement produces approximately 50% 0 and 50% 1.")