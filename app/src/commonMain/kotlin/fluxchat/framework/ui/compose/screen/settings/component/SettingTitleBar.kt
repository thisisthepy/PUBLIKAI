package fluxchat.framework.ui.compose.screen.settings.component

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import fluxchat.framework.ui.compose.theme.ClickAnimation
import fluxchat.framework.ui.compose.theme.FluxIconButton
import fluxchat.framework.ui.compose.theme.SubtitleText
import org.jetbrains.compose.resources.DrawableResource


@Composable
fun SettingTitleBar(
    title: String,
    iconResource: DrawableResource,
    iconDescription: String = "",
    iconAnimation: ClickAnimation = ClickAnimation(0f, -10f),
    modifier: Modifier = Modifier,
    onClick: () -> Unit = { /* Default no-op */ }
) {
    Row(
        modifier = modifier,
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        SubtitleText(title)
        FluxIconButton(
            onClick = onClick,
            iconResource = iconResource,
            iconDescription = iconDescription,
            clickAnimation = iconAnimation
        )
    }
}
