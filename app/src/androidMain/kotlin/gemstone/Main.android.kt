package io.github.thisisthepy.gemstone

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview
import gemstone.framework.ui.viewmodel.ChatViewModel
import gemstone.App


class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)

        setContent {
            App()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        ChatViewModel.onCleared()
    }
}

@Preview
@Composable
fun AppAndroidPreview() {
    App()
}
