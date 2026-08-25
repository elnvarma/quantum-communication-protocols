import random

print("=" * 70)
print("B92 QUANTUM KEY DISTRIBUTION - EAVESDROPPING TEST")
print("=" * 70)

NUM_ROUNDS = 50

# ============================================================
# B92 ROUND WITH EVE
# ============================================================

def b92_round_with_eve(alice_bit):

    # --------------------------------------------------------
    # Alice
    #
    # 0 -> |0>
    # 1 -> |+>
    # --------------------------------------------------------

    # Eve chooses a random measurement
    eve_measurement = random.randint(0, 1)

    # --------------------------------------------------------
    # Eve intercepts the state
    # --------------------------------------------------------

    if eve_measurement == 0:

        # Eve tests for |1>
        #
        # Conclusive result means Alice likely sent bit 1.

        if alice_bit == 1 and random.random() < 0.5:

            eve_bit = 1

        else:

            eve_bit = None

    else:

        # Eve tests for |->
        #
        # Conclusive result means Alice likely sent bit 0.

        if alice_bit == 0 and random.random() < 0.5:

            eve_bit = 0

        else:

            eve_bit = None

    # --------------------------------------------------------
    # Eve resends a state
    # --------------------------------------------------------

    if eve_bit is None:

        # Eve has no conclusive information.
        # Bob receives a random B92 state.

        resent_bit = random.randint(0, 1)

    else:

        resent_bit = eve_bit

    # --------------------------------------------------------
    # Bob chooses a random measurement
    # --------------------------------------------------------

    bob_measurement = random.randint(0, 1)

    # --------------------------------------------------------
    # Bob measurement
    # --------------------------------------------------------

    if bob_measurement == 0:

        # Test for |1>
        #
        # Conclusive bit 1.

        if resent_bit == 1 and random.random() < 0.5:

            bob_bit = 1

        else:

            bob_bit = None

    else:

        # Test for |->
        #
        # Conclusive bit 0.

        if resent_bit == 0 and random.random() < 0.5:

            bob_bit = 0

        else:

            bob_bit = None

    return bob_bit, eve_measurement


# ============================================================
# TRANSMISSION
# ============================================================

alice_key = []
bob_key = []

eve_choices = []

print("\nStarting transmission...")
print("-" * 70)

for round_number in range(NUM_ROUNDS):

    alice_bit = random.randint(0, 1)

    bob_bit, eve_measurement = b92_round_with_eve(alice_bit)

    eve_choices.append(eve_measurement)

    if bob_bit is not None:

        alice_key.append(alice_bit)
        bob_key.append(bob_bit)

        print(
            f"Round {round_number + 1:02d}: "
            f"Alice={alice_bit} "
            f"Bob={bob_bit} "
            f"Eve measurement={eve_measurement}"
        )


# ============================================================
# QBER
# ============================================================

errors = 0

for alice_bit, bob_bit in zip(alice_key, bob_key):

    if alice_bit != bob_bit:

        errors += 1


if len(alice_key) > 0:

    qber = errors / len(alice_key)

else:

    qber = 0


# ============================================================
# RESULTS
# ============================================================

print("\n" + "=" * 70)
print("B92 EAVESDROPPING RESULT")
print("=" * 70)

print("\nAlice raw key:")
print(alice_key)

print("\nBob raw key:")
print(bob_key)

print("\nRaw key length:")
print(len(alice_key))

print("\nErrors:")
print(errors)

print("\nQBER:")
print(qber)

print("\nQBER percentage:")
print(round(qber * 100, 2), "%")


# ============================================================
# SECURITY DECISION
# ============================================================

print("\n" + "=" * 70)

if qber > 0:

    print("Eavesdropping detected!")
    print("Eve introduced errors into the raw key.")

else:

    print("No errors detected.")

print("=" * 70)