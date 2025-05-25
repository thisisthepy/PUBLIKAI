package io.github.thisisthepy.fluxchat

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform