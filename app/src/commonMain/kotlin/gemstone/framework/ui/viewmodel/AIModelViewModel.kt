package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue


object AIModelViewModel {
    var selectedAIModel by mutableStateOf("")
    var selectedAIModelDescription by mutableStateOf("")
    var availableAIModels by mutableStateOf(listOf<Pair<String, String>>())

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
                    selectedAIModelDescription = ""
                }
                break
            }
        }
    }
    fun selectAIModel(model: String, description: String) {
        if (Pair(model, description) in availableAIModels) {
            selectedAIModel = model
            selectedAIModelDescription = description
        }
    }
    fun deselectAIModel() {
        selectedAIModel = ""
        selectedAIModelDescription = ""
    }

    var chatRoomList by mutableStateOf(mapOf<Int, Pair<Boolean, String>>())
    var selectedChatRoom by mutableStateOf(-1)
    fun createChatRoom(chatId: Int, model: ChatViewModel) {
        chatRoomList += mapOf(chatId to Pair(model.starred, model.title))
        if (selectedChatRoom == -1) {
            selectedChatRoom = chatId
        }
    }
    fun removeChatRoom(chatId: Int) {
        chatRoomList = chatRoomList.filterNot { it.key == chatId }
        if (selectedChatRoom == chatId) {
            selectedChatRoom = -1
        }
    }
    fun selectChatRoom(chatId: Int) {
        if (chatId !in chatRoomList) return
        selectedChatRoom = chatId
    }
}
