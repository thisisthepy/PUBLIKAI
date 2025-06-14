package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.chat_new_chat_icon_desc
import gemstone.app.generated.resources.chat_option_icon_desc
import gemstone.framework.ui.compose.theme.*
import gemstone.framework.ui.viewmodel.ChatViewModel
import org.jetbrains.compose.resources.stringResource


@Composable
fun ChatScreen() {
    Column(
        modifier = Modifier.fillMaxSize().padding(Dimen.LAYOUT_PADDING)
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

            Row(
                modifier = Modifier,
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING)
            ) {
                FluxIconButton(
                    onClick = { ChatViewModel.title += 1 },
                    iconResource = IconResource.Vector(Icons.Default.Add),
                    iconDescription = stringResource(Res.string.chat_new_chat_icon_desc)
                )
                FluxIconButton(
                    onClick = { /* TODO: Handle chat options */ },
                    iconResource = IconResource.Vector(Icons.Default.MoreHoriz),
                    iconDescription = stringResource(Res.string.chat_option_icon_desc)
                )
            }
        }
    }
}
