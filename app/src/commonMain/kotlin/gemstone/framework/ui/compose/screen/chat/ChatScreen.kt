package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.animation.core.*
import kotlinx.coroutines.delay
import gemstone.app.generated.resources.*
import gemstone.framework.ui.compose.theme.*
import gemstone.framework.ui.viewmodel.*
import org.jetbrains.compose.resources.stringResource


@Composable
fun ChatScreen(screenWidth: Dp) {
    Column(
        modifier = Modifier.fillMaxSize().imePadding().padding(Dimen.LAYOUT_PADDING)
    ) {
        val uiState by ChatViewModel.uiState.collectAsState()

        Row(
            modifier = Modifier.fillMaxWidth().padding(bottom = Dimen.LIST_ELEMENT_SPACING),
            horizontalArrangement = Arrangement.End,
            verticalAlignment = Alignment.Top
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.Start
            ) {
                TitleText(uiState.titleOrPlaceholder, maxLines = 1)
                CaptionText(AIModelViewModel.selectedAIModelDescription, maxLines = 1)
            }

            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))

            Row(
                modifier = Modifier,
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.End
            ) {
                PrimaryFluxIconButton(
                    onClick = {
                        ChatViewModel.reset()
                    },
                    iconResource = IconResource.Vector(Icons.Default.Add),
                    iconDescription = stringResource(Res.string.chat_new_chat_icon_desc),
                    shape = MaterialTheme.shapes.extraLarge
                )
                SecondaryFluxIconButton(
                    onClick = { /* TODO: Handle chat options */ },
                    iconResource = IconResource.Vector(Icons.Default.MoreHoriz),
                    iconDescription = stringResource(Res.string.chat_option_icon_desc),
                    shape = MaterialTheme.shapes.extraLarge
                )
            }
        }

        val listState = rememberLazyListState()
        val messageHistory: List<Conversation> = when (val currentMessage = uiState.currentMessage) {
            null -> uiState.messages
            else -> uiState.messages + listOf(currentMessage)
        }

        uiState.currentMessage?.tools?.let {
            LaunchedEffect(
                messageHistory.size,
                uiState.currentMessage?.assistant,
                uiState.currentMessage?.thoughts,
                it.size
            ) {
                if (messageHistory.isNotEmpty()) {
                    val totalItems = messageHistory.size + if (uiState.currentMessage != null) 1 else 0
                    if (totalItems > 0) {
                        listState.animateScrollToItem(totalItems - 1)
                    }
                }
            }
        }

        LazyColumn(
            modifier = Modifier.fillMaxWidth().weight(1f),
            contentPadding = PaddingValues(vertical = Dimen.LIST_ELEMENT_SPACING * 2),
            verticalArrangement = when (messageHistory.isEmpty()) {
                true -> Arrangement.Center
                false -> Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING, Alignment.Top)
            },
            horizontalAlignment = Alignment.CenterHorizontally,
            state = listState
        ) {
            if (messageHistory.isEmpty()) {
                item {
                    Column(
                        modifier = Modifier.widthIn(max = 500.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        TitleText(
                            "Hi there, ${SettingsViewModel.userFirstName}!",
                            fontWeight = FontWeight.ExtraBold,
                            fontSize = 38.sp,
                            textAlign = TextAlign.Center,
                            lineHeight = 38.sp
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        TitleText(
                            "What would you like to know?",
                            fontSize = 30.sp,
                            textAlign = TextAlign.Center,
                            lineHeight = 30.sp
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        CaptionText(
                            "Start collaborate with the chat bot AI through examples with buttons below or write something in your mind.",
                            color = Color.Gray,
                            textAlign = TextAlign.Center
                        )
                    }
                    Spacer(modifier = Modifier.height(32.dp))

                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val presets = mapOf(
                            "학사 일정" to Pair(Res.drawable.book_fill, "수강신청 언제야?"),
                            "공지 사항" to Pair(Res.drawable.pencil_fill, "최신 공지사항 알려줘!"),
                            "식단 안내" to Pair(Res.drawable.fork_knife, "오늘 학식은?"),
                            "셔틀 버스" to Pair(Res.drawable.bus_front_fill, "셔틀 버스 언제와?"),
                        )
                        for (data in presets) {
                            BlurredFluxCard(
                                onClick = {
                                    ChatViewModel.setMessageInput(data.value.second)
                                },
                                modifier = Modifier.padding(Dimen.LAYOUT_PADDING / 2).size(120.dp),
                                iconModifier = Modifier.size(34.dp),
                                iconResource = IconResource.Drawable(data.value.first),
                                iconDescription = data.key,
                                hoverAnimation = HoverAnimation(0f, -20f),
                                shape = MaterialTheme.shapes.large.copy(Dimen.BIG_BUTTON_CORNER_RADIUS),
                                contentPadding = PaddingValues(Dimen.BIG_BUTTON_PADDING),
                                elevation = ButtonDefaults.buttonElevation(1.dp),
                                colors = ButtonColors(
                                    containerColor = Color(0xFFFBFBFB),
                                    contentColor = MaterialTheme.colorScheme.onSurface,
                                    disabledContainerColor = Color(0xFFF9F9F9),
                                    disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                                )
                            ) {
                                Spacer(modifier = Modifier.height(14.dp))
                                BodyText(data.key, fontSize = 14.sp)
                                Spacer(modifier = Modifier.height(2.dp))
                                CaptionText(data.value.second, letterSpacing = (-1).sp, fontSize = 12.sp)
                            }
                        }
                    }
                }
            } else {
                for ((index, message) in messageHistory.withIndex()) {
                    item {
                        ConversationBox(
                            userContent = message.user,
                            assistantContent = message.assistant,
                            thoughts = Triple(message.thoughts, message.thoughtElapsed.toInt(), message.isThinking),
                            tools = message.tools.map {
                                Triple(it.key.split("():")[0].trim(), it.value, it.key.split("():")[1].trim())
                            },
                            isStreaming = (index == messageHistory.size-1) && (uiState.currentMessage != null)
                        )
                    }
                }
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth().padding(top = Dimen.LAYOUT_PADDING),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            SecondaryFluxButton(
                onClick = {},
                modifier = if (screenWidth >= 800.dp) Modifier.width(700.dp) else Modifier.weight(1f),
                elevation = ButtonDefaults.buttonElevation(0.4.dp),
                clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                hoverAnimation = null,
                interactionSource = remember { NoRippleInteractionSource() },
                enabled = false,
                shape = MaterialTheme.shapes.extraLarge,
                contentPadding = PaddingValues(0.dp)
            ) {
                TertiaryFluxIconButton(
                    onClick = {},
                    iconResource = IconResource.Drawable(Res.drawable.paperclip),
                    iconDescription = "Attach",
                    shape = MaterialTheme.shapes.extraLarge,
                    elevation = ButtonDefaults.buttonElevation(0.dp)
                )
                BasicTextField(
                    value = uiState.messageInput,
                    onValueChange = { ChatViewModel.setMessageInput(it) },
                    modifier = Modifier.weight(1f).padding(vertical = 6.dp),
                    textStyle = TextStyle(
                        color = MaterialTheme.colorScheme.onSecondary,
                        fontFamily = SuiteFontFamily
                    ),
                    decorationBox = { innerTextField ->
                        if (uiState.messageInput.isEmpty()) {
                            Text(
                                text = stringResource(Res.string.chat_message_placeholder)
                                    .replace("me", AIModelViewModel.selectedAIModelOrDefault),
                                style = TextStyle(color = Color.Gray),
                                fontFamily = SuiteFontFamily
                            )
                        }
                        innerTextField()
                    }
                )
            }
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            PrimaryFluxIconButton(
                onClick = { ChatViewModel.sendMessage() },
                iconResource = IconResource.Drawable(Res.drawable.arrow_up),
                iconDescription = "Send",
                shape = MaterialTheme.shapes.extraLarge,
                modifier = Modifier.size(44.dp)
            )
        }
    }
}


@Composable
fun ConversationBox(
    userContent: String = "",
    assistantContent: String = "",
    thoughts: Triple<String, Int, Boolean> = Triple("", 0, false),
    tools: List<Triple<String, Boolean, String>> = emptyList(),
    isStreaming: Boolean = false
) {
    MessageBubble(ChatRole.USER, userContent)
    MessageBubble(ChatRole.ASSISTANT, assistantContent, thoughts, tools, isStreaming)
}


@Composable
fun MessageBubble(
    role: ChatRole,
    content: String = "",
    thoughts: Triple<String, Int, Boolean> = Triple("", 0, false),
    tools: List<Triple<String, Boolean, String>> = emptyList(),
    isStreaming: Boolean = false
) {
    if (role == ChatRole.USER) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.End,
            verticalArrangement = Arrangement.Top
        ) {
            PrimaryFluxButton(
                onClick = {},
                modifier = Modifier,
                shape = MaterialTheme.shapes.large
            ) {
                BodyText(
                    SettingsViewModel.userInitial,
                    fontSize = 14.sp,
                    fontWeight = FontWeight.ExtraLight,
                    maxLines = 1
                )
            }
            //Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            SecondaryFluxButton(
                onClick = {},
                modifier = Modifier,
                elevation = ButtonDefaults.buttonElevation(0.2.dp),
                clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                hoverAnimation = null,
                interactionSource = remember { NoRippleInteractionSource() },
                shape = MaterialTheme.shapes.extraLarge,
                contentPadding = PaddingValues(vertical = 10.dp, horizontal = 14.dp)
            ) {
                BodyText(content, fontWeight = FontWeight.Light, color = MaterialTheme.colorScheme.primary)
            }
        }
    } else {
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.Start,
            verticalArrangement = Arrangement.Top
        ) {
            var showThoughts by rememberSaveable { mutableStateOf(false) }

            Row(
                modifier = Modifier,
                horizontalArrangement = Arrangement.Start,
                verticalAlignment = Alignment.CenterVertically
            ) {
                PrimaryFluxButton(
                    onClick = {},
                    modifier = Modifier,
                    shape = MaterialTheme.shapes.medium,
                    contentPadding = PaddingValues(vertical = 4.dp, horizontal = 10.dp),
                ) {
                    BodyText(
                        role.value.replaceFirstChar { it.uppercase() },
                        fontSize = 14.sp,
                        fontWeight = FontWeight.ExtraLight,
                        maxLines = 1
                    )
                }
                Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING * 2))
                val status = "${thoughts.second}초 동안 " + when (thoughts.third) {
                    true -> "생각 중..."
                    false -> "생각함"
                } + if (showThoughts) "  <" else "  >"
                BodyText(
                    status,
                    fontWeight = FontWeight.Light,
                    color = MaterialTheme.colorScheme.primary,
                    letterSpacing = (-0.4).sp,
                    modifier = Modifier.pressClickEffect(
                        onClick = { showThoughts = !showThoughts },
                        animation = Dimen.BUTTON_CLICK_ANIMATION
                    )
                )
            }
            if (showThoughts && thoughts.first.isNotBlank()) {
                val color = MaterialTheme.colorScheme.primary
                val lineOffset = 8.dp
                val horizontalPadding = 8.dp
                //Spacer(modifier = Modifier.height(Dimen.LIST_ELEMENT_SPACING))
                CaptionText(
                    thoughts.first,
                    color = color,
                    letterSpacing = (-0.2).sp,
                    lineHeight = 16.sp,
                    modifier = Modifier.padding(start = lineOffset + horizontalPadding, end = horizontalPadding)
                        .drawBehind {
                            drawLine(
                                color = color,
                                start = Offset((-lineOffset).toPx(), 0f),
                                end = Offset((-lineOffset).toPx(), size.height),
                                strokeWidth = 1.2.dp.toPx()
                            )
                        }
                )
                Spacer(modifier = Modifier.height(Dimen.LIST_ELEMENT_SPACING))
            }
            for (tool in tools) {
                TertiaryFluxButton(
                    onClick = {},
                    modifier = Modifier.fillMaxWidth().padding(bottom = Dimen.LIST_ELEMENT_SPACING),
                    elevation = ButtonDefaults.buttonElevation(1.dp),
                    clickAnimation = ClickAnimation(1f, 0.999f),
                    interactionSource = remember { NoRippleInteractionSource() },
                    hoverAnimation = null,
                    shape = MaterialTheme.shapes.small,
                    contentPadding = PaddingValues(vertical = 6.dp, horizontal = 8.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Start,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        SubtitleText(
                            (if (tool.second) "✒️" else "⚒️") + "  Function Call:  " + tool.first.split("_")
                                .joinToString(" ") { it.replaceFirstChar { c -> c.uppercase() } },
                            color = MaterialTheme.colorScheme.primary,
                            fontSize = 14.4.sp,
                            maxLines = 1
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Spacer(modifier = Modifier.weight(1f))
                        CaptionText(
                            tool.third.replace("call_", "timestamp: "),
                            fontWeight = FontWeight.Light,
                            color = Color.DarkGray,
                            maxLines = 1
                        )
                    }
                }
            }
            if (content.isNotBlank()) {
                BlurredFluxButton(
                    onClick = {},
                    modifier = Modifier,
                    elevation = ButtonDefaults.buttonElevation(0.4.dp),
                    clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                    hoverAnimation = null,
                    interactionSource = remember { NoRippleInteractionSource() },
                    shape = MaterialTheme.shapes.medium,
                    contentPadding = PaddingValues(vertical = 10.dp, horizontal = 14.dp),
                    colors = ButtonColors(
                        containerColor = Color(0xFFFBFBFB),
                        contentColor = MaterialTheme.colorScheme.onSurface,
                        disabledContainerColor = Color(0xFFF9F9F9),
                        disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                    )
                ) {
                    val useRandomRenderer by remember { mutableStateOf(kotlin.random.Random.nextBoolean()) }

                    if (useRandomRenderer) {
                        ChatGPTStyleStreaming(content, isStreaming = isStreaming)
                    } else {
                        StreamingMarkdownText(content, isStreaming = isStreaming)
                    }
                }
            }
        }
    }
}


