package gemstone.framework.ui.compose.screen.chat

import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.VerticalDivider
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import gemstone.framework.ui.compose.navigation.SwipeBackNavHost
import gemstone.framework.ui.compose.theme.appColorSet
import gemstone.framework.ui.viewmodel.AIModelViewModel
import kotlinx.serialization.Serializable


@Serializable
object Main

@Serializable
object Chat


@Composable
fun MainScreen() {
    BoxWithConstraints {
        val isLandscape = maxWidth > maxHeight
        val widthPx = with(LocalDensity.current) { maxWidth.toPx() }
        val heightPx = with(LocalDensity.current) { maxHeight.toPx() }

        val backgroundModifier = Modifier.background(
            Brush.linearGradient(
                colors = listOf(appColorSet.appBackgroundColorStart, appColorSet.appBackgroundColorEnd),
                start = Offset(0f, 0f),
                end = Offset(widthPx, heightPx)
            )
        )

        if (isLandscape) {  // Landscape mode
            Row(
                modifier = backgroundModifier.fillMaxSize().systemBarsPadding()
            ) {
                SideScreen(sideBarMode = true)
                VerticalDivider(modifier = Modifier.fillMaxHeight(), thickness = 0.2.dp)
                ChatScreen()
            }
        } else {  // Portrait mode
            val navController = rememberNavController()
            var isTransitioning by remember { mutableStateOf(true) }
            val halfLinearHalfEaseOut = CubicBezierEasing(0.55f, 0.6f, 0.75f, 1.0f)
            val animationPeriod = 250
            val animationSpec = tween<IntOffset>(animationPeriod, easing = halfLinearHalfEaseOut)

            LaunchedEffect(navController) {
                val listener = NavController.OnDestinationChangedListener { _, _, _ ->
                    isTransitioning = !isTransitioning
                }
                navController.addOnDestinationChangedListener(listener)
            }
            NavHost(
                navController = navController,
                startDestination = Main,
                enterTransition = {
                    slideIntoContainer(
                        towards = AnimatedContentTransitionScope.SlideDirection.Left,
                        initialOffset = { it },
                        animationSpec = animationSpec
                    )
                },
                exitTransition = {
                    slideOutOfContainer(
                        towards = AnimatedContentTransitionScope.SlideDirection.Left,
                        targetOffset = { it / 2 },
                        animationSpec = animationSpec
                    )
                },
                popEnterTransition = {
                    slideIntoContainer(
                        towards = AnimatedContentTransitionScope.SlideDirection.Right,
                        initialOffset = { it / 2 },
                        animationSpec = animationSpec
                    )
                },
                popExitTransition = {
                    slideOutOfContainer(
                        towards = AnimatedContentTransitionScope.SlideDirection.Right,
                        targetOffset = { it },
                        animationSpec = animationSpec
                    )
                }
            ) {
                composable<Main> {
                    Box(modifier = Modifier.fillMaxSize()) {
                        Column(
                            modifier = backgroundModifier.fillMaxSize().systemBarsPadding().padding(2.dp)
                        ) {
                            SideScreen(sideBarMode = false) { chatId ->
                                AIModelViewModel.selectChatRoom(chatId)
                                navController.navigate(Chat) {
                                    launchSingleTop = true
                                    restoreState = true
                                }
                                isTransitioning = true
                            }
                        }

                        AnimatedVisibility(
                            visible = isTransitioning,
                            enter = fadeIn(
                                animationSpec = tween(animationPeriod, easing = halfLinearHalfEaseOut)
                            ),
                            exit = fadeOut(
                                animationSpec = tween(animationPeriod, easing = halfLinearHalfEaseOut)
                            )
                        ) {
                            Box(
                                modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.2f))
                            )
                        }
                    }
                }
                composable<Chat> {
                    Column(
                        modifier = backgroundModifier.fillMaxSize().systemBarsPadding().padding(2.dp)
                    ) {
                        ChatScreen()
                    }
                }
            }
        }
    }
}
