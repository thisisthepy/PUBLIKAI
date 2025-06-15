package gemstone.framework.network.http

import io.ktor.client.*
import io.ktor.client.engine.js.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.websocket.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.browser.window


actual val defaultServerHost: String = window.location.host


actual object HttpClientFactory {
    actual fun create(): HttpClient {
        return HttpClient(Js) {
            install(ContentNegotiation) {
                json()
            }
            install(WebSockets)
        }
    }
}
