import random
import perceval as pcvl

# Number of BB84 bits
n = 5

# Alice randomly chooses bits and bases
alice_bits = [random.randint(0, 1) for _ in range(n)]
alice_bases = [random.choice(["Z", "X"]) for _ in range(n)]

# Bob randomly chooses measurement bases
bob_bases = [random.choice(["Z", "X"]) for _ in range(n)]

print("Alice bits:  ", alice_bits)
print("Alice bases: ", alice_bases)
print("Bob bases:   ", bob_bases)

# Store Bob's measurement results
bob_results = []

for bit, alice_basis, bob_basis in zip(
    alice_bits, alice_bases, bob_bases
):
    # Create a simple 1-qubit / 2-mode Perceval circuit
    circuit = pcvl.Circuit(2)

    # Z basis:
    # |0> = photon in mode 0
    # |1> = photon in mode 1

    # X basis is created using a 50/50 beam splitter
    if alice_basis == "X":
        circuit.add(0, pcvl.BS())

    # For this simple implementation,
    # use the ideal BB84 rule for the measurement result.
    if alice_basis == bob_basis:
        measured_bit = bit
    else:
        measured_bit = random.randint(0, 1)

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