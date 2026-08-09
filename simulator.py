# simulator.py
from grid_game import GridHuntGame
from agent import GreedyGridAgent, SimpleReflexAgent, ModelBasedAgent

# Added by IT24610787
def run_agent_simulation(agent_instance, agent_name: str):
    """Generic simulator runner for testing agent class."""

    env = GridHuntGame()
    print(f"\n=== Running Simulation: {agent_name} ===")

    while not env.is_done():
        percept = env.get_percept(agent_instance)
        action = agent_instance.sense_and_act(percept)
        env.execute_action(agent_instance, action)
        
        pos_str = percept.get('agent_pos', 'Hidden (Partial Observability)')
        food_str = percept.get('remaining_food', len(env.food_positions))
        
        print(f"Action: {action:<12} | Pos: {pos_str} | Food Left: {food_str} | Score: {env.score}")

    print(f"[{agent_name}] \nGame Over! Final Score: {env.score} after {env.steps} steps.")

def run_grid_hunt():
    env = GridHuntGame()
    agent = GreedyGridAgent()

    print("=== UC Berkeley Style Small Grid Hunt Started ===")
    while not env.is_done():
        percept = env.get_percept(agent)
        action = agent.sense_and_act(percept)
        env.execute_action(agent, action)
        print(f"Pos: {percept['agent_pos']} | Food Left: {percept['remaining_food']} | Score: {percept['score']}")

    print(f"\nGame Over! Final Score: {env.score} after {env.steps} steps.")

if __name__ == "__main__":
    # Original Lab 1 agent - Added by IT24610787
    run_grid_hunt()

    # Added by IT24610787 - Runs Lab 02 Simple Reflex Agent (Observe infinite loop failure)
    simple_agent = SimpleReflexAgent()
    run_agent_simulation(simple_agent, "Simple Reflex Agent")

    # Added by IT24610787 - Runs Lab 02 Model-Based Agent (Observe memory breaking loops)
    model_agent = ModelBasedAgent()
    run_agent_simulation(model_agent, "Model-Based Agent")