@Composable
fun ChatGPTStyleStreaming(
    message: String,
    isStreaming: Boolean = false
) {
    var cursorAlpha by remember { mutableStateOf(1f) }

    val animatedAlpha by animateFloatAsState(
        targetValue = if (isStreaming && cursorAlpha > 0.5f) 1f else 0.3f,
        animationSpec = infiniteRepeatable(
            animation = tween(800),
            repeatMode = RepeatMode.Reverse
        ),
        label = "cursor_fade"
    )

    LaunchedEffect(isStreaming) {
        while (isStreaming) {
            delay(100)
            cursorAlpha = if (cursorAlpha > 0.5f) 0.3f else 1f
        }
    }

    val styledText = buildAnnotatedString {
        parseAdvancedMarkdown(this, message)

        if (isStreaming) {
            pushStyle(SpanStyle(
                color = MaterialTheme.colorScheme.primary.copy(alpha = animatedAlpha),
                fontSize = 16.sp
            ))
            append("█")
            pop()
        }
    }

    Text(
        text = styledText,
        fontFamily = SuiteFontFamily,
        fontWeight = FontWeight.Light,
        fontSize = 15.sp,
        color = MaterialTheme.colorScheme.primary
    )
}

fun parseAdvancedMarkdown(builder: AnnotatedString.Builder, text: String) {
    val boldRegex = """\*\*(.*?)\*\*""".toRegex()
    var lastIndex = 0

    boldRegex.findAll(text).forEach { match ->
        builder.append(text.substring(lastIndex, match.range.first))
        builder.pushStyle(SpanStyle(fontWeight = FontWeight.Bold))
        builder.append(match.groupValues[1])
        builder.pop()
        lastIndex = match.range.last + 1
    }
    builder.append(text.substring(lastIndex))
}

