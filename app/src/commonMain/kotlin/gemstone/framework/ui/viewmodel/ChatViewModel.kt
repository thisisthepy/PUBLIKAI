package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.chat_title_placeholder
import org.jetbrains.compose.resources.stringResource


object ChatViewModel {
    var chatId by mutableStateOf(-1)
        private set
    var title by mutableStateOf("")
    var starred by mutableStateOf(false)
    var modelDescription by mutableStateOf("")

    @Composable
    fun getTitleOrPlaceholder(): String {
        return title.ifEmpty { stringResource(Res.string.chat_title_placeholder) }
    }

    fun toggleStarred() {
        starred = !starred
    }

    var messageInput by mutableStateOf("")
        private set

    fun sendMessage() {
        messageInput = ""
    }
}
