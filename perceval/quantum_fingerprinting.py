import perceval as pcvl


print("=" * 60)
print("QUANTUM FINGERPRINTING - PERCEVAL")
print("=" * 60)

# Alice and Bob's classical bits
alice_bit = 0
bob_bit = 1

# Encode each bit as a single-photon mode
alice_state = pcvl.BasicState([1, 0]) if alice_bit == 0 else pcvl.BasicState([0, 1])
bob_state = pcvl.BasicState([1, 0]) if bob_bit == 0 else pcvl.BasicState([0, 1])

print("\nAlice's encoded state:")
print(alice_state)

print("\nBob's encoded state:")
print(bob_state)

# Combine Alice and Bob's photonic states
combined_state = pcvl.BasicState(
    [alice_state[0], alice_state[1],
     bob_state[0], bob_state[1]]
)

print("\nCombined fingerprint state:")
print(combined_state)

# Interference circuit
circuit = pcvl.Circuit(4)
circuit // pcvl.BS()
circuit // (0, pcvl.BS())
circuit // (2, pcvl.BS())

print("\nPhotonic comparison circuit:")
print(circuit)

print("\nInterpretation:")
if alice_bit == bob_bit:
    print("Alice and Bob have matching classical inputs.")
else:
    print("Alice and Bob have different classical inputs.")

print("This is an educational photonic fingerprint comparison.")