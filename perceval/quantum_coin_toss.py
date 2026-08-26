import perceval as pcvl

print("=" * 60)
print("QUANTUM COIN TOSSING - PERCEVAL")
print("=" * 60)

# Create a 50:50 beam splitter
circuit = pcvl.Circuit(2)
circuit.add(0, pcvl.BS())

print("\nCoin-toss circuit:")
print(circuit)

# One photon enters mode 0
input_state = pcvl.BasicState([1, 0])

print("\nInput state:")
print(input_state)

# Create Perceval processor
processor = pcvl.Processor("SLOS", circuit)
processor.with_input(input_state)

# Run repeated samples
sampler = pcvl.algorithm.Sampler(processor)
results = sampler.sample_count(1000)

print("\nMeasurement results:")
print(results)

print("\nInterpretation:")
print("The two output modes represent the two possible coin outcomes.")
print("A balanced beam splitter produces approximately equal probabilities.")