package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import gemstone.framework.ui.compose.theme.CaptionText
import gemstone.framework.ui.compose.theme.Dimen
import gemstone.framework.ui.compose.theme.FluxIconButton
import gemstone.framework.ui.compose.theme.TitleText


@Composable
fun ChatScreen(
    chatId: Int,
    chatName: String,
    modelDescription: String
) {
    Column(
        modifier = Modifier.fillMaxSize().padding(Dimen.LAYOUT_PADDING)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.Top
        ) {
            Column(
                modifier = Modifier,
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.Start
            ) {
                TitleText(chatName)
                CaptionText(modelDescription)
            }

            Row(
                modifier = Modifier,
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING)
            ) {
                FluxIconButton(
                    onClick = { /* Handle back navigation */ },
                    iconResource = Icons.Default.Add,
                    iconDescription = "Start new chat"
                )
                FluxIconButton(
                    onClick = { /* Handle back navigation */ },
                    iconResource = Icons.Default.MoreHoriz,
                    iconDescription = "Chatting options"
                )
            }
        }
    }
}
