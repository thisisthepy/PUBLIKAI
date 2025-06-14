package gemstone

import androidx.compose.runtime.Composable
import org.jetbrains.compose.ui.tooling.preview.Preview
import gemstone.framework.ui.compose.screen.chat.MainScreen
import gemstone.framework.ui.compose.theme.GemstoneTheme


@Composable
@Preview
fun App() {
    GemstoneTheme {
        MainScreen()
    }
}
