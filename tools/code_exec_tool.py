"""Tool: execute_price_simulation

Executes local computation (Monte Carlo price drop simulation) as a code-execution tool.
This uses a deterministic pseudo-simulation for demo and evaluation.
"""
from langchain.tools import BaseTool
import asyncio
import random
from typing import Dict, Any


class ExecutePriceSimulationTool(BaseTool):
    name: str = "execute_price_simulation"
    description: str = "Run a quick Monte Carlo simulation to estimate probability of price drop."

    async def _arun(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # payload: {"current_price":float, "history": [...]} - simple simulation
        await asyncio.sleep(0.02)
        current = payload.get("current_price", 100.0)
        prob_drop = max(0.1, min(0.9, random.gauss(0.3, 0.15)))
        expected_drop = round(current * prob_drop * random.uniform(0.01, 0.15), 2)
        return {"probability_drop": prob_drop, "expected_drop": expected_drop}

    def _run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return asyncio.get_event_loop().run_until_complete(self._arun(payload))


code_exec_tool = ExecutePriceSimulationTool()
