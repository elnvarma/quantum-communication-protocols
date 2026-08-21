import random
import perceval as pcvl

# Number of qubits
n = 20

# Alice randomly chooses bits and bases
alice_bits = [random.randint(0, 1) for _ in range(n)]
alice_bases = [random.choice(["Z", "X"]) for _ in range(n)]

# Eve randomly chooses measurement bases
eve_bases = [random.choice(["Z", "X"]) for _ in range(n)]

# Bob randomly chooses measurement bases
bob_bases = [random.choice(["Z", "X"]) for _ in range(n)]

eve_results = []
bob_results = []

# Alice -> Eve
for bit, alice_basis, eve_basis in zip(
    alice_bits, alice_bases, eve_bases
):
    # Create a simple photonic circuit
    circuit = pcvl.Circuit(2)

    # Alice prepares the state
    if bit == 1:
        state = pcvl.BasicState([0, 1])
    else:
        state = pcvl.BasicState([1, 0])

    # X basis uses a beam splitter
    if alice_basis == "X":
        circuit.add(0, pcvl.BS())

    # Eve measures
    # If Eve uses the same basis, she gets Alice's bit.
    # If she uses the wrong basis, the result is random.
    if alice_basis == eve_basis:
        eve_bit = bit
    else:
        eve_bit = random.randint(0, 1)

    eve_results.append(eve_bit)


# Eve -> Bob
for eve_bit, eve_basis, bob_basis in zip(
    eve_results, eve_bases, bob_bases
):
    # Create another photonic circuit
    circuit = pcvl.Circuit(2)

    # Eve resends her measured state
    if eve_bit == 1:
        state = pcvl.BasicState([0, 1])
    else:
        state = pcvl.BasicState([1, 0])

    # Eve's X-basis preparation
    if eve_basis == "X":
        circuit.add(0, pcvl.BS())

    # Bob measures
    if eve_basis == bob_basis:
        bob_bit = eve_bit
    else:
        bob_bit = random.randint(0, 1)

    bob_results.append(bob_bit)


# Sifting
alice_key = []
bob_key = []

for i in range(n):
    if alice_bases[i] == bob_bases[i]:
        alice_key.append(alice_bits[i])
        bob_key.append(bob_results[i])


# Display results
print("Alice bits:        ", alice_bits)
print("Alice bases:       ", alice_bases)
print("Eve bases:         ", eve_bases)
print("Bob bases:         ", bob_bases)
print("Eve results:       ", eve_results)
print("Bob results:       ", bob_results)

print()
print("Alice sifted key:  ", alice_key)
print("Bob sifted key:    ", bob_key)


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