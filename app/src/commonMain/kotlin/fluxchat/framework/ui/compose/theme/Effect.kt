package fluxchat.framework.ui.compose.theme

import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.waitForUpOrCancellation
import androidx.compose.foundation.interaction.Interaction
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsHoveredAsState
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.emptyFlow


/**
 * Non-Clickable Animation Button
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun NoClickEffectButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { NoRippleInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.small,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable RowScope.() -> Unit
) {
    Button(onClick, modifier, enabled, shape, colors, elevation, border, contentPadding, interactionSource, content)
}

class NoRippleInteractionSource : MutableInteractionSource {

    override val interactions: Flow<Interaction> = emptyFlow()

    override suspend fun emit(interaction: Interaction) {}

    override fun tryEmit(interaction: Interaction) = true
}


/**
 * Box can be clicked but not animated
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun NoRippleEffectBox(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    shape: Shape = MaterialTheme.shapes.small,
    color: Color = MaterialTheme.colorScheme.primary,
    contentAlignment: Alignment = Alignment.Center,
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable BoxScope.() -> Unit
) {
    Box(
        modifier = modifier
            .background(
                color = color,
                shape = shape
            )
            .clickable(
                interactionSource = interactionSource,
                indication = null,
                enabled = enabled,
                onClick = onClick
            )
            .padding(contentPadding),
        contentAlignment = contentAlignment,
        content = content
    )
}

enum class ButtonState { Pressed, Idle }

data class ClickAnimation(val initial: Float, val transformTo: Float)
data class HoverAnimation(val initial: Float, val transformTo: Float)


/**
 * Pulsate effect Button
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun PulsateEffectButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    animation: ClickAnimation = ClickAnimation(1f, 0.9f),
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.small,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable RowScope.() -> Unit
) {
    Button(onClick, modifier.bounceClick(animation), enabled, shape, colors, elevation, border, contentPadding, interactionSource, content)
}

/**
 * Pulsate effect
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun Modifier.bounceClick(
    animation: ClickAnimation = ClickAnimation(1f, 0.9f),
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    indication: Indication? = null,
    onClick: () -> Unit = {}
) = composed {
    var buttonState by remember { mutableStateOf(ButtonState.Idle) }
    val scale by animateFloatAsState(
        if (buttonState == ButtonState.Pressed) animation.transformTo else animation.initial
    )

    this
        .graphicsLayer {
            scaleX = scale
            scaleY = scale
        }
        .clickable(
            interactionSource = interactionSource,
            indication = indication,
            onClick = onClick
        )
        .pointerInput(buttonState) {
            awaitPointerEventScope {
                buttonState = if (buttonState == ButtonState.Pressed) {
                    waitForUpOrCancellation()
                    ButtonState.Idle
                } else {
                    awaitFirstDown(false)
                    ButtonState.Pressed
                }
            }
        }
}


/**
 * Press effect Button
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun PressEffectButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    animation: ClickAnimation = ClickAnimation(0f, -10f),
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.small,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable RowScope.() -> Unit
) {
    Button(onClick, modifier.pressClickEffect(animation), enabled, shape, colors, elevation, border, contentPadding, interactionSource, content)
}

/**
 * Press effect
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun Modifier.pressClickEffect(
    animation: ClickAnimation = ClickAnimation(0f, -10f),
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    indication: Indication? = null,
    onClick: () -> Unit = {}
) = composed {
    var buttonState by remember { mutableStateOf(ButtonState.Idle) }
    val ty by animateFloatAsState(
        if (buttonState == ButtonState.Pressed) animation.transformTo else animation.initial
    )

    this
        .graphicsLayer {
            translationY = ty
        }
        .clickable(
            interactionSource = interactionSource,
            indication = indication,
            onClick = onClick
        )
        .pointerInput(buttonState) {
            awaitPointerEventScope {
                buttonState = if (buttonState == ButtonState.Pressed) {
                    waitForUpOrCancellation()
                    ButtonState.Idle
                } else {
                    awaitFirstDown(false)
                    ButtonState.Pressed
                }
            }
        }
}
@Composable
fun Modifier.pressHoverEffect(
    animation: HoverAnimation = HoverAnimation(0f, -10f),
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() }
) = composed {
    val isHovered by interactionSource.collectIsHoveredAsState()
    val ty by animateFloatAsState(
        if (isHovered) animation.transformTo else animation.initial
    )

    this
        .graphicsLayer {
            translationY = ty
        }
        .hoverable(
            interactionSource = interactionSource
        )
}


/**
 * Shake effect Button
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun ShakeEffectButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    animation: ClickAnimation = ClickAnimation(0f, 50f),
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    shape: Shape = MaterialTheme.shapes.small,
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable RowScope.() -> Unit
) {
    Button(onClick, modifier.shakeClickEffect(animation), enabled, shape, colors, elevation, border, contentPadding, interactionSource, content)
}

/**
 * Shake effect
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun Modifier.shakeClickEffect(
    animation: ClickAnimation = ClickAnimation(0f, 50f),
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    indication: Indication? = null,
    onClick: () -> Unit = {}
) = composed {
    var buttonState by remember { mutableStateOf(ButtonState.Idle) }
    val tx by animateFloatAsState(
        targetValue = if (buttonState == ButtonState.Pressed) animation.transformTo else animation.initial,
        animationSpec = repeatable(
            iterations = 3,
            animation = tween(durationMillis = 50, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        )
    )

    this
        .graphicsLayer {
            translationX = tx
        }
        .clickable(
            interactionSource = interactionSource,
            indication = indication,
            onClick = onClick
        )
        .pointerInput(buttonState) {
            awaitPointerEventScope {
                buttonState = if (buttonState == ButtonState.Pressed) {
                    waitForUpOrCancellation()
                    ButtonState.Idle
                } else {
                    awaitFirstDown(false)
                    ButtonState.Pressed
                }
            }
        }
}


/**
 * Transform effect Button
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun AnimatedShapeButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    radiusAnimation: ClickAnimation = ClickAnimation(50f, 20f),
    sizeAnimation: ClickAnimation = ClickAnimation(100f, 80f),
    enabled: Boolean = true,
    interactionSource: MutableInteractionSource = remember { MutableInteractionSource() },
    elevation: ButtonElevation? = ButtonDefaults.buttonElevation(),
    border: BorderStroke? = null,
    colors: ButtonColors = ButtonDefaults.buttonColors(),
    contentPadding: PaddingValues = ButtonDefaults.ContentPadding,
    content: @Composable RowScope.() -> Unit
) {
    val isPressed = interactionSource.collectIsPressedAsState()
    val cornerRadius by animateDpAsState(
        if (isPressed.value) radiusAnimation.transformTo.dp else radiusAnimation.initial.dp
    )
    val size by animateDpAsState(
        if (isPressed.value) sizeAnimation.transformTo.dp else sizeAnimation.initial.dp
    )
    Button(
        onClick,
        modifier
            .size(size)
            .clickable(
                interactionSource = interactionSource,
                indication = null,
                onClick = { }
            ),
        enabled,
        RoundedCornerShape(cornerRadius),
        colors, elevation, border, contentPadding, interactionSource, content)
}

/**
 * Transform effect
 * @see <a href="https://blog.canopas.com/jetpack-compose-cool-button-click-effects-c6bbecec7bcb">Cool Button Click Effects</a>
 */
@Composable
fun Modifier.shapeAnimationEffect(
    radiusAnimation: ClickAnimation = ClickAnimation(50f, 20f),
    sizeAnimation: ClickAnimation = ClickAnimation(100f, 80f),
    indication: Indication? = null,
    onClick: () -> Unit = {}
) = composed {
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed = interactionSource.collectIsPressedAsState()
    val cornerRadius by animateDpAsState(
        if (isPressed.value) radiusAnimation.transformTo.dp else radiusAnimation.initial.dp
    )
    val size by animateDpAsState(
        if (isPressed.value) sizeAnimation.transformTo.dp else sizeAnimation.initial.dp
    )

    this
        .size(size)
        .clip(RoundedCornerShape(cornerRadius))
        .clickable(
            interactionSource = interactionSource,
            indication = indication,
            onClick = onClick
        )
}
