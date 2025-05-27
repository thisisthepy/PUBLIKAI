package fluxchat.framework.ui.compose.screen.chat

import androidx.compose.foundation.layout.*
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp


@Composable
fun MainScreen() {
    BoxWithConstraints {
        val isLandscape = maxWidth > maxHeight

        if (isLandscape) {
            // Landscape mode
            Row(
                modifier = Modifier.fillMaxSize().systemBarsPadding()
            ) {
                SideScreen(sideBarMode = true)
                VerticalDivider(modifier = Modifier.fillMaxHeight(), thickness = 0.2.dp)
                ChatScreen(0, "New Chat", "Qwen3 14B 4bitQ IT")
            }
        } else {
            // Portrait mode
            Column(
                modifier = Modifier.fillMaxSize().systemBarsPadding().padding(2.dp)
            ) {
                SideScreen(sideBarMode = false)
            }
        }
    }
}
