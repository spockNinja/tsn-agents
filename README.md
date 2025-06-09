# TheSpatialNetwork Agent Framework

Hello! Welcome to the Agent Development Framework for the Spatial Network.

We utilize the [Open Agentic Schema Framework](https://github.com/agntcy/oasf) so that Agent Developers can create agents with their preferred technologies and be hosted together on the [workflow server](https://github.com/agntcy/workflow-srv).

For now, we are compiling the agents here. In the future, we will allow agents to be submitted from other project links.

To get your agent included, it must:

1. Align with our goal of enabling Earth Regenerators.
2. Use AI models available via OpenRouter.
3. Provide an Agent manifest that aligns with the OASF specification.

See the other agents in this repository for examples.

There are two ENV variables provided for you to access downstream AI models.

`OPENROUTER_API_URL`
`OPENROUTER_API_KEY`

They can be plugged into any OpenAPI-comatible SDKs.

---

The OASF spec is still relatively new and under active development. The simplest path to success is to use the LlamaIndex Framework in a python script. See the "business_plan" agent to get an idea of how that works.

We want to support generic binaries and docker images as well, they just haven't been tested yet.