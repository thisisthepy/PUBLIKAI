package gemstone.framework.network.websocket

import kotlinx.coroutines.flow.*
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.callbackFlow
import org.w3c.dom.*


actual class WebSocketConnection {
    private var webSocket: WebSocket? = null
    private val messageChannel = Channel<String>(Channel.UNLIMITED)

    actual suspend fun connect(url: String) {
        webSocket = WebSocket(url).apply {
            onopen = {
                println("WebSocket connected")
            }

            onmessage = { event ->
                val message = event.data as String
                messageChannel.trySend(message)
            }

            onerror = { error ->
                println("WebSocket error: $error")
            }

            onclose = {
                println("WebSocket closed")
                messageChannel.close()
            }
        }
    }

    actual suspend fun send(message: String) {
        webSocket?.send(message)
    }

    actual fun receiveMessages(): Flow<String> {
        return messageChannel.receiveAsFlow()
    }

    actual suspend fun close() {
        webSocket?.close()
        messageChannel.close()
    }
}


actual object WebSocketFactory {
    actual fun create(): WebSocketConnection {
        return WebSocketConnection()
    }
}
