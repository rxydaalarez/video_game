import openai
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = ""

client = OpenAI()
#final
counter = 0
conversation_history = []
past_events_context = ""

def get_response_from_llm(context, player_input):
    # Combine context and player's input to create a prompt for the LLM


    response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": {
                "type": "text",
                "text": context
            }
        },
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": player_input
            }
        }
    ]
)

    
    # Extract the LLM's response
    return response.choices[0].text.strip()

def summarize_history(history):
    # Summarize the conversation history using the OpenAI API
    prompt = f"Summarize the following events concisely:\n{history}"
    response = openai.chat.completions.create(
        engine="gpt-4",
        prompt=prompt,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def main():
    global counter, conversation_history, past_events_context
    # Base context of the game
    base_context = (
        "You find yourself in a dimly lit forest. The tall trees tower above you, their leaves rustling in the gentle wind. "
        "There's a narrow path that seems to lead deeper into the forest, and you hear faint noises that could be animals... or something else. "
        "A thick fog begins to roll in, obscuring your vision."
    )
    
    changing_context = ""
    context = base_context + changing_context + past_events_context
    
    print("Welcome to the Enchanted Forest! Type your actions to proceed.")
    print(context)

    while True:
        counter += 1
        # Update changing context based on counter value
        if counter == 1:
            changing_context = "\nThe fog thickens, and you start feeling a strange presence around you."
        elif counter == 2:
            changing_context = "\nYou hear footsteps behind you, but when you turn around, there's nothing there."
        elif counter == 3:
            changing_context = "\nA shadowy figure appears in the distance, barely visible through the fog."
        else:
            changing_context = "\nThe forest seems to be closing in on you, and the air feels heavier with each passing moment."
        
        # Summarize the conversation history if it gets too long
        if len(conversation_history) > 5:
            history_to_summarize = "\n".join(conversation_history[:-5])
            past_events_context = summarize_history(history_to_summarize)
            conversation_history = conversation_history[-5:]
        
        context = base_context + changing_context + "\n" + past_events_context + "\n" + "\n".join(conversation_history)
        
        # Get player's input
        player_input = input("What would you like to do? ")
        
        # Get LLM response based on player's action
        if player_input.lower() in ["quit", "exit"]:
            print("Thanks for playing! Goodbye.")
            break
        
        # Generate the next part of the game using LLM
        response = get_response_from_llm(context, player_input)
        print(response)

        # Update conversation history with player's input and LLM response for prompt chaining
        conversation_history.append(f"Player: {player_input}\nNarrator: {response}")

if __name__ == "__main__":
    main()
