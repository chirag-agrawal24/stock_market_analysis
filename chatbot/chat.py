import json
import google.generativeai as genai
from chatbot.functions import available_functions, functions
import streamlit as st # for secret api key

# Configure the API key for generative AI
genai.configure(api_key=st.secrets["general"]["gemini_api_key"])
model = genai.GenerativeModel('gemini-pro')


def process_user_input(user_input):
    """Processes user input, extracts parameters, calls functions, and returns output."""
    
    prompt = f"""
    User Input: {user_input}

    Instructions:
    1. Analyze the user's input and identify if it requires any of the following functions.
    2. If a function is required, extract the necessary parameters (e.g., ticker, window).
    3. Call the appropriate function with the extracted parameters.
    4. Format the function's output into a human-readable sentence.

    Available Functions:
    {functions}

    Output:
    A JSON object with the following structure:
    {{
        "function_to_call": "function_name",
        "parameters": {{
        "parameter_name": "parameter_value",
        ...
        }}
    }}

    If no function is required, output an empty JSON object: {{}}
    """
    # Send prompt to model and get response
    response = model.generate_content(prompt)  # Assuming `model.generate_content` returns a response object with `.text`

    try:
        # Parse the response as JSON
        response_json = json.loads(response.text)

        function_name = response_json.get("function_to_call")
        params = response_json.get("parameters", {})

        if function_name:
            try:
                function = available_functions.get(function_name)

                if function:
                    # Call the selected function with the parameters extracted
                    result = function(**params)  # Call the function with unpacked parameters

                    # Check if the result is a plot (based on function name)
                    if function_name in ["plot_stock_price", "plot_crypto_price_graph"]:
                        # Return the plot object (matplotlib figure)
                        return {"plot": result}
                    else:
                        # Return the result in a human-readable format
                        follow_up_prompt = f"""
            The result of the function call {function_name} with parameters {params} is: {result}.
            Please rephrase this result in a human-readable sentence.
            """
                        follow_up_response = model.generate_content(follow_up_prompt)

                       
                        return {"text": follow_up_response.text}

                else:
                    return {"error": f"Function {function_name} not found."}
            except Exception as e:
                return {"error": f"Error executing function: {e}"}
        else:
            # If no function is called, generate a response from the model to display
            own_response = model.generate_content(
                user_input,
                generation_config={"temperature": 0},  # Optional: Adjust temperature for response variability
            )
            return {"text": own_response.text}  # Return the model's response as text

    except json.JSONDecodeError:
        return {"error": f"Error decoding JSON from model response: {response.text}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

