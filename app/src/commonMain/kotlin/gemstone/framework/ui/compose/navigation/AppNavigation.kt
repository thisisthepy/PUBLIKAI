package gemstone.framework.ui.compose.navigation

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.navigation.NavGraphBuilder
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import kotlin.math.min
import kotlin.math.roundToInt


/**
 * iOS 스타일 스와이프 백 제스처가 적용된 NavHost 컴포저블
 *
 * @param navController 네비게이션 컨트롤러
 * @param startDestination 시작 목적지
 * @param modifier 수정자
 * @param enableHaptics 햅틱 피드백 활성화 여부
 * @param swipeThreshold 뒤로가기가 실행되는 임계값 (0.0 ~ 1.0)
 * @param edgeWidth 스와이프가 감지되는 가장자리 영역의 너비 (dp)
 * @param builder NavHost의 콘텐츠
 */
@Composable
fun SwipeBackNavHost(
    navController: NavHostController,
    startDestination: Any,
    modifier: Modifier = Modifier,
    enableHaptics: Boolean = true,
    swipeThreshold: Float = 0.4f,
    edgeWidth: Float = 150f,
    builder: NavGraphBuilder.() -> Unit
) {
    val density = LocalDensity.current
    val hapticFeedback = LocalHapticFeedback.current
    var screenWidth by remember { mutableFloatStateOf(0f) }
    val edgeWidthPx = with(density) { edgeWidth.dp.toPx() }

    var dragOffset by remember { mutableFloatStateOf(0f) }
    var isDragging by remember { mutableStateOf(false) }
    var isSwipeBack by remember { mutableStateOf(false) }
    var lastHapticThreshold by remember { mutableIntStateOf(0) }

    val currentBackStackEntry by navController.currentBackStackEntryAsState()
    val canNavigateBack by remember(currentBackStackEntry) {
        derivedStateOf { navController.previousBackStackEntry != null }
    }

    val animatedOffset by animateFloatAsState(
        targetValue = if (isDragging) dragOffset else 0f,
        animationSpec = if (isDragging) {
            tween(0) // 드래그 중에는 즉시 반응
        } else {
            spring(
                dampingRatio = Spring.DampingRatioNoBouncy,
                stiffness = Spring.StiffnessMedium
            )
        },
        label = "drag_offset"
    )

    LaunchedEffect(dragOffset, enableHaptics) {
        if (!enableHaptics || !isDragging) return@LaunchedEffect

        val progress = (dragOffset / screenWidth * 100).toInt()

        when {
            progress >= 70 && lastHapticThreshold < 70 -> {
                hapticFeedback.performHapticFeedback(HapticFeedbackType.LongPress)
                lastHapticThreshold = 70
            }
            progress >= 40 && lastHapticThreshold < 40 -> {
                hapticFeedback.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                lastHapticThreshold = 40
            }
            progress >= 20 && lastHapticThreshold < 20 -> {
                hapticFeedback.performHapticFeedback(HapticFeedbackType.TextHandleMove)
                lastHapticThreshold = 20
            }
            progress < 20 -> {
                lastHapticThreshold = 0
            }
        }
    }

    BoxWithConstraints(
        modifier = modifier.fillMaxSize()
    ) {
        screenWidth = constraints.maxWidth.toFloat()

        Box(
            modifier = Modifier
                .fillMaxSize()
                .pointerInput(canNavigateBack) {
                    if (!canNavigateBack) return@pointerInput

                    detectDragGestures(
                        onDragStart = { offset ->
                            if (offset.x <= edgeWidthPx) {
                                isDragging = true
                                lastHapticThreshold = 0
                            }
                        },
                        onDragEnd = {
                            if (isDragging) {
                                val threshold = screenWidth * swipeThreshold
                                if (dragOffset > threshold) {
                                    if (enableHaptics) {
                                        hapticFeedback.performHapticFeedback(HapticFeedbackType.LongPress)
                                    }
                                    isSwipeBack = true
                                    navController.popBackStack()
                                } else {
                                    dragOffset = 0f
                                }
                                isDragging = false
                                lastHapticThreshold = 0
                            }
                        },
                        onDrag = { _, dragAmount ->
                            if (isDragging) {
                                val runningRatio = dragOffset / screenWidth
                                val newOffset = (dragOffset + dragAmount.x)
                                    .coerceIn(0f, screenWidth)
                                val newRunningRatio = newOffset / screenWidth - runningRatio
                                dragOffset = (newRunningRatio * edgeWidthPx + newOffset).coerceIn(0f, screenWidth)
                            }
                        }
                    )
                }
        ) {
            val previousEntry = navController.previousBackStackEntry
            if (previousEntry != null && isDragging) {
                NavHost(
                    navController = rememberNavController(),
                    startDestination = startDestination,
                    modifier = Modifier
                        .fillMaxSize()
                        .graphicsLayer {
                            translationX = (animatedOffset - screenWidth) / 2
                            alpha = (animatedOffset / screenWidth * 1f).coerceIn(0f, 1f)
                        },
                    builder = builder
                )
            }
            NavHost(
                navController = navController,
                startDestination = startDestination,
                modifier = Modifier
                    .fillMaxSize()
                    .graphicsLayer {
                        translationX = animatedOffset
                    },
                enterTransition = {
                    slideInHorizontally(
                        initialOffsetX = { it },
                        animationSpec = tween(300, easing = FastOutSlowInEasing)
                    )
                },
                exitTransition = {
                    slideOutHorizontally(
                        targetOffsetX = { it },
                        animationSpec = tween(300, easing = FastOutSlowInEasing)
                    )
                },
                popEnterTransition = {
                    EnterTransition.None
                },
                popExitTransition = {
                    ExitTransition.None
                },
                builder = builder
            )
        }
    }

    // 네비게이션 애니메이션 완료 후 상태 초기화
    LaunchedEffect(currentBackStackEntry) {
        if (isSwipeBack) {
            // 애니메이션 시간만큼 대기 후 상태 초기화
            kotlinx.coroutines.delay(300)
            isSwipeBack = false
            dragOffset = 0f
        }
    }
}
