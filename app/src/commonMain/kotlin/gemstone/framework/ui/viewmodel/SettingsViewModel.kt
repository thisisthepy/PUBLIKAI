package gemstone.framework.ui.viewmodel

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue


object SettingsViewModel {
    var userInitial by mutableStateOf("CU")
    var userFirstName by mutableStateOf("Chaeun")
}
