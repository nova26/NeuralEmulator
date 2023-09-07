# NeuralEmulator
Was used in :
https://www.mdpi.com/2076-3417/12/9/4528
## About
**OZ neural emulator**
The OZ neural emulator, a scalable Python framework, facilitates the construction, testing, and deployment of Spiking Neural Networks architecture. This framework relies on our OZ, PES, and STDP analog circuit designs as its foundational elements.

Through the OZ neural emulator, we can gauge the efficacy of our methodologies without resorting to costly hardware implementations or spending extensive time on hardware circuit design in CAD tools and subsequent SPICE simulations.

Furthermore, as the neuron count rises, SPICE simulation durations become impractical. Consequently, our goal is to strike a balance between emulation precision and scalability.

## Architecture

The previously mentioned building blocks have been subdivided into smaller components, each of which corresponds to a specific model. These models are derived from their SPICE simulations with varying input signals.

For instance, the Pulse-current synapse model features two inputs: VIN and VW, with a constant VDD and an IOUT as its output. Hence, its model can be represented as F(VIN, VW) = IOUT.

Among other components, the OZ neuron model incorporates the Pulse-current synapse as a modifiable sub-component. To formulate the Pulse-current synapse model, its circuit design is simulated in a SPICE simulator. Here, each input spans from 0 to VDD in 10mv increments.

Once the Python model for the Pulse-current synapse is established, the results from SPICE are integrated using an Interface class. This class processes the SPICE simulation output file and offers a query interface for specific (VIN, VW) pairs.

Given that the SPICE output file organizes data based on VIN and VW values, we've opted for a Binary Search method to determine the model's output current. Every model within the OZ neural emulator adheres to one of two primary interfaces: VoltageSource or CurrentSource. Both these classes possess their respective virtual functions: GetVoltage and GetCurrent.

## More
Following the previous example,
The pulse-current synapse derives deriving the CurrentSource class because it provides current that can be used as input to another model.

The OZ neural emulator is a time-based simulation, meaning the simulation will run for a predefined number of seconds, where each simulation cycle is also predefined, i.e. there will be (SIM_TIME/SIM_CYCLE_TIME) steps.

To enforce a uniform interface for the simulation scheduler, VoltageSource, and CurrentSource classes are deriving an interface named SimBase, which has a pure virtual function named Run.

At each step, the simulation scheduler goes over a list of SimBase objects, and just activating the Run function, the SimBase object’s structure (network design) is up to the user to define, I.e., the iteration order. In the future, we would like to add multi-threading capabilities to the scheduler to fasten each layer run.

Each SimBase object in the simulation is aware of the simulation cycle time via a configuration class, and its responsibility is to process the input data it received via either VoltageSource or CurrentSource or both, at each Run call and store the corresponding result for when some will use the interface it implementing as discussed earlier, with O(SIM_CYCLE_TIME/totalNumberOfSimBaseObjects) run time.

For example, at each step the scheduler will trigger the Pulse-current synapse model Run function, The Run function implementation will take the input voltages VIN, and VW values via two VoltageSource objects that were given during Pulse-current synapse creation, with the GetVoltage function. It will then use its model to calculate the output current IOUT and will store the received value.

The OZ neuron is composed of a Pulse-current synapse object, i.e. with a CurrentSource object. In the OZ Run function implementation, it will use the GetCurrent of the CurrentSource object it received during the construction time, to calculate the frequency of the spikes. Therefore, in the network construction, we need to ensure that the model of the Pulse-current synapse will run before the OZ neuron with some structure like the trivial layers that are used in the classic artificial neural networks. These are the basic principles of the OZ neural emulator, 
and a full class diagram is provided in “A”.


