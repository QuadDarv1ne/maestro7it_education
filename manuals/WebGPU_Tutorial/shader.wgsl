// WebGPU Compute Shader: Grayscale Filter

@group(0) @binding(0) var inputTex: texture_2d<f32>;
@group(0) @binding(1) var outputTex: texture_storage_2d<rgba8unorm, write>;

@compute @workgroup_size(8, 8)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
    let dims = textureDimensions(inputTex);
    
    // Проверка границ
    if (id.x >= dims.x || id.y >= dims.y) {
        return;
    }

    // Читаем исходный цвет
    let color = textureLoad(inputTex, vec2<i32>(id.xy), 0);
    
    // Считаем яркость (Luminosity)
    let gray = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b;

    // Записываем результат
    textureStore(outputTex, vec2<i32>(id.xy), vec4<f32>(gray, gray, gray, 1.0));
}
