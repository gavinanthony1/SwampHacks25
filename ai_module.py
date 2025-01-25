import openai

# Initialize the OpenAI API
openai.api_key = "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"

def get_ai_response(player_state):
    """
    Sends player data to the AI and returns its response.
    :param player_state: Dict containing game and player data.
    :return: AI response as a string.
    """
    prompt = f"""
    You are an AI testing a player in a game simulation. Here is the player's current state:
    {player_state}.
    React to their performance and suggest changes to make the game harder or easier.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a witty AI supervising a gaming simulation."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error communicating with AI: {e}"
