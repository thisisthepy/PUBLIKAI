package gemstone.framework.network.http

import io.ktor.client.*


expect val defaultServerHost: String


expect object HttpClientFactory {
    fun create(): HttpClient
}