@Composable
fun StreamingMarkdownText(
    text: String,
    isStreaming: Boolean = false
) {
    var cursorVisible by remember { mutableStateOf(true) }
    val fontFamily = SuiteFontFamily
    val textColor = MaterialTheme.colorScheme.primary

    LaunchedEffect(isStreaming) {
        if (isStreaming) {
            while (true) {
                delay(600)
                cursorVisible = !cursorVisible
            }
        } else {
            cursorVisible = false
        }
    }

    val annotatedString = remember(text, isStreaming, cursorVisible) {
        buildAnnotatedString {
            if (isStreaming) {
                parseSimpleMarkdownInto(this, text)
            } else {
                parseAdvancedMarkdownInto(this, text)
            }

            if (isStreaming && cursorVisible) {
                pushStyle(SpanStyle(
                    fontFamily = fontFamily,
                    fontWeight = FontWeight.Light,
                    fontSize = 15.sp,
                    color = textColor
                ))
                append("●")
                pop()
            } else if (isStreaming) {
                append(" ")
            }
        }
    }

    Text(
        text = annotatedString,
        fontFamily = fontFamily,
        fontWeight = FontWeight.Light,
        fontSize = 15.sp,
        color = textColor,
        lineHeight = 22.sp
    )
}

fun parseSimpleMarkdownInto(builder: AnnotatedString.Builder, text: String) {
    val boldRegex = """\*\*(.*?)\*\*""".toRegex()
    var lastIndex = 0

    boldRegex.findAll(text).forEach { match ->
        builder.append(text.substring(lastIndex, match.range.first))
        builder.pushStyle(SpanStyle(fontWeight = FontWeight.Bold))
        builder.append(match.groupValues[1])
        builder.pop()
        lastIndex = match.range.last + 1
    }
    builder.append(text.substring(lastIndex))
}

fun parseAdvancedMarkdownInto(builder: AnnotatedString.Builder, text: String) {
    val boldRegex = """\*\*(.*?)\*\*""".toRegex()
    val italicRegex = """\*(.*?)\*""".toRegex()
    val codeRegex = """`(.*?)`""".toRegex()

    val patterns = listOf(
        boldRegex to SpanStyle(fontWeight = FontWeight.Bold),
        italicRegex to SpanStyle(fontStyle = FontStyle.Italic),
        codeRegex to SpanStyle(
            fontFamily = FontFamily.Monospace,
            background = Color.Gray.copy(alpha = 0.2f)
        )
    )

    val matches = mutableListOf<Triple<IntRange, String, SpanStyle>>()

    patterns.forEach { (regex, style) ->
        regex.findAll(text).forEach { match ->
            matches.add(Triple(match.range, match.groupValues[1], style))
        }
    }

    matches.sortBy { it.first.first }

    var lastIndex = 0
    matches.forEach { (range, content, style) ->
        if (range.first >= lastIndex) {
            builder.append(text.substring(lastIndex, range.first))
            builder.pushStyle(style)
            builder.append(content)
            builder.pop()
            lastIndex = range.last + 1
        }
    }
    builder.append(text.substring(lastIndex))
}
