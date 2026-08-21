import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Number of qubits
n = 5

# Alice randomly chooses bits and bases
alice_bits = [random.randint(0, 1) for _ in range(n)]
alice_bases = [random.choice(["Z", "X"]) for _ in range(n)]

# Bob randomly chooses measurement bases
bob_bases = [random.choice(["Z", "X"]) for _ in range(n)]

print("Alice bits:  ", alice_bits)
print("Alice bases: ", alice_bases)
print("Bob bases:   ", bob_bases)

simulator = AerSimulator()

bob_results = []

for bit, alice_basis, bob_basis in zip(
    alice_bits, alice_bases, bob_bases
):
    qc = QuantumCircuit(1, 1)

    # Alice prepares the qubit
    if bit == 1:
        qc.x(0)

    # Alice uses X basis
    if alice_basis == "X":
        qc.h(0)

    # Bob measures in his chosen basis
    if bob_basis == "X":
        qc.h(0)

    qc.measure(0, 0)

    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts()

    measured_bit = int(list(counts.keys())[0])
    bob_results.append(measured_bit)

print("Bob results: ", bob_results)

# Sifting
alice_key = []
bob_key = []

for i in range(n):
    if alice_bases[i] == bob_bases[i]:
        alice_key.append(alice_bits[i])
        bob_key.append(bob_results[i])

print("Alice sifted key:", alice_key)
print("Bob sifted key:  ", bob_key)

# Verification
if alice_key == bob_key:
    print("BB84 verification: SUCCESS")
else:
    print("BB84 verification: FAILED")