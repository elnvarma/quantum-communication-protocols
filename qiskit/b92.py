import random

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


print("=" * 50)
print("B92 QUANTUM KEY DISTRIBUTION")
print("=" * 50)

# Number of transmitted bits
NUM_BITS = 20

# Alice generates random bits
alice_bits = [random.randint(0, 1) for _ in range(NUM_BITS)]

print("\nAlice bits:")
print(alice_bits)

# Bob randomly chooses a measurement for every photon
#
# Measurement 0:
# Test for |1>  -> conclusive Alice bit 1
#
# Measurement 1:
# Test for |->  -> conclusive Alice bit 0

bob_measurements = [random.randint(0, 1) for _ in range(NUM_BITS)]

print("\nBob measurement choices:")
print(bob_measurements)

simulator = AerSimulator()

bob_results = []
alice_key = []
bob_key = []

print("\nRunning B92 transmission...")
print("-" * 50)

for i in range(NUM_BITS):

    alice_bit = alice_bits[i]
    measurement_choice = bob_measurements[i]

    qc = QuantumCircuit(1, 1)

    # ==========================================
    # ALICE ENCODING
    # ==========================================

    if alice_bit == 0:
        # Bit 0 -> |0>
        pass
    else:
        # Bit 1 -> |+>
        qc.h(0)

    # ==========================================
    # BOB MEASUREMENT
    # ==========================================

    if measurement_choice == 0:
        # Test for |1>
        #
        # Computational basis measurement.
        qc.measure(0, 0)

        conclusive_state = 1

    else:
        # Test for |->
        #
        # H changes:
        # |+> -> |0>
        # |-> -> |1>
        qc.h(0)
        qc.measure(0, 0)

        conclusive_state = 1

    # ==========================================
    # RUN CIRCUIT
    # ==========================================

    result = simulator.run(
        qc,
        shots=1
    ).result()

    counts = result.get_counts()
    measured_bit = int(next(iter(counts)))

    bob_results.append(measured_bit)

    # ==========================================
    # INTERPRET B92 RESULT
    # ==========================================

    if measurement_choice == 0:

        # Test for |1>
        #
        # If result = 1:
        # Alice cannot have sent |0>
        # Therefore Alice sent |+> -> bit 1

        if measured_bit == 1:
            alice_key.append(alice_bit)
            bob_key.append(1)

    else:

        # Test for |->
        #
        # If result = 1 after H:
        # Bob detected |->
        # Therefore Alice sent |0> -> bit 0

        if measured_bit == 1:
            alice_key.append(alice_bit)
            bob_key.append(0)


# ==============================================
# RESULTS
# ==============================================

print("\nBob measurement results:")
print(bob_results)

print("\nAlice raw key:")
print(alice_key)

print("\nBob raw key:")
print(bob_key)

print("\nKey length:")
print(len(alice_key))

# ==============================================
# VERIFY
# ==============================================

if alice_key == bob_key:
    print("\nSUCCESS!")
    print("Alice and Bob have the same raw key.")
else:
    print("\nERROR!")
    print("Alice and Bob keys do not match.")