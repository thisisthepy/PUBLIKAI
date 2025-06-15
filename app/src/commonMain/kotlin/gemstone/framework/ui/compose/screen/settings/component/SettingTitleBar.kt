package gemstone.framework.ui.compose.screen.settings.component

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import gemstone.framework.ui.compose.theme.*
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
        SecondaryFluxIconButton(
            onClick = onClick,
            iconResource = IconResource.Drawable(iconResource),
            iconDescription = iconDescription,
            modifier = Modifier,
            clickAnimation = iconAnimation
        )
    }
}
