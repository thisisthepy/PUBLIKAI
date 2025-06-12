package gemstone.framework.ui.compose.theme

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.RowScope
import androidx.compose.foundation.layout.defaultMinSize
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import org.jetbrains.compose.resources.DrawableResource
import org.jetbrains.compose.resources.painterResource


@Composable
fun FluxButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING),
    content: @Composable RowScope.() -> Unit
) {
    val buttonModifier = when (hoverAnimation) {
        null -> modifier
        else -> modifier.pressHoverEffect(animation = hoverAnimation)
    }
    PulsateEffectButton(
        onClick = onClick,
        modifier = buttonModifier.defaultMinSize(minWidth = 1.dp, minHeight = 1.dp),
        animation = clickAnimation,
        enabled = enabled,
        interactionSource = interactionSource,
        elevation = elevation,
        shape = shape,
        border = border,
        colors = colors,
        contentPadding = contentPadding,
        content = content
    )
}

@Composable
fun FluxIconButton(
    onClick: () -> Unit,
    iconResource: DrawableResource,
    iconDescription: String,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.extraLarge,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING)
) {
    FluxButton(
        onClick = onClick,
        modifier = modifier,
        clickAnimation = clickAnimation,
        hoverAnimation = hoverAnimation,
        enabled = enabled,
        interactionSource = interactionSource,
        elevation = elevation,
        shape = shape,
        border = border,
        colors = colors,
        contentPadding = contentPadding
    ) {
        Icon(painterResource(iconResource), iconDescription, tint = colors.contentColor)
    }
}

@Composable
fun FluxIconButton(
    onClick: () -> Unit,
    iconResource: ImageVector,
    iconDescription: String,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.extraLarge,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING)
) {
    FluxButton(
        onClick = onClick,
        modifier = modifier,
        clickAnimation = clickAnimation,
        hoverAnimation = hoverAnimation,
        enabled = enabled,
        interactionSource = interactionSource,
        elevation = elevation,
        shape = shape,
        border = border,
        colors = colors,
        contentPadding = contentPadding
    ) {
        Icon(iconResource, iconDescription, tint = colors.contentColor)
    }
}

@Composable
fun FluxCard(

) {

}

