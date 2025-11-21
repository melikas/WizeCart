# Real-Time Shopping Personal Assistant (LangChain ADK)-Concierge Agents


Our project builds a "Real-Time Shopping Personal Assistant" a lightweight, practical agent designed to help people make smarter buying choices in the moment. When you add items to a cart, drop something onto a wishlist, or get a price alert, the assistant gathers context (price history, competing sellers, reviews, coupons, stock) and uses several specialized agents to produce a single, clear recommendation: "BUY", "NOT BUY", or "DEFER / WAIT." The goal is to save time, reduce impulse spending, and make decisions more confident and evidence-based.

this assistant acts like a knowledgeable friend who knows your budget, your favorite brands, and what deals are active. Instead of you juggling dozens of tabs or spreadsheets, the assistant checks the numbers, reads the signals, and gives one short, actionable suggestion, plus the evidence if you want to look deeper.

Problems for us everyday 
- Time wasted manually comparing prices and reading many reviews.
- Uncertainty about whether a current price is actually a good deal.
- Overspending or buyer's remorse due to impulse purchases.

The Impact of WizeCart
- Saves time and money for everyday shoppers.
- Increases purchase satisfaction and reduces returns for retailers.
- Personalizes recommendations over time using long-term memory and user preferences.

Our agents act like a personal assistant for everyday life. They automate routine tasks such as meal planning and shopping lists, travel planning and reservations, and other repetitive chores. The idea is to remove friction from daily tasks and make small decisions for the user based on predefined preferences and rules.

Shopping example: a concierge agent could generate your weekly grocery list from your dietary preferences, match each item to the best sellers and available coupons, and either place orders automatically at the right time or notify you when a desired item goes on sale.

instead of spending time juggling tabs and spreadsheets to figure out whether a sale is actually a good deal or whether you can afford that gadget, this assistant does the heavy lifting. It checks price history, compares sellers, looks for coupons, skims reviews for sentiment, and takes your budget and preferences into account. Then it gives you a short, actionable suggestion — and the evidence behind it if you want to dig in.

Who benefits from our agent?
- Busy shoppers who want to make smarter, faster buying decisions.
- People on a budget who need to avoid impulse overspending.
- Power users who want automated price-watching and coupon hunting.

Why this matters
- Saves time: no more manual price hunting or reading dozens of reviews.
- Saves money: finds better deals, applicable coupons, and suggests cheaper alternatives.
- Reduces regret: recommends purchases based on both personal finance and real product signals, so users are less likely to return items.

Example User Flows (step-by-step scenarios)

1) Quick Buy Decision
    - User action: Adds a pair of headphones to the cart.
    - System: Ingests the cart event and retrieves price listings, price history, reviews, and available coupons.
    - Agents: Price Agent computes attractiveness, Review Agent computes sentiment, Finance Agent checks affordability.
    - Fusion: Scores components and outputs `BUY` with "add_to_cart" action or `DEFER` if a better deal is likely.
    - Outcome: User sees a short recommendation and a short evidence summary (best price, coupon, key review snippets).

2) Budget-Conscious Shopper
    - User action: Marks an expensive kitchen appliance to wishlist.
    - System: Agent runs affordability check vs. user's budget and looks for cheaper alternatives.
    - Agents: Finance Agent flags possible overspend, Alternative Agent suggests similar cheaper models.
    - Fusion: Recommends `NOT_BUY` or `CHOOSE_ALTERNATIVE` with suggested alternatives and expected savings.
    - Outcome: User receives alternatives and can swap the wishlist item with a recommended cheaper model.

3) Price Watch & Auto-Order
    - User action: Sets a price-watch alert or opts into auto-order rules for a product.
    - System: Long-running orchestrator monitors price feeds and coupon sources.
    - Agents: Price Agent detects a price drop and runs a short simulation for expected further drops.
    - Fusion: If the buy score crosses threshold and user rules allow, the system either auto-orders or notifies the user with a one-click action.
    - Outcome: User either gets a notification "Good deal — buy now" or the product is auto-ordered per their saved rule.

Architecture (ASCII)

```
[Event Source] -> [Loop Orchestrator] -> parallel -> [Agents: Finance, Price, Reviews, Alternative] \
             \-> [Fusion Agent] -> [Decision + Memory + Observability]
```

Features
- Multi-agent LangChain architecture (Chains, Agents, Tools)
- Async tools for external lookups (placeholders)
- Short-term and long-term memory (ConversationBufferMemory + FAISS VectorStore)
- Observability (structured JSON logs + CSV metrics)
- Evaluation harness with synthetic events and report generation

Quick start

1. Create a virtual environment (Python 3.11+)

```powershell
python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.sample` to `.env` and fill provider placeholders.

3. Run the demo (uses synthetic events):

```powershell
python demo.py
```

Project layout
- `main.py` - production entrypoint for loop/event mode
- `demo.py` - demo runner with synthetic events
- `agents/` - individual agent implementations
- `tools/` - LangChain tool wrappers (async-capable)
- `memory/` - short- and long-term memory modules
- `evaluation/` - evaluator and reports
- `infra/` - logging and metrics utilities
- `config/` - settings (env-driven)

Notes
- No real API keys included. Use environment variables (see `.env.sample`).
- LangChain constructs are used throughout (Agents, Tools, Chains, Memory).

See `infra/deployment_notes.md` for deployment guidance.

