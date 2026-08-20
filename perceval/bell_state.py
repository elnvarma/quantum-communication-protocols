import perceval as pcvl

circuit = pcvl.Circuit(4)
circuit.add((0, 1), pcvl.BS.Rx())
circuit.add((2, 3), pcvl.BS.Rx())

input_state = pcvl.BasicState([1, 1, 0, 0])

processor = pcvl.Processor("SLOS", circuit)
processor.with_input(input_state)

sampler = pcvl.algorithm.Sampler(processor)
results = sampler.probs()["results"]

print("Input state:", input_state)
print("Bell-state experiment:")

for state, probability in results.items():
    print(state, "->", probability)