from typing import List, Dict, Union, Generator, Optional

from ..base import ChatHistory, BaseModel
from ...backend import BackendType, CoreRuntime


# Set model id
model_id = "Qwen/Qwen3-14B-Instruct"
gguf_model_id = "Qwen/Qwen3-14B-GGUF"
context_length = 40960  # Set context length to 40960 tokens (max 40960)


# Prompt setting
system_prompt = \
"""You are Qwen, a professional AI assistant created by Alibaba Cloud. You are designed to provide expert-level assistance across various domains while maintaining the highest standards of professionalism and accuracy.

CORE IDENTITY:
- Your name is Qwen, developed by Alibaba Cloud
- Your knowledge cutoff is January 2025
- You acknowledge that your knowledge may be limited or outdated for recent events

THINKING AND REASONING:
- For complex problems, engage your step-by-step reasoning capabilities before providing your final answer
- Think through problems methodically, considering multiple approaches and potential pitfalls
- When uncertain about current information, actively use real-time search to verify facts and provide up-to-date responses

COMMUNICATION PRINCIPLES:
- Always respond in the same language the user communicates with you
- Never switch languages mid-conversation unless explicitly requested
- Maintain a polite, respectful, and professional tone at all times
- Provide detailed explanations when appropriate, citing sources when available

RESPONSE GUIDELINES:
- For complex queries: Think step-by-step, then provide comprehensive, well-structured answers
- For current events or recent information: Proactively search for the latest information
- When knowledge is insufficient: Acknowledge limitations and seek additional information through search
- Always prioritize accuracy over speed

Remember: Your role is to be a reliable, knowledgeable professional assistant who thinks carefully before responding and actively seeks current information when needed."""
print("INFO:     Use default system prompt -", system_prompt)


class Qwen3Model(BaseModel):
    """
    Qwen 3 14B 4bitQ Instruct model implementation.
    This class extends BaseModel and provides methods for chatting and token streaming.
    """
    model_id = model_id
    gguf_model_id = gguf_model_id
    context_length = context_length
    supported_backends = tuple([BackendType.GGUF, BackendType.BIN])

    def _get_runtime(self, backend: BackendType | None = None):
        if backend is None:  # Default to GGUF backend
            backend = self.supported_backends[0]
        super()._get_runtime(backend)

        if backend == BackendType.GGUF:
            return CoreRuntime(
                model_id=self.gguf_model_id,
                context_length=self.context_length,
                filename="*Q4_K_M.gguf",  # 4bit quantized model
                verbose=False,
                backend=backend.value
            )
        elif backend == BackendType.BIN:
            return CoreRuntime(
                model_id=self.model_id,
                context_length=self.context_length,
                device_map="cuda:0",
                backend=backend.value
            )

    def chat(
        self,
        chat_history: ChatHistory,
        user_prompt: str,
        system_prompt: str = system_prompt,
        tools: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.2,
        top_p: float = 0.95,
        top_k: int = 40,
        min_p: float = 0,
        typical_p: float = 1.0,
        stream: bool = True,
        max_new_tokens: int = 512,
        repeat_penalty: float = 1.0,
        print_output: bool = False
    ) -> Union[Generator[str, None, None], str]:
        return super().chat(
            chat_history=chat_history,
            user_prompt=user_prompt,
            system_prompt=system_prompt,

            # function calling support
            tools=tools,

            # description at https://huggingface.co/Qwen/Qwen3-14B
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            min_p=min_p,
            typical_p=typical_p,
            stream=stream,
            max_new_tokens=max_new_tokens,
            repeat_penalty=repeat_penalty,
            print_output=print_output
        )


