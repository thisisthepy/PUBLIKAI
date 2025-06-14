package gemstone.framework.ui.compose.screen.chat

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
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
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import gemstone.app.generated.resources.*
import gemstone.app.generated.resources.Res
import gemstone.app.generated.resources.chat_new_chat_icon_desc
import gemstone.app.generated.resources.chat_option_icon_desc
import gemstone.app.generated.resources.chat_title_placeholder
import gemstone.framework.ui.compose.theme.*
import gemstone.framework.ui.viewmodel.AIModelViewModel
import gemstone.framework.ui.viewmodel.ChatRole
import gemstone.framework.ui.viewmodel.ChatViewModel
import gemstone.framework.ui.viewmodel.ChatViewModel.messageHistory
import gemstone.framework.ui.viewmodel.SettingsViewModel
import org.jetbrains.compose.resources.stringResource


@Composable
fun ChatScreen(screenWidth: Dp) {
    Column(
        modifier = Modifier.fillMaxSize().imePadding().padding(Dimen.LAYOUT_PADDING)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.End,
            verticalAlignment = Alignment.Top
        ) {
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.Start
            ) {
                TitleText(ChatViewModel.getTitleOrPlaceholder(), maxLines = 1)
                CaptionText(ChatViewModel.modelDescription)
            }

            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))

            Row(
                modifier = Modifier,
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.End
            ) {
                val newChatTitle = stringResource(Res.string.chat_title_placeholder)
                PrimaryFluxIconButton(
                    onClick = {
                        ChatViewModel.clear(newChatTitle)
                        AIModelViewModel.createChatRoom(-1, ChatViewModel)
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

        LazyColumn(
            modifier = Modifier.fillMaxWidth().weight(1f),
            verticalArrangement = when (messageHistory.size) {
                0 -> Arrangement.Center
                else -> Arrangement.spacedBy(Dimen.LIST_ELEMENT_SPACING, Alignment.Top)
            },
            horizontalAlignment = Alignment.CenterHorizontally
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
                                    ChatViewModel.messageInput = data.value.second
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
                for (message in messageHistory) {
                    item {
                        ConversationBox(message.key, message.value.first, message.value.second, message.value.third)
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
                val placeholder = stringResource(Res.string.chat_message_placeholder)
                val modelName = ChatViewModel.modelName
                val placeholderWithModelName = if (modelName.isNotEmpty()) {
                    placeholder.replace("me", modelName)
                } else {
                    placeholder
                }
                BasicTextField(
                    value = ChatViewModel.messageInput,
                    onValueChange = { ChatViewModel.messageInput = it },
                    modifier = Modifier.weight(1f).padding(vertical = 6.dp),
                    textStyle = TextStyle(
                        color = MaterialTheme.colorScheme.onSecondary,
                        fontFamily = SuiteFontFamily
                    ),
                    decorationBox = { innerTextField ->
                        if (ChatViewModel.messageInput.isEmpty()) {
                            Text(
                                text = placeholderWithModelName,
                                style = TextStyle(color = Color.Gray)
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
    tools: List<String> = emptyList(),
) {
    MessageBubble(ChatRole.USER, userContent)
    MessageBubble(ChatRole.ASSISTANT, assistantContent, thoughts, tools)
}


@Composable
fun MessageBubble(
    role: ChatRole,
    content: String = "",
    thoughts: Triple<String, Int, Boolean> = Triple("", 0, false),
    tools: List<String> = emptyList(),
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
                BodyText(SettingsViewModel.userInitial, fontWeight = FontWeight.ExtraLight, maxLines = 1)
            }
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            SecondaryFluxButton(
                onClick = {},
                modifier = Modifier,
                elevation = ButtonDefaults.buttonElevation(6.dp),
                clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                hoverAnimation = null,
                interactionSource = remember { NoRippleInteractionSource() },
                enabled = false,
                shape = MaterialTheme.shapes.extraLarge,
                contentPadding = PaddingValues(0.dp)
            ) {
                BodyText(content, fontWeight = FontWeight.Light)
            }
        }
    } else {
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.Start,
            verticalArrangement = Arrangement.Top
        ) {
            var showThoughts by rememberSaveable { mutableStateOf(false) }

            Row {
                PrimaryFluxButton(
                    onClick = {},
                    modifier = Modifier,
                    shape = MaterialTheme.shapes.large
                ) {
                    BodyText(role.value, fontWeight = FontWeight.ExtraLight, maxLines = 1)
                }
                Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
                val status = "${thoughts.second}초 동안 " + when (thoughts.third) {
                    true -> "생각 중..."
                    false -> "생각함"
                } + if (showThoughts) " <" else " >"
                BodyText(
                    status, fontWeight = FontWeight.Light, color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.pressClickEffect(
                        onClick = { },
                        animation = Dimen.BUTTON_CLICK_ANIMATION
                    )
                )
                if (showThoughts) {
                    val color = MaterialTheme.colorScheme.primary
                    CaptionText(
                        thoughts.first,
                        color = color,
                        modifier = Modifier.padding(horizontal = 4.dp)
                            .drawBehind {
                                drawLine(
                                    color = color,
                                    start = Offset(0f, 0f),
                                    end = Offset(0f, size.height),
                                    strokeWidth = 2.dp.toPx()
                                )
                            }
                    )
                }
            }
            Spacer(modifier = Modifier.width(Dimen.LIST_ELEMENT_SPACING))
            BlurredFluxButton(
                onClick = {},
                modifier = Modifier,
                elevation = ButtonDefaults.buttonElevation(6.dp),
                clickAnimation = Dimen.SURFACE_CLICK_ANIMATION,
                hoverAnimation = null,
                interactionSource = remember { NoRippleInteractionSource() },
                enabled = false,
                shape = MaterialTheme.shapes.extraLarge,
                contentPadding = PaddingValues(0.dp)
            ) {
                BodyText(content, fontWeight = FontWeight.Light)
            }
        }
    }
}
