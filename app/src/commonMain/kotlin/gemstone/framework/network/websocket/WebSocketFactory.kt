package gemstone.framework.network.websocket

import kotlinx.coroutines.flow.Flow


expect class WebSocketConnection {
    suspend fun connect(url: String)
    suspend fun send(message: String)
    fun receiveMessages(): Flow<String>
    suspend fun close()
}


expect object WebSocketFactory {
    fun create(): WebSocketConnection
}
