import math
import random


# Number of measurements
shots = 2000


# Create an entangled Bell pair
def bell_pair():
    return random.choice([
        (0, 0),
        (1, 1)
    ])


# Simulate measurement correlation
def run_measurement(alice_angle, bob_angle):

    results = []

    for _ in range(shots):

        alice_bit, bob_bit = bell_pair()

        # Quantum correlation for |Phi+>
        correlation = math.cos(
            2 * (alice_angle - bob_angle)
        )

        # Convert correlation to probability
        probability_same = (1 + correlation) / 2

        # Decide whether results are same
        if random.random() < probability_same:
            bob_result = alice_bit
        else:
            bob_result = 1 - alice_bit

        results.append((alice_bit, bob_result))

    return results


# Calculate correlation E
def calculate_correlation(results):

    same = 0
    different = 0

    for alice, bob in results:

        if alice == bob:
            same += 1
        else:
            different += 1

    return (same - different) / len(results)


# E91 / CHSH measurement settings
A0 = 0
A1 = math.pi / 4

B0 = math.pi / 8
B1 = -math.pi / 8


# Calculate four correlations
E_A0B0 = calculate_correlation(
    run_measurement(A0, B0)
)

E_A0B1 = calculate_correlation(
    run_measurement(A0, B1)
)

E_A1B0 = calculate_correlation(
    run_measurement(A1, B0)
)

E_A1B1 = calculate_correlation(
    run_measurement(A1, B1)
)


print("E(A0,B0) =", E_A0B0)
print("E(A0,B1) =", E_A0B1)
print("E(A1,B0) =", E_A1B0)
print("E(A1,B1) =", E_A1B1)


# CHSH value
S = abs(
    E_A0B0
    + E_A0B1
    + E_A1B0
    - E_A1B1
)


print()
print("CHSH value =", S)

print()
print("Classical limit =", 2)
print("Quantum maximum =", 2 * math.sqrt(2))


if S > 2:
    print("Bell inequality violated!")
    print("E91 quantum correlation verified.")
else:
    print("No Bell inequality violation.")