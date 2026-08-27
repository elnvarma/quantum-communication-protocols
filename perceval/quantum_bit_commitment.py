import perceval as pcvl


print("=" * 60)
print("QUANTUM BIT COMMITMENT - PERCEVAL")
print("=" * 60)

# Alice commits to bit 1
secret_bit = 1

# Encode bit using a single photon:
# |1,0> represents logical 0
# |0,1> represents logical 1

if secret_bit == 0:
    input_state = pcvl.BasicState([1, 0])
else:
    input_state = pcvl.BasicState([0, 1])

print("\nCommitted state:")
print(input_state)

# Beam splitter used as a quantum transformation
circuit = pcvl.Circuit(2)
circuit // pcvl.BS()

print("\nCommitment circuit:")
print(circuit)

# Simulation
backend = pcvl.BackendFactory.get_backend("SLOS")
processor = pcvl.Processor(backend, circuit)
processor.with_input(input_state)

sampler = pcvl.algorithm.Sampler(processor)

results = sampler.samples(1000)

print("\nMeasurement results:")
print(results)

print("\nSecret bit committed by Alice:", secret_bit)

print("\nInterpretation:")
print("A photonic state represents the committed bit.")
print("A beam splitter provides a quantum optical transformation.")
print("This is an educational photonic demonstration.")
print("It is not a complete secure quantum bit-commitment protocol.")