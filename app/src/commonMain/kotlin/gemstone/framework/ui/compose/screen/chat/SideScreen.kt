package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import gemstone.framework.ui.compose.screen.settings.component.SettingTitleBar
import gemstone.framework.ui.compose.theme.*
import gemstone.app.generated.resources.*
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.bell
import gemstone.app.generated.resources.search
import gemstone.app.generated.resources.sliders


@Composable
fun SideScreen(
    sideBarMode: Boolean = true
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
            TitleText("Gemstone")
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            Row(
                modifier = Modifier,
                horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING),
                verticalAlignment = Alignment.CenterVertically
            ) {
                FluxIconButton(
                    onClick = {},
                    iconResource = Res.drawable.bell,
                    iconDescription = "Notifications",
                    modifier = Modifier,
                    shape = MaterialTheme.shapes.large
                )
                FluxButton(
                    onClick = { /* TODO: Handle new chat */ }
                ) {
                    SubtitleText("CU", fontWeight = FontWeight.ExtraLight)
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

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING),
            verticalAlignment = Alignment.CenterVertically
        ) {
            FluxButton(onClick = { /* TODO: Handle new chat */ }) {
                BodyText("Qwen3")
            }
            FluxButton(onClick = { /* TODO: Handle new chat */ }) {
                BodyText("Llama3.2")
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
                onClick = { /* TODO: Handle new chat */ },
                clickAnimation = ClickAnimation(1f, 0.98f),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Start,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    FluxIconButton(
                        onClick = { /* TODO: Handle chat settings */ },
                        iconResource = Res.drawable.arrow_up_right,
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



