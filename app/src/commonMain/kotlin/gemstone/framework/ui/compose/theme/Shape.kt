package gemstone.framework.ui.compose.theme

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.border
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
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
fun PrimaryFluxButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_BLACK,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.primary,
        contentColor = MaterialTheme.colorScheme.onPrimary,
        disabledContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING),
    content: @Composable RowScope.() -> Unit
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
        contentPadding = contentPadding,
        content = content
    )
}

@Composable
fun SecondaryFluxButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_WHITE,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.secondary,
        contentColor = MaterialTheme.colorScheme.onSecondary,
        disabledContainerColor = MaterialTheme.colorScheme.secondary.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onSecondary.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING),
    content: @Composable RowScope.() -> Unit
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
        contentPadding = contentPadding,
        content = content
    )
}

@Composable
fun TertiaryFluxButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_BLACK,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.tertiary,
        contentColor = MaterialTheme.colorScheme.onTertiary,
        disabledContainerColor = MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onTertiary.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING),
    content: @Composable RowScope.() -> Unit
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
        contentPadding = contentPadding,
        content = content
    )
}

@Composable
fun BlurredFluxButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { NoRippleInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_WHITE,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = BorderStroke(1.4.dp, Color.White.copy(alpha = 0.9f)),
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.surface,
        contentColor = MaterialTheme.colorScheme.onSurface,
        disabledContainerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING),
    content: @Composable RowScope.() -> Unit
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
        contentPadding = contentPadding,
        content = content
    )
}

sealed class IconResource {
    data class Drawable(val resource: DrawableResource) : IconResource()
    data class Vector(val resource: ImageVector) : IconResource()
}

@Composable
fun FluxIconButton(
    onClick: () -> Unit,
    iconResource: IconResource,
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
        when (iconResource) {
            is IconResource.Drawable -> Icon(painterResource(iconResource.resource), iconDescription, tint = colors.contentColor)
            is IconResource.Vector -> Icon(iconResource.resource, iconDescription, tint = colors.contentColor)
        }
    }
}

@Composable
fun PrimaryFluxIconButton(
    onClick: () -> Unit,
    iconResource: IconResource,
    iconDescription: String,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_BLACK,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.primary,
        contentColor = MaterialTheme.colorScheme.onPrimary,
        disabledContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING)
) {
    FluxIconButton(
        onClick = onClick,
        iconResource = iconResource,
        iconDescription = iconDescription,
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
    )
}

@Composable
fun SecondaryFluxIconButton(
    onClick: () -> Unit,
    iconResource: IconResource,
    iconDescription: String,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_WHITE,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.secondary,
        contentColor = MaterialTheme.colorScheme.onSecondary,
        disabledContainerColor = MaterialTheme.colorScheme.secondary.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onSecondary.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING)
) {
    FluxIconButton(
        onClick = onClick,
        iconResource = iconResource,
        iconDescription = iconDescription,
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
    )
}

@Composable
fun TertiaryFluxIconButton(
    onClick: () -> Unit,
    iconResource: IconResource,
    iconDescription: String,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_BLACK,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.tertiary,
        contentColor = MaterialTheme.colorScheme.onTertiary,
        disabledContainerColor = MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onTertiary.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING)
) {
    FluxIconButton(
        onClick = onClick,
        iconResource = iconResource,
        iconDescription = iconDescription,
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
    )
}

@Composable
fun BlurredFluxIconButton(
    onClick: () -> Unit,
    iconResource: IconResource,
    iconDescription: String,
    modifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { NoRippleInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_WHITE,
    shape: Shape = MaterialTheme.shapes.large,
    border: BorderStroke? = BorderStroke(1.4.dp, Color.White.copy(alpha = 0.9f)),
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.surface,
        contentColor = MaterialTheme.colorScheme.onSurface,
        disabledContainerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING)
) {
    FluxIconButton(
        onClick = onClick,
        iconResource = iconResource,
        iconDescription = iconDescription,
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
    )
}

@Composable
fun BlurredFluxCard(
    onClick: () -> Unit,
    iconResource: IconResource,
    iconDescription: String,
    modifier: Modifier = Modifier,
    iconModifier: Modifier = Modifier,
    clickAnimation: ClickAnimation = Dimen.BUTTON_CLICK_ANIMATION,
    hoverAnimation: HoverAnimation? = Dimen.BUTTON_HOVER_ANIMATION,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { NoRippleInteractionSource() },
    elevation: ButtonElevation? = Dimen.BUTTON_ELEVATIONS_WHITE,
    shape: Shape = MaterialTheme.shapes.medium,
    iconShape: Shape = MaterialTheme.shapes.small,
    border: BorderStroke? = BorderStroke(1.4.dp, Color.White.copy(alpha = 0.9f)),
    colors: ButtonColors = ButtonColors(
        containerColor = MaterialTheme.colorScheme.surface,
        contentColor = MaterialTheme.colorScheme.onSurface,
        disabledContainerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.5f),
        disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
    ),
    contentPadding: PaddingValues = PaddingValues(Dimen.BUTTON_PADDING),
    content: @Composable ColumnScope.() -> Unit
) {
    BlurredFluxButton(
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
        Column(
            modifier = Modifier.fillMaxSize()
        ) {
            PrimaryFluxIconButton(
                onClick = onClick,
                iconResource = iconResource,
                iconDescription = iconDescription,
                modifier = iconModifier,
                hoverAnimation = null,
                enabled = enabled,
                interactionSource = remember { NoRippleInteractionSource() },
                elevation = null,
                shape = iconShape,
                contentPadding = PaddingValues(8.dp),
                colors = ButtonColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    contentColor = Color.White,
                    disabledContainerColor = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f),
                    disabledContentColor = Color.White.copy(alpha = 0.5f)
                )
            )
            content()
        }
    }
}
