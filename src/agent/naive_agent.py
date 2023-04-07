from agent.abstract_agent import Agent


class NaiveAgent(Agent):
    def __init__(self):
        super().__init__(name="naive", is_human=False)
