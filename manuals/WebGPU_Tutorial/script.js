const canvas = document.getElementById('gpuCanvas');
const video = document.getElementById('webcam');
const errorDiv = document.getElementById('error');

// Основная функция
async function main() {
    if (!navigator.gpu) {
        throw new Error('WebGPU не поддерживается в этом браузере.');
    }

    // 1. Инициализация
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) throw new Error('Не удалось получить GPU адаптер.');
    const device = await adapter.requestDevice();

    // 2. Настройка камеры
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, width: 640, height: 480 });
    video.srcObject = stream;
    await video.play();

    const width = video.videoWidth;
    const height = video.videoHeight;
    canvas.width = width;
    canvas.height = height;

    // 3. Загрузка шейдера
    const shaderResponse = await fetch('shader.wgsl');
    const shaderCode = await shaderResponse.text();
    const shaderModule = device.createShaderModule({ code: shaderCode });

    // 4. Создание Pipeline
    const pipeline = device.createComputePipeline({
        layout: 'auto',
        compute: { module: shaderModule, entryPoint: 'main' }
    });

    // 5. Создание текстур
    // Input Texture (для видео)
    const inputTexture = device.createTexture({
        size: [width, height],
        format: 'rgba8unorm',
        usage: GPUTextureUsage.TEXTURE_BINDING | GPUTextureUsage.COPY_DST | GPUTextureUsage.RENDER_ATTACHMENT,
    });
    
    // Output Texture (для результата)
    const outputTexture = device.createTexture({
        size: [width, height],
        format: 'rgba8unorm',
        usage: GPUTextureUsage.STORAGE_BINDING | GPUTextureUsage.TEXTURE_BINDING,
    });

    // 6. Context для отображения результата
    const ctx = canvas.getContext('webgpu');
    ctx.configure({
        device: device,
        format: navigator.gpu.getPreferredCanvasFormat(),
        usage: GPUTextureUsage.RENDER_ATTACHMENT,
    });

    // 7. Bind Group (связка ресурсов)
    const bindGroup = device.createBindGroup({
        layout: pipeline.getBindGroupLayout(0),
        entries: [
            { binding: 0, resource: inputTexture.createView() },
            { binding: 1, resource: outputTexture.createView() },
        ],
    });

    // Функция рендеринга
    function frame() {
        // 1. Копируем кадр видео в Input Texture
        device.queue.copyExternalImageToTexture(
            { source: video, flipY: true },
            { texture: inputTexture },
            [width, height]
        );

        // 2. Запускаем вычисления
        const commandEncoder = device.createCommandEncoder();
        const passEncoder = commandEncoder.beginComputePass();
        passEncoder.setPipeline(pipeline);
        passEncoder.setBindGroup(0, bindGroup);
        passEncoder.dispatchWorkgroups(Math.ceil(width / 8), Math.ceil(height / 8));
        passEncoder.end();

        // 3. Рисуем результат на Canvas
        // (Просто копируем outputTexture на экран)
        passEncoder = commandEncoder.beginRenderPass({
            colorAttachments: [{
                view: ctx.getCurrentTexture().createView(),
                clearValue: { r: 0, g: 0, b: 0, a: 1.0 },
                loadOp: 'clear',
                storeOp: 'store',
            }]
        });
        // Примечание: Для простоты мы выводим результат через текстурный проход,
        // но здесь мы просто используем copyTextureToTexture для демонстрации.
        // Однако, самый быстрый способ - отрисовать выходную текстуру на кваде.
        // Для упрощения примера используем copyExternalImageToTexture в обратную сторону? 
        // Нет, WebGPU не позволяет читать Storage Texture напрямую в copyExternalImageToTexture.
        
        passEncoder.end(); // Закрываем пасс
        
        // Просто копируем результат обратно для отображения (технический трюк для простоты)
        // В реальности лучше использовать Render Pipeline с текстурой.
        // Но чтобы код оставался понятным, давайте просто скопируем:
        commandEncoder.copyTextureToTexture(
            { texture: outputTexture },
            { texture: ctx.getCurrentTexture() },
            [width, height]
        );

        device.queue.submit([commandEncoder.finish()]);
        requestAnimationFrame(frame);
    }

    requestAnimationFrame(frame);
}

main().catch(err => {
    console.error(err);
    errorDiv.textContent = err.message;
});
