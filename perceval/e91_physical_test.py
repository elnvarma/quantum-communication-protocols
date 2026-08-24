import perceval as pcvl
import math

print("Perceval version:", pcvl.__version__)


# ==========================================
# 1. CREATE ENTANGLED TWO-PHOTON STATE
# ==========================================

state1 = pcvl.BasicState([1, 0, 0, 1])
state2 = pcvl.BasicState([0, 1, 1, 0])

entangled_state = pcvl.StateVector()
entangled_state += state1
entangled_state += state2

print()
print("Entangled state:")
print(entangled_state)


# ==========================================
# 2. ALICE MEASUREMENT BLOCK
# ==========================================

alice = pcvl.Circuit(2)

# Alice measurement setting
alice.add(0, pcvl.PS(phi=math.pi / 4))

# Beam splitter
alice.add((0, 1), pcvl.BS())


# ==========================================
# 3. BOB MEASUREMENT BLOCK
# ==========================================

bob = pcvl.Circuit(2)

# Bob measurement setting
bob.add(0, pcvl.PS(phi=-math.pi / 4))

# Beam splitter
bob.add((0, 1), pcvl.BS())


# ==========================================
# 4. COMBINE ALICE + BOB
# ==========================================

e91_circuit = pcvl.Circuit(4)

# Alice uses modes 0 and 1
e91_circuit.add(0, alice)

# Bob uses modes 2 and 3
e91_circuit.add(2, bob)


print()
print("Complete E91 optical circuit:")
print(e91_circuit)


# ==========================================
# 5. CREATE PERCEVAL PROCESSOR
# ==========================================

processor = pcvl.Processor("SLOS", e91_circuit)

processor.with_input(entangled_state)

# Keep only events where both photons are detected
processor.min_detected_photons_filter(2)

print()
print("Processor created successfully.")
print("Minimum detected photons: 2")


 # ==========================================
# 6. CALCULATE OUTPUT PROBABILITIES
# ==========================================

sampler = pcvl.algorithm.Sampler(processor)

print()
print("Calculating output probabilities...")

output = sampler.probs()

print()
print("Output probabilities:")
print(output)