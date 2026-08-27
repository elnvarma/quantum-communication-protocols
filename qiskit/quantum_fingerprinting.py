from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("QUANTUM FINGERPRINTING - QISKIT")
print("=" * 60)

# Alice and Bob's classical bits
alice_bit = 0
bob_bit = 1

# Create a two-qubit comparison circuit
fingerprint = QuantumCircuit(2, 1)

# Encode Alice's bit
if alice_bit == 1:
    fingerprint.x(0)

# Encode Bob's bit
if bob_bit == 1:
    fingerprint.x(1)

# Compare using CNOT
fingerprint.cx(0, 1)

# Measure comparison qubit
fingerprint.measure(1, 0)

print("\nFingerprint comparison circuit:")
print(fingerprint)

simulator = AerSimulator()

job = simulator.run(fingerprint, shots=1000)
result = job.result()

counts = result.get_counts()

print("\nMeasurement results:")
print(counts)

print("\nAlice's bit:", alice_bit)
print("Bob's bit:", bob_bit)

if counts.get('0', 0) > counts.get('1', 0):
    print("\nResult: The fingerprints match.")
else:
    print("\nResult: The fingerprints differ.")

print("\nInterpretation:")
print("The circuit compares information encoded by Alice and Bob.")
print("A 0 measurement indicates matching encoded bits.")
print("A 1 measurement indicates different encoded bits.")
print("This is an educational demonstration of quantum fingerprint comparison.")