package gemstone.framework.network.websocket

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.websocket.*
import io.ktor.websocket.*
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers


actual class WebSocketConnection {
    private val client = HttpClient(CIO) {
        install(WebSockets)
    }
    private var session: DefaultClientWebSocketSession? = null
    private val messageChannel = Channel<String>(Channel.UNLIMITED)

    actual suspend fun connect(url: String) {
        client.webSocket(url) {
            session = this

            for (frame in incoming) {
                when (frame) {
                    is Frame.Text -> {
                        messageChannel.send(frame.readText())
                    }
                    else -> {}
                }
            }
        }
    }

    actual suspend fun send(message: String) {
        session?.send(Frame.Text(message))
    }

    actual fun receiveMessages(): Flow<String> {
        return messageChannel.receiveAsFlow()
    }

    actual suspend fun close() {
        session?.close()
        client.close()
        messageChannel.close()
    }
}


actual object WebSocketFactory {
    actual fun create(): WebSocketConnection {
        return WebSocketConnection()
    }
}
