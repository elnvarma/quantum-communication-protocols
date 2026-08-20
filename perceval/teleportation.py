import perceval as pcvl

# Simple photonic quantum communication experiment
# based on the teleportation intermediate state.

input_state = pcvl.BasicState([0, 1, 1, 0, 1, 0])

circuit = pcvl.Circuit(6)

# Beam splitter operation
circuit.add((1, 2), pcvl.BS.Rx())

processor = pcvl.Processor("SLOS", circuit)
processor.with_input(input_state)

sampler = pcvl.algorithm.Sampler(processor)
results = sampler.probs()["results"]

print("Teleportation intermediate result:")

for state, probability in results.items():
    print(state, "->", probability)