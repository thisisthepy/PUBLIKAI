# Gemstone AI

This is a open-source multi-platform AI Chat UI written with Compose Multiplatform.


## Stacks
### Model Serving API
- PyTorch
- Transformers
- BitsAndBytes

### Mobile/Web Client APP
- Kotlin Multiplatform Mobile
- Compose Multiplatform Mobile


## Model
### Server
- Qwen 3 14b 4bitQ (BitsAndBytes)
- To be done...

### On-Device
- Llama 3.1 8B (llama.cpp)
- Qwen 3 14b 4bitQ (llama.cpp)
- To be done...


## Architecture
```
app/
├── domain/
│   ├── entity/
│   │   ├── Message.kt
│   │   ├── ChatSession.kt
│   │   ├── User.kt
│   │   ├── AIModel.kt
│   │   └── value/
│   │       ├── MessageId.kt
│   │       ├── SessionId.kt
│   │       └── Timestamp.kt
│   ├── usecase/
│   │   ├── chat/
│   │   │   ├── SendMessageUseCase.kt
│   │   │   ├── GetChatHistoryUseCase.kt
│   │   │   ├── CreateSessionUseCase.kt
│   │   │   └── DeleteSessionUseCase.kt
│   │   ├── ai/
│   │   │   ├── SwitchAIModelUseCase.kt
│   │   │   ├── DownloadModelUseCase.kt
│   │   │   └── GetAvailableModelsUseCase.kt
│   │   └── user/
│   │       ├── SaveUserPreferencesUseCase.kt
│   │       └── GetUserPreferencesUseCase.kt
│   ├── repository/
│   │   ├── ChatRepository.kt
│   │   ├── AIModelRepository.kt
│   │   └── UserRepository.kt
│   └── service/
│       ├── AIService.kt
│       ├── ValidationService.kt
│       └── NotificationService.kt
├── adapter/
│   ├── controller/
│   │   ├── chat/
│   │   │   ├── ChatController.kt
│   │   │   ├── SessionController.kt
│   │   │   └── dto/
│   │   │       ├── SendMessageRequest.kt
│   │   │       └── CreateSessionRequest.kt
│   │   ├── ai/
│   │   │   ├── AIModelController.kt
│   │   │   └── dto/
│   │   │       └── SwitchModelRequest.kt
│   │   └── settings/
│   │       ├── SettingsController.kt
│   │       └── dto/
│   │           └── UpdatePreferencesRequest.kt
│   ├── presenter/
│   │   ├── chat/
│   │   │   ├── ChatPresenter.kt
│   │   │   ├── SessionPresenter.kt
│   │   │   └── model/
│   │   │       ├── ChatUiState.kt
│   │   │       ├── MessageUiModel.kt
│   │   │       └── SessionUiModel.kt
│   │   ├── ai/
│   │   │   ├── AIModelPresenter.kt
│   │   │   └── model/
│   │   │       ├── AIModelUiState.kt
│   │   │       └── ModelDownloadUiModel.kt
│   │   └── settings/
│   │       ├── SettingsPresenter.kt
│   │       └── model/
│   │           └── SettingsUiState.kt
└── framework/
    ├── ui/
    │   ├── compose/
    │   │   ├── screen/
    │   │   │   ├── chat/
    │   │   │   │   ├── MainScreen.kt
    │   │   │   │   ├── SideScreen.kt
    │   │   │   │   ├── ChatScreen.kt
    │   │   │   │   └── component/
    │   │   │   │       ├── MessageItem.kt
    │   │   │   │       ├── MessageInput.kt
    │   │   │   │       └── SubjectCard.kt
    │   │   │   ├── model/
    │   │   │   │   ├── ModelSelectionScreen.kt
    │   │   │   │   └── component/
    │   │   │   │       ├── ModelItem.kt
    │   │   │   │       └── DownloadProgress.kt
    │   │   │   └── settings/
    │   │   │       ├── SettingsScreen.kt
    │   │   │       └── component/
    │   │   │           └── PreferenceItem.kt
    │   │   ├── navigation/
    │   │   │   ├── AppNavigation.kt
    │   │   │   └── NavigationRoute.kt
    │   │   └── theme/
    │   │       ├── Color.kt
    │   │       ├── Dimen.kt
    │   │       ├── Shape.kt
    │   │       ├── Theme.kt
    │   │       └── Type.kt
    │   └── viewmodel/
    │       ├── ChatViewModel.kt
    │       ├── AIModelViewModel.kt
    │       └── SettingsViewModel.kt
    ├── database/
    │   └── ChatDatabase.kt
    ├── network/
    │   ├── ktor/
    │   │   ├── HttpClientFactory.kt
    │   │   └── api/
    │   │       ├── ChatApiService.kt
    │   │       └── AIModelApiService.kt
    │   └── websocket/
    │       └── ChatWebSocketClient.kt
    ├── ai/
    │   ├── local/
    │   │   └── LocalModelManager.kt
    │   ├── remote/
    │   │   ├── OpenAIClient.kt
    │   │   ├── AnthropicClient.kt
    │   │   └── HuggingFaceClient.kt
    │   └── common/
    │       └── ModelManager.kt
    └── storage/
        └── FileManager.kt
```


## Installation
### Clone this repo
```bash
git clone https://github.com/thisisthepy/FluxChatUI.git
cd FluxChatUI
```


### Install dependencies
```bash
uv sync
```
- Llama-cpp-python fix for Qwen
```bash
CMAKE_ARGS="-DGGML_CUDA=on -DLLAVA_BUILD=off -DCMAKE_CUDA_ARCHITECTURES=native" FORCE_CMAKE=1 uv pip install llama-cpp-python --no-cache-dir --force-reinstall --upgrade
```


### Run the server
```bash
python -m api run server
```
