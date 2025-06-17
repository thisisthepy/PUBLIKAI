package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.chat_title_placeholder
import gemstone.framework.network.websocket.ChatEvent
import gemstone.framework.network.websocket.ChatState
import kotlinx.serialization.Serializable
import org.jetbrains.compose.resources.stringResource
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlinx.serialization.json.*


@Serializable
enum class ChatRole(val value: String) {
    SYSTEM("system"),
    USER("user"),
    ASSISTANT("assistant"),
    TOOL("tool")
}


@Serializable
data class ChatMessage(
    val role: String,
    val content: String,
    val tool_calls: List<ToolCall>? = null,
    val tool_call_id: String? = null
)


@Serializable
data class ToolCall(
    val id: String,
    val function: ToolFunction
)


@Serializable
data class ToolFunction(
    val name: String,
    val arguments: JsonElement
)


class ChatHistory : MutableList<ChatMessage> {
    private val messages = mutableListOf<ChatMessage>()

    override val size: Int get() = messages.size
    override fun contains(element: ChatMessage): Boolean = messages.contains(element)
    override fun containsAll(elements: Collection<ChatMessage>): Boolean = messages.containsAll(elements)
    override fun get(index: Int): ChatMessage = messages[index]
    override fun indexOf(element: ChatMessage): Int = messages.indexOf(element)
    override fun isEmpty(): Boolean = messages.isEmpty()
    override fun iterator(): MutableIterator<ChatMessage> = messages.iterator()
    override fun lastIndexOf(element: ChatMessage): Int = messages.lastIndexOf(element)
    override fun add(element: ChatMessage): Boolean = messages.add(element)
    override fun add(index: Int, element: ChatMessage) = messages.add(index, element)
    fun add(role: String, content: String = "", tool_calls: List<ToolCall>? = null, tool_call_id: String? = null) {
        messages.add(ChatMessage(role, content, tool_calls, tool_call_id))
    }
    override fun addAll(index: Int, elements: Collection<ChatMessage>): Boolean = messages.addAll(index, elements)
    override fun addAll(elements: Collection<ChatMessage>): Boolean = messages.addAll(elements)
    override fun clear() = messages.clear()
    override fun listIterator(): MutableListIterator<ChatMessage> = messages.listIterator()
    override fun listIterator(index: Int): MutableListIterator<ChatMessage> = messages.listIterator(index)
    override fun remove(element: ChatMessage): Boolean = messages.remove(element)
    override fun removeAll(elements: Collection<ChatMessage>): Boolean = messages.removeAll(elements)
    override fun removeAt(index: Int): ChatMessage = messages.removeAt(index)
    override fun retainAll(elements: Collection<ChatMessage>): Boolean = messages.retainAll(elements)
    override fun set(index: Int, element: ChatMessage): ChatMessage = messages.set(index, element)
    override fun subList(fromIndex: Int, toIndex: Int): MutableList<ChatMessage> = messages.subList(fromIndex, toIndex)
}


@Serializable
data class Conversation(
    val user: String,
    val assistant: String = "",
    val thoughts: String = "",
    val thoughtElapsed: Float = 0f,
    val isThinking: Boolean = false,
    val tools: Map<String, Boolean> = emptyMap()
)


data class ChatUiState(
    val chatId: Int = -1,
    val title: String = "",
    val messages: List<Conversation> = emptyList(),
    val currentMessage: Conversation? = null,
    val messageInput: String = "",
    val isBookmarked: Boolean = false,
    val isResponding: Boolean = true,
    val isConnected: Boolean = false,
    val error: String? = null
) {
    val titleOrPlaceholder: String
        @Composable get() = title.ifEmpty { stringResource(Res.string.chat_title_placeholder) }
}


object ChatViewModel {
    private val chatHistory = ChatHistory()

    private val _uiState = MutableStateFlow(ChatUiState())
    val uiState: StateFlow<ChatUiState> = _uiState.asStateFlow()

    private val coroutineScope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    fun runBlocking(block: suspend CoroutineScope.() -> Unit) {
        coroutineScope.launch { block() }
    }

    fun initialize() {
        observeClientEvents()
        observeClientState()
    }

    fun cleanup() {
        coroutineScope.cancel()
        coroutineScope.launch {
            webSocketClient.deleteSession()
        }
    }

    fun reset() {
        _uiState.value = ChatUiState()
        chatHistory.clear()
    }

