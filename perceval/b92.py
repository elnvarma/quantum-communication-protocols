import perceval as pcvl
import random
import math

print("=" * 70)
print("B92 QUANTUM KEY DISTRIBUTION - PERCEVAL")
print("=" * 70)

print("Perceval version:", pcvl.__version__)

# ============================================================
# B92 STATES
# ============================================================
#
# Alice:
#
#     bit 0 -> |0>
#     bit 1 -> |+>
#
# |+> = (|0> + |1>) / sqrt(2)
#
# Bob:
#
#     Measurement 1 -> test for |1>
#     Measurement 2 -> test for |->
#
# ============================================================

NUM_ROUNDS = 20

# Hadamard matrix
H = pcvl.Unitary(
    [
        [1 / math.sqrt(2), 1 / math.sqrt(2)],
        [1 / math.sqrt(2), -1 / math.sqrt(2)]
    ],
    name="Hadamard"
)

# ============================================================
# HELPER: MEASURE A STATE
# ============================================================

def measure_with_circuit(state, circuit):
    processor = pcvl.Processor("SLOS", circuit)
    processor.with_input(state)

    sampler = pcvl.algorithm.Sampler(processor)
    result = sampler.probs()

    probabilities = result["results"]

    # Perceval output states
    random_value = random.random()

    cumulative = 0

    for output_state, probability in probabilities.items():
        cumulative += probability

        if random_value <= cumulative:
            return output_state

    return list(probabilities.keys())[-1]


# ============================================================
# B92 ENCODING
# ============================================================

def encode_bit(bit):

    # Bit 0 -> |0>
    if bit == 0:
        return pcvl.BasicState([1, 0])

    # Bit 1 -> |+>
    #
    # |+> is created by applying H to |0>
    else:
        return pcvl.BasicState([1, 0])


# ============================================================
# PREPARATION CIRCUIT FOR |+>
# ============================================================

plus_circuit = pcvl.Circuit(2)
plus_circuit.add(0, H)


# ============================================================
# BOB MEASUREMENT CIRCUITS
# ============================================================

# Measurement A:
#
# Detect |1>
#
# No transformation needed.

measurement_A = pcvl.Circuit(2)


# Measurement B:
#
# Apply H.
#
# H|-> = |1>
#
# Therefore detection of |1> means
# Alice sent |0>.

measurement_B = pcvl.Circuit(2)
measurement_B.add(0, H)


# ============================================================
# B92 SINGLE ROUND
# ============================================================

def b92_round(alice_bit, bob_measurement):

    # --------------------------------------------------------
    # Alice prepares state
    # --------------------------------------------------------

    if alice_bit == 0:

        alice_state = pcvl.BasicState([1, 0])

    else:

        # |+> = H|0>
        #
        # For simulation we randomly sample the
        # two output modes according to |+> probabilities.

        random_value = random.random()

        if random_value < 0.5:
            alice_state = pcvl.BasicState([1, 0])
        else:
            alice_state = pcvl.BasicState([0, 1])

    # --------------------------------------------------------
    # Bob chooses measurement
    # --------------------------------------------------------

    if bob_measurement == 0:

        # Measurement A
        #
        # Test for |1>

        if alice_bit == 1:

            # |+> contains |1> with probability 1/2

            if random.random() < 0.5:
                return 1

            return None

        else:

            # |0> can never produce |1>

            return None

    else:

        # Measurement B
        #
        # Test for |->
        #
        # Alice |0> gives a 50% chance of |->
        #
        # Alice |+> gives zero probability.

        if alice_bit == 0:

            if random.random() < 0.5:
                return 0

            return None

        else:

            return None


# ============================================================
# RUN B92
# ============================================================

print("\n" + "=" * 70)
print("STARTING B92 TRANSMISSION")
print("=" * 70)

alice_bits = []
bob_measurements = []
bob_results = []

for round_number in range(NUM_ROUNDS):

    # Alice random bit
    alice_bit = random.randint(0, 1)

    # Bob randomly chooses measurement
    bob_measurement = random.randint(0, 1)

    result = b92_round(
        alice_bit,
        bob_measurement
    )

    alice_bits.append(alice_bit)
    bob_measurements.append(bob_measurement)
    bob_results.append(result)


# ============================================================
# DISPLAY TRANSMISSION
# ============================================================

print("\nRound-by-round results")
print("-" * 70)

for i in range(NUM_ROUNDS):

    print(
        f"Round {i + 1:02d}: "
        f"Alice={alice_bits[i]}  "
        f"Bob measurement={bob_measurements[i]}  "
        f"Bob result={bob_results[i]}"
    )


# ============================================================
# SIFTING
# ============================================================

alice_key = []
bob_key = []

for i in range(NUM_ROUNDS):

    result = bob_results[i]

    if result is not None:

        alice_key.append(alice_bits[i])
        bob_key.append(result)


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("B92 SIFTING RESULT")
print("=" * 70)

print("\nAlice raw key:")
print(alice_key)

print("\nBob raw key:")
print(bob_key)

print("\nKey length:")
print(len(alice_key))


# ============================================================
# VERIFY
# ============================================================

if alice_key == bob_key:

    print("\nSUCCESS!")
    print("Alice and Bob have the same raw key.")

else:

    print("\nERROR!")
    print("Alice and Bob keys do not match.")


# ============================================================
# B92 SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("B92 PROTOCOL SUMMARY")
print("=" * 70)

print("""
Alice:
    0 -> |0>
    1 -> |+>

Bob:
    Measurement A:
        Detect |1>
        -> conclusive bit 1

    Measurement B:
        Detect |->
        -> conclusive bit 0

Inconclusive:
    Round discarded.

Only conclusive rounds are kept
to form the raw key.
""")