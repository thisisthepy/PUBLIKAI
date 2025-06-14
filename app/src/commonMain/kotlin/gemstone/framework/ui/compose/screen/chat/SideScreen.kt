package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.shape.CornerSize
import androidx.compose.material3.ButtonColors
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import gemstone.framework.ui.compose.screen.settings.component.SettingTitleBar
import gemstone.framework.ui.compose.theme.*
import gemstone.app.generated.resources.*
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.bell
import gemstone.app.generated.resources.search
import gemstone.app.generated.resources.sliders
import gemstone.framework.ui.viewmodel.AIModelViewModel
import gemstone.framework.ui.viewmodel.SettingsViewModel
import org.jetbrains.compose.resources.stringResource


@Composable
fun SideScreen(
    sideBarMode: Boolean = true,
    onChatSelected: (Int) -> Unit = { _ -> }
) {
    val modifier = when (sideBarMode) {
        false -> Modifier.fillMaxSize()
        true -> Modifier.fillMaxHeight().width(Dimen.SIDEBAR_WIDTH)
    }

    Column(modifier = modifier) {
        Spacer(modifier = Modifier.fillMaxWidth().padding(top = Dimen.LAYOUT_PADDING))

        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = Dimen.LAYOUT_PADDING),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TitleText(stringResource(Res.string.app_title), letterSpacing = (-1).sp, fontSize = 25.sp)
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            Row(
                modifier = Modifier,
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                BlurredFluxIconButton(
                    onClick = {},
                    iconResource = IconResource.Drawable(Res.drawable.bell),
                    iconDescription = stringResource(Res.string.sidebar_notification_section),
                    modifier = Modifier.size(Dimen.BIG_BUTTON_SIZE),
                    shape = MaterialTheme.shapes.large.copy(Dimen.BIG_BUTTON_CORNER_RADIUS),
                    contentPadding = PaddingValues(Dimen.BIG_BUTTON_PADDING)
                )
                Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
                PrimaryFluxButton(
                    onClick = { /* TODO: Handle new chat */ },
                    modifier = Modifier.size(Dimen.BIG_BUTTON_SIZE),
                    shape = MaterialTheme.shapes.large.copy(Dimen.BIG_BUTTON_CORNER_RADIUS)
                ) {
                    SubtitleText(SettingsViewModel.userName, fontWeight = FontWeight.ExtraLight, maxLines = 1)
                }
            }
        }

        Spacer(modifier = Modifier.height(Dimen.LAYOUT_PADDING))

//        SettingTitleBar(
//            title = stringResource(Res.string.sidebar_models_section),
//            iconResource = Res.drawable.sliders,
//            iconDescription = stringResource(Res.string.sidebar_models_section_desc),
//            modifier = Modifier.fillMaxWidth().padding(horizontal = Dimen.LAYOUT_PADDING)
//        )

        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = Dimen.LAYOUT_PADDING),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            SubtitleText(stringResource(Res.string.sidebar_models_section))
            SecondaryFluxIconButton(
                onClick = {},
                iconResource = IconResource.Drawable(Res.drawable.sliders),
                iconDescription = stringResource(Res.string.sidebar_models_section_desc),
                elevation = ButtonDefaults.elevatedButtonElevation(0.4.dp),
                shape = MaterialTheme.shapes.medium.copy(CornerSize(14.dp)),
                modifier = Modifier,
            )
        }

        LazyRow(
            modifier = Modifier.fillMaxWidth(),
            contentPadding = PaddingValues(horizontal = Dimen.LAYOUT_PADDING),
            horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING),
            verticalAlignment = Alignment.CenterVertically
        ) {
            for (modelInfo in listOf(Pair("All", "Using Default Model")) + AIModelViewModel.availableAIModels) {
                item(modelInfo) {
                    if (modelInfo.first == AIModelViewModel.selectedAIModel || modelInfo.first == "All") {
                        PrimaryFluxButton(
                            onClick = { AIModelViewModel.selectAIModel(modelInfo.first, modelInfo.second) },
                            shape = MaterialTheme.shapes.large.copy(Dimen.BIG_BUTTON_CORNER_RADIUS),
                            contentPadding = PaddingValues(Dimen.BIG_BUTTON_PADDING)
                        ) {
                            BodyText(modelInfo.first)
                        }
                    } else {
                        BlurredFluxButton(
                            onClick = { AIModelViewModel.selectAIModel(modelInfo.first, modelInfo.second) },
                            shape = MaterialTheme.shapes.large.copy(Dimen.BIG_BUTTON_CORNER_RADIUS),
                            contentPadding = PaddingValues(Dimen.BIG_BUTTON_PADDING)
                        ) {
                            BodyText(modelInfo.first)
                        }
                    }
                }
            }
        }

        val titlePlacement = mapOf(-2 to Pair(false, stringResource(Res.string.sidebar_recent_chats_section)))
        val newChatPlacement = mapOf(-1 to Pair(false, stringResource(Res.string.chat_title_placeholder)))
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(Dimen.LAYOUT_PADDING),
            verticalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING),
            reverseLayout = !sideBarMode
        ) {
            val list = when (sideBarMode) {
                true -> titlePlacement + newChatPlacement + AIModelViewModel.chatRoomList
                false -> newChatPlacement + AIModelViewModel.chatRoomList + titlePlacement
            }
            list.forEach { (key, value) ->
                item(key) {
                    if (key == -2) {
//                        SettingTitleBar(
//                            title = value.second,
//                            iconResource = Res.drawable.search,
//                            iconDescription = stringResource(Res.string.sidebar_recent_chats_section_desc),
//                            modifier = Modifier.fillMaxWidth()
//                        )
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            SubtitleText(value.second)
                            SecondaryFluxIconButton(
                                onClick = {},
                                iconResource = IconResource.Drawable(Res.drawable.search),
                                iconDescription = stringResource(Res.string.sidebar_recent_chats_section_desc),
                                elevation = ButtonDefaults.elevatedButtonElevation(0.4.dp),
                                shape = MaterialTheme.shapes.medium.copy(CornerSize(14.dp)),
                                modifier = Modifier,
                            )
                        }
                    } else {
                        BlurredFluxButton(
                            onClick = { onChatSelected(key) },
                            shape = MaterialTheme.shapes.large.copy(Dimen.SURFACE_CORNER_RADIUS),
                            clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                            elevation = Dimen.SURFACE_ELEVATIONS,
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.Start,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                SecondaryFluxIconButton(
                                    onClick = { onChatSelected(key) },
                                    iconResource = IconResource.Drawable(Res.drawable.arrow_up_right),
                                    iconDescription = "Open This Chat",
                                    modifier = Modifier,
                                    shape = MaterialTheme.shapes.extraLarge,
                                    elevation = ButtonDefaults.elevatedButtonElevation(0.dp)
                                )
                                SubtitleText(value.second, fontSize = 16.sp, fontWeight = FontWeight.Normal)
                            }
                        }
                    }
                }
            }
        }
    }
}
