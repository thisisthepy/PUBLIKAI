package gemstone.framework.ui.compose.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable


@Composable
fun GemstoneTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = AppColorSet.currentAppColorSet.materialColorScheme,
        content = content
    )
}
