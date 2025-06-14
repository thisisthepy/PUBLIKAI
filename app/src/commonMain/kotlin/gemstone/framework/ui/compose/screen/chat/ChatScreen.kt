package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import gemstone.app.generated.resources.*
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.chat_new_chat_icon_desc
import gemstone.app.generated.resources.chat_option_icon_desc
import gemstone.app.generated.resources.chat_title_placeholder
import gemstone.framework.ui.compose.theme.*
import gemstone.framework.ui.viewmodel.AIModelViewModel
import gemstone.framework.ui.viewmodel.ChatViewModel
import gemstone.framework.ui.viewmodel.ChatViewModel.messageHistory
import org.jetbrains.compose.resources.stringResource


@Composable
fun ChatScreen(screenWidth: Dp) {
    Column(
        modifier = Modifier.fillMaxSize().imePadding().padding(Dimen.LAYOUT_PADDING)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.End,
            verticalAlignment = Alignment.Top
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.Start
            ) {
                TitleText(ChatViewModel.getTitleOrPlaceholder(), maxLines = 1)
                CaptionText(ChatViewModel.modelDescription)
            }

            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))

            Row(
                modifier = Modifier,
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.End
            ) {
                val newChatTitle = stringResource(Res.string.chat_title_placeholder)
                PrimaryFluxIconButton(
                    onClick = {
                        ChatViewModel.chatId = -1
                        ChatViewModel.title = newChatTitle
                        ChatViewModel.starred = false
                        AIModelViewModel.createChatRoom(-1, ChatViewModel)
                    },
                    iconResource = IconResource.Vector(Icons.Default.Add),
                    iconDescription = stringResource(Res.string.chat_new_chat_icon_desc),
                    shape = MaterialTheme.shapes.extraLarge
                )
                SecondaryFluxIconButton(
                    onClick = { /* TODO: Handle chat options */ },
                    iconResource = IconResource.Vector(Icons.Default.MoreHoriz),
                    iconDescription = stringResource(Res.string.chat_option_icon_desc),
                    shape = MaterialTheme.shapes.extraLarge
                )
            }
        }

        LazyColumn(
            modifier = Modifier.fillMaxWidth().weight(1f),
            verticalArrangement = when (messageHistory.size) {
                0 -> Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING)
                else -> Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING, Alignment.Top)
            }
        ) {
            if (messageHistory.size == 0) {
                item {

                }
            } else {
                for (message in messageHistory) {
                    item {
                        MessageBubble(
                            message = message,
                            modifier = Modifier.fillMaxWidth().padding(Dimen.LIST_ELEMENT_SPACING)
                        )
                    }
                }
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth().padding(top = Dimen.LAYOUT_PADDING),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            SecondaryFluxButton(
                onClick = {},
                modifier = if (screenWidth >= 750.dp) Modifier.width(700.dp) else Modifier.weight(1f),
                elevation = ButtonDefaults.buttonElevation(0.4.dp),
                clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                hoverAnimation = null,
                interactionSource = remember { NoRippleInteractionSource() },
                enabled = false,
                shape = MaterialTheme.shapes.extraLarge,
                contentPadding = PaddingValues(0.dp)
            ) {
                TertiaryFluxIconButton(
                    onClick = {},
                    iconResource = IconResource.Drawable(Res.drawable.paperclip),
                    iconDescription = "Attach",
                    shape = MaterialTheme.shapes.extraLarge,
                    elevation = ButtonDefaults.buttonElevation(0.dp)
                )
                val placeholder = stringResource(Res.string.chat_message_placeholder)
                val modelName = ChatViewModel.modelName
                val placeholderWithModelName = if (modelName.isNotEmpty()) {
                    placeholder.replace("me", modelName)
                } else {
                    placeholder
                }
                BasicTextField(
                    value = ChatViewModel.messageInput,
                    onValueChange = { ChatViewModel.messageInput = it },
                    modifier = Modifier.weight(1f).padding(vertical = 6.dp),
                    textStyle = TextStyle(
                        color = MaterialTheme.colorScheme.onSecondary,
                        fontFamily = SuiteFontFamily
                    ),
                    decorationBox = { innerTextField ->
                        if (ChatViewModel.messageInput.isEmpty()) {
                            Text(
                                text = placeholderWithModelName,
                                style = TextStyle(color = Color.Gray)
                            )
                        }
                        innerTextField()
                    }
                )
            }
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            PrimaryFluxIconButton(
                onClick = { ChatViewModel.sendMessage() },
                iconResource = IconResource.Drawable(Res.drawable.arrow_up),
                iconDescription = "Send",
                shape = MaterialTheme.shapes.extraLarge,
                modifier = Modifier.size(44.dp)
            )
        }
    }
}


fun MessageBubble(message: String, modifier: Any) {

}