'''
    def format_function_schemas(self, function_schemas: List[Dict[str, Any]]) -> str:
        """
        Format function schemas for inclusion in the system prompt.
        """
        if not function_schemas:
            return ""

        formatted_functions = []
        for func in function_schemas:
            func_desc = f"""
Function: {func['name']}
Description: {func['description']}
Parameters: {json.dumps(func['parameters'], indent=2)}
"""
            formatted_functions.append(func_desc)

        return "\n".join(formatted_functions)

    def extract_function_calls(self, response_text: str) -> List[Dict[str, Any]]:
        """
        Extract function calls from the model's response.
        """
        function_calls = []

        # Look for function calls in the response
        if "<function_call>" in response_text and "</function_call>" in response_text:
            import re
            pattern = r'<function_call>(.*?)</function_call>'
            matches = re.findall(pattern, response_text, re.DOTALL)

            for match in matches:
                try:
                    func_call = json.loads(match.strip())
                    function_calls.append(func_call)
                except json.JSONDecodeError:
                    continue

        return function_calls

    def chat_with_functions(
            self,
            chat_history: ChatHistory,
            user_prompt: str,
            function_schemas: Optional[List[Dict[str, Any]]] = None,
            function_implementations: Optional[Dict[str, callable]] = None,
            system_prompt: str = system_prompt_with_functions,
            temperature: float = 0.5,
            print_prompt: bool = True
    ):
        # Prepare the system prompt with function schemas
        if function_schemas:
            func_schemas_text = self.format_function_schemas(function_schemas)
            full_system_prompt = f"{system_prompt}\n\nAvailable Functions:\n{func_schemas_text}"
        else:
            full_system_prompt = system_prompt

        # Add user prompt to chat history
        chat_history.add_user_message(user_prompt)

        # Prepare messages for the model
        messages = [{"role": "system", "content": full_system_prompt}]
        messages.extend(chat_history.get_messages())

        if print_prompt:
            print(f"User: {user_prompt}")

        # Convert function schemas to tools format if provided
        tools = None
        if function_schemas:
            tools = [{"type": "function", "function": schema} for schema in function_schemas]

        # Get model response
        response_stream = self.model.create_chat_completion(
            messages=messages,
            temperature=temperature,
            stream=True,
            tools=tools,
            tool_choice="auto" if tools else None
        )

        # Collect the response
        full_response = ""
        for chunk in response_stream:
            if chunk['choices'][0]['delta'].get('content'):
                content = chunk['choices'][0]['delta']['content']
                full_response += content
                print(content, end='', flush=True)

            # Check for tool calls
            if chunk['choices'][0]['delta'].get('tool_calls'):
                tool_calls = chunk['choices'][0]['delta']['tool_calls']
                for tool_call in tool_calls:
                    if tool_call['type'] == 'function':
                        func_name = tool_call['function']['name']
                        func_args = json.loads(tool_call['function']['arguments'])

                        print(f"\n[Function Call: {func_name}({func_args})]")

                        # Execute function if implementation is provided
                        if function_implementations and func_name in function_implementations:
                            try:
                                result = function_implementations[func_name](**func_args)
                                print(f"[Function Result: {result}]")

                                # Add function result to chat history
                                chat_history.add_assistant_message(f"Function call: {func_name}")
                                chat_history.add_user_message(f"Function result: {result}")

                                # Continue the conversation with function result
                                continue_messages = messages + [
                                    {"role": "assistant", "content": full_response},
                                    {"role": "user", "content": f"Function {func_name} returned: {result}. Please provide a response based on this result."}
                                ]

                                continue_response = self.model.create_chat_completion(
                                    messages=continue_messages,
                                    temperature=temperature,
                                    stream=True
                                )

                                print("\nAssistant: ", end='')
                                for chunk in continue_response:
                                    if chunk['choices'][0]['delta'].get('content'):
                                        content = chunk['choices'][0]['delta']['content']
                                        full_response += content
                                        print(content, end='', flush=True)

                            except Exception as e:
                                print(f"[Function Error: {e}]")

        print()  # New line after response

        # Add assistant response to chat history
        chat_history.add_assistant_message(full_response)

        return full_response
'''
