package gemstone

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.app_name
import gemstone.app.generated.resources.simple_white
import gemstone.framework.ui.viewmodel.ChatViewModel
import org.jetbrains.compose.resources.painterResource
import org.jetbrains.compose.resources.stringResource
import org.jetbrains.jewel.intui.standalone.theme.IntUiTheme
import org.jetbrains.jewel.intui.window.DecoratedWindowIconKeys


fun main() = application {
    IntUiTheme(
        isDark = isSystemInDarkTheme()
    ) {
        Window(
            onCloseRequest = {
                ChatViewModel.onCleared()
                exitApplication()
            },
            title = stringResource(Res.string.app_name),
            icon = painterResource(Res.drawable.simple_white)
        ) {
            App()
        }
        DecoratedWindowIconKeys
    }
}
