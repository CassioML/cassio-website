# Hotels/LangChain

A hotel-searching application (Web app + API)
which uses an LLMs and Vector Search to provide hotel
summaries customized to the user preferences.

## Key traits

- LangChain and CassIO;
- a Python API (FastAPI) and a React/Typescript client;
- a partitioned vector store to optimize **vector-based search** of hotel reviews;
- use of LLMs to prepare a **user summary** from user-provided preferences ...
- which is then used to evaluate hotel summaries and provide information **relevant to the user**;
- features also a **real-time** "post new review" flow: new review contribute immediately to the experience;
- usage of (Astra DB) **LLM response cache** to save on latencies and costs with minimal boilerplate;
- "Open in Gitpod" zero-hassle start mode available.

Visit the repository [here](https://github.com/CassioML/langchain-hotels-app#readme).

## Screenshot

User experience on the client:

![Hotels demo, UI](/demo_apps/images/hotels_animated.gif)
