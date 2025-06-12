package gemstone

import androidx.compose.runtime.Composable
import androidx.compose.material3.MaterialTheme
import gemstone.framework.ui.compose.screen.chat.MainScreen
import org.jetbrains.compose.ui.tooling.preview.Preview


@Composable
@Preview
fun App() {
    MaterialTheme {
        MainScreen()
    }
}

