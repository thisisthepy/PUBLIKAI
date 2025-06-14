package gemstone.framework.ui.compose.theme

import androidx.compose.foundation.shape.CornerSize
import androidx.compose.material3.ButtonDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp


object Dimen {
    // App settings
    val SIDEBAR_WIDTH = 300.dp

    // Layout settings
    val LAYOUT_PADDING = 16.dp
    val LIST_ELEMENT_SPACING = 6.dp

    // Button settings
    val BUTTON_PADDING = 8.dp
    val BUTTON_ELEVATION_WHITE = 22.dp
    val BUTTON_ELEVATION_BLACK = 22.dp
    val BUTTON_ELEVATIONS_WHITE
        @Composable get() = ButtonDefaults.buttonElevation(
            defaultElevation = BUTTON_ELEVATION_WHITE,
            pressedElevation = BUTTON_ELEVATION_WHITE * 0.8f,
            hoveredElevation = BUTTON_ELEVATION_WHITE * 0.9f,
            focusedElevation = BUTTON_ELEVATION_WHITE * 0.9f,
            disabledElevation = BUTTON_ELEVATION_WHITE * 0.5f
        )
    val BUTTON_ELEVATIONS_BLACK
        @Composable get() = ButtonDefaults.buttonElevation(
        defaultElevation = BUTTON_ELEVATION_BLACK,
        pressedElevation = BUTTON_ELEVATION_BLACK * 0.8f,
        hoveredElevation = BUTTON_ELEVATION_BLACK * 0.9f,
        focusedElevation = BUTTON_ELEVATION_BLACK * 0.9f,
        disabledElevation = BUTTON_ELEVATION_BLACK * 0.5f
    )
    val BUTTON_CLICK_ANIMATION = ClickAnimation(1f, 0.95f)
    val BUTTON_HOVER_ANIMATION = HoverAnimation(0f, -2f)
    val BIG_BUTTON_PADDING = 14.dp
    val BIG_BUTTON_SIZE = 48.dp
    val BIG_BUTTON_CORNER_RADIUS = CornerSize(20.dp)
}
