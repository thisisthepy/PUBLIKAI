package gemstone.framework.ui.compose.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color


abstract class AppColorSet {
    abstract val materialColorScheme: ColorScheme

    val appBackgroundColorStart: Color
        get() = materialColorScheme.background
    abstract val appBackgroundColorEnd: Color

    companion object {
        enum class ColorSet {
            Black, Blue, Orange
        }

        val currentColorSet: ColorSet = ColorSet.Black  // Black is the default color set

        val isLight
            @Composable get() = !isSystemInDarkTheme()

        val currentColorScheme
            @Composable get() = MaterialTheme.colorScheme

        val currentAppColorSet
            @Composable get() = when (currentColorSet) {
                ColorSet.Black -> if (isLight) BlackLightColorSet else BlackDarkColorSet
                ColorSet.Blue -> if (isLight) BlackLightColorSet else BlackDarkColorSet
                ColorSet.Orange -> if (isLight) BlackLightColorSet else BlackDarkColorSet
            }
    }
}


val appColorSet
    @Composable get() = AppColorSet.currentAppColorSet


object BlackLightColorSet: AppColorSet() {
    override val materialColorScheme = lightColorScheme(
        primary = Color(0xFF262626),
        onPrimary = Color(0xFFBEBEBE),
        secondary = Color.White.copy(alpha = 0.7f),
        onSecondary = Color(0xFF414244),
        tertiary = Color(0xFFD6D6D6),
        onTertiary = Color(0xFF414244),
        background = Color(0xFFF2F2F2),
        onBackground = Color(0xFF262626),
        surface = Color(0x66FFFFFF),
        onSurface = Color(0xFF414244)
    )
    override val appBackgroundColorEnd: Color = Color(0xFFEFEFEF)
}


object BlackDarkColorSet: AppColorSet() {
    override val materialColorScheme = darkColorScheme(
        primary = Color(0xFF262626),
        onPrimary = Color(0xFFBEBEBE),
        secondary = Color.White,
        onSecondary = Color(0xFF414244),
        tertiary = Color(0xFFD6D6D6),
        onTertiary = Color(0xFF414244),
        background = Color(0xFFF2F2F2),
        onBackground = Color(0xFF262626),
        surface = Color(0x66FFFFFF),
        onSurface = Color(0xFF414244)
    )
    override val appBackgroundColorEnd: Color = Color(0xFFEFEFEF)
}
