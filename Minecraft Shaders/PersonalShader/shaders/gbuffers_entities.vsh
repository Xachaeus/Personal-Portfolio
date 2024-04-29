#version 120

varying vec2 TexCoords;
varying vec2 LightmapCoords;
varying vec4 Color;
varying vec3 Normal;

void main(){
	gl_Position = ftransform();
	TexCoords = gl_MultiTexCoord0.st;
	Color = gl_Color;
	Normal = gl_NormalMatrix * gl_Normal;
	// Use the texture matrix instead of dividing by 15 to maintain compatiblity for each version of Minecraft
    LightmapCoords = mat2(gl_TextureMatrix[1]) * gl_MultiTexCoord1.st;
    // Transform them into the [0, 1] range
    LightmapCoords = (LightmapCoords * 33.05f / 32.0f) - (1.05f / 32.0f);
}