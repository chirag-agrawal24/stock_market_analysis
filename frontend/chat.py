import streamlit as st
import json
import google.generativeai as genai
from chatbot.functions import available_functions, functions

# Configure the API key for generative AI
genai.configure(api_key=json.load(open("data/config.json"))['gemini api key'])
model = genai.GenerativeModel('gemini-pro')


def process_user_input(user_input):
    """Processes user input, extracts parameters, calls functions, and generates output."""
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
    response = model.generate_content(prompt)

    try:
        response_json = json.loads(response.text)

        function_name = response_json.get("function_to_call")
        params = response_json.get("parameters", {})

        if function_name:
            try:
                function = available_functions[function_name]
                result = function(**params)  # Call the selected function

                # If the result is a plot, display it
                if function_name in ["plot_stock_price", "plot_crypto_price_graph"]:
                    
                    st.pyplot(result)

                else:
                    # Feed the result back to Gemini for human-readable output
                    follow_up_prompt = f"""
            The result of the function call {function_name} with parameters {params} is: {result}.
            Please rephrase this result in a human-readable sentence.
            """

                    follow_up_response = model.generate_content(follow_up_prompt)

                    st.write(follow_up_response.text)

            except Exception as e:
                st.write(f"Error executing function: {e}")

        else:
            own_response = model.generate_content(
                user_input,
                generation_config={"temperature": 0},
            )
            st.write(own_response.text)

    except json.JSONDecodeError:
        st.write(f"Error decoding JSON from Gemini response: {response.text}")

if __name__=='__main__':
    # Streamlit app
    st.title('Market Analysis Tool')

    user_input = st.text_input("Enter your query:")

    if user_input:
        process_user_input(user_input)
