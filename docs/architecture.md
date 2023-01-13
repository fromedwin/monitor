# System architecture

<!--     
	High-level overview of the system architecture
    Detailed description of the major components and how they interact with each other
    Information on the technologies and frameworks used to build the system
    Details on the system's scalability and performance characteristics
    Diagrams or illustrations to help explain the architecture
    Information on how the system integrates with other tools and systems
    Information on the security and data protection measures that are in place 
--> 

The high-level overview of the FromEdwin's system architecture is a star pattern with a centralized server that acts as the hub for all the major components of the system. 

With such configuration, the centralized server is connected to multiple other systems or devices, which are referred as workers in the architecture. These workers are responsible for collecting data and sending it to the centralized server for processing and storage.

## Server

The UI and APIs provided by the centralized server allows users to **access** and **interact** with the monitoring data.

It is responsible for:

- The **user interface** (UI)
- The **application programming interfaces** (APIs) that allow communication between the different components
- The **configuration files** that define the settings and parameters of the workers
- The **databases** that store the data

## Workers

Each worker is responsible for **collecting** monitoring data, **processing**, and **storage**. 

The worker functions as follows:

- Upon initialization, the worker **registers itself** with the centralized server and **loads its configuration** files.
- The worker then begins sending **regular updates**, called *"heartbeats",* to the centralized server at a set interval *(e.g., 10 seconds)*. These updates include information about the worker's status.
- The worker also stores **non-critical data** locally used to trigger an alert.

In this way, the worker functions as a monitoring agent that is able to function independently but still communicates with the centralized server to ensure data integrity and consistency.

---

It is important to note that this is a high-level overview and more details about the different components and how they interact with each other will be discussed later in the documentation.
