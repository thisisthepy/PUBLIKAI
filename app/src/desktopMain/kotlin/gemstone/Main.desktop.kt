package gemstone

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.ui.Alignment
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.WindowPosition
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.app_name
import gemstone.app.generated.resources.simple_white
import gemstone.framework.ui.viewmodel.ChatViewModel
import kotlinx.coroutines.runBlocking
import org.jetbrains.compose.resources.painterResource
import org.jetbrains.compose.resources.stringResource
import org.jetbrains.jewel.intui.standalone.theme.IntUiTheme
import org.jetbrains.jewel.intui.window.DecoratedWindowIconKeys


fun main(args: Array<String>) = application {
    parseCommandLineArgs(args) {
        exitApplication()
    }

    IntUiTheme(
        isDark = isSystemInDarkTheme()
    ) {
        Window(
            onCloseRequest = {
                runBlocking {
                    ChatViewModel.onCleared()
                }
                exitApplication()
            },
            title = stringResource(Res.string.app_name),
            icon = painterResource(Res.drawable.simple_white),
            state = rememberWindowState(
                width = 1024.dp,
                height = 720.dp,
                position = WindowPosition.Aligned(Alignment.Center)
            ),
        ) {
            App()
        }
        DecoratedWindowIconKeys
    }
}


private fun parseCommandLineArgs(args: Array<String>, exitApplication: () -> Unit) {
    var i = 0
    while (i < args.size) {
        when (args[i]) {
            "--server", "-s" -> {
                if (i + 1 < args.size) {
                    val serverAddress = args[i + 1]
                    if (serverAddress.contains(":")) {
                        val parts = serverAddress.split(":", limit = 2)
                        System.setProperty("GEMSTONE_SERVER_HOST", parts[0])
                        System.setProperty("GEMSTONE_SERVER_PORT", ":${parts[1]}")
                    } else {
                        System.setProperty("GEMSTONE_SERVER_HOST", serverAddress)
                    }
                    i += 2
                } else {
                    println("Error: --server option requires a value")
                    i++
                }
            }
            "--host", "-h" -> {
                if (i + 1 < args.size) {
                    System.setProperty("GEMSTONE_SERVER_HOST", args[i + 1])
                    i += 2
                } else {
                    println("Error: --host option requires a value")
                    i++
                }
            }
            "--port", "-p" -> {
                if (i + 1 < args.size) {
                    System.setProperty("GEMSTONE_SERVER_PORT", ":${args[i + 1]}")
                    i += 2
                } else {
                    println("Error: --port option requires a value")
                    i++
                }
            }
            "--help" -> {
                printHelp()
                exitApplication()
            }
            else -> {
                if (args[i].startsWith("-")) {
                    println("Unknown option: ${args[i]}")
                }
                i++
            }
        }
    }
}


private fun printHelp() {
    println("""
        Gemstone Desktop Application
        
        Usage: gemstone [options]
        
        Options:
            --server, -s <address>    Server address (host:port format)
            --host, -h <host>         Server host (default: localhost)
            --port, -p <port>         Server port (default: 23100)
            --help                    Show this help message

        Examples:
            gemstone --server localhost:8080
            gemstone --host 192.168.1.100 --port 9000
            gemstone -s example.com:3000
    """.trimIndent())
}
