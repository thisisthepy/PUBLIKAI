package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.mutableStateOf


object AIModelViewModel {
    val selectedAIModel = mutableStateOf("")
    val selectedAIModelDescription = mutableStateOf("")
    val availableAIModels = mutableStateOf(listOf<Pair<String, String>>())

    fun addAIModel(model: String, description: String) {
        val new = Pair(model, description)
        if (new !in availableAIModels.value) {
            availableAIModels.value += new
            if (selectedAIModel.value.isEmpty()) {
                selectAIModel(model, description)
            }
        }
    }
    fun removeAIModel(model: String) {
        for (pair in availableAIModels.value) {
            if (pair.first == model) {
                availableAIModels.value -= pair
                if (selectedAIModel.value == model) {
                    selectedAIModel.value = ""
                    selectedAIModelDescription.value = ""
                }
                break
            }
        }
    }
    fun selectAIModel(model: String, description: String) {
        if (Pair(model, description) in availableAIModels.value) {
            selectedAIModel.value = model
            selectedAIModelDescription.value = description
        }
    }
    fun deselectAIModel() {
        selectedAIModel.value = ""
        selectedAIModelDescription.value = ""
    }

    val chatRoomList = mutableStateOf(mapOf<Int, Pair<Boolean, String>>())
    val selectedChatRoom = mutableStateOf(-1)
    fun createChatRoom(chatId: Int, model: ChatViewModel) {
        chatRoomList.value += mapOf(chatId to Pair(model.starred, model.title))
        if (selectedChatRoom.value == -1) {
            selectedChatRoom.value = chatId
        }
    }
    fun removeChatRoom(chatId: Int) {
        chatRoomList.value = chatRoomList.value.filterNot { it.key == chatId }
        if (selectedChatRoom.value == chatId) {
            selectedChatRoom.value = -1
        }
    }
    fun selectChatRoom(chatId: Int) {
        if (chatId !in chatRoomList.value) return
        selectedChatRoom.value = chatId
    }
}
