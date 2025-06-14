package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.chat_title_placeholder
import kotlinx.serialization.Serializable
import org.jetbrains.compose.resources.stringResource


@Serializable
data class ChatHistory(
    val role: Int,
    val content: String = "",
    val tool_call_id: String
)


object ChatViewModel {
    var chatId by mutableStateOf(-1)
    var title by mutableStateOf("")
    var starred by mutableStateOf(false)
    var modelName = AIModelViewModel.selectedAIModel
    var modelDescription = AIModelViewModel.defaultAIModelDescription

    var messageInput by mutableStateOf("")

    fun clear(newTitle: String = "") {
        chatId = -1
        title = newTitle
        starred = false
        messageInput = ""
        messageHistory = listOf()
    }

    @Composable
    fun getTitleOrPlaceholder(): String {
        return title.ifEmpty { stringResource(Res.string.chat_title_placeholder) }
    }

    fun toggleStarred() {
        starred = !starred
    }

    fun sendMessage() {
        messageInput = ""
    }

    var messageHistory by mutableStateOf(listOf<String>())
        private set
}
