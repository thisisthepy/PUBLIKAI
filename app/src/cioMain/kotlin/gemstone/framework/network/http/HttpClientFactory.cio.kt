package gemstone.framework.network.http

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.websocket.*
import io.ktor.serialization.kotlinx.json.*


actual val defaultServerHost: String = (
    System.getenv("GEMSTONE_SERVER_HOST") ?: "localhost"
) + (
    System.getenv("GEMSTONE_SERVER_PORT") ?: ":23100"
)


actual object HttpClientFactory {
    actual fun create(): HttpClient {
        return HttpClient(CIO) {
            install(ContentNegotiation) {
                json()
            }
            install(WebSockets)
            engine {
                maxConnectionsCount = 1000
                endpoint {
                    maxConnectionsPerRoute = 100
                    pipelineMaxSize = 20
                    keepAliveTime = 5000
                    connectTimeout = 5000
                    requestTimeout = 15000
                }
            }
        }
    }
}
