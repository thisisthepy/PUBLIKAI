package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import gemstone.framework.network.websocket.ChatWebSocketClient


val webSocketClient = ChatWebSocketClient()


object AIModelViewModel {
    var defaultAIModel by mutableStateOf("Qwen3")
    var defaultAIModelDescription by mutableStateOf("Qwen3 14B 4bitQ IT")

    var selectedAIModel by mutableStateOf("")
    var selectedAIModelDescription by mutableStateOf(defaultAIModelDescription)
    var availableAIModels by mutableStateOf(listOf<Pair<String, String>>(
        Pair("Qwen3", "Qwen3 14B 4bitQ IT"),
        Pair("Llama3", "Llama3.1 8B 4bitQ Instruct"),
    ))
    val selectedAIModelOrDefault
        get() = selectedAIModel.ifEmpty { defaultAIModel }

    fun addAIModel(model: String, description: String) {
        val new = Pair(model, description)
        if (new !in availableAIModels) {
            availableAIModels += new
            if (selectedAIModel.isEmpty()) {
                selectAIModel(model, description)
            }
        }
    }
    fun removeAIModel(model: String) {
        for (pair in availableAIModels) {
            if (pair.first == model) {
                availableAIModels -= pair
                if (selectedAIModel == model) {
                    selectedAIModel = ""
                    selectedAIModelDescription = defaultAIModelDescription
                }
                break
            }
        }
    }
    fun selectAIModel(model: String, description: String) {
        if (selectedAIModel == model) return
        if (Pair(model, description) in availableAIModels) {
            selectedAIModel = model
            selectedAIModelDescription = description
            ChatViewModel.runBlocking {
                initializeModel(webSocketClient, model.lowercase())
            }
        }
    }
    fun deselectAIModel() {
        if (selectedAIModel.isEmpty()) return
        selectedAIModel = ""
        selectedAIModelDescription = defaultAIModelDescription
        ChatViewModel.runBlocking {
            initializeModel(webSocketClient)
        }
    }
    suspend fun initializeModel(
        client: ChatWebSocketClient,
        model: String = defaultAIModel,
        failureCallback: () -> Unit = {}
    ) {
        client.deleteSession()
        val result = client.createSession(model.lowercase())
        if (!result.isSuccess) {
            println("ERROR: Failed to create WebSocket session: ${result.exceptionOrNull()?.message}")
            failureCallback()
        }
    }

    var chatRoomList by mutableStateOf(mapOf<Int, Pair<Boolean, String>>())
    var selectedChatRoom by mutableStateOf(-1)
}
