from typing import Iterator
import traceback

from llama_cpp import Llama, CreateChatCompletionStreamResponse
from .config import ChatHistory


# Set model id
model_id = "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF"
context_length = 128000  # Set context length to 128000 tokens

# Load model
model = Llama.from_pretrained(
    repo_id=model_id,
    filename="*Q4_K_M.gguf",  # 4bit quantized model
    n_ctx=context_length,
    verbose=False
)

# Prompt setting
system_prompt = "" \
                + "Your name is `Llama 3.1` developed by Meta AI. " \
                + "You are a helpful, smart, kind, and efficient AI Assistant. " \
                + "Your knowledge is based on data available up to December 2023. " \
                + "You always fulfill the user's requests to the best of your ability. " \
                + "You are not aware of any events or developments that occurred after that date unless explicitly provided by the user. " \
                + "Do not fabricate information about events beyond your knowledge cutoff. If uncertain, state that clearly. " \
                + "Detect the user's input language and always respond in the same language. " \
                + "Do not switch languages unless explicitly instructed. " \
                + "Maintain a consistent, polite, and contextually appropriate tone for each language."
print("INFO: Use default system prompt -", system_prompt)


def chat(
        chat_history: ChatHistory, user_prompt: str, temperature=0.5, print_prompt=True
) -> tuple[
    Iterator[CreateChatCompletionStreamResponse], bool
]:
    """ Chatting interface """
    prompt = chat_history.create_prompt(system_prompt, user_prompt)
    chat_history.append("user", user_prompt)

    if print_prompt:
        print("PROMPT:")
        for line in prompt:
            print(line)
        print()

    return model.create_chat_completion(prompt, temperature=temperature, stream=True), print_prompt


def token_streamer(tokens: Iterator[CreateChatCompletionStreamResponse], print_prompt: bool = True) -> Iterator[str]:
    """ Token streamer """
    if print_prompt:
        print("ANSWER:")

    try:
        for token in tokens:
            delta: dict = token['choices'][0]['delta']
            token_delta = delta.get('content')
            if token_delta:
                print(token_delta, end="")
            yield token_delta if token_delta else ""
    except ValueError:  # Over token limit error
        traceback.print_exc()
        yield "\n\nERROR: Chat is unexpectedly terminated due to token limit. Please shorten your prompt or chat history."
    finally:
        print()
