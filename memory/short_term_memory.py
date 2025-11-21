"""Short-term session memory using LangChain ConversationBufferMemory.

This module provides a graceful fallback if LangChain's memory classes
are not available in the running environment (helps in fresh installs).
"""
try:
    from langchain.memory import ConversationBufferMemory
except Exception:
    # Lightweight fallback implementation with the minimal interface used
    class ConversationBufferMemory:
        def __init__(self, memory_key: str = "session_history", k: int = 10):
            self.memory_key = memory_key
            self.k = k
            self.buffer = []

        def save_context(self, inputs, outputs):
            self.buffer.append({"input": inputs, "output": outputs})
            if len(self.buffer) > self.k:
                self.buffer = self.buffer[-self.k:]

        def load_memory_variables(self, inputs=None):
            return {self.memory_key: self.buffer}


def create_short_term_memory():
    # Stores recent conversation/events; configured to keep last 10 events
    return ConversationBufferMemory(memory_key="session_history", k=10)