    private fun observeClientEvents() {
        coroutineScope.launch {
            webSocketClient.events.collect { event: ChatEvent ->
                when (event) {
                    is ChatEvent.MessageReceived -> {
                        if (event.isThinking) {
                            _uiState.value = _uiState.value.copy(
                                currentMessage = _uiState.value.currentMessage?.copy(
                                    thoughts = (_uiState.value.currentMessage?.thoughts?.trimStart() ?: "") + event.content
                                )
                            )
                        } else {
                            _uiState.value = _uiState.value.copy(
                                currentMessage = _uiState.value.currentMessage?.copy(
                                    assistant = (_uiState.value.currentMessage?.assistant?.trimStart() ?: "") + event.content
                                )
                            )
                        }
                    }

                    is ChatEvent.ThinkingStarted -> {
                        _uiState.value = _uiState.value.copy(
                            currentMessage = _uiState.value.currentMessage?.copy(
                                isThinking = true
                            )
                        )
                    }

                    is ChatEvent.ThinkingEnded -> {
                        _uiState.value = _uiState.value.copy(
                            currentMessage = _uiState.value.currentMessage?.thoughts?.let {
                                _uiState.value.currentMessage?.copy(
                                    isThinking = false,
                                    thoughts = it.trim()
                                )
                            }
                        )
                    }

                    is ChatEvent.ToolCallReceived -> {
                        val keys = event.toolCall.jsonObject.keys
                        when (val type = keys.firstOrNull()) {
                            "call", "result" -> {
                                val data = event.toolCall.jsonObject[type]?.jsonObject
                                if (data != null) {
                                    val id = data["id"]?.jsonPrimitive?.content ?: ""
                                    val functionName = data["function"]?.jsonObject?.get("name")?.jsonPrimitive?.content ?: ""
                                    val toolKey = "$functionName(): $id"

                                    val currentMsg = _uiState.value.currentMessage
                                    if (currentMsg != null && !currentMsg.tools.containsKey(toolKey)) {
                                        val newTools = currentMsg.tools + (toolKey to false)

                                        _uiState.value = _uiState.value.copy(
                                            currentMessage = currentMsg.copy(tools = newTools)
                                        )
                                    }
                                }
                            }
                            "history" -> {
                                event.toolCall.jsonObject[type]?.jsonArray?.forEach { item ->
                                    val data = item.jsonObject

                                    val role = data["role"]?.jsonPrimitive?.content ?: "error"
                                    val content = data["content"]?.jsonPrimitive?.content ?: ""
                                    val toolCalls = data["tool_calls"]?.jsonArray?.map { toolCall ->
                                        val toolCallObj = toolCall.jsonObject
                                        ToolCall(
                                            id = toolCallObj["id"]?.jsonPrimitive?.content ?: "",
                                            function = ToolFunction(
                                                name = toolCallObj["function"]?.jsonObject?.get("name")?.jsonPrimitive?.content ?: "",
                                                arguments = toolCallObj["function"]?.jsonObject?.get("arguments") ?: JsonNull
                                            )
                                        )
                                    }
                                    val toolCallId = data["tool_call_id"]?.jsonPrimitive?.content
                                    chatHistory.add(role, content, toolCalls, toolCallId)
                                }
                            }
                            else -> {
                                println("WARNING: Unknown event type: $type")
                            }
                        }
                    }

                    is ChatEvent.MessageComplete -> {
                        // Add assistant message to history and UI
                        val data = _uiState.value.currentMessage?.assistant?.trim()
                        val assistantMessage = if (data.isNullOrEmpty()) {
                            "[ERROR] The connection was closed unexpectedly, please try again."
                        } else {
                            data
                        }
                        chatHistory.add(ChatRole.ASSISTANT.value, assistantMessage)
                        val currentMessage = Conversation(
                            user = _uiState.value.currentMessage?.user ?: "",
                            assistant = assistantMessage,
                            thoughts = _uiState.value.currentMessage?.thoughts ?: "",
                            thoughtElapsed = _uiState.value.currentMessage?.thoughtElapsed ?: 0f,
                            isThinking = false,
                            tools = _uiState.value.currentMessage?.tools ?: emptyMap()
                        )

                        _uiState.value = _uiState.value.copy(
                            messages = _uiState.value.messages + currentMessage,
                            currentMessage = null,
                            isResponding = false
                        )
                    }

                    is ChatEvent.ErrorOccurred -> {
                        _uiState.value = _uiState.value.copy(
                            error = event.error,
                            isResponding = false
                        )
                    }
                }
            }
        }
    }

    private fun observeClientState() {
        coroutineScope.launch {
            webSocketClient.state.collect { state ->
                when (state) {
                    is ChatState.Connected -> {
                        _uiState.value = _uiState.value.copy(
                            isConnected = true,
                            error = null
                        )
                    }

                    is ChatState.Disconnected -> {
                        _uiState.value = _uiState.value.copy(
                            isConnected = false
                        )
                    }

                    is ChatState.Thinking -> {
                        _uiState.value = _uiState.value.copy(
                            currentMessage = _uiState.value.currentMessage?.thoughtElapsed?.let {
                                _uiState.value.currentMessage?.copy(
                                    thoughtElapsed = it + state.elapsedSeconds,
                                )
                            }
                        )
                    }

                    is ChatState.Error -> {
                        _uiState.value = _uiState.value.copy(
                            error = state.message,
                            isResponding = false
                        )
                    }

                    else -> { /* Handle other states */ }
                }
            }
        }
    }

    fun setMessageInput(input: String) {
        _uiState.value = _uiState.value.copy(messageInput = input)
    }

    fun sendMessage() {
        val messageInput = _uiState.value.messageInput.trim()
        if (messageInput.isBlank()) return
        println("INFO: Sending message: $messageInput")

        coroutineScope.launch {
            _uiState.value = _uiState.value.copy(isResponding = true)

            // Add user message to UI
            val userMessage = Conversation(messageInput)
            _uiState.value = _uiState.value.copy(
                currentMessage = userMessage,
                messageInput = ""
            )

            if (webSocketClient.sessionId == null) {
                run {
                    AIModelViewModel.initializeModel(webSocketClient) {
                        AIModelViewModel.selectedAIModel = "Server Error"
                        AIModelViewModel.selectedAIModelDescription = "Server Not Available"
                    }
                }
                initialize()
            }

            val result = webSocketClient.sendMessage(messageInput, chatHistory)
            if (result.isFailure) {
                _uiState.value = _uiState.value.copy(
                    error = "Failed to send message: ${result.exceptionOrNull()?.message}",
                    isResponding = false
                )
            }
        }
    }

    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }

    fun onCleared() {
        cleanup()
    }
}
