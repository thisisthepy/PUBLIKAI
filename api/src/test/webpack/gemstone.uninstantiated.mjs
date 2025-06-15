
export async function instantiate(imports={}, runInitializer=true) {
    const cachedJsObjects = new WeakMap();
    // ref must be non-null
    function getCachedJsObject(ref, ifNotCached) {
        if (typeof ref !== 'object' && typeof ref !== 'function') return ifNotCached;
        const cached = cachedJsObjects.get(ref);
        if (cached !== void 0) return cached;
        cachedJsObjects.set(ref, ifNotCached);
        return ifNotCached;
    }

    const _ref_Li9za2lrby5tanM_ = imports['./skiko.mjs'];
    const _ref_QGpzLWpvZGEvY29yZQ_ = imports['@js-joda/core'];
    
    const js_code = {
        'kotlin.captureStackTrace' : () => new Error().stack,
        'kotlin.wasm.internal.stringLength' : (x) => x.length,
        'kotlin.wasm.internal.jsExportStringToWasm' : (src, srcOffset, srcLength, dstAddr) => { 
            const mem16 = new Uint16Array(wasmExports.memory.buffer, dstAddr, srcLength);
            let arrayIndex = 0;
            let srcIndex = srcOffset;
            while (arrayIndex < srcLength) {
                mem16.set([src.charCodeAt(srcIndex)], arrayIndex);
                srcIndex++;
                arrayIndex++;
            }     
             },
        'kotlin.wasm.internal.importStringFromWasm' : (address, length, prefix) => { 
            const mem16 = new Uint16Array(wasmExports.memory.buffer, address, length);
            const str = String.fromCharCode.apply(null, mem16);
            return (prefix == null) ? str : prefix + str;
             },
        'kotlin.wasm.internal.externrefToBoolean' : (ref) => Boolean(ref),
        'kotlin.wasm.internal.getJsEmptyString' : () => '',
        'kotlin.wasm.internal.externrefToInt' : (ref) => Number(ref),
        'kotlin.wasm.internal.externrefToString' : (ref) => String(ref),
        'kotlin.wasm.internal.externrefEquals' : (lhs, rhs) => lhs === rhs,
        'kotlin.wasm.internal.externrefHashCode' : 
        (() => {
        const dataView = new DataView(new ArrayBuffer(8));
        function numberHashCode(obj) {
            if ((obj | 0) === obj) {
                return obj | 0;
            } else {
                dataView.setFloat64(0, obj, true);
                return (dataView.getInt32(0, true) * 31 | 0) + dataView.getInt32(4, true) | 0;
            }
        }
        
        const hashCodes = new WeakMap();
        function getObjectHashCode(obj) {
            const res = hashCodes.get(obj);
            if (res === undefined) {
                const POW_2_32 = 4294967296;
                const hash = (Math.random() * POW_2_32) | 0;
                hashCodes.set(obj, hash);
                return hash;
            }
            return res;
        }
        
        function getStringHashCode(str) {
            var hash = 0;
            for (var i = 0; i < str.length; i++) {
                var code  = str.charCodeAt(i);
                hash  = (hash * 31 + code) | 0;
            }
            return hash;
        }
        
        return (obj) => {
            if (obj == null) {
                return 0;
            }
            switch (typeof obj) {
                case "object":
                case "function":
                    return getObjectHashCode(obj);
                case "number":
                    return numberHashCode(obj);
                case "boolean":
                    return obj ? 1231 : 1237;
                default:
                    return getStringHashCode(String(obj)); 
            }
        }
        })(),
        'kotlin.wasm.internal.isNullish' : (ref) => ref == null,
        'kotlin.wasm.internal.intToExternref' : (x) => x,
        'kotlin.wasm.internal.getJsTrue' : () => true,
        'kotlin.wasm.internal.getJsFalse' : () => false,
        'kotlin.wasm.internal.newJsArray' : () => [],
        'kotlin.wasm.internal.jsArrayPush' : (array, element) => { array.push(element); },
        'kotlin.wasm.internal.getCachedJsObject_$external_fun' : (p0, p1) => getCachedJsObject(p0, p1),
        'kotlin.js.jsCatch' : (f) => { 
            let result = null;
            try { 
                f();
            } catch (e) {
               result = e;
            }
            return result;
             },
        'kotlin.js.__convertKotlinClosureToJsClosure_(()->Unit)' : (f) => getCachedJsObject(f, () => wasmExports['__callFunction_(()->Unit)'](f, )),
        'kotlin.js.jsThrow' : (e) => { throw e; },
        'kotlin.io.printError' : (error) => console.error(error),
        'kotlin.io.printlnImpl' : (message) => console.log(message),
        'kotlin.js.jsArrayGet' : (array, index) => array[index],
        'kotlin.js.jsArraySet' : (array, index, value) => { array[index] = value },
        'kotlin.js.JsArray_$external_fun' : () => new Array(),
        'kotlin.js.length_$external_prop_getter' : (_this) => _this.length,
        'kotlin.js.JsArray_$external_class_instanceof' : (x) => x instanceof Array,
        'kotlin.js.stackPlaceHolder_js_code' : () => (''),
        'kotlin.js.message_$external_prop_getter' : (_this) => _this.message,
        'kotlin.js.stack_$external_prop_getter' : (_this) => _this.stack,
        'kotlin.js.JsError_$external_class_instanceof' : (x) => x instanceof Error,
        'kotlin.js.then_$external_fun' : (_this, p0) => _this.then(p0),
        'kotlin.js.__convertKotlinClosureToJsClosure_((Js?)->Js?)' : (f) => getCachedJsObject(f, (p0) => wasmExports['__callFunction_((Js?)->Js?)'](f, p0)),
        'kotlin.js.then_$external_fun_1' : (_this, p0, p1) => _this.then(p0, p1),
        'kotlin.js.__convertKotlinClosureToJsClosure_((Js)->Js?)' : (f) => getCachedJsObject(f, (p0) => wasmExports['__callFunction_((Js)->Js?)'](f, p0)),
        'kotlin.js.catch_$external_fun' : (_this, p0) => _this.catch(p0),
        'kotlin.random.initialSeed' : () => ((Math.random() * Math.pow(2, 32)) | 0),
        'kotlin.wasm.internal.getJsClassName' : (jsKlass) => jsKlass.name,
        'kotlin.wasm.internal.instanceOf' : (ref, jsKlass) => ref instanceof jsKlass,
        'kotlin.wasm.internal.getConstructor' : (obj) => obj.constructor,
        'kotlin.time.tryGetPerformance' : () => typeof globalThis !== 'undefined' && typeof globalThis.performance !== 'undefined' ? globalThis.performance : null,
        'kotlin.time.getPerformanceNow' : (performance) => performance.now(),
        'kotlin.time.dateNow' : () => Date.now(),
        'kotlinx.coroutines.tryGetProcess' : () => (typeof(process) !== 'undefined' && typeof(process.nextTick) === 'function') ? process : null,
        'kotlinx.coroutines.tryGetWindow' : () => (typeof(window) !== 'undefined' && window != null && typeof(window.addEventListener) === 'function') ? window : null,
        'kotlinx.coroutines.nextTick_$external_fun' : (_this, p0) => _this.nextTick(p0),
        'kotlinx.coroutines.error_$external_fun' : (_this, p0) => _this.error(p0),
        'kotlinx.coroutines.console_$external_prop_getter' : () => console,
        'kotlinx.coroutines.createScheduleMessagePoster' : (process) => () => Promise.resolve(0).then(process),
        'kotlinx.coroutines.__callJsClosure_(()->Unit)' : (f, ) => f(),
        'kotlinx.coroutines.createRescheduleMessagePoster' : (window) => () => window.postMessage('dispatchCoroutine', '*'),
        'kotlinx.coroutines.subscribeToWindowMessages' : (window, process) => {
            const handler = (event) => {
                if (event.source == window && event.data == 'dispatchCoroutine') {
                    event.stopPropagation();
                    process();
                }
            }
            window.addEventListener('message', handler, true);
        },
        'kotlinx.coroutines.setTimeout' : (window, handler, timeout) => window.setTimeout(handler, timeout),
        'kotlinx.coroutines.clearTimeout' : (handle) => { if (typeof clearTimeout !== 'undefined') clearTimeout(handle); },
        'kotlinx.coroutines.clearTimeout_$external_fun' : (_this, p0) => _this.clearTimeout(p0),
        'kotlinx.coroutines.setTimeout_$external_fun' : (p0, p1) => setTimeout(p0, p1),
        'kotlinx.browser.window_$external_prop_getter' : () => window,
        'kotlinx.browser.document_$external_prop_getter' : () => document,
        'org.w3c.dom.length_$external_prop_getter' : (_this) => _this.length,
        'org.w3c.dom.item_$external_fun' : (_this, p0) => _this.item(p0),
        'org.khronos.webgl.getMethodImplForUint8Array' : (obj, index) => { return obj[index]; },
        'org.khronos.webgl.getMethodImplForInt8Array' : (obj, index) => { return obj[index]; },
        'org.khronos.webgl.slice_$external_fun' : (_this, p0, p1, isDefault0) => _this.slice(p0, isDefault0 ? undefined : p1, ),
        'org.khronos.webgl.Int8Array_$external_fun' : (p0, p1, p2, isDefault0, isDefault1) => new Int8Array(p0, isDefault0 ? undefined : p1, isDefault1 ? undefined : p2, ),
        'org.khronos.webgl.length_$external_prop_getter' : (_this) => _this.length,
        'org.khronos.webgl.Uint8Array_$external_fun' : (p0, p1, p2, isDefault0, isDefault1) => new Uint8Array(p0, isDefault0 ? undefined : p1, isDefault1 ? undefined : p2, ),
        'org.khronos.webgl.length_$external_prop_getter_1' : (_this) => _this.length,
        'org.khronos.webgl.buffer_$external_prop_getter' : (_this) => _this.buffer,
        'org.khronos.webgl.byteOffset_$external_prop_getter' : (_this) => _this.byteOffset,
        'org.khronos.webgl.byteLength_$external_prop_getter' : (_this) => _this.byteLength,
        'org.w3c.dom.clipboard.clipboardData_$external_prop_getter' : (_this) => _this.clipboardData,
        'org.w3c.dom.clipboard.ClipboardEvent_$external_class_instanceof' : (x) => x instanceof ClipboardEvent,
        'org.w3c.dom.css.cursor_$external_prop_setter' : (_this, v) => _this.cursor = v,
        'org.w3c.dom.css.height_$external_prop_setter' : (_this, v) => _this.height = v,
        'org.w3c.dom.css.left_$external_prop_setter' : (_this, v) => _this.left = v,
        'org.w3c.dom.css.position_$external_prop_setter' : (_this, v) => _this.position = v,
        'org.w3c.dom.css.top_$external_prop_setter' : (_this, v) => _this.top = v,
        'org.w3c.dom.css.width_$external_prop_setter' : (_this, v) => _this.width = v,
        'org.w3c.dom.css.setProperty_$external_fun' : (_this, p0, p1, p2, isDefault0) => _this.setProperty(p0, p1, isDefault0 ? undefined : p2, ),
        'org.w3c.dom.css.style_$external_prop_getter' : (_this) => _this.style,
        'org.w3c.dom.events.type_$external_prop_getter' : (_this) => _this.type,
        'org.w3c.dom.events.timeStamp_$external_prop_getter' : (_this) => _this.timeStamp,
        'org.w3c.dom.events.preventDefault_$external_fun' : (_this, ) => _this.preventDefault(),
        'org.w3c.dom.events.Event_$external_class_instanceof' : (x) => x instanceof Event,
        'org.w3c.dom.events.addEventListener_$external_fun' : (_this, p0, p1, p2) => _this.addEventListener(p0, p1, p2),
        'org.w3c.dom.events.__convertKotlinClosureToJsClosure_((Js)->Unit)' : (f) => getCachedJsObject(f, (p0) => wasmExports['__callFunction_((Js)->Unit)'](f, p0)),
        'org.w3c.dom.events.addEventListener_$external_fun_1' : (_this, p0, p1) => _this.addEventListener(p0, p1),
        'org.w3c.dom.events.addEventListener_$external_fun_2' : (_this, p0, p1) => _this.addEventListener(p0, p1),
        'org.w3c.dom.events.removeEventListener_$external_fun' : (_this, p0, p1) => _this.removeEventListener(p0, p1),
        'org.w3c.dom.events.removeEventListener_$external_fun_1' : (_this, p0, p1) => _this.removeEventListener(p0, p1),
        'org.w3c.dom.events.ctrlKey_$external_prop_getter' : (_this) => _this.ctrlKey,
        'org.w3c.dom.events.shiftKey_$external_prop_getter' : (_this) => _this.shiftKey,
        'org.w3c.dom.events.altKey_$external_prop_getter' : (_this) => _this.altKey,
        'org.w3c.dom.events.metaKey_$external_prop_getter' : (_this) => _this.metaKey,
        'org.w3c.dom.events.button_$external_prop_getter' : (_this) => _this.button,
        'org.w3c.dom.events.buttons_$external_prop_getter' : (_this) => _this.buttons,
        'org.w3c.dom.events.offsetX_$external_prop_getter' : (_this) => _this.offsetX,
        'org.w3c.dom.events.offsetY_$external_prop_getter' : (_this) => _this.offsetY,
        'org.w3c.dom.events.MouseEvent_$external_class_instanceof' : (x) => x instanceof MouseEvent,
        'org.w3c.dom.events.key_$external_prop_getter' : (_this) => _this.key,
        'org.w3c.dom.events.code_$external_prop_getter' : (_this) => _this.code,
        'org.w3c.dom.events.ctrlKey_$external_prop_getter_1' : (_this) => _this.ctrlKey,
        'org.w3c.dom.events.shiftKey_$external_prop_getter_1' : (_this) => _this.shiftKey,
        'org.w3c.dom.events.altKey_$external_prop_getter_1' : (_this) => _this.altKey,
        'org.w3c.dom.events.metaKey_$external_prop_getter_1' : (_this) => _this.metaKey,
        'org.w3c.dom.events.repeat_$external_prop_getter' : (_this) => _this.repeat,
        'org.w3c.dom.events.isComposing_$external_prop_getter' : (_this) => _this.isComposing,
        'org.w3c.dom.events.KeyboardEvent_$external_class_instanceof' : (x) => x instanceof KeyboardEvent,
        'org.w3c.dom.events.deltaX_$external_prop_getter' : (_this) => _this.deltaX,
        'org.w3c.dom.events.deltaY_$external_prop_getter' : (_this) => _this.deltaY,
        'org.w3c.dom.events.WheelEvent_$external_class_instanceof' : (x) => x instanceof WheelEvent,
        'org.w3c.dom.events.data_$external_prop_getter' : (_this) => _this.data,
        'org.w3c.dom.events.CompositionEvent_$external_class_instanceof' : (x) => x instanceof CompositionEvent,
        'org.w3c.dom.AddEventListenerOptions_js_code' : (passive, once, capture) => { return { passive, once, capture }; },
        'org.w3c.dom.location_$external_prop_getter' : (_this) => _this.location,
        'org.w3c.dom.navigator_$external_prop_getter' : (_this) => _this.navigator,
        'org.w3c.dom.devicePixelRatio_$external_prop_getter' : (_this) => _this.devicePixelRatio,
        'org.w3c.dom.requestAnimationFrame_$external_fun' : (_this, p0) => _this.requestAnimationFrame(p0),
        'org.w3c.dom.__convertKotlinClosureToJsClosure_((Double)->Unit)' : (f) => getCachedJsObject(f, (p0) => wasmExports['__callFunction_((Double)->Unit)'](f, p0)),
        'org.w3c.dom.matchMedia_$external_fun' : (_this, p0) => _this.matchMedia(p0),
        'org.w3c.dom.dropEffect_$external_prop_setter' : (_this, v) => _this.dropEffect = v,
        'org.w3c.dom.setDragImage_$external_fun' : (_this, p0, p1, p2) => _this.setDragImage(p0, p1, p2),
        'org.w3c.dom.getData_$external_fun' : (_this, p0) => _this.getData(p0),
        'org.w3c.dom.setData_$external_fun' : (_this, p0, p1) => _this.setData(p0, p1),
        'org.w3c.dom.matches_$external_prop_getter' : (_this) => _this.matches,
        'org.w3c.dom.addListener_$external_fun' : (_this, p0) => _this.addListener(p0),
        'org.w3c.dom.host_$external_prop_getter' : (_this) => _this.host,
        'org.w3c.dom.focus_$external_fun' : (_this, ) => _this.focus(),
        'org.w3c.dom.blur_$external_fun' : (_this, ) => _this.blur(),
        'org.w3c.dom.HTMLElement_$external_class_instanceof' : (x) => x instanceof HTMLElement,
        'org.w3c.dom.documentElement_$external_prop_getter' : (_this) => _this.documentElement,
        'org.w3c.dom.body_$external_prop_getter' : (_this) => _this.body,
        'org.w3c.dom.activeElement_$external_prop_getter' : (_this) => _this.activeElement,
        'org.w3c.dom.createElement_$external_fun' : (_this, p0, p1, isDefault0) => _this.createElement(p0, isDefault0 ? undefined : p1, ),
        'org.w3c.dom.hasFocus_$external_fun' : (_this, ) => _this.hasFocus(),
        'org.w3c.dom.binaryType_$external_prop_setter' : (_this, v) => _this.binaryType = v,
        'org.w3c.dom.close_$external_fun' : (_this, p0, p1, isDefault0, isDefault1) => _this.close(isDefault0 ? undefined : p0, isDefault1 ? undefined : p1, ),
        'org.w3c.dom.send_$external_fun' : (_this, p0) => _this.send(p0),
        'org.w3c.dom.send_$external_fun_1' : (_this, p0) => _this.send(p0),
        'org.w3c.dom.data_$external_prop_getter' : (_this) => _this.data,
        'org.w3c.dom.fetch_$external_fun' : (_this, p0, p1, isDefault0) => _this.fetch(p0, isDefault0 ? undefined : p1, ),
        'org.w3c.dom.namespaceURI_$external_prop_getter' : (_this) => _this.namespaceURI,
        'org.w3c.dom.localName_$external_prop_getter' : (_this) => _this.localName,
        'org.w3c.dom.clientWidth_$external_prop_getter' : (_this) => _this.clientWidth,
        'org.w3c.dom.clientHeight_$external_prop_getter' : (_this) => _this.clientHeight,
        'org.w3c.dom.getAttribute_$external_fun' : (_this, p0) => _this.getAttribute(p0),
        'org.w3c.dom.getAttributeNS_$external_fun' : (_this, p0, p1) => _this.getAttributeNS(p0, p1),
        'org.w3c.dom.setAttribute_$external_fun' : (_this, p0, p1) => _this.setAttribute(p0, p1),
        'org.w3c.dom.getBoundingClientRect_$external_fun' : (_this, ) => _this.getBoundingClientRect(),
        'org.w3c.dom.Element_$external_class_instanceof' : (x) => x instanceof Element,
        'org.w3c.dom.language_$external_prop_getter' : (_this) => _this.language,
        'org.w3c.dom.nodeName_$external_prop_getter' : (_this) => _this.nodeName,
        'org.w3c.dom.childNodes_$external_prop_getter' : (_this) => _this.childNodes,
        'org.w3c.dom.lookupPrefix_$external_fun' : (_this, p0) => _this.lookupPrefix(p0),
        'org.w3c.dom.appendChild_$external_fun' : (_this, p0) => _this.appendChild(p0),
        'org.w3c.dom.dataTransfer_$external_prop_getter' : (_this) => _this.dataTransfer,
        'org.w3c.dom.DragEvent_$external_class_instanceof' : (x) => x instanceof DragEvent,
        'org.w3c.dom.item_$external_fun_1' : (_this, p0) => _this.item(p0),
        'org.w3c.dom.identifier_$external_prop_getter' : (_this) => _this.identifier,
        'org.w3c.dom.clientX_$external_prop_getter' : (_this) => _this.clientX,
        'org.w3c.dom.clientY_$external_prop_getter' : (_this) => _this.clientY,
        'org.w3c.dom.top_$external_prop_getter' : (_this) => _this.top,
        'org.w3c.dom.right_$external_prop_getter' : (_this) => _this.right,
        'org.w3c.dom.bottom_$external_prop_getter' : (_this) => _this.bottom,
        'org.w3c.dom.left_$external_prop_getter' : (_this) => _this.left,
        'org.w3c.dom.Companion_$external_object_getInstance' : () => ({}),
        'org.w3c.dom.remove_$external_fun' : (_this, ) => _this.remove(),
        'org.w3c.dom.width_$external_prop_setter' : (_this, v) => _this.width = v,
        'org.w3c.dom.height_$external_prop_setter' : (_this, v) => _this.height = v,
        'org.w3c.dom.HTMLCanvasElement_$external_class_instanceof' : (x) => x instanceof HTMLCanvasElement,
        'org.w3c.dom.targetTouches_$external_prop_getter' : (_this) => _this.targetTouches,
        'org.w3c.dom.changedTouches_$external_prop_getter' : (_this) => _this.changedTouches,
        'org.w3c.dom.TouchEvent_$external_class_instanceof' : (x) => x instanceof TouchEvent,
        'org.w3c.dom.matches_$external_prop_getter_1' : (_this) => _this.matches,
        'org.w3c.dom.MediaQueryListEvent_$external_class_instanceof' : (x) => x instanceof MediaQueryListEvent,
        'org.w3c.dom.code_$external_prop_getter' : (_this) => _this.code,
        'org.w3c.dom.reason_$external_prop_getter' : (_this) => _this.reason,
        'org.w3c.dom.parsing.DOMParser_$external_fun' : () => new DOMParser(),
        'org.w3c.dom.parsing.parseFromString_$external_fun' : (_this, p0, p1) => _this.parseFromString(p0, p1),
        'org.w3c.fetch.status_$external_prop_getter' : (_this) => _this.status,
        'org.w3c.fetch.ok_$external_prop_getter' : (_this) => _this.ok,
        'org.w3c.fetch.statusText_$external_prop_getter' : (_this) => _this.statusText,
        'org.w3c.fetch.headers_$external_prop_getter' : (_this) => _this.headers,
        'org.w3c.fetch.body_$external_prop_getter' : (_this) => _this.body,
        'org.w3c.fetch.blob_$external_fun' : (_this, ) => _this.blob(),
        'org.w3c.fetch.get_$external_fun' : (_this, p0) => _this.get(p0),
        'org.w3c.fetch.Companion_$external_object_getInstance' : () => ({}),
        'org.w3c.files.slice_$external_fun' : (_this, p0, p1, p2, isDefault0, isDefault1, isDefault2) => _this.slice(isDefault0 ? undefined : p0, isDefault1 ? undefined : p1, isDefault2 ? undefined : p2, ),
        'org.w3c.performance.now_$external_fun' : (_this, ) => _this.now(),
        'org.w3c.performance.performance_$external_prop_getter' : (_this) => _this.performance,
        'org.w3c.xhr.XMLHttpRequest_$external_fun' : () => new XMLHttpRequest(),
        'org.w3c.xhr.status_$external_prop_getter' : (_this) => _this.status,
        'org.w3c.xhr.open_$external_fun' : (_this, p0, p1, p2, p3, p4, isDefault0, isDefault1) => _this.open(p0, p1, p2, isDefault0 ? undefined : p3, isDefault1 ? undefined : p4, ),
        'org.w3c.xhr.send_$external_fun' : (_this, ) => _this.send(),
        'org.w3c.xhr.overrideMimeType_$external_fun' : (_this, p0) => _this.overrideMimeType(p0),
        'androidx.compose.runtime.internal.weakMap_js_code' : () => (new WeakMap()),
        'androidx.compose.runtime.internal.set_$external_fun' : (_this, p0, p1) => _this.set(p0, p1),
        'androidx.compose.runtime.internal.get_$external_fun' : (_this, p0) => _this.get(p0),
        'org.jetbrains.skiko.w3c.language_$external_prop_getter' : (_this) => _this.language,
        'org.jetbrains.skiko.w3c.userAgent_$external_prop_getter' : (_this) => _this.userAgent,
        'org.jetbrains.skiko.w3c.navigator_$external_prop_getter' : (_this) => _this.navigator,
        'org.jetbrains.skiko.w3c.performance_$external_prop_getter' : (_this) => _this.performance,
        'org.jetbrains.skiko.w3c.requestAnimationFrame_$external_fun' : (_this, p0) => _this.requestAnimationFrame(p0),
        'org.jetbrains.skiko.w3c.open_$external_fun' : (_this, p0, p1) => _this.open(p0, p1),
        'org.jetbrains.skiko.w3c.window_$external_object_getInstance' : () => window,
        'org.jetbrains.skiko.w3c.now_$external_fun' : (_this, ) => _this.now(),
        'org.jetbrains.skiko.w3c.width_$external_prop_getter' : (_this) => _this.width,
        'org.jetbrains.skiko.w3c.height_$external_prop_getter' : (_this) => _this.height,
        'org.jetbrains.skiko.w3c.HTMLCanvasElement_$external_class_instanceof' : (x) => x instanceof HTMLCanvasElement,
        'org.jetbrains.skia.impl.FinalizationRegistry_$external_fun' : (p0) => new FinalizationRegistry(p0),
        'org.jetbrains.skia.impl.register_$external_fun' : (_this, p0, p1) => _this.register(p0, p1),
        'org.jetbrains.skia.impl.unregister_$external_fun' : (_this, p0) => _this.unregister(p0),
        'org.jetbrains.skia.impl._releaseLocalCallbackScope_$external_fun' : () => _ref_Li9za2lrby5tanM_._releaseLocalCallbackScope(),
        'org.jetbrains.skiko.getNavigatorInfo' : () => navigator.userAgentData ? navigator.userAgentData.platform : navigator.platform,
        'org.jetbrains.skiko.wasm.createContext_$external_fun' : (_this, p0, p1) => _this.createContext(p0, p1),
        'org.jetbrains.skiko.wasm.makeContextCurrent_$external_fun' : (_this, p0) => _this.makeContextCurrent(p0),
        'org.jetbrains.skiko.wasm.GL_$external_object_getInstance' : () => _ref_Li9za2lrby5tanM_.GL,
        'org.jetbrains.skiko.wasm.createDefaultContextAttributes' : () => {
            return {
                alpha: 1,
                depth: 1,
                stencil: 8,
                antialias: 0,
                premultipliedAlpha: 1,
                preserveDrawingBuffer: 0,
                preferLowPowerToHighPerformance: 0,
                failIfMajorPerformanceCaveat: 0,
                enableExtensionsByDefault: 1,
                explicitSwapControl: 0,
                renderViaOffscreenBackBuffer: 0,
                majorVersion: 2,
            }
        }
        ,
        'androidx.compose.ui.text.intl.getUserPreferredLanguagesAsArray' : () => window.navigator.languages,
        'androidx.compose.ui.text.intl.parseLanguageTagToIntlLocale' : (languageTag) => new Intl.Locale(languageTag),
        'androidx.compose.ui.text.intl._language_$external_prop_getter' : (_this) => _this.language,
        'androidx.compose.ui.text.intl._region_$external_prop_getter' : (_this) => _this.region,
        'androidx.compose.ui.text.intl._baseName_$external_prop_getter' : (_this) => _this.baseName,
        'androidx.compose.ui.internal.weakMap_js_code' : () => (new WeakMap()),
        'androidx.compose.ui.internal.set_$external_fun' : (_this, p0, p1) => _this.set(p0, p1),
        'androidx.compose.ui.internal.get_$external_fun' : (_this, p0) => _this.get(p0),
        'androidx.compose.ui.platform.isSecureContext' : () => window.isSecureContext,
        'androidx.compose.ui.platform.invalidClipboardItems' : () => [],
        'androidx.compose.ui.platform.createClipboardItemWithPlainText' : (text) => [new ClipboardItem({'text/plain': new Blob([text], { type: 'text/plain' })})],
        'androidx.compose.ui.platform.getW3CClipboard' : () => window.navigator.clipboard,
        'androidx.compose.ui.platform.emptyClipboardItems' : () => [new ClipboardItem({'text/plain': new Blob([''], { type: 'text/plain' })})],
        'androidx.compose.ui.platform.read_$external_fun' : (_this, ) => _this.read(),
        'androidx.compose.ui.platform.write_$external_fun' : (_this, p0) => _this.write(p0),
        'androidx.compose.ui.platform.types_$external_prop_getter' : (_this) => _this.types,
        'androidx.compose.ui.platform.getType_$external_fun' : (_this, p0) => _this.getType(p0),
        'androidx.compose.ui.window.isMatchMediaSupported' : () => window.matchMedia != undefined,
        'androidx.compose.ui.events.withSignal' : (signal) => ({signal: signal}),
        'androidx.compose.ui.events.AbortController_$external_fun' : () => new AbortController(),
        'androidx.compose.ui.events.signal_$external_prop_getter' : (_this) => _this.signal,
        'androidx.compose.ui.platform.isTypedEvent' : (evt) => !evt.metaKey && !evt.ctrlKey && evt.key.charAt(0) === evt.key,
        'androidx.compose.ui.platform.value_$external_prop_setter' : (_this, v) => _this.value = v,
        'androidx.compose.ui.platform.setSelectionRange_$external_fun' : (_this, p0, p1, p2, isDefault0) => _this.setSelectionRange(p0, p1, isDefault0 ? undefined : p2, ),
        'androidx.compose.ui.platform.inputType_$external_prop_getter' : (_this) => _this.inputType,
        'androidx.compose.ui.platform.data_$external_prop_getter' : (_this) => _this.data,
        'androidx.compose.ui.platform.InputEvent_$external_class_instanceof' : (x) => x instanceof InputEvent,
        'androidx.compose.ui.window.force_$external_prop_getter' : (_this) => _this.force,
        'androidx.compose.foundation.internal.doesJsArrayContainValue' : (jsArray, value) => jsArray.includes(value),
        'androidx.compose.foundation.internal.getTextFromBlob' : (blob) => blob.text(),
        'androidx.compose.foundation.text.EventListener' : (handler) => (event) => { handler(event) },
        'kotlinx.datetime.internal.JSJoda.compareTo_$external_fun' : (_this, p0) => _this.compareTo(p0),
        'kotlinx.datetime.internal.JSJoda.dayOfMonth_$external_fun' : (_this, ) => _this.dayOfMonth(),
        'kotlinx.datetime.internal.JSJoda.dayOfWeek_$external_fun' : (_this, ) => _this.dayOfWeek(),
        'kotlinx.datetime.internal.JSJoda.equals_$external_fun' : (_this, p0) => _this.equals(p0),
        'kotlinx.datetime.internal.JSJoda.hashCode_$external_fun' : (_this, ) => _this.hashCode(),
        'kotlinx.datetime.internal.JSJoda.month_$external_fun' : (_this, ) => _this.month(),
        'kotlinx.datetime.internal.JSJoda.monthValue_$external_fun' : (_this, ) => _this.monthValue(),
        'kotlinx.datetime.internal.JSJoda.plusDays_$external_fun' : (_this, p0) => _this.plusDays(p0),
        'kotlinx.datetime.internal.JSJoda.plusMonths_$external_fun' : (_this, p0) => _this.plusMonths(p0),
        'kotlinx.datetime.internal.JSJoda.toEpochDay_$external_fun' : (_this, ) => _this.toEpochDay(),
        'kotlinx.datetime.internal.JSJoda.toString_$external_fun' : (_this, ) => _this.toString(),
        'kotlinx.datetime.internal.JSJoda.year_$external_fun' : (_this, ) => _this.year(),
        'kotlinx.datetime.internal.JSJoda.MIN_$external_prop_getter' : (_this) => _this.MIN,
        'kotlinx.datetime.internal.JSJoda.MAX_$external_prop_getter' : (_this) => _this.MAX,
        'kotlinx.datetime.internal.JSJoda.of_$external_fun' : (_this, p0, p1, p2) => _this.of(p0, p1, p2),
        'kotlinx.datetime.internal.JSJoda.parse_$external_fun' : (_this, p0) => _this.parse(p0),
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance' : () => _ref_QGpzLWpvZGEvY29yZQ_.LocalDate,
        'kotlinx.datetime.internal.JSJoda.LocalDate_$external_class_instanceof' : (x) => x instanceof _ref_QGpzLWpvZGEvY29yZQ_.LocalDate,
        'kotlinx.datetime.internal.JSJoda.value_$external_fun' : (_this, ) => _this.value(),
        'kotlinx.datetime.internal.JSJoda.value_$external_fun_1' : (_this, ) => _this.value(),
        'kotlinx.datetime.internal.JSJoda.compareTo_$external_fun_1' : (_this, p0) => _this.compareTo(p0),
        'kotlinx.datetime.internal.JSJoda.equals_$external_fun_1' : (_this, p0) => _this.equals(p0),
        'kotlinx.datetime.internal.JSJoda.hashCode_$external_fun_1' : (_this, ) => _this.hashCode(),
        'kotlinx.datetime.internal.JSJoda.toSecondOfDay_$external_fun' : (_this, ) => _this.toSecondOfDay(),
        'kotlinx.datetime.internal.JSJoda.toString_$external_fun_1' : (_this, ) => _this.toString(),
        'kotlinx.datetime.internal.JSJoda.MIN_$external_prop_getter_1' : (_this) => _this.MIN,
        'kotlinx.datetime.internal.JSJoda.MAX_$external_prop_getter_1' : (_this) => _this.MAX,
        'kotlinx.datetime.internal.JSJoda.of_$external_fun_1' : (_this, p0, p1, p2, p3) => _this.of(p0, p1, p2, p3),
        'kotlinx.datetime.internal.JSJoda.parse_$external_fun_1' : (_this, p0) => _this.parse(p0),
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance_1' : () => _ref_QGpzLWpvZGEvY29yZQ_.LocalTime,
        'kotlinx.datetime.internal.JSJoda.LocalTime_$external_class_instanceof' : (x) => x instanceof _ref_QGpzLWpvZGEvY29yZQ_.LocalTime,
        'kotlinx.datetime.internal.JSJoda.parse_$external_fun_2' : (_this, p0) => _this.parse(p0),
        'kotlinx.datetime.internal.JSJoda.DateTimeFormatterBuilder_$external_fun' : () => new _ref_QGpzLWpvZGEvY29yZQ_.DateTimeFormatterBuilder(),
        'kotlinx.datetime.internal.JSJoda.appendOffset_$external_fun' : (_this, p0, p1) => _this.appendOffset(p0, p1),
        'kotlinx.datetime.internal.JSJoda.appendOffsetId_$external_fun' : (_this, ) => _this.appendOffsetId(),
        'kotlinx.datetime.internal.JSJoda.parseCaseInsensitive_$external_fun' : (_this, ) => _this.parseCaseInsensitive(),
        'kotlinx.datetime.internal.JSJoda.toFormatter_$external_fun' : (_this, p0) => _this.toFormatter(p0),
        'kotlinx.datetime.internal.JSJoda.STRICT_$external_prop_getter' : (_this) => _this.STRICT,
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance_2' : () => _ref_QGpzLWpvZGEvY29yZQ_.ResolverStyle,
        'kotlinx.datetime.internal.JSJoda.equals_$external_fun_2' : (_this, p0) => _this.equals(p0),
        'kotlinx.datetime.internal.JSJoda.hashCode_$external_fun_2' : (_this, ) => _this.hashCode(),
        'kotlinx.datetime.internal.JSJoda.toString_$external_fun_2' : (_this, ) => _this.toString(),
        'kotlinx.datetime.internal.JSJoda.totalSeconds_$external_fun' : (_this, ) => _this.totalSeconds(),
        'kotlinx.datetime.internal.JSJoda.UTC_$external_prop_getter' : (_this) => _this.UTC,
        'kotlinx.datetime.internal.JSJoda.ofHoursMinutesSeconds_$external_fun' : (_this, p0, p1, p2) => _this.ofHoursMinutesSeconds(p0, p1, p2),
        'kotlinx.datetime.internal.JSJoda.ofTotalSeconds_$external_fun' : (_this, p0) => _this.ofTotalSeconds(p0),
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance_3' : () => _ref_QGpzLWpvZGEvY29yZQ_.ZoneOffset,
        'kotlinx.datetime.internal.JSJoda.ZoneOffset_$external_class_instanceof' : (x) => x instanceof _ref_QGpzLWpvZGEvY29yZQ_.ZoneOffset,
        'kotlinx.datetime.internal.JSJoda.get_$external_fun' : (_this, p0) => _this.get(p0),
        'kotlinx.datetime.internal.JSJoda.OFFSET_SECONDS_$external_prop_getter' : (_this) => _this.OFFSET_SECONDS,
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance_4' : () => _ref_QGpzLWpvZGEvY29yZQ_.ChronoField,
        'kotlinx.datetime.internal.JSJoda.instant_$external_fun' : (_this, ) => _this.instant(),
        'kotlinx.datetime.internal.JSJoda.systemUTC_$external_fun' : (_this, ) => _this.systemUTC(),
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance_5' : () => _ref_QGpzLWpvZGEvY29yZQ_.Clock,
        'kotlinx.datetime.internal.JSJoda.compareTo_$external_fun_2' : (_this, p0) => _this.compareTo(p0),
        'kotlinx.datetime.internal.JSJoda.epochSecond_$external_fun' : (_this, ) => _this.epochSecond(),
        'kotlinx.datetime.internal.JSJoda.equals_$external_fun_3' : (_this, p0) => _this.equals(p0),
        'kotlinx.datetime.internal.JSJoda.hashCode_$external_fun_3' : (_this, ) => _this.hashCode(),
        'kotlinx.datetime.internal.JSJoda.nano_$external_fun' : (_this, ) => _this.nano(),
        'kotlinx.datetime.internal.JSJoda.toString_$external_fun_3' : (_this, ) => _this.toString(),
        'kotlinx.datetime.internal.JSJoda.MIN_$external_prop_getter_2' : (_this) => _this.MIN,
        'kotlinx.datetime.internal.JSJoda.MAX_$external_prop_getter_2' : (_this) => _this.MAX,
        'kotlinx.datetime.internal.JSJoda.ofEpochSecond_$external_fun' : (_this, p0, p1) => _this.ofEpochSecond(p0, p1),
        'kotlinx.datetime.internal.JSJoda.Companion_$external_object_getInstance_6' : () => _ref_QGpzLWpvZGEvY29yZQ_.Instant,
        'kotlinx.datetime.internal.JSJoda.Instant_$external_class_instanceof' : (x) => x instanceof _ref_QGpzLWpvZGEvY29yZQ_.Instant,
        'kotlinx.datetime.withCaughtJsException' : (body) => {
            try {
                body();
                return null;
            } catch(e) {
                return e;
            }
        },
        'kotlinx.datetime.getExceptionMessage' : (jsException) => jsException.message,
        'kotlinx.datetime.checkExceptionName' : (exception, name) => exception.name === name,
        'androidx.compose.material3.internal.weakMap_js_code' : () => (new WeakMap()),
        'androidx.compose.material3.internal.set_$external_fun' : (_this, p0, p1) => _this.set(p0, p1),
        'androidx.compose.material3.internal.get_$external_fun' : (_this, p0) => _this.get(p0),
        'org.jetbrains.compose.resources.Locale_$external_fun' : (p0) => new Intl.Locale(p0),
        'org.jetbrains.compose.resources.language_$external_prop_getter' : (_this) => _this.language,
        'org.jetbrains.compose.resources.region_$external_prop_getter' : (_this) => _this.region,
        'org.jetbrains.compose.resources.jsExportBlobAsArrayBuffer' : (blob) => blob.arrayBuffer(),
        'org.jetbrains.compose.resources.jsExportInt8ArrayToWasm' :  (src, size, dstAddr) => {
                const mem8 = new Int8Array(wasmExports.memory.buffer, dstAddr, size);
                mem8.set(src);
            }
        ,
        'org.jetbrains.compose.resources.requestResponseAsByteArray' : (req) =>  {
                var text = req.responseText;
                var int8Arr = new Int8Array(text.length);
                for (var i = 0; i < text.length; i++) {
                    int8Arr[i] = text.charCodeAt(i) & 0xFF;
                }
                return int8Arr;
            },
        'org.jetbrains.compose.resources.isInTestEnvironment' : () => window.composeResourcesTesting == true,
        'androidx.navigation.internal.weakMap_js_code' : () => (new WeakMap()),
        'androidx.navigation.internal.set_$external_fun' : (_this, p0, p1) => _this.set(p0, p1),
        'androidx.navigation.internal.get_$external_fun' : (_this, p0) => _this.get(p0),
        'io.ktor.utils.io.js.decode' : (decoder, buffer) => { try { return decoder.decode(buffer) } catch(e) { return null } },
        'io.ktor.utils.io.js.tryCreateTextDecoder' : (encoding, fatal) => { try { return new TextDecoder(encoding, { fatal: fatal }) } catch(e) { return null } },
        'io.ktor.utils.io.charsets.toJsArrayImpl' : (x) => new Int8Array(x),
        'io.ktor.util.requireCrypto' : () => eval('require')('crypto'),
        'io.ktor.util.windowCrypto' : () => (window ? (window.crypto ? window.crypto : window.msCrypto) : self.crypto),
        'io.ktor.util.getRandomValues_$external_fun' : (_this, p0) => _this.getRandomValues(p0),
        'io.ktor.util.randomFillSync_$external_fun' : (_this, p0) => _this.randomFillSync(p0),
        'io.ktor.util.hasNodeApi' : () => 
        (typeof process !== 'undefined' 
            && process.versions != null 
            && process.versions.node != null) ||
        (typeof window !== 'undefined' 
            && typeof window.process !== 'undefined' 
            && window.process.versions != null 
            && window.process.versions.node != null)
        ,
        'io.ktor.util.logging.getKtorLogLevel' : () => process.env.KTOR_LOG_LEVEL,
        'io.ktor.util.logging.debug_$external_fun' : (_this, p0) => _this.debug(p0),
        'io.ktor.util.logging.console_$external_prop_getter' : () => console,
        'io.ktor.util.toJsArrayImpl' : (x) => new Int8Array(x),
        'io.ktor.util.date.Date_$external_fun' : () => new Date(),
        'io.ktor.util.date.Date_$external_fun_1' : (p0) => new Date(p0),
        'io.ktor.util.date.getTime_$external_fun' : (_this, ) => _this.getTime(),
        'io.ktor.util.date.getUTCDate_$external_fun' : (_this, ) => _this.getUTCDate(),
        'io.ktor.util.date.getUTCDay_$external_fun' : (_this, ) => _this.getUTCDay(),
        'io.ktor.util.date.getUTCFullYear_$external_fun' : (_this, ) => _this.getUTCFullYear(),
        'io.ktor.util.date.getUTCHours_$external_fun' : (_this, ) => _this.getUTCHours(),
        'io.ktor.util.date.getUTCMinutes_$external_fun' : (_this, ) => _this.getUTCMinutes(),
        'io.ktor.util.date.getUTCMonth_$external_fun' : (_this, ) => _this.getUTCMonth(),
        'io.ktor.util.date.getUTCSeconds_$external_fun' : (_this, ) => _this.getUTCSeconds(),
        'io.ktor.http.locationOrigin' : () => function() {
            var tmpLocation = null
            if (typeof window !== 'undefined') {
              tmpLocation = window.location
            } else if (typeof self !== 'undefined') {
              tmpLocation = self.location
            }
            var origin = ""
            if (tmpLocation) {
              origin = tmpLocation.origin
            }
            return origin && origin != "null" ? origin : "http://localhost"    
        }(),
        'io.ktor.client.engine.js.createBrowserWebSocket' : (urlString_capturingHack, protocols) => new WebSocket(urlString_capturingHack, protocols),
        'io.ktor.client.engine.js.createWebSocketNodeJs' : (socketCtor, urlString_capturingHack, headers_capturingHack, protocols) => new socketCtor(urlString_capturingHack, protocols, { headers: headers_capturingHack }),
        'io.ktor.client.engine.js.getKeys' : (headers) => Array.from(headers.keys()),
        'io.ktor.client.engine.js.eventAsString' : (event) => JSON.stringify(event, ['message', 'target', 'type', 'isTrusted']),
        'io.ktor.client.engine.js.compatibility.abortControllerCtorBrowser' : () => AbortController,
        'io.ktor.client.engine.js.node.bodyOn' : (body, type, handler) => body.on(type, handler),
        'io.ktor.client.engine.js.node.bodyOn_1' : (body, type, handler) => body.on(type, handler),
        'io.ktor.client.engine.js.node.pause_$external_fun' : (_this, ) => _this.pause(),
        'io.ktor.client.engine.js.node.resume_$external_fun' : (_this, ) => _this.resume(),
        'io.ktor.client.engine.js.node.destroy_$external_fun' : (_this, p0) => _this.destroy(p0),
        'io.ktor.client.fetch.body_$external_prop_setter' : (_this, v) => _this.body = v,
        'io.ktor.client.fetch.headers_$external_prop_setter' : (_this, v) => _this.headers = v,
        'io.ktor.client.fetch.method_$external_prop_setter' : (_this, v) => _this.method = v,
        'io.ktor.client.fetch.redirect_$external_prop_setter' : (_this, v) => _this.redirect = v,
        'io.ktor.client.fetch.signal_$external_prop_setter' : (_this, v) => _this.signal = v,
        'io.ktor.client.fetch.signal_$external_prop_getter' : (_this) => _this.signal,
        'io.ktor.client.fetch.abort_$external_fun' : (_this, ) => _this.abort(),
        'io.ktor.client.fetch.fetch_$external_fun' : (p0, p1, isDefault0) => fetch(p0, isDefault0 ? undefined : p1, ),
        'io.ktor.client.fetch.getReader_$external_fun' : (_this, ) => _this.getReader(),
        'io.ktor.client.fetch.cancel_$external_fun' : (_this, p0, isDefault0) => _this.cancel(isDefault0 ? undefined : p0, ),
        'io.ktor.client.fetch.read_$external_fun' : (_this, ) => _this.read(),
        'io.ktor.client.fetch.done_$external_prop_getter' : (_this) => _this.done,
        'io.ktor.client.fetch.value_$external_prop_getter' : (_this) => _this.value,
        'io.ktor.client.plugins.websocket.tryGetEventDataAsString' : (data) => typeof(data) === 'string' ? data : null,
        'io.ktor.client.plugins.websocket.tryGetEventDataAsArrayBuffer' : (data) => data instanceof ArrayBuffer ? data : null,
        'io.ktor.client.utils.makeJsObject' : () => { return {}; },
        'io.ktor.client.utils.makeRequire' : (name) => require(name),
        'io.ktor.client.utils.setObjectField' : (obj, name, value) => obj[name]=value,
        'io.ktor.client.utils.makeJsNew' : (ctor) => new ctor(),
        'io.ktor.client.utils.makeJsCall' : (func, arg) => func.apply(null, arg),
        'io.ktor.client.utils.toJsArrayImpl' : (x) => new Uint8Array(x)
    }
    
    // Placed here to give access to it from externals (js_code)
    let wasmInstance;
    let require; 
    let wasmExports;

    const isNodeJs = (typeof process !== 'undefined') && (process.release.name === 'node');
    const isDeno = !isNodeJs && (typeof Deno !== 'undefined')
    const isStandaloneJsVM =
        !isDeno && !isNodeJs && (
            typeof d8 !== 'undefined' // V8
            || typeof inIon !== 'undefined' // SpiderMonkey
            || typeof jscOptions !== 'undefined' // JavaScriptCore
        );
    const isBrowser = !isNodeJs && !isDeno && !isStandaloneJsVM && (typeof window !== 'undefined' || typeof self !== 'undefined');
    
    if (!isNodeJs && !isDeno && !isStandaloneJsVM && !isBrowser) {
      throw "Supported JS engine not detected";
    }
    
    const wasmFilePath = './gemstone.wasm';
    const importObject = {
        js_code,
        intrinsics: {
            
        },
        './skiko.mjs': imports['./skiko.mjs'],

    };
    
    try {
      if (isNodeJs) {
        const module = await import(/* webpackIgnore: true */'node:module');
        const importMeta = import.meta;
        require = module.default.createRequire(importMeta.url);
        const fs = require('fs');
        const url = require('url');
        const filepath = import.meta.resolve(wasmFilePath);
        const wasmBuffer = fs.readFileSync(url.fileURLToPath(filepath));
        const wasmModule = new WebAssembly.Module(wasmBuffer);
        wasmInstance = new WebAssembly.Instance(wasmModule, importObject);
      }
      
      if (isDeno) {
        const path = await import(/* webpackIgnore: true */'https://deno.land/std/path/mod.ts');
        const binary = Deno.readFileSync(path.fromFileUrl(import.meta.resolve(wasmFilePath)));
        const module = await WebAssembly.compile(binary);
        wasmInstance = await WebAssembly.instantiate(module, importObject);
      }
      
      if (isStandaloneJsVM) {
        const wasmBuffer = read(wasmFilePath, 'binary');
        const wasmModule = new WebAssembly.Module(wasmBuffer);
        wasmInstance = new WebAssembly.Instance(wasmModule, importObject);
      }
      
      if (isBrowser) {
        wasmInstance = (await WebAssembly.instantiateStreaming(fetch(new URL('./gemstone.wasm',import.meta.url).href), importObject)).instance;
      }
    } catch (e) {
      if (e instanceof WebAssembly.CompileError) {
        let text = `Please make sure that your runtime environment supports the latest version of Wasm GC and Exception-Handling proposals.
For more information, see https://kotl.in/wasm-help
`;
        if (isBrowser) {
          console.error(text);
        } else {
          const t = "\n" + text;
          if (typeof console !== "undefined" && console.log !== void 0) 
            console.log(t);
          else 
            print(t);
        }
      }
      throw e;
    }
    
    wasmExports = wasmInstance.exports;
    if (runInitializer) {
        wasmExports._initialize();
    }

    return { instance: wasmInstance,  exports: wasmExports };
}
