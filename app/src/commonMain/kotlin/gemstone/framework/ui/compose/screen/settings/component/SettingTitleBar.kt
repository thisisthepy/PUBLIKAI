package gemstone.framework.ui.compose.screen.settings.component

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import org.jetbrains.compose.resources.DrawableResource
import gemstone.framework.ui.compose.theme.ClickAnimation
import gemstone.framework.ui.compose.theme.FluxIconButton
import gemstone.framework.ui.compose.theme.IconResource
import gemstone.framework.ui.compose.theme.SubtitleText


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
            iconResource = IconResource.Drawable(iconResource),
            iconDescription = iconDescription,
            clickAnimation = iconAnimation
        )
    }
}
