import org.jetbrains.kotlin.gradle.targets.js.webpack.KotlinWebpackConfig
import org.jetbrains.compose.desktop.application.dsl.TargetFormat
import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.android.application)
    alias(libs.plugins.compose.multiplatform)
    alias(libs.plugins.compose.compiler)
    alias(libs.plugins.compose.hotreload)
    kotlin("plugin.serialization").version(libs.versions.kotlin.get())
}


kotlin {
    androidTarget {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_11)
        }
    }
    
    listOf(
        iosX64(),
        iosArm64(),
        iosSimulatorArm64()
    ).forEach { iosTarget ->
        iosTarget.binaries.framework {
            baseName = "Gemstone"
            isStatic = true
        }
    }
    
    jvm("desktop")
    
    @OptIn(ExperimentalWasmDsl::class)
    wasmJs {
        moduleName = "gemstone"
        browser {
            val rootDirPath = project.rootDir.path
            val projectDirPath = project.projectDir.path
            commonWebpackConfig {
                outputFileName = "gemstone.js"
                devServer = (devServer ?: KotlinWebpackConfig.DevServer()).apply {
                    static = (static ?: mutableListOf()).apply {
                        // Serve sources to debug inside browser
                        add(rootDirPath)
                        add(projectDirPath)
                    }
                }
            }
        }
        binaries.executable()
    }
    
    sourceSets {
        val commonMain by getting
        val androidMain by getting
        val desktopMain by getting
        val cioMain by creating {
            dependencies {
                api(libs.ktor.client.cio)
            }
            androidMain.dependsOn(this)
            desktopMain.dependsOn(this)
            iosMain {
                dependsOn(this)
            }
            dependsOn(commonMain)
        }
        wasmJsMain.dependencies {
            api(libs.ktor.client.js)
        }
        
        androidMain.dependencies {
            api(compose.material3)
            api(compose.preview)
            api(libs.androidx.activity.compose)
        }
        commonMain.dependencies {
            api(compose.runtime)
            api(compose.foundation)
            api(compose.material3)
            api(compose.materialIconsExtended)
            api(compose.ui)
            api(compose.components.resources)
            api(compose.components.uiToolingPreview)
            api(libs.androidx.lifecycle.viewmodel)
            api(libs.androidx.lifecycle.runtimeCompose)
            api(libs.navigation.compose)

            // For API calls and JSON serialization
            implementation(libs.ktor.client.core)
            implementation(libs.ktor.client.websockets)
            implementation(libs.ktor.client.content.negotiation)
            implementation(libs.ktor.serialization.kotlinx.json)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.kotlinx.datetime)

            // For Compose WebView support
            //api(libs.compose.webview.multiplatform)
        }
        commonTest.dependencies {
            api(libs.kotlin.test)
        }
        desktopMain.dependencies {
            api(compose.desktop.currentOs) {
                exclude(group = "org.jetbrains.compose.material3")
            }
            api(libs.kotlinx.coroutines.swing)

            implementation(libs.jewel.standalone)
            implementation(libs.jewel.decorated.window)
            implementation(libs.jewel.foundation)
        }
    }
}

android {
    namespace = "io.github.thisisthepy.gemstone"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        applicationId = "io.github.thisisthepy.gemstone"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = libs.versions.android.targetSdk.get().toInt()
        versionCode = 1
        versionName = "1.0"
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.androidx.runtime.android)
    debugImplementation(compose.uiTooling)
}

compose.desktop {
    application {
        mainClass = "gemstone.Main_desktopKt"

        nativeDistributions {
            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)
            packageName = "Gemstone AI"
            packageVersion = "1.0.0"
            macOS {
                iconFile.set(project.file("src/desktopMain/resources/simple_white.icns"))
                installationPath = "/Applications/StoneManager"
                bundleID = "io.github.thisisthepy.gemstone"
            }
            windows {
                iconFile.set(project.file("src/desktopMain/resources/simple_white.ico"))
                dirChooser = true
                installationPath = "C:\\Program Files\\Gemstone"
                perUserInstall = true
            }
            linux {
                iconFile.set(project.file("src/desktopMain/resources/simple_white.png"))
                installationPath = "/usr/local/bin/gemstone"
            }
        }
    }
}
