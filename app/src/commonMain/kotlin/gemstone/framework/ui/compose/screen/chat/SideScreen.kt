package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
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

    Column(
        modifier = modifier.padding(Dimen.LAYOUT_PADDING)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TitleText(stringResource(Res.string.app_title), letterSpacing = (-1).sp, fontSize = 25.sp)
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            Row(
                modifier = Modifier,
                horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING),
                verticalAlignment = Alignment.CenterVertically
            ) {
                SecondaryFluxIconButton(
                    onClick = {},
                    iconResource = IconResource.Drawable(Res.drawable.bell),
                    iconDescription = stringResource(Res.string.sidebar_notification_section),
                    modifier = Modifier.size(Dimen.BIG_BUTTON_SIZE),
                    shape = MaterialTheme.shapes.large.copy(Dimen.BIG_BUTTON_CORNER_RADIUS),
                    contentPadding = PaddingValues(Dimen.BIG_BUTTON_PADDING)
                )
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

        SettingTitleBar(
            title = "Models",
            iconResource = Res.drawable.sliders,
            iconDescription = "Model Settings",
            modifier = Modifier.fillMaxWidth()
        )

        LazyRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING),
            verticalAlignment = Alignment.CenterVertically
        ) {
            for (modelInfo in listOf(Pair("All", "Using Default Model")) + AIModelViewModel.availableAIModels.value) {
                item(modelInfo) {
                    FluxButton(
                        onClick = { AIModelViewModel.selectAIModel(modelInfo.first, modelInfo.second) },

                    ) {
                        BodyText(modelInfo.first)
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(Dimen.LAYOUT_PADDING))

        SettingTitleBar(
            title = "Recent",
            iconResource = Res.drawable.search,
            iconDescription = "Search Recent Chats",
            modifier = Modifier.fillMaxWidth()
        )

        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING)
        ) {
            FluxButton(
                onClick = { onChatSelected(-1) },
                clickAnimation = ClickAnimation(1f, 0.99f),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Start,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    FluxIconButton(
                        onClick = { onChatSelected(-1) },
                        iconResource = IconResource.Drawable(Res.drawable.arrow_up_right),
                        iconDescription = "Open This Chat",
                        modifier = Modifier,
                        shape = MaterialTheme.shapes.extraLarge
                    )
                    SubtitleText("Daily Routine and Meals", fontSize = 16.sp, fontWeight = FontWeight.Normal)
                }
            }
        }
    }
}



