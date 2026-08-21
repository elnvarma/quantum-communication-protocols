import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Number of qubits
n = 20

# Alice randomly chooses bits and bases
alice_bits = [random.randint(0, 1) for _ in range(n)]
alice_bases = [random.choice(["Z", "X"]) for _ in range(n)]

# Eve randomly chooses measurement bases
eve_bases = [random.choice(["Z", "X"]) for _ in range(n)]

# Bob randomly chooses measurement bases
bob_bases = [random.choice(["Z", "X"]) for _ in range(n)]

simulator = AerSimulator()

eve_results = []
bob_results = []

# Alice -> Eve
for bit, alice_basis, eve_basis in zip(
    alice_bits, alice_bases, eve_bases
):
    qc = QuantumCircuit(1, 1)

    # Alice prepares the qubit
    if bit == 1:
        qc.x(0)

    if alice_basis == "X":
        qc.h(0)

    # Eve measures
    if eve_basis == "X":
        qc.h(0)

    qc.measure(0, 0)

    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()
    eve_bit = int(list(counts.keys())[0])

    eve_results.append(eve_bit)

# Eve -> Bob
for eve_bit, eve_basis, bob_basis in zip(
    eve_results, eve_bases, bob_bases
):
    qc = QuantumCircuit(1, 1)

    # Eve prepares the measured state
    if eve_bit == 1:
        qc.x(0)

    if eve_basis == "X":
        qc.h(0)

    # Bob measures
    if bob_basis == "X":
        qc.h(0)

    qc.measure(0, 0)

    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()
    bob_bit = int(list(counts.keys())[0])

    bob_results.append(bob_bit)

# Sifting
alice_key = []
bob_key = []

for i in range(n):
    if alice_bases[i] == bob_bases[i]:
        alice_key.append(alice_bits[i])
        bob_key.append(bob_results[i])

print("Alice bits:       ", alice_bits)
print("Alice bases:      ", alice_bases)
print("Eve bases:        ", eve_bases)
print("Bob bases:        ", bob_bases)
print("Eve results:      ", eve_results)
print("Bob results:      ", bob_results)

print()
print("Alice sifted key: ", alice_key)
print("Bob sifted key:   ", bob_key)

# Calculate QBER
if len(alice_key) > 0:
    errors = sum(
        a != b for a, b in zip(alice_key, bob_key)
    )

    qber = errors / len(alice_key)

    print()
    print("Errors: ", errors)
    print("QBER:   ", qber)

    if qber > 0.11:
        print("EAVESDROPPING DETECTED!")
    else:
        print("No significant eavesdropping detected.")
else:
    print("No matching bases. No key generated.")