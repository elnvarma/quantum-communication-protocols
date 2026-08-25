import random

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 60)
print("B92 QUANTUM KEY DISTRIBUTION - EAVESDROPPING TEST")
print("=" * 60)

NUM_BITS = 50

simulator = AerSimulator()

# -------------------------------------------------
# ALICE
# -------------------------------------------------

alice_bits = [random.randint(0, 1) for _ in range(NUM_BITS)]

print("\nAlice bits:")
print(alice_bits)


# -------------------------------------------------
# BOB'S RANDOM MEASUREMENT CHOICES
# -------------------------------------------------

bob_choices = [random.randint(0, 1) for _ in range(NUM_BITS)]

print("\nBob measurement choices:")
print(bob_choices)


# -------------------------------------------------
# EVE'S RANDOM MEASUREMENT CHOICES
# -------------------------------------------------

eve_choices = [random.randint(0, 1) for _ in range(NUM_BITS)]

print("\nEve measurement choices:")
print(eve_choices)


# -------------------------------------------------
# STORAGE
# -------------------------------------------------

alice_key = []
bob_key = []

print("\nStarting transmission...")
print("-" * 60)


# -------------------------------------------------
# TRANSMISSION
# -------------------------------------------------

for i in range(NUM_BITS):

    alice_bit = alice_bits[i]

    # =============================================
    # ALICE ENCODING
    # =============================================

    alice_circuit = QuantumCircuit(1, 1)

    if alice_bit == 0:
        # 0 -> |0>
        pass
    else:
        # 1 -> |+>
        alice_circuit.h(0)

    # =============================================
    # EVE INTERCEPTS
    # =============================================

    eve_choice = eve_choices[i]

    # Eve measures the incoming state.
    eve_circuit = QuantumCircuit(1, 1)

    if eve_choice == 0:

        # Eve tests computational basis |0>, |1>
        eve_circuit.measure(0, 0)

        eve_measurement = 0

    else:

        # Eve tests |+>, |->
        eve_circuit.h(0)
        eve_circuit.measure(0, 0)

        eve_measurement = 1

    # We need a simple simulated Eve outcome.
    eve_result = simulator.run(
        eve_circuit,
        shots=1
    ).result()

    eve_counts = eve_result.get_counts()
    eve_bit = int(next(iter(eve_counts)))

    # =============================================
    # EVE RESENDS A STATE
    # =============================================

    resend_circuit = QuantumCircuit(1, 1)

    if eve_choice == 0:

        # Eve measured computational basis.
        if eve_bit == 0:
            # Resend |0>
            pass
        else:
            # Resend |1>
            resend_circuit.x(0)

    else:

        # Eve measured |+>, |->
        if eve_bit == 0:
            # Resend |+>
            resend_circuit.h(0)
        else:
            # Resend |->
            resend_circuit.x(0)
            resend_circuit.h(0)

    # =============================================
    # BOB RECEIVES EVE'S RESENT STATE
    # =============================================

    bob_choice = bob_choices[i]

    if bob_choice == 0:

        # Bob tests for |1>
        resend_circuit.measure(0, 0)

    else:

        # Bob tests for |->
        resend_circuit.h(0)
        resend_circuit.measure(0, 0)

    bob_result = simulator.run(
        resend_circuit,
        shots=1
    ).result()

    bob_counts = bob_result.get_counts()
    bob_bit = int(next(iter(bob_counts)))

    # =============================================
    # B92 INTERPRETATION
    # =============================================

    if bob_bit == 1:

        if bob_choice == 0:

            # Bob detected |1>
            # Conclusive -> Alice bit 1
            alice_key.append(alice_bit)
            bob_key.append(1)

        else:

            # Bob detected |->
            # Conclusive -> Alice bit 0
            alice_key.append(alice_bit)
            bob_key.append(0)


# -------------------------------------------------
# RESULTS
# -------------------------------------------------

print("\nAlice raw key:")
print(alice_key)

print("\nBob raw key:")
print(bob_key)

print("\nRaw key length:")
print(len(alice_key))


# -------------------------------------------------
# COMPARE KEYS
# -------------------------------------------------

if len(alice_key) == 0:

    print("\nNo conclusive results.")

else:

    errors = 0

    for a, b in zip(alice_key, bob_key):

        if a != b:
            errors += 1

    qber = errors / len(alice_key)

    print("\nErrors:")
    print(errors)

    print("\nQBER:")
    print(qber)

    print("\nQBER percentage:")
    print(round(qber * 100, 2), "%")


# -------------------------------------------------
# FINAL RESULT
# -------------------------------------------------

print("\n" + "=" * 60)
print("B92 EAVESDROPPING RESULT")
print("=" * 60)

if len(alice_key) > 0 and qber > 0:

    print("Eavesdropping detected!")
    print("Eve introduced errors into the raw key.")

else:

    print("No errors detected in this run.")