#version 120

varying vec2 TexCoords;

uniform sampler2D colortex0;

uniform ivec2 eyeBrightnessSmooth;
uniform float screenBrightness;

#define CONTRAST 1.005 // Contrast [0.9 0.95 1.0 1.005 1.1 1.2 1.3 1.5 1.75 2.0]
#define SATURATION 1.15 // Saturation [0.0 0.25 0.5 0.75 1.0 1.1 1.2 1.3 1.5 1.75 2.0]
#define TONE_MAPPING 0.3 // Tonemapping [0.0 0.1 0.2 0.3 0.5 0.7 0.8 1.0]

const float gamma = 2.2f;
const float contrast = CONTRAST;
const float brightness = 1.5f;
const float saturation = SATURATION;
const float tone_mapping = 0.3f;

float luminence(in vec3 color){
	return (0.2126f * color.r + 0.7152f * color.g + 0.0722f * color.b);
}

void main() {
	float exposure = pow(4.0f - 3.0f*(eyeBrightnessSmooth.y / 240.0f), 0.5f);
	//float exposure = pow(1.0f - screenBrightness, 0.5f);
	vec3 Color = texture2D(colortex0, TexCoords).rgb;
	Color *= exposure;
	Color = contrast*(Color-0.5f) + 0.5f + Color*(brightness-1.0f);
	Color = mix(vec3(luminence(Color)), Color, saturation);
	float a = 2.51f;
	float b = 0.03f;
	float c = 2.43f;
	float d = 0.59f;
	float e = 0.14f;
	Color = Color*(1.0f-tone_mapping) + tone_mapping*clamp((Color*(a*Color+b))/(Color*(c*Color+d)+e), 0.0f, 1.0f);
    gl_FragColor = vec4(pow(Color, vec3(1.0f/gamma)), 1.0f);
}